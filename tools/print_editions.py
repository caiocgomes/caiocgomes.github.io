#!/usr/bin/env python3
"""Build downloadable, standalone TeX/PDF books and the web edition's TikZ figures.

Run from any directory: python3 tools/print_editions.py
Requires a TeX Live installation with latexmk, TikZ and standalone, and Poppler's pdftocairo.
"""
import argparse
import re
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
EDITIONS = {"pt-br": "livro-pt-br", "en": "book-en"}
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


def render_edition(language):
    slug = EDITIONS[language]
    content = ROOT / "content"
    preamble = (content / f"preamble-{language}.tex").read_text(encoding="utf-8")
    chapters = sorted((content / language).glob("[0-9][0-9].tex"))
    if not chapters or [int(p.stem) for p in chapters] != list(range(1, len(chapters) + 1)):
        raise SystemExit(f"Number the {language} chapter files consecutively from 01.")
    texts = [p.read_text(encoding="utf-8") for p in chapters]
    book = preamble.rstrip() + "\n\n\\begin{document}\n\n" + "\n\n".join(
        chapter.strip() for chapter in texts) + "\n\n\\end{document}\n"
    downloads = ROOT / "docs" / "downloads"
    assets = ROOT / "docs" / "assets"
    downloads.mkdir(parents=True, exist_ok=True)
    assets.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f"coin-toss-{language}-") as temp:
        work = Path(temp)
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
        peak, = PICTURE.findall(texts[2])
        render_figure("likelihood", peak, colors, work, assets / f"likelihood-{language}.svg")
        for suffix in (".tex", ".pdf"):
            shutil.copyfile(source.with_suffix(suffix), downloads / f"{slug}{suffix}")
    print(f"Built {language}: {len(chapters)} chapters, PDF, TeX and three SVGs.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--edition", choices=EDITIONS, help="Build just this language.")
    args = parser.parse_args()
    for language in ([args.edition] if args.edition else EDITIONS):
        render_edition(language)


if __name__ == "__main__":
    main()
