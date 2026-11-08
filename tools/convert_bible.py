#!/usr/bin/env python3
"""Convert the eng-web_html World English Bible HTML edition into per-chapter XML.

The converter:
  * reads the book list from index.htm,
  * reads each book's chapter list from its table-of-contents page,
  * writes one XML file per Bible chapter under bible/{ot,deut,nt}/<book>/,
  * converts the Preface and Glossary into bible/other/,
  * writes bible/toc.xml, an ordered XML table of contents.

Only the standard library is required.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable, Iterator, Sequence
from xml.sax.saxutils import escape, quoteattr

_HERE = Path(__file__).resolve().parent
ROOT = _HERE.parent if _HERE.name == "tools" else _HERE

# ---------------------------------------------------------------------------
# HTML parsing (small DOM built on html.parser)
# ---------------------------------------------------------------------------

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag: str, attrs=None, parent: "Node | None" = None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children: list["Node | str"] = []
        self.parent = parent

    def classes(self) -> list[str]:
        return self.attrs.get("class", "").split()

    def has_class(self, name: str) -> bool:
        return name in self.classes()

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{self.tag} {self.attrs!r}>"


class DOMBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document")
        self.stack = [self.root]
        self.errors: list[tuple] = []

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs, self.stack[-1]))

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return
        if self.stack[-1].tag == tag:
            self.stack.pop()
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                self.errors.append((tag, [n.tag for n in self.stack[i:]]))
                del self.stack[i:]
                return
        self.errors.append(("unmatched", tag))

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_html(path: Path) -> DOMBuilder:
    parser = DOMBuilder()
    with path.open("r", encoding="utf-8-sig") as fh:
        parser.feed(fh.read())
    if parser.errors:
        raise ValueError(f"malformed HTML in {path}: {parser.errors[:3]}")
    return parser


def walk(node: Node) -> Iterator[Node]:
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def find_first(node: Node, tag: str, class_name: str) -> Node | None:
    for candidate in walk(node):
        if candidate.tag == tag and candidate.has_class(class_name):
            return candidate
    return None


def contains_verse(node: Node) -> bool:
    return any(
        child.tag == "span" and child.has_class("verse")
        for child in walk(node)
    )


# ---------------------------------------------------------------------------
# Text / inline rendering
# ---------------------------------------------------------------------------

# Characters that XML 1.0 forbids. The source is clean, but this makes the
# converter safe against odd control characters in a future source update.
INVALID_XML_CHARS = re.compile(
    r"[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]"
)
WHITESPACE = re.compile(r"[\s\u00a0]+")


def clean_text(value: str) -> str:
    return INVALID_XML_CHARS.sub("", value)


def normalize_ws(value: str) -> str:
    return WHITESPACE.sub(" ", clean_text(value))


def plain_text(node: Node, skip_note_markers: bool = True) -> str:
    """Return readable text without any markup.

    Verse numbers and footnote popups are omitted.  This is used for titles and
    labels, not for verse content.
    """
    parts: list[str] = []

    def visit(current: Node | str) -> None:
        if isinstance(current, str):
            parts.append(current)
            return
        classes = current.classes()
        if "popup" in classes:
            return
        if current.tag == "span" and "verse" in classes:
            return
        if skip_note_markers and current.tag == "a" and "notemark" in classes:
            return
        for child in current.children:
            visit(child)

    visit(node)
    return normalize_ws("".join(parts)).strip()


class InlineRenderer:
    """Render HTML inline content as small, XML-friendly fragments.

    ``noteref`` markers are created for footnote markers.  The corresponding
    note bodies live in the chapter-level ``<notes>`` block.
    """

    def __init__(
        self,
        note_prefix: str,
        note_ids: set[str],
        book_codes: Sequence[str],
    ):
        self.note_prefix = note_prefix
        self.note_ids = note_ids
        self.book_codes = sorted(book_codes, key=len, reverse=True)

    def render(self, nodes: Iterable[Node | str], strip: bool = True) -> str:
        text_parts: list[str] = []
        element_parts: list[str] = []

        def add_text(value: str) -> None:
            text_parts.append(escape(normalize_ws(value)))

        def add_element(value: str) -> None:
            # Private-use delimiters survive whitespace normalization and are
            # extremely unlikely to occur in the source text.
            text_parts.append(f"\ue000{len(element_parts)}\ue001")
            element_parts.append(value)

        def visit(current: Node | str, in_note: bool = False) -> None:
            if isinstance(current, str):
                add_text(current)
                return

            classes = current.classes()

            # Footnote markers in the running text.
            if current.tag == "a" and "notemark" in classes:
                if in_note:
                    return
                href = current.attrs.get("href", "")
                source_id = href[1:] if href.startswith("#") else href
                if source_id in self.note_ids:
                    note_id = f"{self.note_prefix}.{source_id}"
                    add_element(f"<noteref ref={quoteattr(note_id)}/>")
                return

            if current.tag == "a" and "notebackref" in classes:
                return
            if current.tag == "span" and "popup" in classes:
                return
            if current.tag == "span" and "verse" in classes:
                # The verse number itself is metadata, not verse text.
                return

            if current.tag == "span" and "wj" in classes:
                add_element(f"<wj>{self.render(current.children, strip=False)}</wj>")
                return
            if current.tag == "span" and "k" in classes:
                add_element(
                    f"<term>{self.render(current.children, strip=False)}</term>"
                )
                return
            if current.tag == "span" and "fq" in classes:
                add_element(
                    f"<quote>{self.render(current.children, strip=False)}</quote>"
                )
                return
            if current.tag == "span" and "fqa" in classes:
                add_element(
                    f"<alternative>"
                    f"{self.render(current.children, strip=False)}</alternative>"
                )
                return
            if current.tag == "span" and "fl" in classes:
                add_element(
                    f"<label>{self.render(current.children, strip=False)}</label>"
                )
                return

            if current.tag == "a":
                target = self.parse_bible_href(current.attrs.get("href", ""))
                inner = self.render(current.children, strip=False)
                if target is not None:
                    code, chapter, verse = target
                    attrs = f" book={quoteattr(code)} chapter={quoteattr(str(chapter))}"
                    if verse is not None:
                        attrs += f" verse={quoteattr(str(verse))}"
                    add_element(f"<ref{attrs}>{inner}</ref>")
                else:
                    # Non-Bible links are represented only by their text; the
                    # HTML files they point to are not part of the XML corpus.
                    add_element(inner)
                return

            if current.tag == "br":
                add_element("<br/>")
                return
            if current.tag in ("i", "em"):
                add_element(f"<em>{self.render(current.children, strip=False)}</em>")
                return
            if current.tag in ("b", "strong"):
                add_element(
                    f"<strong>{self.render(current.children, strip=False)}</strong>"
                )
                return
            if current.tag in ("sup", "sub"):
                add_element(
                    f"<{current.tag}>"
                    f"{self.render(current.children, strip=False)}"
                    f"</{current.tag}>"
                )
                return
            if current.tag in ("img", "hr"):
                return

            # Unknown containers (including ft/xt spans) contribute their
            # inline content without an extra wrapper.
            for child in current.children:
                visit(child, in_note=in_note)

        for node in nodes:
            visit(node)

        raw = "".join(text_parts)
        raw = normalize_ws(raw)
        if strip:
            raw = raw.strip()

        def restore(match: re.Match) -> str:
            return element_parts[int(match.group(1))]

        return re.sub(r"\ue000(\d+)\ue001", restore, raw)

    def parse_bible_href(self, href: str) -> tuple[str, int, int | None] | None:
        """Turn ``GEN01.htm#V1`` into ``("GEN", 1, 1)``."""
        if not href or href.startswith("http://") or href.startswith("https://"):
            return None
        path, _, fragment = href.partition("#")
        if not path.endswith(".htm"):
            return None
        stem = path[:-4]
        for code in self.book_codes:
            if not stem.startswith(code):
                continue
            number_part = stem[len(code):]
            if not number_part.isdigit():
                continue
            chapter = int(number_part)
            verse = None
            match = re.fullmatch(r"V(\d+)", fragment)
            if match:
                parsed = int(match.group(1))
                if parsed > 0:
                    verse = parsed
            return code, chapter, verse
        return None


# ---------------------------------------------------------------------------
# Source discovery
# ---------------------------------------------------------------------------

TESTAMENT_META = {
    "oo": ("ot", "Old Testament"),
    "aa": ("deut", "Deuterocanon"),
    "nn": ("nt", "New Testament"),
}


@dataclass
class Chapter:
    number: int
    source_file: Path
    output_file: Path | None = None
    verses: int = 0
    notes: int = 0


@dataclass
class Book:
    code: str
    name: str
    testament: str
    source_toc: Path
    chapters: list[Chapter] = field(default_factory=list)
    directory: Path | None = None


@dataclass
class OtherDocument:
    code: str
    name: str
    doc_type: str
    source_file: Path
    output_file: Path | None = None
    notes: int = 0


INDEX_ENTRY_RE = re.compile(
    r"<li><a class='(oo|aa|nn|xx)' href='([^']+)'>([^<]+)</a></li>"
)
TOC_LINK_RE = re.compile(r"<li><a href='([^']+)'>([^<]+)</a></li>")


def find_toc_path(source_dir: Path, first_chapter_href: str) -> Path:
    """Derive a book's TOC page from the first chapter link in index.htm.

    Most books use two-digit chapters (GEN01.htm -> GEN.htm), Psalms uses
    three (PSA001.htm -> PSA.htm), and Psalm 151 uses PS201.htm -> PS2.htm.
    """
    for width in (2, 3, 1):
        candidate = source_dir / (first_chapter_href[:-4 - width] + ".htm")
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        f"could not locate book TOC for index link {first_chapter_href!r}"
    )


def discover_books(source_dir: Path) -> tuple[list[Book], list[OtherDocument]]:
    index_path = source_dir / "index.htm"
    index_html = index_path.read_text(encoding="utf-8-sig")
    entries = INDEX_ENTRY_RE.findall(index_html)

    books: list[Book] = []
    other: list[OtherDocument] = []

    for css_class, href, name in entries:
        toc_path = find_toc_path(source_dir, href)
        code = toc_path.stem
        toc_html = toc_path.read_text(encoding="utf-8-sig")
        links = TOC_LINK_RE.findall(toc_html)

        if css_class not in TESTAMENT_META:
            # Front/back matter (Preface, Glossary).  Only convert actual
            # content pages; the empty TOC pages are skipped.
            first_chapter = source_dir / href
            if first_chapter.is_file():
                doc_type = "preface" if code.upper() == "FRT" else "glossary"
                other.append(
                    OtherDocument(
                        code=code,
                        name=html.unescape(name),
                        doc_type=doc_type,
                        source_file=first_chapter,
                    )
                )
            continue

        testament, _ = TESTAMENT_META[css_class]
        chapters: list[Chapter] = []
        seen: set[int] = set()
        for chapter_href, label in links:
            if not label.strip().isdigit():
                continue
            number = int(label.strip())
            if number == 0:
                # Chapter 0 pages are generated TOCs, not Bible chapters.
                continue
            if number in seen:
                continue
            seen.add(number)
            source_file = source_dir / chapter_href
            if not source_file.is_file():
                raise FileNotFoundError(f"missing chapter file {source_file}")
            chapters.append(Chapter(number=number, source_file=source_file))
        chapters.sort(key=lambda c: c.number)
        books.append(
            Book(
                code=code,
                name=html.unescape(name),
                testament=testament,
                source_toc=toc_path,
                chapters=chapters,
            )
        )

    return books, other


# ---------------------------------------------------------------------------
# Footnotes
# ---------------------------------------------------------------------------

@dataclass
class NoteDef:
    source_id: str
    note_type: str
    marker: str
    backref_verse: int | None
    content_nodes: list[Node | str]


def parse_note_definitions(tree: DOMBuilder) -> list[NoteDef]:
    note_box = find_first(tree.root, "div", "footnote")
    if note_box is None:
        return []

    notes: list[NoteDef] = []
    for paragraph in note_box.children:
        if not isinstance(paragraph, Node) or paragraph.tag != "p":
            continue
        classes = paragraph.classes()
        if "f" not in classes and "x" not in classes:
            continue
        source_id = paragraph.attrs.get("id", "")
        if not source_id:
            continue

        marker = ""
        backref_verse = None
        content_nodes: list[Node | str] = []

        for child in paragraph.children:
            if isinstance(child, str):
                content_nodes.append(child)
                continue
            child_classes = child.classes()
            if child.tag == "span" and "notemark" in child_classes:
                marker = plain_text(child)
                continue
            if child.tag == "a" and "notebackref" in child_classes:
                match = re.fullmatch(r"#V(\d+)", child.attrs.get("href", ""))
                if match:
                    parsed = int(match.group(1))
                    if parsed > 0:
                        backref_verse = parsed
                continue
            content_nodes.append(child)

        notes.append(
            NoteDef(
                source_id=source_id,
                note_type="cross-reference" if "x" in classes else "footnote",
                marker=marker,
                backref_verse=backref_verse,
                content_nodes=content_nodes,
            )
        )

    return notes


def note_id(prefix: str, source_id: str) -> str:
    return f"{prefix}.{source_id}"


# ---------------------------------------------------------------------------
# Chapter builder
# ---------------------------------------------------------------------------

HEADING_KINDS = {
    "mt": "book-title",
    "mt2": "book-title",
    "mt3": "book-title",
    "ms": "major-section",
    "s": "section",
    "is": "section",
    "d": "psalm-title",
}

CONTENT_CLASSES = {"p", "q", "q2", "q3", "qs", "m", "mi", "nb", "pi", "li"}


class ChapterBuilder:
    def __init__(self, code: str, chapter: int, inline: InlineRenderer):
        self.code = code
        self.chapter = chapter
        self.prefix = f"{code}.{chapter}"
        self.inline = inline
        self.lines: list[str] = []
        self.current_verse: int | None = None
        self.verse_parts: list[str] = []
        self.pending_speakers: list[str] = []
        self.seen_verses: set[int] = set()

    # -- low level ---------------------------------------------------------

    def _emit_verse(self) -> None:
        if self.current_verse is None:
            return
        text = self._join(self.verse_parts)
        number = self.current_verse
        omitted = not re.sub(r"<[^>]+>", "", text).strip()
        omitted_attr = ' omitted="true"' if omitted else ""
        self.lines.append(
            f'  <verse number={quoteattr(str(number))} '
            f'id={quoteattr(f"{self.prefix}.{number}")}{omitted_attr}>{text}</verse>'
        )
        self.seen_verses.add(number)
        self.current_verse = None
        self.verse_parts = []

    @staticmethod
    def _join(parts: Iterable[str]) -> str:
        return normalize_ws(" ".join(part for part in parts if part)).strip()

    def _emit_pending_speakers(self) -> None:
        for speaker in self.pending_speakers:
            if speaker.startswith("<speaker>"):
                inner = speaker[len("<speaker>"):-len("</speaker>")]
                self.lines.append(
                    f'  <heading kind="speaker">{inner}</heading>'
                )
            else:  # pragma: no cover - defensive
                self.lines.append(f'  <heading kind="speaker">{speaker}</heading>')
        self.pending_speakers = []

    def start_verse(self, number: int) -> None:
        self._emit_verse()
        self.current_verse = number
        # Speaker labels immediately before a new verse belong to that verse.
        self.verse_parts = list(self.pending_speakers)
        self.pending_speakers = []

    def add_chunk(self, fragment: str, tight: bool = False) -> None:
        if not fragment:
            return
        if self.pending_speakers:
            if self.current_verse is not None:
                self.verse_parts.extend(self.pending_speakers)
                self.pending_speakers = []
            else:
                # A speaker label with no verse context is a standalone heading.
                self._emit_pending_speakers()
        if self.current_verse is not None:
            if tight and self.verse_parts:
                # "Lord—" + "Selah" is adjacent in the source, while
                # "forever." + "Selah" needs a separating space.
                previous_text = re.sub(r"<[^>]+>", "", self.verse_parts[-1]).rstrip()
                if previous_text.endswith(("—", "–")):
                    self.verse_parts[-1] += fragment
                else:
                    self.verse_parts.append(fragment)
            else:
                self.verse_parts.append(fragment)
        else:
            self.intro(fragment)

    def speaker(self, text: str) -> None:
        text = text.strip()
        if text:
            self.pending_speakers.append(f"<speaker>{text}</speaker>")

    def heading(self, kind: str, text: str) -> None:
        text = text.strip()
        if not text:
            return
        self._emit_verse()
        self._emit_pending_speakers()
        self.lines.append(f'  <heading kind={quoteattr(kind)}>{text}</heading>')

    def intro(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        self._emit_verse()
        self._emit_pending_speakers()
        self.lines.append(f"  <intro>{text}</intro>")

    def finish(self) -> None:
        if self.pending_speakers and self.current_verse is not None:
            self.verse_parts.extend(self.pending_speakers)
            self.pending_speakers = []
        self._emit_pending_speakers()
        self._emit_verse()

    # -- source block handling --------------------------------------------

    def process_content_block(self, block: Node) -> None:
        buffer: list[Node | str] = []
        tight = "qs" in block.classes()

        def flush() -> None:
            if buffer:
                self.add_chunk(self.inline.render(buffer), tight=tight)
                buffer.clear()

        for child in block.children:
            if isinstance(child, Node) and child.tag == "span" and child.has_class("verse"):
                flush()
                verse_id = child.attrs.get("id", "")
                match = re.fullmatch(r"V(\d+)", verse_id)
                if match:
                    self.start_verse(int(match.group(1)))
                continue
            buffer.append(child)
        flush()


def is_heading_block(classes: Sequence[str]) -> bool:
    return any(name in HEADING_KINDS for name in classes)


def heading_kind(classes: Sequence[str]) -> str:
    for name in classes:
        if name in HEADING_KINDS:
            return HEADING_KINDS[name]
    return "section"


def chapter_title(book: Book, chapter_number: int, label: str) -> str:
    if len(book.chapters) == 1:
        return book.name
    if label.startswith("Psalm"):
        return label
    return f"{book.name} {chapter_number}"


def convert_chapter(
    book: Book,
    chapter: Chapter,
    output_root: Path,
    book_codes: Sequence[str],
) -> tuple[str, int, int]:
    tree = parse_html(chapter.source_file)
    main = find_first(tree.root, "div", "main")
    if main is None:
        raise ValueError(f"no main content in {chapter.source_file}")

    note_defs = parse_note_definitions(tree)
    note_ids = {note.source_id for note in note_defs}
    prefix = f"{book.code}.{chapter.number}"
    inline = InlineRenderer(prefix, note_ids, book_codes)
    builder = ChapterBuilder(book.code, chapter.number, inline)

    label = ""
    chapter_label = find_first(main, "div", "chapterlabel")
    if chapter_label is not None:
        label = plain_text(chapter_label)

    for block in main.children:
        if not isinstance(block, Node):
            continue
        classes = block.classes()

        # Navigation, copyright, footnote apparatus and generated TOC pages.
        if any(
            name in classes
            for name in (
                "tnav", "footnote", "copyright", "chapterlabel",
                "toc", "toc1", "toc2", "b", "pc",
            )
        ):
            continue

        if "sp" in classes:
            builder.speaker(inline.render(block.children))
            continue

        if is_heading_block(classes):
            builder.heading(heading_kind(classes), inline.render(block.children))
            continue

        if "ip" in classes:
            builder.intro(inline.render(block.children))
            continue

        if any(name in CONTENT_CLASSES for name in classes) or contains_verse(block):
            builder.process_content_block(block)
            continue

        # Safe fallback for any future non-verse material in a chapter.
        builder.intro(inline.render(block.children))

    builder.finish()

    title = chapter_title(book, chapter.number, label)
    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<chapter code={quoteattr(book.code)} "
        f"name={quoteattr(book.name)} "
        f"testament={quoteattr(book.testament)} "
        f"number={quoteattr(str(chapter.number))} "
        f"id={quoteattr(prefix)}>",
        f"  <title>{escape(title)}</title>",
        *builder.lines,
    ]

    if note_defs:
        lines.append("  <notes>")
        for note in note_defs:
            attrs = [
                f'id={quoteattr(note_id(prefix, note.source_id))}',
                f'source-id={quoteattr(note.source_id)}',
                f'type={quoteattr(note.note_type)}',
            ]
            if note.marker:
                attrs.append(f"marker={quoteattr(note.marker)}")
            if note.backref_verse is not None:
                attrs.append(f"verse={quoteattr(str(note.backref_verse))}")
            body = inline.render(note.content_nodes)
            if body:
                lines.append(f"    <note {' '.join(attrs)}>{body}</note>")
            else:
                lines.append(f"    <note {' '.join(attrs)}/>")
        lines.append("  </notes>")

    lines.append("</chapter>")
    lines.append("")

    if chapter.output_file is None:
        raise ValueError("chapter output path was not assigned")
    chapter.output_file.parent.mkdir(parents=True, exist_ok=True)
    chapter.output_file.write_text("\n".join(lines), encoding="utf-8")
    chapter.verses = len(builder.seen_verses)
    chapter.notes = len(note_defs)
    return title, chapter.verses, chapter.notes


# ---------------------------------------------------------------------------
# Non-Bible documents (Preface, Glossary)
# ---------------------------------------------------------------------------

def convert_other_document(
    document: OtherDocument,
    output_root: Path,
    book_codes: Sequence[str],
) -> tuple[int, int]:
    tree = parse_html(document.source_file)
    main = find_first(tree.root, "div", "main")
    if main is None:
        raise ValueError(f"no main content in {document.source_file}")

    note_defs = parse_note_definitions(tree)
    note_ids = {note.source_id for note in note_defs}
    prefix = document.code
    inline = InlineRenderer(prefix, note_ids, book_codes)

    content: list[str] = []
    title = document.name

    for block in main.children:
        if not isinstance(block, Node):
            continue
        classes = block.classes()
        if any(
            name in classes
            for name in (
                "tnav", "footnote", "copyright", "chapterlabel",
                "toc", "toc1", "toc2", "b", "pc",
            )
        ):
            continue

        rendered = inline.render(block.children)
        if not rendered:
            continue

        if "mt" in classes:
            if not content:
                title = rendered
            else:
                content.append(f'  <heading kind="book-title">{rendered}</heading>')
        elif "is" in classes:
            content.append(f'  <heading kind="section">{rendered}</heading>')
        elif "ip" in classes:
            content.append(f"  <paragraph>{rendered}</paragraph>")
        elif "ili" in classes:
            tag = "entry" if document.doc_type == "glossary" else "list-item"
            content.append(f"  <{tag}>{rendered}</{tag}>")
        elif "li" in classes:
            content.append(f"  <list-item>{rendered}</list-item>")
        else:
            content.append(f"  <paragraph>{rendered}</paragraph>")

    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f"<document code={quoteattr(document.code)} "
        f"name={quoteattr(document.name)} "
        f"type={quoteattr(document.doc_type)}>",
        f"  <title>{escape(title)}</title>",
        *content,
    ]

    if note_defs:
        lines.append("  <notes>")
        for note in note_defs:
            attrs = [
                f'id={quoteattr(note_id(prefix, note.source_id))}',
                f'source-id={quoteattr(note.source_id)}',
                f'type={quoteattr(note.note_type)}',
            ]
            if note.marker:
                attrs.append(f"marker={quoteattr(note.marker)}")
            body = inline.render(note.content_nodes)
            if body:
                lines.append(f"    <note {' '.join(attrs)}>{body}</note>")
            else:
                lines.append(f"    <note {' '.join(attrs)}/>")
        lines.append("  </notes>")

    lines.append("</document>")
    lines.append("")

    if document.output_file is None:
        raise ValueError("document output path was not assigned")
    document.output_file.parent.mkdir(parents=True, exist_ok=True)
    document.output_file.write_text("\n".join(lines), encoding="utf-8")
    document.notes = len(note_defs)
    return len(note_defs), len(content)


# ---------------------------------------------------------------------------
# TOC
# ---------------------------------------------------------------------------

TESTAMENT_NAMES = {
    "ot": "Old Testament",
    "deut": "Deuterocanon",
    "nt": "New Testament",
}


def relative_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def write_toc(
    output_root: Path,
    books: Sequence[Book],
    other_documents: Sequence[OtherDocument],
) -> None:
    lines: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<bible name="World English Bible Classic" language="en" source="eng-web">',
    ]

    for testament in ("ot", "deut", "nt"):
        testament_books = [book for book in books if book.testament == testament]
        if not testament_books:
            continue
        lines.append(
            f'  <testament code={quoteattr(testament)} '
            f'name={quoteattr(TESTAMENT_NAMES[testament])}>'
        )
        for book in testament_books:
            if book.directory is None:
                raise ValueError(f"directory not assigned for {book.code}")
            lines.append(
                f'    <book code={quoteattr(book.code)} '
                f'name={quoteattr(book.name)} '
                f'directory={quoteattr(relative_path(book.directory, output_root))} '
                f'chapters={quoteattr(str(len(book.chapters)))}>'
            )
            for chapter in book.chapters:
                if chapter.output_file is None:
                    raise ValueError(f"output path not assigned for {book.code} {chapter.number}")
                lines.append(
                    f'      <chapter number={quoteattr(str(chapter.number))} '
                    f'id={quoteattr(f"{book.code}.{chapter.number}")} '
                    f'file={quoteattr(relative_path(chapter.output_file, output_root))} '
                    f'verses={quoteattr(str(chapter.verses))} '
                    f'notes={quoteattr(str(chapter.notes))}/>'
                )
            lines.append("    </book>")
        lines.append("  </testament>")

    if other_documents:
        lines.append("  <other>")
        for document in other_documents:
            if document.output_file is None:
                raise ValueError(f"output path not assigned for {document.code}")
            lines.append(
                f'    <document code={quoteattr(document.code)} '
                f'name={quoteattr(document.name)} '
                f'type={quoteattr(document.doc_type)} '
                f'file={quoteattr(relative_path(document.output_file, output_root))} '
                f'notes={quoteattr(str(document.notes))}/>'
            )
        lines.append("  </other>")

    lines.append("</bible>")
    lines.append("")
    (output_root / "toc.xml").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_output(output_root: Path, books: Sequence[Book], other: Sequence[OtherDocument]) -> None:
    errors: list[str] = []
    total_chapters = 0
    total_verses = 0
    total_notes = 0

    for book in books:
        for chapter in book.chapters:
            total_chapters += 1
            if chapter.output_file is None or not chapter.output_file.is_file():
                errors.append(f"missing output: {book.code} {chapter.number}")
                continue
            try:
                root = ET.parse(chapter.output_file).getroot()
            except ET.ParseError as exc:
                errors.append(f"XML parse error in {chapter.output_file}: {exc}")
                continue

            verse_elements = root.findall("verse")
            note_elements = root.findall("notes/note")
            note_ids = {note.get("id") for note in note_elements}
            referenced_ids = {ref.get("ref") for ref in root.iter("noteref")}
            verse_numbers = [int(v.get("number", "0")) for v in verse_elements]
            total_verses += len(verse_elements)
            total_notes += len(note_elements)

            if len(verse_numbers) != len(set(verse_numbers)):
                errors.append(f"duplicate verse number in {chapter.output_file}")
            if verse_numbers != sorted(verse_numbers):
                errors.append(f"verses out of order in {chapter.output_file}")
            if len(note_ids) != len(note_elements):
                errors.append(f"duplicate note id in {chapter.output_file}")

            for noteref in root.iter("noteref"):
                ref = noteref.get("ref")
                if ref not in note_ids:
                    errors.append(
                        f"unresolved noteref {ref!r} in {chapter.output_file}"
                    )
            for note in note_elements:
                if note.get("id") not in referenced_ids:
                    errors.append(
                        f"unreferenced note {note.get('id')!r} "
                        f"in {chapter.output_file}"
                    )
                verse = note.get("verse")
                if verse is not None and int(verse) not in set(verse_numbers):
                    errors.append(
                        f"note {note.get('id')!r} points to missing verse {verse} "
                        f"in {chapter.output_file}"
                    )

    for document in other:
        if document.output_file is None or not document.output_file.is_file():
            errors.append(f"missing output: {document.code}")
            continue
        try:
            root = ET.parse(document.output_file).getroot()
        except ET.ParseError as exc:
            errors.append(f"XML parse error in {document.output_file}: {exc}")
            continue
        note_elements = root.findall("notes/note")
        note_ids = {note.get("id") for note in note_elements}
        referenced_ids = {ref.get("ref") for ref in root.iter("noteref")}
        total_notes += len(note_elements)
        if len(note_ids) != len(note_elements):
            errors.append(f"duplicate note id in {document.output_file}")
        for noteref in root.iter("noteref"):
            ref = noteref.get("ref")
            if ref not in note_ids:
                errors.append(
                    f"unresolved noteref {ref!r} in {document.output_file}"
                )
        for note in note_elements:
            if note.get("id") not in referenced_ids:
                errors.append(
                    f"unreferenced note {note.get('id')!r} "
                    f"in {document.output_file}"
                )

    try:
        toc_root = ET.parse(output_root / "toc.xml").getroot()
    except ET.ParseError as exc:
        errors.append(f"XML parse error in toc.xml: {exc}")
    else:
        for element in toc_root.iter("chapter"):
            file_path = output_root / element.get("file", "")
            if not file_path.is_file():
                errors.append(f"TOC points to missing file: {file_path}")
        for element in toc_root.iter("document"):
            file_path = output_root / element.get("file", "")
            if not file_path.is_file():
                errors.append(f"TOC points to missing file: {file_path}")

    if errors:
        for error in errors[:50]:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(f"validation failed with {len(errors)} error(s)")

    print(
        f"Validated {total_chapters} chapter files, "
        f"{total_verses} verses, {total_notes} notes, "
        f"{len(other)} other document(s)."
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    default_source = ROOT / "eng-web_html"
    default_output = ROOT / "bible"
    parser.add_argument(
        "--source", type=Path, default=default_source,
        help=f"directory containing the HTML edition (default: {default_source})",
    )
    parser.add_argument(
        "--output", type=Path, default=default_output,
        help=f"directory for generated XML (default: {default_output})",
    )
    parser.add_argument(
        "--no-validate", action="store_true",
        help="skip the post-conversion XML validation pass",
    )
    args = parser.parse_args(argv)

    source_dir: Path = args.source
    output_root: Path = args.output
    if not (source_dir / "index.htm").is_file():
        raise SystemExit(f"index.htm not found in {source_dir}")

    books, other_documents = discover_books(source_dir)
    if not books:
        raise SystemExit("no Bible books found")

    book_codes = [book.code for book in books] + [doc.code for doc in other_documents]

    # Assign output paths before conversion so the TOC can use them.
    for book in books:
        book.directory = output_root / book.testament / book.code.lower()
        for chapter in book.chapters:
            chapter.output_file = (
                book.directory / f"{book.code.lower()}_{chapter.number:03d}.xml"
            )

    for document in other_documents:
        slug = re.sub(r"[^a-z0-9]+", "-", document.name.lower()).strip("-")
        document.output_file = output_root / "other" / slug / f"{slug}.xml"

    total_chapters = 0
    total_verses = 0
    total_notes = 0

    for book in books:
        book_verses = 0
        book_notes = 0
        for chapter in book.chapters:
            _, verses, notes = convert_chapter(
                book, chapter, output_root, book_codes
            )
            book_verses += verses
            book_notes += notes
            total_chapters += 1
            total_verses += verses
            total_notes += notes
        print(
            f"{book.testament:4} {book.code:5} {book.name:25} "
            f"{len(book.chapters):3} chapters, {book_verses:5} verses, "
            f"{book_notes:4} notes"
        )

    for document in other_documents:
        notes, blocks = convert_other_document(document, output_root, book_codes)
        total_notes += notes
        print(
            f"other {document.code:5} {document.name:25} "
            f"{blocks:3} blocks, {notes:4} notes"
        )

    write_toc(output_root, books, other_documents)

    print(
        f"\nWrote {total_chapters} chapters, {total_verses} verses, "
        f"{total_notes} notes to {output_root}"
    )
    print(f"Table of contents: {output_root / 'toc.xml'}")

    if not args.no_validate:
        validate_output(output_root, books, other_documents)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
