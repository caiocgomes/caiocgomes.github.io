"""Shared, dependency-free HTML for both editions of the book."""
from html import escape

EDITION = {
    "pt-br": {
        "html": "pt-BR", "title": "The CAIO Lectures on Machine Learning",
        "subtitle": "Como pensar em aprendizado de máquina", "lang": "Português",
        "brand": "Caderno de aprendizado", "toc": "Sumário", "home": "Capa", "search": "Buscar",
        "searchLabel": "Buscar neste livro", "hint": "Digite uma palavra ou expressão",
        "close": "Fechar", "skip": "Ir para o conteúdo", "chapter": "Capítulo", "chapters": "capítulos",
        "author": "Por Caio Gomes", "edition": "Edição em português", "begin": "Ler o primeiro capítulo",
        "pdf": "Baixar PDF", "pdfFile": "livro-pt-br.pdf", "prep": "Em preparação",
        "part": "Parte", "interlude": "Interlúdio",
        "partNames": ("A aposta e a moeda", "A régua contínua", "A cascata de perguntas",
                      "O apostador com agência", "A memória aberta"),
        "upcoming": {8: "O preço na reta real", 9: "A balança das retas",
                     10: "O jogo das vinte perguntas", 11: "Quando a floresta vê o que a árvore cega perde",
                     12: "Quanto custa descobrir a melhor alavanca?", 13: "O caixa fechado no futuro",
                     14: "Réguas multidimensionais e o gargalo do esquecimento",
                     15: "O Transformer: a mesa que nunca se fecha"},
        "contentsTitle": "Os capítulos", "contentsIntro": "Da primeira cara à escolha do que um modelo precisa guardar.",
        "open": "Índice de leitura", "previous": "Anterior", "next": "Próximo", "back": "Voltar ao sumário",
        "here": "Nesta página", "nav": "Navegação do livro", "languages": "Idioma da edição", "top": "Voltar ao topo",
        "desc": "Uma das minhas moedas dá cara três vezes em quatro. A outra, uma vez em quatro. Escolho uma delas ao acaso e lanço. Sai cara. Quanto você apostaria que escolhi a primeira?",
        "figure": "Um lançamento", "side1": "Cara", "side2": "Coroa", "plate": "Prancha",
        "intro": "Um livro aberto de", "number": "Cap.", "read": "Abrir capítulo",
        "introduction": "Introdução", "frontmatter": "Sobre este livro",
        "introductionDesc": "",
        "section": "Seção", "forthcoming": "Capítulos em preparação", "searchIntro": "Busque um conceito, um exemplo ou um capítulo.",
        "descriptions": (
            "Quando uma nova observação nos obriga a mudar de aposta?",
            "O que outra cara acrescenta àquilo que a primeira já ensinou?",
            "Como inferir a regra de uma moeda a partir dos lançamentos?",
            "O que muda quando lemos os mesmos dados em outra direção?",
            "Que informação o aprendiz pode esquecer depois de ver os dados?",
            "Quanto custa errar e por que há mais de um jeito de aprender a separar?",
            "Duas apostas iguais hoje mudam da mesma maneira amanhã?",
        ),
    },
    "en": {
        "html": "en", "title": "The CAIO Lectures on Machine Learning",
        "subtitle": "How to Think About Machine Learning", "lang": "English",
        "brand": "A notebook on learning", "toc": "Contents", "home": "Cover", "search": "Search",
        "searchLabel": "Search this book", "hint": "Enter a word or phrase",
        "close": "Close", "skip": "Skip to content", "chapter": "Chapter", "chapters": "chapters",
        "author": "By Caio Gomes", "edition": "English edition", "begin": "Read the first chapter",
        "pdf": "Download PDF", "pdfFile": "book-en.pdf", "prep": "In preparation",
        "part": "Part", "interlude": "Interlude",
        "partNames": ("The bet and the coin", "The continuous ruler", "A cascade of questions",
                      "The bettor with agency", "Open memory"),
        "upcoming": {8: "A price on the real line", 9: "Balancing the lines",
                     10: "The game of twenty questions", 11: "When the forest sees what one tree is blind to",
                     12: "What does it cost to find the best lever?", 13: "The cashbox that opens in the future",
                     14: "Multidimensional rulers and the bottleneck of forgetting",
                     15: "The Transformer: the table that never closes"},
        "contentsTitle": "The chapters", "contentsIntro": "From the first toss to deciding what a model needs to remember.",
        "open": "Reading menu", "previous": "Previous", "next": "Next", "back": "Back to contents",
        "here": "On this page", "nav": "Book navigation", "languages": "Edition language", "top": "Back to top",
        "desc": "One of my coins comes up heads three times out of four. The other does so once in four. I pick one at random and toss it. Heads. What would you bet that I picked the first coin?",
        "figure": "One toss", "side1": "Heads", "side2": "Tails", "plate": "Plate",
        "intro": "An open book on", "number": "Ch.", "read": "Open chapter",
        "introduction": "Introduction", "frontmatter": "About this book",
        "introductionDesc": "",
        "section": "Section", "forthcoming": "Chapters in preparation", "searchIntro": "Find a concept, an example, or a chapter.",
        "descriptions": (
            "When does a new observation oblige us to change a bet?",
            "What does a second head add to what the first one taught us?",
            "How can we infer a coin’s rule from the tosses we have seen?",
            "What changes when we read the same data in another direction?",
            "What can a learner afford to forget after seeing the data?",
            "What does a mistake cost, and why is there more than one way to learn to separate?",
            "Will two equal bets today change in the same way tomorrow?",
        ),
    },
}

def icon(name):
    paths = {
        "right": '<path d="M4 12h14m-5-5 5 5-5 5"/>',
        "left": '<path d="M20 12H6m5-5-5 5 5 5"/>',
        "down": '<path d="M12 3v11m-4-4 4 4 4-4M5 16v4h14v-4"/>',
        "search": '<circle cx="10.5" cy="10.5" r="6.3"/><path d="m15.3 15.3 5 5"/>',
        "book": '<path d="M4 5.5c3-.9 5.5-.5 8 1.1 2.5-1.6 5-2 8-1.1v13c-3-.9-5.5-.5-8 1.1-2.5-1.6-5-2-8-1.1Zm8 1.1v13"/>',
        "cross": '<path d="m6 6 12 12M18 6 6 18"/>',
    }
    return '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">'+paths[name]+'</svg>'

def mark():
    return '<svg class="imprint" aria-hidden="true" viewBox="0 0 38 38"><circle cx="19" cy="19" r="16.5" fill="none" stroke="currentColor" stroke-width="1.2"/><circle cx="19" cy="19" r="13.6" fill="none" stroke="currentColor" stroke-width=".55"/><path d="M9 23.2 14.8 14l4.1 6 4.3-8.5L29.1 24H9z" fill="none" stroke="currentColor" stroke-width="1.45" stroke-linejoin="round"/></svg>'

def shell(lang, title, summary, filename, inner):
    t = EDITION[lang]
    other = "en" if lang == "pt-br" else "pt-br"
    labels = {"pt-br":"PT-BR", "en":"EN"}
    source_label = "Fonte LaTeX" if lang == "pt-br" else "LaTeX source"
    source_file = t["pdfFile"].replace(".pdf", "-source.zip")
    edlinks = "".join(
        f'<a class="lang{" active" if code==lang else ""}" lang="{EDITION[code]["html"]}" hreflang="{EDITION[code]["html"]}" href="../{code}/{filename}"'
        + (' aria-current="true"' if code==lang else '') + f'>{labels[code]}</a>' for code in ("pt-br","en")
    )
    return f'''<!doctype html>
<html lang="{t["html"]}" data-edition="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(summary,quote=True)}"><meta name="author" content="Caio Gomes"><meta name="theme-color" content="#f9f6ed">
<link rel="alternate" hreflang="{EDITION[other]["html"]}" href="../{other}/{filename}"><link rel="stylesheet" href="../assets/book.css"><script defer src="../assets/book.js"></script></head>
<body id="top"><a class="skip" href="#main">{t["skip"]}</a>
<header class="mast"><div class="mast-inner"><a class="brand" href="index.html">{mark()}<span><strong>Caio Gomes</strong><small>{t["brand"]}</small></span></a>
<nav aria-label="{t["nav"]}"><a href="index.html#contents" class="nav-contents">{t["toc"]}</a>
<button class="search-open" type="button" data-search-open hidden aria-label="{t["searchLabel"]}">{icon("search")}<span>{t["search"]}</span></button>
<span class="langs" aria-label="{t["languages"]}">{edlinks}</span></nav></div></header>
{inner}
<footer class="foot"><span>{mark()} <b>Caio Gomes</b></span><a download href="../downloads/{source_file}">{source_label}</a><a href="#top">{t["top"]} ↑</a></footer>
<dialog class="search-dialog" aria-labelledby="search-title"><div class="dialog-title"><h2 id="search-title">{t["searchLabel"]}</h2><button type="button" data-search-close aria-label="{t["close"]}">{icon("cross")}</button></div>
<label class="search-entry">{icon("search")}<input type="search" autocomplete="off" aria-label="{t["searchLabel"]}" placeholder="{t["hint"]}"></label><p class="search-status" aria-live="polite">{t["searchIntro"]}</p><ul class="search-results"></ul></dialog></body></html>'''

def plate(t):
    # Openwork sun and crescent on two milled coins. All marks are vector linework.
    teeth = ''.join(f'<path d="M0 -73v3" transform="rotate({i*6})"/>' for i in range(60))
    rays = ''.join(f'<path d="M0 -30 Q3 -36 0 -43 Q-3 -47 0 -53" transform="rotate({i*15})"/>' for i in range(24))
    sun = f'<g fill="none" stroke="currentColor">{rays}<circle r="25" stroke-width="1.7"/><circle r="21.5" stroke-width=".8"/><circle r="16" fill="url(#lines)" stroke-width=".7"/></g>'
    moon = '<g fill="none" stroke="currentColor"><path d="M11-34a36 36 0 1 0 18 57A32 32 0 0 1 11-34Z" fill="url(#lines)" stroke-width="2"/><path d="m30-31 2.3 5.4 5.4 2.3-5.4 2.3-2.3 5.4-2.3-5.4-5.4-2.3 5.4-2.3Z"/><circle cx="40" cy="-1" r="1.3" fill="currentColor"/></g>'
    def coin(x,y,r,g):
        return f'<g transform="translate({x} {y}) rotate({r})"><g fill="#243f36" stroke="currentColor"><circle r="80" cy="5"/><circle r="80" stroke-width="2"/><circle r="76" stroke-width="1.2"/><g stroke-width=".85">{teeth}</g><circle r="66.5" stroke-width="1"/><circle r="64" stroke-dasharray="1 3" stroke-width=".7"/></g>{g}</g>'
    return f'''<svg class="cover-art" viewBox="0 0 455 335" role="img" aria-labelledby="plate-name"><title id="plate-name">{t["figure"]} · {t["side1"]} / {t["side2"]}</title>
<defs><pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="currentColor" opacity=".38"/></pattern><pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(38)"><path d="M0 0v4" stroke="currentColor" stroke-width="1.1"/></pattern></defs>
<rect width="455" height="335" fill="#253f36"/><rect x="12" y="12" width="431" height="311" fill="none" stroke="currentColor" opacity=".42"/>
<rect x="27" y="47" width="401" height="225" fill="url(#dots)"/>
<g fill="none" stroke="currentColor" opacity=".68"><path d="M54 184C92 104 212 57 285 97" stroke-dasharray="2 5"/><path d="M70 211c22 30 65 48 111 51" stroke-dasharray="2 5"/>
<path d="M26 31h11M31.5 25.5v11m387 268h11m-5.5-5.5v11" stroke-width=".8"/></g>
<g fill="currentColor" font-family="Georgia,serif" font-size="13" font-style="italic"><text x="43" y="35">Fig. 01</text><text x="418" y="35" text-anchor="end">A · B</text></g>
{coin(150,147,-12,sun)}{coin(290,186,14,moon)}
<path d="M29 278h397" stroke="currentColor" opacity=".55"/><g fill="currentColor" font-family="Georgia,serif" font-style="italic" font-size="17"><text x="33" y="305">{t["figure"]}</text></g><text fill="currentColor" font-family="monospace" font-size="11" letter-spacing="1" x="410" y="305" text-anchor="end">{t["side1"].upper()} / {t["side2"].upper()}</text></svg>'''

def search_attrs(page):
    return f'data-chapter-title="{escape(page.title, quote=True)}" data-page-label="{escape(page.label, quote=True)}"'


def landing(lang, introduction, parts):
    t = EDITION[lang]

    def catalog_row(page):
        number = f'{page.number:02}' if page.number else '—'
        detail = page.label if page.number is None else page.description
        note = f'<small>{escape(detail)}</small>' if detail else ''
        return (f'<li><a href="{page.url}" {search_attrs(page)}><span class="row-n">{number}</span>'
                f'<span class="row-t"><strong>{escape(page.title)}</strong>{note}</span>'
                f'<span class="row-arrow">{icon("right")}</span></a></li>')

    groups = [f'<ol class="chapter-list">{catalog_row(introduction)}</ol>']
    for part in parts:
        status = f'<small>{t["prep"]}</small>' if not part.pages else ''
        groups.append(f'<div class="group-head future"><span>{part.label}</span>'
                      f'<h3>{escape(part.title)}</h3>{status}</div>')
        if part.pages:
            groups.append('<ol class="chapter-list">' + ''.join(catalog_row(p) for p in part.pages) + '</ol>')
        if part.planned:
            rows = ''.join(f'<li><span>{n:02}</span>{escape(title)}</li>' for n, title in part.planned)
            if part.pages:
                groups.append(f'<p class="tiny">{t["forthcoming"]}</p>')
            groups.append(f'<ol class="planned" start="{part.planned[0][0]}">{rows}</ol>')
    inner = f'''<main id="main" class="home">
<section class="hero"><div class="hero-copy"><div class="kicker"><span></span>{t["edition"]}</div><h1>{escape(t["title"])}</h1><p class="sub">{t["subtitle"]}</p><p class="deck">{t["desc"]}</p>
<div class="actions"><a class="button primary" href="01.html">{t["begin"]}{icon("right")}</a><a class="button secondary" href="../downloads/{t["pdfFile"]}" download>{icon("down")}{t["pdf"]}</a></div></div>
<div class="plate-wrap">{plate(t)}</div></section>
<section id="contents" class="catalog" aria-labelledby="toc-heading"><div class="catalog-intro"><div class="kicker"><span></span>{t["toc"]}</div><h2 id="toc-heading">{t["contentsTitle"]}</h2><p>{t["contentsIntro"]}</p></div>
<div class="catalog-list">{''.join(groups)}</div></section></main>'''
    return shell(lang,t["title"]+' · Caio Gomes',t["desc"],'index.html',inner)

def reader(lang, page, introduction, parts, body, sections, previous, following):
    t = EDITION[lang]

    def link_attrs(target):
        current = ' aria-current="page"' if target.url == page.url else ''
        return f'href="{target.url}" {search_attrs(target)}{current}'

    groups = []
    for part in parts:
        if part.pages:
            links = []
            for entry in part.pages:
                number = f'{entry.number:02}' if entry.number else '—'
                links.append(f'<li><a {link_attrs(entry)}><span>{number}</span>{escape(entry.title)}</a></li>')
            groups.append(f'<p class="tiny">{part.label}</p><ol>{"".join(links)}</ol>')
    subsections = ''.join(f'<li><a href="#{escape(anchor,quote=True)}">{escape(label)}</a></li>' for anchor,label in sections)

    def page_nav(target, side):
        name = target.title if target else t["toc"]
        dest = target.url if target else 'index.html#contents'
        label = t["previous" if side == "left" else "next"] if target else t["back"]
        return f'<a class="pager-{side}" href="{dest}"><span>{icon(side)}{label}</span><b>{escape(name)}</b></a>'
    intro_link = f'<a class="contents-link" {link_attrs(introduction)}>{escape(introduction.title)}</a>'
    inner=f'''<main class="read-layout" id="main"><aside class="index-rail"><details class="book-menu" open><summary>{icon("book")} {t["open"]}</summary><div><a class="contents-link" href="index.html#contents">{t["toc"]}</a>{intro_link}{''.join(groups)}<a class="rail-pdf" href="../downloads/{t["pdfFile"]}" download>{icon("down")}{t["pdf"]}</a></div></details></aside>
<div class="reading"><header class="chapter-head"><a class="crumb" href="index.html">{escape(t["title"])}</a><div class="kicker"><span></span>{escape(page.label)}</div><h1>{escape(page.title)}</h1><div class="by">{t["author"]}</div></header>
{('<details class="local-index"><summary>'+t["here"]+'</summary><ol>'+subsections+'</ol></details>') if sections else ''}
<article class="prose">{body}</article><nav class="pager" aria-label="{t["nav"]}">{page_nav(previous,"left")}{page_nav(following,"right")}</nav></div></main>'''
    return shell(lang,page.title+' · '+t["title"],page.description or page.label,page.url,inner)
