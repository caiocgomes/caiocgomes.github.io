#!/usr/bin/env python3
"""Build PDF books, cover previews, bundled TeX sources and web TikZ figures.

Run from any directory: python3 tools/print_editions.py
Requires a TeX Live installation with latexmk, TikZ and standalone, and Poppler's pdftocairo.
"""
import argparse
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile, ZIP_DEFLATED

from layout import EDITION
from manuscript import read_manuscript


ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {"pt-br": "livro-pt-br", "en": "book-en"}
COVER_TEXT = {
    "pt-br": ("Como pensar em aprendizado de máquina", "EDIÇÃO EM PORTUGUÊS", "Capa"),
    "en": ("How to Think About Machine Learning", "ENGLISH EDITION", "Cover"),
}
PICTURE = re.compile(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", re.DOTALL)


def run(args, work):
    task = subprocess.run(args, cwd=work, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, errors="replace")
    if task.returncode:
        raise SystemExit(f"{' '.join(args)} failed in {work}\n{task.stdout[-5000:]}")


def render_figure(name, picture, colors, work, target):
    source = work / f"{name}.tex"
    source.write_text(
        r"""\documentclass[11pt,border=3pt]{standalone}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[sc]{mathpazo}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
""" + colors + "\n\\begin{document}\n" + picture + "\n\\end{document}\n",
        encoding="utf-8")
    run(["pdflatex", "-halt-on-error", "-interaction=nonstopmode", source.name], work)
    run(["pdftocairo", "-svg", f"{name}.pdf", f"{name}.svg"], work)
    shutil.copyfile(work / f"{name}.svg", target)


def render_interlude_proof(language, content, setup):
    name, title = ("interludios-pt-br", "Interlúdios") if language == "pt-br" else ("interludes-en", "Interludes")
    files = sorted((content / language).glob("interlude-[0-9][0-9].tex"))
    body = "\n\n".join(path.read_text(encoding="utf-8").strip() for path in files)
    heading = rf"\hypersetup{{pdftitle={{{title} · {EDITION[language]['title']}}},pdfsubject={{{title}}}}}"
    with TemporaryDirectory(prefix=f"interludes-{language}-") as temp:
        work = Path(temp)
        source = work / f"{name}.tex"
        source.write_text(setup + heading + "\n\\begin{document}\n" + body + "\n\\end{document}\n", encoding="utf-8")
        run(["latexmk", "-pdf", "-halt-on-error", "-interaction=nonstopmode", source.name], work)
        proofs = ROOT / "provas"
        proofs.mkdir(exist_ok=True)
        shutil.copyfile(source.with_suffix(".pdf"), proofs / f"{name}.pdf")
    print(f"Built {language}: {len(files)} interludes in provas/{name}.pdf.")


def render_edition(language, interludes_only=False):
    slug = EDITIONS[language]
    content = ROOT / "content"
    preamble = (content / f"preamble-{language}.tex").read_text(encoding="utf-8")
    frontmatter = (content / "frontmatter.tex").read_text(encoding="utf-8")
    labels = EDITION[language]
    interlude_label = rf"\newcommand{{\bookinterludename}}{{{labels['interlude']}}}"
    setup = preamble.rstrip() + "\n\n" + interlude_label + "\n" + frontmatter + "\n"
    if interludes_only:
        render_interlude_proof(language, content, setup)
        return
    cover = (content / "cover" / "cover.tex").read_text(encoding="utf-8")
    introduction, parts = read_manuscript(content / language, labels)
    pages = [page for part in parts for page in part.pages]
    chapters = [page for page in pages if page.number]
    contents = [
        r"\pagenumbering{roman}",
        rf"\bookfrontheading{{{labels['toc']}}}{{contents}}",
        rf"\booktocentry{{}}{{{introduction.tex_title}}}{{front:introduction}}",
    ]
    for part in parts:
        if part.pages:
            contents.append(rf"\booktocpart{{{part.label}}}{{{part.title}}}")
        for page in part.pages:
            if page.number:
                contents.append(rf"\booktocentry{{{page.number}}}{{{page.tex_title}}}{{chapter:{page.number}}}")
            else:
                contents.append(rf"\booktocentry{{}}{{\textit{{{labels['interlude']}}} · {page.tex_title}}}{{interlude:{part.numeral}}}")
    if any(part.planned for part in parts):
        contents.append(rf"\bookfrontheading{{{labels['forthcoming']}}}{{upcoming}}")
        for part in parts:
            if part.planned:
                contents.append(rf"\bookplannedpart{{{part.label}}}{{{part.title}}}")
                contents.extend(rf"\bookplannedentry{{{n}}}{{{title}}}" for n, title in part.planned)
    cover_command = "\\bookcover" + "".join("{" + text + "}" for text in COVER_TEXT[language])
    front = setup + cover + "\n\\begin{document}\n\n" + cover_command + "\n\n"
    book = front + "\n".join(contents) + "\n\n" + introduction.source + "\n\\clearpage\n\\pagenumbering{arabic}\n\n" + "\n\n".join(
        page.source.strip() for page in pages) + "\n\n\\end{document}\n"
    downloads = ROOT / "docs" / "downloads"
    assets = ROOT / "docs" / "assets"
    downloads.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f"coin-toss-{language}-") as temp:
        work = Path(temp)
        shutil.copyfile(content / "cover" / "coin-toss.png", work / "coin-toss.png")
        source = work / f"{slug}.tex"
        source.write_text(book, encoding="utf-8")
        run(["latexmk", "-pdf", "-halt-on-error", "-interaction=nonstopmode", source.name], work)
        log = source.with_suffix(".log").read_text(errors="replace")
        for item in re.findall(r"(?:Overfull \\[hv]box|Missing character:)[^\n]+", log):
            print(f"{language}: {item}")
        colors = "\n".join(re.findall(r"^\\definecolor[^\n]+", preamble, re.MULTILINE))
        # Two figures are reusable preamble macros. The likelihood curve lives with its text.
        for name, macro in (("tables", "mesas"), ("margin", "perdasmargem")):
            start = preamble.index("\\newcommand{\\" + macro + "}")
            picture = PICTURE.search(preamble, start)
            if not picture:
                raise ValueError(f"No TikZ picture found in {macro}.")
            render_figure(name, picture.group(), colors, work, assets / f"{name}-{language}.svg")
        peak, = PICTURE.findall(chapters[2].source)
        render_figure("likelihood", peak, colors, work, assets / f"likelihood-{language}.svg")
        for suffix in (".tex", ".pdf"):
            shutil.copyfile(source.with_suffix(suffix), downloads / f"{slug}{suffix}")
        with ZipFile(downloads / f"{slug}-source.zip", "w", ZIP_DEFLATED) as bundle:
            bundle.write(source, source.name)
            bundle.write(work / "coin-toss.png", "coin-toss.png")
        cover_source = work / f"cover-{language}.tex"
        cover_source.write_text(front + "\\end{document}\n", encoding="utf-8")
        run(["latexmk", "-pdf", "-halt-on-error", "-interaction=nonstopmode", cover_source.name], work)
        shutil.copyfile(cover_source.with_suffix(".pdf"), downloads / f"cover-{language}.pdf")
        run(["pdftocairo", "-png", "-singlefile", "-scale-to", "1600",
             cover_source.with_suffix(".pdf").name, f"cover-{language}"], work)
        shutil.copyfile(work / f"cover-{language}.png", assets / f"cover-{language}.png")
    print(f"Built {language}: {len(chapters)} chapters, PDF, TeX bundle, cover and three SVGs.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", choices=EDITIONS, help="Build just this language.")
    parser.add_argument("--interludes-only", action="store_true", help="Build author proofs of all interludes in provas/.")
    args = parser.parse_args()
    for language in ([args.edition] if args.edition else EDITIONS):
        render_edition(language, args.interludes_only)


if __name__ == "__main__":
    main()
