#!/usr/bin/env python3
"""Structural checks for the Bible commentary manuscript.

This is a Markdown-level checker, not a build. It verifies the things that can
be established before rendering: the 1,408-file manifest derived from
``bible/toc.xml``, headings, the commentary's required bold labels, chapter
length targets, the combined footnote namespace, pipe-table shape, local links,
house typography, and word counts. It does not verify that a citation supports
a claim, that a quotation matches its edition, that an exegetical judgment is
sound, that a visual asset exists, or that a table fits a typeset page.

Usage (from the repository root):
    python3 tools/check_book.py
    python3 tools/check_book.py --book GEN
    python3 tools/check_book.py chapters/ot/gen/001-gen-1.md
    python3 tools/check_book.py --list
    python3 tools/check_book.py --strict
    python3 tools/check_book.py --json

Exit status is 0 when there are no errors, 1 when there are errors (or, with
--strict, warnings), and 2 for invalid usage or a missing manifest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent if _HERE.name == "tools" else _HERE
CHAPTERS = "chapters"
EXPECTED_CHAPTERS = 1402


# ---------------------------------------------------------------------------
# Data structures


@dataclass
class Issue:
    level: str  # "error", "warning", or "info"
    code: str
    path: Path
    line: int
    message: str

    def as_dict(self, root: Path) -> dict:
        try:
            shown = str(self.path.relative_to(root))
        except ValueError:
            shown = str(self.path)
        return {
            "level": self.level,
            "code": self.code,
            "file": shown,
            "line": self.line,
            "message": self.message,
        }


@dataclass
class Heading:
    level: int
    text: str
    line: int
    number: tuple[int, ...] | None = None


@dataclass
class Table:
    start: int
    end: int
    columns: int
    rows: list[tuple[int, list[str]]] = field(default_factory=list)
    caption: str | None = None
    caption_line: int | None = None
    number: int | None = None


@dataclass
class ManifestEntry:
    path: Path
    kind: str  # "intro", "chapter", "appendix"
    testament: str | None = None
    book_code: str | None = None
    book_name: str | None = None
    chapter: int | None = None
    chapters_in_book: int | None = None
    appendix: str | None = None

    @property
    def reference(self) -> str:
        if self.kind == "chapter":
            if self.book_code == "PS2":
                return "Psalm 151"
            if self.chapters_in_book == 1:
                return self.book_name or ""
            return f"{self.book_name} {self.chapter}"
        if self.kind == "intro":
            return "Introduction"
        if self.kind == "appendix":
            return f"Appendix {self.appendix}"
        return ""


@dataclass
class Doc:
    path: Path
    text: str
    lines: list[str]
    masked: list[str]
    defs: dict[str, int] = field(default_factory=dict)
    refs: dict[str, list[int]] = field(default_factory=dict)
    headings: list[Heading] = field(default_factory=list)
    tables: list[Table] = field(default_factory=list)
    words: int = 0


@dataclass
class Stats:
    expected: int = 0
    found: int = 0
    missing: int = 0
    files: int = 0
    words: int = 0
    notes: int = 0
    tables: int = 0
    links: int = 0


# ---------------------------------------------------------------------------
# File manifest


def load_manifest(root: Path) -> list[ManifestEntry]:
    """Build the stable manifest from ``bible/toc.xml``.

    The XML table of contents is authoritative. A book's declared chapter
    count must match its chapter elements, and the chapter numbers must run
    from 1 to that count without gaps or duplicates.
    """
    toc_path = root / "bible" / "toc.xml"
    if not toc_path.is_file():
        raise FileNotFoundError(f"manifest not found: {toc_path}")

    tree = ET.parse(toc_path)
    toc_root = tree.getroot()

    entries: list[ManifestEntry] = [
        ManifestEntry(path=root / CHAPTERS / "00-introduction.md", kind="intro")
    ]

    for testament in toc_root.findall("testament"):
        testament_code = testament.get("code")
        if not testament_code:
            raise ValueError("testament element has no code")
        for book in testament.findall("book"):
            code = book.get("code")
            name = book.get("name")
            directory = book.get("directory")
            declared = book.get("chapters")
            if not code or not name or not directory or not declared:
                raise ValueError(f"incomplete book element: {book.attrib}")
            chapter_elements = book.findall("chapter")
            declared_count = int(declared)
            if len(chapter_elements) != declared_count:
                raise ValueError(
                    f"book {code} declares {declared_count} chapters "
                    f"but contains {len(chapter_elements)}"
                )
            numbers = [int(element.get("number", "0")) for element in chapter_elements]
            if numbers != list(range(1, declared_count + 1)):
                raise ValueError(
                    f"book {code} chapter numbers are not 1..{declared_count}: {numbers}"
                )
            for number in numbers:
                filename = f"{number:03d}-{code.lower()}-{number}.md"
                entries.append(
                    ManifestEntry(
                        path=root / CHAPTERS / directory / filename,
                        kind="chapter",
                        testament=testament_code,
                        book_code=code,
                        book_name=name,
                        chapter=number,
                        chapters_in_book=declared_count,
                    )
                )

    for index, letter in enumerate("abcde"):
        entries.append(
            ManifestEntry(
                path=root / CHAPTERS / f"{51 + index}-appendix-{letter}.md",
                kind="appendix",
                appendix=letter.upper(),
            )
        )

    seen: set[Path] = set()
    for entry in entries:
        key = entry.path.resolve()
        if key in seen:
            raise ValueError(f"duplicate manifest path: {entry.path}")
        seen.add(key)
    return entries


def expected_files(root: Path) -> list[Path]:
    return [entry.path for entry in load_manifest(root)]


def expected_prefix(path: Path) -> str | None:
    """Return the required footnote prefix for a manuscript file."""
    name = path.name
    if name == "00-introduction.md":
        return "intro-"
    match = re.fullmatch(r"5[1-5]-appendix-([a-e])\.md", name)
    if match:
        return f"app-{match.group(1)}-"
    match = re.fullmatch(r"\d{3}-([a-z0-9]+)-(\d+)\.md", name)
    if match:
        return f"{match.group(1)}-{match.group(2)}-"
    return None


def reference_variants(entry: ManifestEntry) -> list[str]:
    """Return acceptable ways a chapter title may name its reference."""
    name = entry.book_name or ""
    number = entry.chapter or 0
    if entry.book_code == "PS2":
        return ["Psalm 151", "Psalm 151 1"]
    if entry.book_code == "PSA":
        return [f"Psalm {number}", f"Psalms {number}"]
    if entry.chapters_in_book == 1:
        variants = [name, f"{name} 1"]
    else:
        variants = [f"{name} {number}"]
    if entry.book_code == "ESG":
        variants += [f"Esther {number}", f"Greek Esther {number}"]
    if entry.book_code == "DAG":
        variants += [f"Daniel {number}", f"Greek Daniel {number}"]
    return variants


def normalize_title(text: str) -> str:
    text = re.sub(r"[*_`#]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


# ---------------------------------------------------------------------------
# Masking and parsing


def mask_document(text: str) -> list[str]:
    """Return lines with code spans, link targets, and URLs blanked out.

    Length is preserved so column positions and line numbers remain valid.
    """
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    fence = ""
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence = True, marker
                out.append(" " * len(line))
                continue
            if marker == fence:
                in_fence = False
                out.append(" " * len(line))
                continue
        if in_fence:
            out.append(" " * len(line))
            continue
        masked = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        masked = re.sub(
            r"\]\([^)]*\)",
            lambda m: "](" + " " * (len(m.group(0)) - 3) + ")",
            masked,
        )
        masked = re.sub(r"https?://\S+", lambda m: " " * len(m.group(0)), masked)
        out.append(masked)
    return out


DEF_RE = re.compile(r"^\[\^([^\]\s]+)\]:")
REF_RE = re.compile(r"\[\^([^\]\s]+)\](?!:)")


def parse_document(path: Path) -> Doc:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    masked = mask_document(text)
    doc = Doc(path=path, text=text, lines=lines, masked=masked)

    for i, line in enumerate(masked, start=1):
        match = DEF_RE.match(line)
        if match:
            doc.defs[match.group(1)] = i
        for ref in REF_RE.finditer(line):
            doc.refs.setdefault(ref.group(1), []).append(i)

    doc.headings = parse_headings(masked)
    doc.tables = parse_tables(lines, masked)
    doc.words = count_words(masked, doc.defs)
    return doc


def parse_headings(masked: list[str]) -> list[Heading]:
    headings: list[Heading] = []
    for i, line in enumerate(masked, start=1):
        match = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        number = None
        numbered = re.match(r"^(\d+(?:\.\d+)*)\.\s+", text)
        if numbered:
            number = tuple(int(part) for part in numbered.group(1).split("."))
        headings.append(Heading(level=level, text=text, line=i, number=number))
    return headings


def split_row(line: str) -> list[str]:
    value = line.strip()
    while value.startswith(">"):
        value = value[1:].lstrip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|"):
        value = value[:-1]
    return [cell.strip() for cell in re.split(r"(?<!\\)\|", value)]


def is_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def parse_tables(lines: list[str], masked: list[str]) -> list[Table]:
    tables: list[Table] = []
    i = 0
    while i < len(lines) - 1:
        if "|" not in masked[i] or "|" not in masked[i + 1]:
            i += 1
            continue
        header = split_row(masked[i])
        separator = split_row(masked[i + 1])
        if is_separator(header) or not is_separator(separator):
            i += 1
            continue
        columns = len(header)
        table = Table(start=i + 1, end=i + 2, columns=columns)
        j = i + 2
        while j < len(lines) and "|" in masked[j] and masked[j].strip():
            if masked[j].lstrip().startswith("#"):
                break
            table.rows.append((j + 1, split_row(masked[j])))
            table.end = j + 1
            j += 1
        tables.append(table)
        i = max(j, i + 2)
    return tables


def count_words(lines: list[str], defs: dict[str, int]) -> int:
    """Count body words, excluding fenced code and footnote definitions."""
    text_lines: list[str] = []
    in_fence = False
    fence = ""
    def_lines = set()
    for key, start in defs.items():
        def_lines.add(start)
        n = start
        while n < len(lines):
            line = lines[n]
            if line.strip() and not line.startswith((" ", "\t")):
                break
            if line.strip():
                def_lines.add(n + 1)
            n += 1
    for i, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence, fence = True, marker
                continue
            if marker == fence:
                in_fence = False
                continue
        if in_fence or i in def_lines:
            continue
        if "|" in line and is_separator(split_row(line)):
            continue
        line = REF_RE.sub("", line)
        text_lines.append(line)
    words = re.findall(r"[\w’'-]+", "\n".join(text_lines), re.UNICODE)
    return len(words)


# ---------------------------------------------------------------------------
# Commentary labels

LABEL_ALIASES = {"the passage": "The text"}

LABEL_RANK = {
    "The text": 10,
    "Context": 20,
    "History": 30,
    "Form": 30,
    "Language": 30,
    "A closer look": 30,
    "Exposition": 40,
    "Interpretive options": 45,
    "Christian reading": 50,
    "Theology": 60,
    "Ethics": 60,
    "Teaching and application": 70,
    "For reflection": 80,
    "Further reading": 90,
    "Textual note": 90,
}

LABEL_CANONICAL = {name.lower(): name for name in LABEL_RANK}

REQUIRED_LABELS = ["The text", "Context", "Exposition", "Christian reading"]


# ---------------------------------------------------------------------------
# Checks


class Checker:
    def __init__(self, root: Path):
        self.root = root
        self.issues: list[Issue] = []
        self.stats = Stats()

    def add(self, level: str, code: str, path: Path, line: int, message: str) -> None:
        self.issues.append(Issue(level, code, path, line, message))

    # -- per-file checks ---------------------------------------------------

    def check_doc(self, doc: Doc, entry: ManifestEntry | None) -> None:
        self.stats.files += 1
        self.stats.words += doc.words
        self.stats.notes += len(doc.defs)
        self.stats.tables += len(doc.tables)
        self.check_title(doc, entry)
        self.check_headings(doc)
        self.check_labels(doc, entry)
        self.check_chapter_length(doc, entry)
        self.check_tables(doc)
        self.check_typography(doc)
        self.check_definitions(doc)
        self.check_links(doc)

    def check_title(self, doc: Doc, entry: ManifestEntry | None) -> None:
        first = next((i for i, line in enumerate(doc.lines) if line.strip()), None)
        if first is None:
            self.add("error", "file-empty", doc.path, 1, "file is empty")
            return
        line = doc.lines[first]
        if not re.match(r"^#\s+\S", line):
            self.add(
                "error",
                "title-missing",
                doc.path,
                first + 1,
                "first nonblank line must be a level-one heading",
            )
        h1s = [h for h in doc.headings if h.level == 1]
        if len(h1s) != 1:
            self.add(
                "error",
                "title-count",
                doc.path,
                h1s[1].line if len(h1s) > 1 else 1,
                f"expected exactly one level-one heading, found {len(h1s)}",
            )
        if entry is None or not h1s:
            return
        title = normalize_title(h1s[0].text)
        if entry.kind == "chapter":
            variants = [normalize_title(value) for value in reference_variants(entry)]
            if not any(value in title for value in variants):
                self.add(
                    "warning",
                    "title-reference",
                    doc.path,
                    h1s[0].line,
                    f"title does not name the expected reference: {entry.reference}",
                )
        elif entry.kind == "intro":
            if "introduction" not in title:
                self.add(
                    "warning",
                    "title-reference",
                    doc.path,
                    h1s[0].line,
                    "Introduction title does not contain “Introduction”",
                )
        elif entry.kind == "appendix" and entry.appendix:
            if f"appendix {entry.appendix.lower()}" not in title:
                self.add(
                    "warning",
                    "title-reference",
                    doc.path,
                    h1s[0].line,
                    f"appendix title does not contain “Appendix {entry.appendix}”",
                )

    def check_headings(self, doc: Doc) -> None:
        previous = 0
        numbered_h2: list[Heading] = []
        for heading in doc.headings:
            if previous and heading.level > previous + 1:
                self.add(
                    "error",
                    "heading-skip",
                    doc.path,
                    heading.line,
                    f"heading level jumps from {previous} to {heading.level}",
                )
            previous = heading.level
            if heading.level == 2 and heading.number and len(heading.number) == 1:
                numbered_h2.append(heading)
            if heading.level == 3 and heading.number and len(heading.number) == 2:
                if not numbered_h2:
                    self.add(
                        "error",
                        "subsection-orphan",
                        doc.path,
                        heading.line,
                        "numbered subsection has no numbered section",
                    )
                elif heading.number[0] != numbered_h2[-1].number[0]:
                    self.add(
                        "error",
                        "subsection-parent",
                        doc.path,
                        heading.line,
                        f"subsection {heading.number[0]}.{heading.number[1]} "
                        f"is under section {numbered_h2[-1].number[0]}",
                    )
        if numbered_h2:
            expected = list(range(1, len(numbered_h2) + 1))
            actual = [h.number[0] for h in numbered_h2]
            if actual != expected:
                first_bad = next(
                    (h for h, want in zip(numbered_h2, expected) if h.number[0] != want),
                    numbered_h2[-1],
                )
                self.add(
                    "error",
                    "section-sequence",
                    doc.path,
                    first_bad.line,
                    f"numbered sections are {actual}, expected {expected}",
                )
            current = None
            expected_sub = 0
            for heading in [
                h
                for h in doc.headings
                if h.level == 3 and h.number and len(h.number) == 2
            ]:
                parent = heading.number[0]
                if parent != current:
                    current = parent
                    expected_sub = 0
                expected_sub += 1
                if heading.number[1] != expected_sub:
                    self.add(
                        "error",
                        "subsection-sequence",
                        doc.path,
                        heading.line,
                        f"subsection {parent}.{heading.number[1]} is out of order; "
                        f"expected {parent}.{expected_sub}",
                    )

    def check_labels(self, doc: Doc, entry: ManifestEntry | None) -> None:
        if entry is None or entry.kind != "chapter":
            return
        first_def = min(doc.defs.values()) if doc.defs else len(doc.lines) + 1
        found: list[tuple[int, str, int]] = []
        for i, line in enumerate(doc.masked, start=1):
            if i >= first_def:
                break
            stripped = line.strip()
            if not stripped.startswith("**") or stripped.startswith("|"):
                continue
            match = re.match(r"^\*\*([^*]+?)\.\*\*(.*)$", stripped)
            if not match:
                continue
            raw = match.group(1).strip()
            raw_lower = raw.lower()
            canonical = LABEL_ALIASES.get(raw_lower) or LABEL_CANONICAL.get(raw_lower)
            if canonical is None:
                self.add(
                    "warning",
                    "label-unknown",
                    doc.path,
                    i,
                    f"unknown bold label: {raw!r}; see AGENTS.md §5",
                )
                continue
            tail = match.group(2).strip()
            if not tail:
                self.add(
                    "warning",
                    "label-empty",
                    doc.path,
                    i,
                    f"label **{raw}.** has no text after it",
                )
            found.append((LABEL_RANK[canonical], canonical, i))

        present = {label for _, label, _ in found}
        for label in REQUIRED_LABELS:
            if label not in present:
                self.add(
                    "warning",
                    "label-missing",
                    doc.path,
                    1,
                    f"missing required label: **{label}.**",
                )

        counts = Counter(label for _, label, _ in found)
        for label in REQUIRED_LABELS:
            if counts[label] > 1:
                self.add(
                    "warning",
                    "label-duplicate",
                    doc.path,
                    next(line for _, name, line in found if name == label),
                    f"required label **{label}.** appears {counts[label]} times",
                )

        last_rank = 0
        for rank, label, line_number in found:
            if rank < last_rank:
                self.add(
                    "warning",
                    "label-order",
                    doc.path,
                    line_number,
                    f"**{label}.** appears out of order",
                )
            last_rank = max(last_rank, rank)

    def check_chapter_length(self, doc: Doc, entry: ManifestEntry | None) -> None:
        if entry is None or entry.kind != "chapter":
            return
        if doc.words < 250:
            self.add(
                "warning",
                "chapter-short",
                doc.path,
                1,
                f"chapter has {doc.words} body words; the standard target is 350–550",
            )
        elif doc.words > 900:
            self.add(
                "warning",
                "chapter-long",
                doc.path,
                1,
                f"chapter has {doc.words} body words; emphasis must be recorded and "
                f"the two-page ceiling is about 900",
            )
        elif doc.words > 650:
            self.add(
                "info",
                "chapter-emphasis",
                doc.path,
                1,
                f"chapter has {doc.words} body words; review whether the emphasis "
                f"allowance is recorded in README.md",
            )

    def check_tables(self, doc: Doc) -> None:
        for table in doc.tables:
            header = split_row(doc.masked[table.start - 1])
            separator = split_row(doc.masked[table.start])
            if len(header) != len(separator):
                self.add(
                    "error",
                    "table-header",
                    doc.path,
                    table.start,
                    f"header has {len(header)} cells but separator has {len(separator)}",
                )
            for line, cells in table.rows:
                if len(cells) != table.columns:
                    self.add(
                        "error",
                        "table-ragged",
                        doc.path,
                        line,
                        f"row has {len(cells)} cells; expected {table.columns}",
                    )
            if not table.rows:
                self.add(
                    "warning",
                    "table-empty",
                    doc.path,
                    table.start,
                    "table has no body rows",
                )
            self.find_caption(doc, table)
            if table.caption is None:
                self.add(
                    "info",
                    "table-uncaptioned",
                    doc.path,
                    table.start,
                    "table has no caption; treated as a planning table, not a registered manuscript table",
                )
                continue
            self.check_table_reference(doc, table)
            self.check_table_bold(doc, table)

    def find_caption(self, doc: Doc, table: Table) -> None:
        for offset in range(0, 5):
            index = table.end + offset
            if index >= len(doc.lines):
                break
            line = doc.lines[index].strip()
            if not line:
                continue
            match = re.match(r"^\*\*Caption\.\*\*", line)
            number_match = re.search(r"Table\s+(\d+)", line)
            if match:
                table.caption = line
                table.caption_line = index + 1
                if number_match:
                    table.number = int(number_match.group(1))
                return
            break

    def check_table_reference(self, doc: Doc, table: Table) -> None:
        if table.number is None:
            return
        pattern = re.compile(rf"\bTable\s+{table.number}\b")
        exclude = set(range(table.start, table.end + 1))
        if table.caption_line:
            exclude.add(table.caption_line)
        for i, line in enumerate(doc.masked, start=1):
            if i in exclude:
                continue
            if pattern.search(line):
                return
        self.add(
            "warning",
            "table-reference",
            doc.path,
            table.start,
            f"Table {table.number} is never cited in the surrounding text",
        )

    def check_table_bold(self, doc: Doc, table: Table) -> None:
        for line, cells in table.rows:
            if not cells:
                continue
            if not re.fullmatch(r"\*\*.+\*\*", cells[0]):
                self.add(
                    "warning",
                    "table-leading-cell",
                    doc.path,
                    line,
                    "leading cell is not bold",
                )

    def check_typography(self, doc: Doc) -> None:
        for i, line in enumerate(doc.masked, start=1):
            raw_line = doc.lines[i - 1]
            if '"' in line:
                self.add(
                    "error",
                    "straight-double-quote",
                    doc.path,
                    i,
                    "use curly quotation marks",
                )
            if "'" in line:
                self.add(
                    "error",
                    "straight-apostrophe",
                    doc.path,
                    i,
                    "use curly apostrophes",
                )
            if "..." in line:
                self.add(
                    "error",
                    "three-periods",
                    doc.path,
                    i,
                    "use the ellipsis character …",
                )
            if "\u00a0" in line:
                self.add(
                    "error",
                    "nonbreaking-space",
                    doc.path,
                    i,
                    "use an ordinary space",
                )
            if raw_line.rstrip("\n").endswith("  "):
                self.add(
                    "warning",
                    "hard-break",
                    doc.path,
                    i,
                    "paragraph ends with a Markdown hard break",
                )
            if re.search(r"\t", raw_line):
                self.add("warning", "tab", doc.path, i, "line contains a tab")
            if re.search(
                r"\b(?:Chs?\.|chapters?|vv?\.|verses?|pp?\.|pages?)\s*\d+-\d+",
                line,
            ):
                self.add(
                    "error",
                    "hyphen-range",
                    doc.path,
                    i,
                    "use an en dash in a range",
                )
            for match in re.finditer(r"(?<![\w-])(\d{4})-(\d{2}|\d{4})(?![\w-])", line):
                tail = line[match.start() : match.end() + 1]
                if re.match(r"\d{4}-\d{2}-\d{2}", tail):
                    continue
                self.add(
                    "error",
                    "hyphen-range",
                    doc.path,
                    i,
                    f"use an en dash in the range {match.group(0)}",
                )
            if re.search(r"\b\d+:\d+-\d+(?=[\s,;.)]|$)", line):
                self.add(
                    "error",
                    "hyphen-range",
                    doc.path,
                    i,
                    "use an en dash in a Scripture verse range",
                )
            if re.search(r"(?<!-)(?<!---)--(?!-)(?!-)", line):
                self.add(
                    "warning",
                    "double-hyphen",
                    doc.path,
                    i,
                    "use an em dash or en dash, not --",
                )

    def check_definitions(self, doc: Doc) -> None:
        if not doc.defs:
            return
        first_def = min(doc.defs.values())
        for i, line in enumerate(doc.lines, start=1):
            if i <= first_def or not line.strip():
                continue
            if DEF_RE.match(line):
                continue
            if line.startswith((" ", "\t")):
                continue
            self.add(
                "error",
                "content-after-notes",
                doc.path,
                i,
                "content appears after the footnote definitions",
            )
            break

        for key, start in doc.defs.items():
            if re.fullmatch(r"\d+", key):
                self.add(
                    "error",
                    "note-numeric-key",
                    doc.path,
                    start,
                    f"footnote key {key!r} is numeric; use a descriptive key",
                )
            prefix = expected_prefix(doc.path)
            if prefix and not key.startswith(prefix):
                self.add(
                    "warning",
                    "note-prefix",
                    doc.path,
                    start,
                    f"footnote key {key!r} does not start with {prefix!r}",
                )
            block = definition_block(doc.lines, start)
            body = block.split("]:", 1)[-1].lstrip()
            if not body:
                self.add(
                    "warning",
                    "note-empty",
                    doc.path,
                    start,
                    f"footnote {key!r} has no content",
                )
            if re.search(r"\bibid\.?\b", block, re.IGNORECASE):
                self.add(
                    "error",
                    "note-ibid",
                    doc.path,
                    start,
                    "do not use ibid.; give the short citation",
                )
            for ref in REF_RE.finditer(block):
                self.add(
                    "error",
                    "note-nested-reference",
                    doc.path,
                    start,
                    f"definition for {key!r} contains a footnote reference",
                )
            has_used_for = "Used for:" in block
            has_label = body.startswith(
                ("Editorial check —", "Explanation —", "Text —")
            )
            has_url = "http" in block.lower() or "doi:" in block.lower()
            if has_url and not has_used_for:
                self.add(
                    "warning",
                    "note-used-for",
                    doc.path,
                    start,
                    f"citation note {key!r} has no 'Used for:' annotation",
                )
            elif not has_label and not has_used_for:
                self.add(
                    "warning",
                    "note-annotation",
                    doc.path,
                    start,
                    f"note {key!r} needs 'Used for:', an 'Explanation —', "
                    f"'Text —', or 'Editorial check —' label",
                )

    def check_links(self, doc: Doc) -> None:
        for i, line in enumerate(doc.lines, start=1):
            if not line.strip() or doc.masked[i - 1].strip() == "":
                continue
            for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", line):
                if match.start() > 0 and line[match.start() - 1] == "!":
                    continue
                target = match.group(1).strip()
                if target.startswith("<") and target.endswith(">"):
                    target = target[1:-1]
                target = target.split()[0] if target else ""
                if not target or target.startswith(
                    ("http://", "https://", "mailto:", "tel:", "#")
                ):
                    continue
                self.stats.links += 1
                path_part, _, anchor = target.partition("#")
                path_part = unquote(path_part)
                if not path_part:
                    target_path = doc.path
                else:
                    target_path = (doc.path.parent / path_part).resolve()
                if not target_path.exists():
                    self.add(
                        "error",
                        "link-missing",
                        doc.path,
                        i,
                        f"link target does not exist: {target}",
                    )
                    continue
                if anchor:
                    self.check_anchor(doc, i, target_path, anchor, target)

    def check_anchor(
        self, doc: Doc, line: int, target_path: Path, anchor: str, target: str
    ) -> None:
        try:
            text = target_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return
        slugs = set()
        for heading_line in mask_document(text):
            match = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", heading_line)
            if match:
                slugs.add(slugify(match.group(1)))
        if anchor not in slugs:
            self.add(
                "warning",
                "link-anchor",
                doc.path,
                line,
                f"link anchor not found in target: {target}",
            )

    # -- cross-file checks -------------------------------------------------

    def check_notes(self, docs: list[Doc]) -> None:
        definitions: dict[str, list[tuple[Path, int]]] = defaultdict(list)
        for doc in docs:
            for key, line in doc.defs.items():
                definitions[key].append((doc.path, line))

        for key, places in definitions.items():
            if len(places) > 1:
                path, line = places[1]
                first = places[0]
                self.add(
                    "error",
                    "note-duplicate-definition",
                    path,
                    line,
                    f"footnote {key!r} is already defined at "
                    f"{first[0].name}:{first[1]}",
                )

        for doc in docs:
            for key, lines in doc.refs.items():
                if key not in doc.defs:
                    self.add(
                        "error",
                        "note-missing-definition",
                        doc.path,
                        lines[0],
                        f"footnote {key!r} has no definition in this file",
                    )
            for key, line in doc.defs.items():
                if key not in doc.refs:
                    self.add(
                        "error",
                        "note-unused-definition",
                        doc.path,
                        line,
                        f"footnote {key!r} is defined but never referenced in this file",
                    )

    def check_sources_heading(self, doc: Doc) -> None:
        for i, line in enumerate(doc.masked, start=1):
            if re.match(
                r"^#{1,6}\s+(?:Sources|References|Bibliography|Works Cited)\s*$",
                line,
                re.IGNORECASE,
            ):
                self.add(
                    "error",
                    "separate-sources",
                    doc.path,
                    i,
                    "citations belong in the combined footnote list, not a separate list",
                )
            if re.match(
                r"^#{1,6}\s+(?:Notes|Footnotes)\s*$",
                line,
                re.IGNORECASE,
            ):
                self.add(
                    "error",
                    "separate-notes-heading",
                    doc.path,
                    i,
                    "do not add a manual heading for the footnote list",
                )


def definition_block(lines: list[str], start: int) -> str:
    selected = [lines[start - 1]]
    n = start
    while n < len(lines):
        line = lines[n]
        if line.strip() and not line.startswith((" ", "\t")):
            break
        selected.append(line)
        n += 1
    return "\n".join(selected)


def slugify(text: str) -> str:
    text = re.sub(r"[`*_~\[\]()]", "", text)
    text = unicodedata.normalize("NFKD", text)
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s]+", "-", text).strip("-")
    return text


# ---------------------------------------------------------------------------
# Runner


def run(
    paths: list[Path],
    root: Path,
    full_manifest: bool,
    manifest: list[ManifestEntry],
) -> Checker:
    checker = Checker(root)
    checker.stats.expected = len(paths)
    by_path = {entry.path.resolve(): entry for entry in manifest}

    chapter_count = sum(1 for entry in manifest if entry.kind == "chapter")
    if chapter_count != EXPECTED_CHAPTERS:
        checker.add(
            "warning",
            "manifest-count",
            root / "bible" / "toc.xml",
            1,
            f"manifest contains {chapter_count} Bible chapters; "
            f"README.md and AGENTS.md plan for {EXPECTED_CHAPTERS}",
        )

    docs: list[Doc] = []
    for path in paths:
        if not path.exists():
            checker.add(
                "error",
                "file-missing",
                path,
                1,
                "manuscript file is missing",
            )
            continue
        doc = parse_document(path)
        docs.append(doc)
        checker.check_doc(doc, by_path.get(path.resolve()))

    checker.check_notes(docs)
    for doc in docs:
        checker.check_sources_heading(doc)

    checker.stats.found = len(docs)
    checker.stats.missing = checker.stats.expected - checker.stats.found

    if full_manifest:
        expected = {path.resolve() for path in paths}
        chapters_dir = root / CHAPTERS
        if chapters_dir.is_dir():
            for path in sorted(chapters_dir.rglob("*.md")):
                if path.resolve() not in expected:
                    checker.add(
                        "warning",
                        "file-extra",
                        path,
                        1,
                        "file is not part of the stable manifest",
                    )
    return checker


def format_issue(issue: Issue, root: Path) -> str:
    data = issue.as_dict(root)
    return (
        f"{data['level'].upper()} {data['file']}:{data['line']}: "
        f"[{data['code']}] {data['message']}"
    )


def print_capped(
    issues: list[Issue], root: Path, max_per_code: int = 20
) -> None:
    counts = Counter(issue.code for issue in issues)
    shown = Counter()
    for issue in issues:
        if shown[issue.code] >= max_per_code:
            continue
        shown[issue.code] += 1
        print(format_issue(issue, root))
    for code, count in counts.items():
        if count > max_per_code:
            print(f"... and {count - max_per_code} more [{code}]")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check the Bible commentary for structural, citation, table, link, and style problems.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="manuscript files to check; default is the full stable manifest",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root (default: detected from the script location)",
    )
    parser.add_argument(
        "--book",
        metavar="CODE",
        help="check only the chapters of one biblical book, e.g. GEN or 1CO",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="print the expected manuscript paths and exit",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="treat warnings as failures",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a JSON report",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print only the summary",
    )
    args = parser.parse_args(argv)

    if args.book and args.paths:
        parser.error("--book cannot be combined with positional paths")
    if args.list and args.paths:
        parser.error("--list cannot be combined with positional paths")

    root = args.root.resolve()
    try:
        manifest = load_manifest(root)
    except (FileNotFoundError, ValueError, ET.ParseError) as exc:
        print(f"check_book: {exc}", file=sys.stderr)
        return 2

    if args.list:
        selected = manifest
        if args.book:
            code = args.book.upper()
            selected = [
                entry
                for entry in manifest
                if entry.book_code and entry.book_code.upper() == code
            ]
            if not selected:
                print(f"check_book: unknown book code {args.book!r}", file=sys.stderr)
                return 2
        for entry in selected:
            try:
                shown = entry.path.relative_to(root)
            except ValueError:
                shown = entry.path
            print(shown)
        return 0

    if args.book:
        code = args.book.upper()
        selected = [
            entry
            for entry in manifest
            if entry.book_code and entry.book_code.upper() == code
        ]
        if not selected:
            print(f"check_book: unknown book code {args.book!r}", file=sys.stderr)
            return 2
        paths = [entry.path for entry in selected]
        full_manifest = False
    elif args.paths:
        paths = [
            Path(p) if Path(p).is_absolute() else (root / p) for p in args.paths
        ]
        full_manifest = False
    else:
        paths = [entry.path for entry in manifest]
        full_manifest = True

    checker = run(paths, root, full_manifest, manifest)
    errors = [issue for issue in checker.issues if issue.level == "error"]
    warnings = [issue for issue in checker.issues if issue.level == "warning"]
    infos = [issue for issue in checker.issues if issue.level == "info"]
    failed = bool(errors) or (args.strict and bool(warnings))

    if args.json:
        payload = {
            "ok": not failed,
            "root": str(root),
            "stats": {
                "expected": checker.stats.expected,
                "found": checker.stats.found,
                "missing": checker.stats.missing,
                "files": checker.stats.files,
                "words": checker.stats.words,
                "notes": checker.stats.notes,
                "tables": checker.stats.tables,
                "links": checker.stats.links,
            },
            "counts": {
                "errors": len(errors),
                "warnings": len(warnings),
                "info": len(infos),
            },
            "issues": [issue.as_dict(root) for issue in checker.issues],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        if not args.quiet:
            print_capped(errors + warnings, root)
            if infos:
                print()
                print_capped(infos, root)
        print(
            f"{checker.stats.found} files checked of "
            f"{checker.stats.expected} expected "
            f"({checker.stats.missing} missing), "
            f"{checker.stats.words:,} words, "
            f"{checker.stats.notes} notes, {checker.stats.tables} tables, "
            f"{checker.stats.links} local links; "
            f"{len(errors)} errors, {len(warnings)} warnings"
        )
        if failed:
            print("check_book: FAIL")
        else:
            print("check_book: OK")

    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # The consumer closed the pipe, as in `python3 tools/check_book.py --list | head`.
        sys.exit(0)
