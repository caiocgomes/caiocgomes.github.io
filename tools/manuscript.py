"""Reading order shared by the print and web editions."""
from dataclasses import dataclass
import re


PART_ENDS = (("I", 7), ("II", 9), ("III", 11), ("IV", 13), ("V", 15))


@dataclass
class Page:
    slug: str
    tex_title: str
    label: str
    source: str
    number: int | None = None
    description: str = ""

    @property
    def title(self):
        return self.tex_title.replace(r"\%", "%")

    @property
    def url(self):
        return self.slug + ".html"


@dataclass
class Part:
    numeral: str
    label: str
    title: str
    pages: list[Page]
    planned: list[tuple[int, str]]


def read_page(path, heading_pattern, label, number=None, description=""):
    source = path.read_text(encoding="utf-8")
    source = re.sub(r"\A(?:[ \t]*%[^\n]*\n|\s*\n)*", "", source)
    heading = re.fullmatch(heading_pattern, source.split("\n", 1)[0].strip())
    if not heading:
        raise ValueError(f"Unexpected heading in {path}")
    return Page(path.stem, heading[1], label, source, number, description)


def read_manuscript(directory, labels):
    introduction = read_page(directory / "introduction.tex", r"\\bookintroduction\{(.+)\}",
                             labels["frontmatter"], number=0, description=labels["introductionDesc"])
    files = sorted(directory.glob("[0-9][0-9].tex"))
    if not files or [int(path.stem) for path in files] != list(range(1, len(files) + 1)):
        raise ValueError(f"Number the chapters in {directory} consecutively from 01.")

    parts = []
    first = 1
    for index, (numeral, end) in enumerate(PART_ENDS):
        pages = []
        planned = []
        last = max(end, len(files)) if index == len(PART_ENDS) - 1 else end
        for n in range(first, last + 1):
            if n <= len(files):
                description = labels["descriptions"][n-1] if n <= len(labels["descriptions"]) else ""
                pages.append(read_page(files[n-1], rf"\\capitulo\{{{n}\}}\{{(.+)\}}",
                                       f"{labels['chapter']} {n:02}", n, description))
            elif n in labels["upcoming"]:
                planned.append((n, labels["upcoming"][n]))
        if end <= len(files) and index + 1 < len(PART_ENDS):
            following = PART_ENDS[index+1][0]
            pages.append(read_page(directory / f"interlude-{end:02}.tex",
                                   rf"\\bookinterlude\{{{numeral}\}}\{{{following}\}}\{{(.+)\}}",
                                   f"{labels['interlude']} · {numeral} → {following}"))
        parts.append(Part(numeral, f"{labels['part']} {numeral}",
                          labels["partNames"][index], pages, planned))
        first = end + 1
    return introduction, parts
