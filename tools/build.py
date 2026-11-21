"""Build the bilingual HTML reader from the same chapter files that produce the PDFs."""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
import json
import re
import subprocess

from layout import EDITION, reader, landing
from gateway import gateway
from manuscript import Page, read_manuscript, subject_entries

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
CONTENT = ROOT / 'content'
LANGS = ('pt-br', 'en')
FIGURE = re.compile(r'\\par\\addvspace\{[^}]+\}\\noindent\\begin\{minipage\}.*?\\end\{minipage\}\\par\\addvspace\{[^}]+\}', re.S)
FIGURES = {
    'pt-br': {
        'tables': ('Em cada linha há 16 mesas. Na linha A, 12 deram cara e 9 repetiram a cara. Na linha B, foram 4 e 1.',
                   'Cada quadrado representa uma mesa nas contagens esperadas. Os quadrados coloridos deram cara na primeira jogada. Os escuros deram cara também na segunda.'),
        'likelihood': ('A verossimilhança relativa sobe até a taxa de caras de 0,75 e depois desce. A tangente no pico é horizontal.', ''),
        'margin': ('A perda logística cai continuamente com a margem. A perda hinge chega a zero na margem 1 e então permanece em zero.',
                   'Nas duas curvas, uma margem positiva corresponde à letra certa. Para a hinge, a partir de m = 1 a cobrança por aquele exemplo chega a zero.'),
    },
    'en': {
        'tables': ('Each row has 16 tables. In row A, 12 show a first head and 9 a second head as well. In row B the counts are 4 and 1.',
                   'Each square represents one table in the expected counts. Colored squares show heads on the first toss. Dark squares show heads on the second toss as well.'),
        'likelihood': ('Relative likelihood rises to a peak at a heads rate of 0.75 and then falls. The tangent at the peak is horizontal.', ''),
        'margin': ('Logistic loss falls continuously as the margin grows. Hinge loss reaches zero at a margin of 1 and stays there.',
                   'On both curves, a positive margin means the predicted letter is correct. For hinge loss, once m reaches 1 the charge for that example falls to zero.'),
    },
}

class SearchText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bits = []
        self.skip = 0

    def handle_starttag(self, name, attrs):
        if name == 'annotation':
            self.skip += 1

    def handle_endtag(self, name):
        if name == 'annotation':
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.bits.append(data.strip())

def plain(html):
    p = SearchText()
    p.feed(html)
    return ' '.join(' '.join(p.bits).split())

def render(source, lang):
    tex = source.split('\n', 1)[1]
    tex = re.sub(r'\\bookanchor\{([^{}]+)\}', r'\\hypertarget{\1}{}', tex)
    captions = {}
    def inline_figure(match):
        text = re.search(r'\\footnotesize\\raggedright (.*?)\\par\}', match[0], re.S)
        if not text:
            raise ValueError("Expected a caption inside the inline TikZ figure")
        captions['likelihood'] = text[1].strip()
        return '\n\nFIGURELIKELIHOOD\n\n'
    tex = FIGURE.sub(inline_figure, tex)
    tex = tex.replace(r'\perdasmargem', '\n\nFIGUREMARGIN\n\n').replace(r'\mesas', '\n\nFIGURETABLES\n\n')
    tex = re.sub(r'^\\secao\{(.*)\}$', r'\\section{\1}',tex,flags=re.M)
    tex = re.sub(r'^\\begin\{quadro\}\{(.*)\}$', r'\\begin{quote}'+'\n'+r'\\textbf{\1}'+'\n',tex,flags=re.M)
    # TeX's legacy \rm declaration is valid in print; texmath accepts \mathrm.
    tex = re.sub(r'\{\\rm\s+([^{}]+)\}', r'{\\mathrm{\1}}', tex)
    tex = tex.replace(r'\end{quadro}', r'\end{quote}')
    tex = re.sub(r'^\\itemq\{(.*?)\}\s*',r'\n\\textbf{\1.} ',tex,flags=re.M)
    tex = r'\newcommand{\F}{\mathcal F}'+'\n'+tex
    proc = subprocess.run(['pandoc','-f','latex','-t','html5','--math-method=mathml','--wrap=none'],input=tex,text=True,capture_output=True,check=True)
    if proc.stderr.strip():
        raise RuntimeError(proc.stderr.strip())
    html = proc.stdout.replace('<blockquote>', '<blockquote class="recap">')
    sections = []
    def heading(match):
        label = plain(match[1]); loc = f'section-{len(sections)+1}'
        sections.append((loc,label))
        return f'<h2 id="{loc}">{match[1]}</h2>'
    html = re.sub(r'<h1\b[^>]*>(.*?)</h1>',heading,html,flags=re.S)
    for key,(alt,caption) in FIGURES[lang].items():
        token='<p>FIGURE'+key.upper()+'</p>'
        if token in html:
            caption = captions.get(key,caption)
            html = html.replace(token,'<figure><img src="../assets/'+key+'-'+lang+'.svg" alt="'+escape(alt,quote=True)+'"><figcaption>'+escape(caption)+'</figcaption></figure>')
    return html,sections

def main():
    for lang in LANGS:
        directory = DOCS/lang
        directory.mkdir(parents=True,exist_ok=True)
        opening, parts = read_manuscript(CONTENT/lang, EDITION[lang])
        labels = EDITION[lang]
        index = Page('subject-index', labels['subjectIndex'], labels['frontmatter'], '', number=0)
        (directory/'index.html').write_text(landing(lang, opening, parts, index))
        pages = opening + [page for part in parts for page in part.pages] + [index]
        entries = []
        for i, page in enumerate(pages):
            if page is index:
                rows = []
                for term, refs in subject_entries(parts):
                    links = [f'<a href="{target.url}#{key}">{escape(target.label)}</a>' for target, key in refs]
                    rows.append(f'<dt>{escape(term)}</dt><dd>{", ".join(links)}</dd>')
                body, sections = '<dl class="subject-index">' + ''.join(rows) + '</dl>', []
            else:
                body, sections = render(page.source, lang)
            previous = pages[i-1] if i else None
            following = pages[i+1] if i+1 < len(pages) else None
            (directory/page.url).write_text(reader(lang, page, opening, parts, index, body, sections, previous, following))
            entries.append({'n': page.number, 'label': page.label, 'title': page.title, 'url': page.url, 'text': plain(body)})
        (DOCS/'assets'/f'search-{lang}.json').write_text(json.dumps(entries,ensure_ascii=False))
    (DOCS/'index.html').write_text(gateway())
    (DOCS/'.nojekyll').touch()

if __name__=='__main__':
    main()
