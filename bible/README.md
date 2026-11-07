# World English Bible Classic — XML Corpus Guide

This directory contains a machine-readable XML edition of the **World English Bible Classic**. It is organized so that a person or an AI system can locate a verse by book, chapter, and verse number, search the text, and retrieve the footnotes attached to that verse.

The corpus contains:

- **81 books**: 39 Old Testament, 15 Deuterocanon, and 27 New Testament.
- **1,402 chapter files**.
- **38,058 numbered verses**.
- **2,218 notes** (2,217 in Bible chapters and 1 in the Preface).
- **2 additional documents**: the Preface and the Glossary.

No other files are needed to read or search the corpus.

## Quick start

- **Known reference** (for example Genesis 1:1): find the book code in the table below or in `bible/toc.xml`, open that book's chapter file, and locate `<verse number="1" id="GEN.1.1">`.
- **Text search**: search the XML files for the phrase. Every matching verse carries `verse/@id` in the form `BOOK.CHAPTER.VERSE`; every matching Bible note carries `note/@verse`.
- **Footnotes for a verse**: find its `<noteref ref="..."/>` markers, then resolve each `ref` against `<note id="...">`, or query `//notes/note[@verse='...']` directly.
- **Cross-reference in a note**: the `<ref book="..." chapter="..." verse="...">` attributes identify the target passage; map the book code to its directory with the table below.

The rest of this guide documents the schema and gives exact query examples.

---

## 1. Directory layout

Unless noted otherwise, paths in this guide are relative to the repository root.

```text
bible/
├── README.md                  <- this guide
├── toc.xml                    <- overall XML table of contents
├── ot/                        <- Old Testament
│   ├── gen/
│   │   ├── gen_001.xml
│   │   ├── gen_002.xml
│   │   └── ...
│   ├── exo/
│   └── ...
├── deut/                      <- Deuterocanon
│   ├── tob/
│   ├── jdt/
│   ├── ps2/                   <- Psalm 151
│   └── ...
├── nt/                        <- New Testament
│   ├── mat/
│   ├── mrk/
│   └── ...
└── other/
    ├── preface/
    │   └── preface.xml
    └── glossary/
        └── glossary.xml
```

### File naming

A chapter file is named:

```text
<lowercase-book-code>_<three-digit-chapter>.xml
```

Examples:

| Reference | File |
| --- | --- |
| Genesis 1 | `bible/ot/gen/gen_001.xml` |
| Genesis 50 | `bible/ot/gen/gen_050.xml` |
| 1 Chronicles 12 | `bible/ot/1ch/1ch_012.xml` |
| Psalm 119 | `bible/ot/psa/psa_119.xml` |
| Psalm 151 | `bible/deut/ps2/ps2_001.xml` |
| Matthew 5 | `bible/nt/mat/mat_005.xml` |
| Revelation 22 | `bible/nt/rev/rev_022.xml` |

Chapter numbers are zero-padded to three digits so that filenames sort in numerical order. Psalm 151 uses the book code `PS2`, following the source's own code for that book.

### Book codes and directories

The code in the `Code` column is the uppercase identifier used in XML attributes and verse IDs. The directory is the lowercase form of that code.

#### Old Testament (`ot`)

| Code | Book | Directory | Chapters |
| --- | --- | --- | ---: |
| `GEN` | Genesis | `bible/ot/gen/` | 50 |
| `EXO` | Exodus | `bible/ot/exo/` | 40 |
| `LEV` | Leviticus | `bible/ot/lev/` | 27 |
| `NUM` | Numbers | `bible/ot/num/` | 36 |
| `DEU` | Deuteronomy | `bible/ot/deu/` | 34 |
| `JOS` | Joshua | `bible/ot/jos/` | 24 |
| `JDG` | Judges | `bible/ot/jdg/` | 21 |
| `RUT` | Ruth | `bible/ot/rut/` | 4 |
| `1SA` | 1 Samuel | `bible/ot/1sa/` | 31 |
| `2SA` | 2 Samuel | `bible/ot/2sa/` | 24 |
| `1KI` | 1 Kings | `bible/ot/1ki/` | 22 |
| `2KI` | 2 Kings | `bible/ot/2ki/` | 25 |
| `1CH` | 1 Chronicles | `bible/ot/1ch/` | 29 |
| `2CH` | 2 Chronicles | `bible/ot/2ch/` | 36 |
| `EZR` | Ezra | `bible/ot/ezr/` | 10 |
| `NEH` | Nehemiah | `bible/ot/neh/` | 13 |
| `EST` | Esther | `bible/ot/est/` | 10 |
| `JOB` | Job | `bible/ot/job/` | 42 |
| `PSA` | Psalms | `bible/ot/psa/` | 150 |
| `PRO` | Proverbs | `bible/ot/pro/` | 31 |
| `ECC` | Ecclesiastes | `bible/ot/ecc/` | 12 |
| `SNG` | Song of Solomon | `bible/ot/sng/` | 8 |
| `ISA` | Isaiah | `bible/ot/isa/` | 66 |
| `JER` | Jeremiah | `bible/ot/jer/` | 52 |
| `LAM` | Lamentations | `bible/ot/lam/` | 5 |
| `EZK` | Ezekiel | `bible/ot/ezk/` | 48 |
| `DAN` | Daniel | `bible/ot/dan/` | 12 |
| `HOS` | Hosea | `bible/ot/hos/` | 14 |
| `JOL` | Joel | `bible/ot/jol/` | 3 |
| `AMO` | Amos | `bible/ot/amo/` | 9 |
| `OBA` | Obadiah | `bible/ot/oba/` | 1 |
| `JON` | Jonah | `bible/ot/jon/` | 4 |
| `MIC` | Micah | `bible/ot/mic/` | 7 |
| `NAM` | Nahum | `bible/ot/nam/` | 3 |
| `HAB` | Habakkuk | `bible/ot/hab/` | 3 |
| `ZEP` | Zephaniah | `bible/ot/zep/` | 3 |
| `HAG` | Haggai | `bible/ot/hag/` | 2 |
| `ZEC` | Zechariah | `bible/ot/zec/` | 14 |
| `MAL` | Malachi | `bible/ot/mal/` | 4 |

#### Deuterocanon (`deut`)

| Code | Book | Directory | Chapters |
| --- | --- | --- | ---: |
| `TOB` | Tobit | `bible/deut/tob/` | 14 |
| `JDT` | Judith | `bible/deut/jdt/` | 16 |
| `ESG` | Esther (Greek) | `bible/deut/esg/` | 10 |
| `DAG` | Daniel (Greek) | `bible/deut/dag/` | 14 |
| `WIS` | Wisdom | `bible/deut/wis/` | 19 |
| `SIR` | Sirach | `bible/deut/sir/` | 51 |
| `BAR` | Baruch | `bible/deut/bar/` | 6 |
| `1MA` | 1 Maccabees | `bible/deut/1ma/` | 16 |
| `2MA` | 2 Maccabees | `bible/deut/2ma/` | 15 |
| `1ES` | 1 Esdras | `bible/deut/1es/` | 9 |
| `MAN` | Prayer of Manasses | `bible/deut/man/` | 1 |
| `PS2` | Psalm 151 | `bible/deut/ps2/` | 1 |
| `3MA` | 3 Maccabees | `bible/deut/3ma/` | 7 |
| `2ES` | 2 Esdras | `bible/deut/2es/` | 16 |
| `4MA` | 4 Maccabees | `bible/deut/4ma/` | 18 |

#### New Testament (`nt`)

| Code | Book | Directory | Chapters |
| --- | --- | --- | ---: |
| `MAT` | Matthew | `bible/nt/mat/` | 28 |
| `MRK` | Mark | `bible/nt/mrk/` | 16 |
| `LUK` | Luke | `bible/nt/luk/` | 24 |
| `JHN` | John | `bible/nt/jhn/` | 21 |
| `ACT` | Acts | `bible/nt/act/` | 28 |
| `ROM` | Romans | `bible/nt/rom/` | 16 |
| `1CO` | 1 Corinthians | `bible/nt/1co/` | 16 |
| `2CO` | 2 Corinthians | `bible/nt/2co/` | 13 |
| `GAL` | Galatians | `bible/nt/gal/` | 6 |
| `EPH` | Ephesians | `bible/nt/eph/` | 6 |
| `PHP` | Philippians | `bible/nt/php/` | 4 |
| `COL` | Colossians | `bible/nt/col/` | 4 |
| `1TH` | 1 Thessalonians | `bible/nt/1th/` | 5 |
| `2TH` | 2 Thessalonians | `bible/nt/2th/` | 3 |
| `1TI` | 1 Timothy | `bible/nt/1ti/` | 6 |
| `2TI` | 2 Timothy | `bible/nt/2ti/` | 4 |
| `TIT` | Titus | `bible/nt/tit/` | 3 |
| `PHM` | Philemon | `bible/nt/phm/` | 1 |
| `HEB` | Hebrews | `bible/nt/heb/` | 13 |
| `JAS` | James | `bible/nt/jas/` | 5 |
| `1PE` | 1 Peter | `bible/nt/1pe/` | 5 |
| `2PE` | 2 Peter | `bible/nt/2pe/` | 3 |
| `1JN` | 1 John | `bible/nt/1jn/` | 5 |
| `2JN` | 2 John | `bible/nt/2jn/` | 1 |
| `3JN` | 3 John | `bible/nt/3jn/` | 1 |
| `JUD` | Jude | `bible/nt/jud/` | 1 |
| `REV` | Revelation | `bible/nt/rev/` | 22 |

---

## 2. Overall table of contents: `bible/toc.xml`

`bible/toc.xml` is the canonical index of the corpus. It lists books in Bible order and chapters in numerical order. It is the safest way to map a book name to its code, directory, and chapter files.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bible name="World English Bible Classic" language="en" source="eng-web">
  <testament code="ot" name="Old Testament">
    <book code="GEN" name="Genesis" directory="ot/gen" chapters="50">
      <chapter number="1" id="GEN.1"
               file="ot/gen/gen_001.xml" verses="31" notes="2"/>
      <chapter number="2" id="GEN.2"
               file="ot/gen/gen_002.xml" verses="25" notes="3"/>
      <!-- ... -->
    </book>
    <!-- ... -->
  </testament>

  <testament code="deut" name="Deuterocanon">
    <!-- ... -->
  </testament>

  <testament code="nt" name="New Testament">
    <!-- ... -->
  </testament>

  <other>
    <document code="FRT" name="Preface" type="preface"
              file="other/preface/preface.xml" notes="1"/>
    <document code="GLO" name="Glossary" type="glossary"
              file="other/glossary/glossary.xml" notes="0"/>
  </other>
</bible>
```

Attribute meanings:

- `testament/@code`: `ot`, `deut`, or `nt`.
- `book/@code`: uppercase book code (for example `GEN`, `1CH`, `PS2`).
- `book/@name`: display name.
- `book/@directory`: directory relative to `bible/`.
- `book/@chapters`: number of chapter files.
- `chapter/@number`: chapter number as an integer string.
- `chapter/@id`: canonical chapter ID, `BOOK.CHAPTER` (for example `GEN.1`).
- `chapter/@file`: file path relative to `bible/`.
- `chapter/@verses`: number of verse elements in that file.
- `chapter/@notes`: number of note definitions in that file.
- `document/@file`: path to a non-Bible document relative to `bible/`.

The section order is Old Testament, Deuterocanon, New Testament. The book order within each section is the traditional order used by this edition.

---

## 3. Chapter XML schema

Every Bible chapter file has a single `<chapter>` root. There is no XML namespace.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<chapter code="GEN" name="Genesis" testament="ot" number="1" id="GEN.1">
  <title>Genesis 1</title>

  <heading kind="book-title">The First Book of Moses,</heading>
  <heading kind="book-title">Commonly Called</heading>
  <heading kind="book-title">Genesis</heading>

  <verse number="1" id="GEN.1.1">In the beginning, God<noteref ref="GEN.1.FN1"/> created the heavens and the earth.</verse>
  <verse number="2" id="GEN.1.2">The earth was formless and empty. Darkness was on the surface of the deep and God’s Spirit was hovering over the surface of the waters.</verse>
  <!-- ... -->

  <notes>
    <note id="GEN.1.FN1" source-id="FN1" type="footnote" marker="†" verse="1">The Hebrew word rendered “God” is “אֱלֹהִ֑ים” (Elohim).</note>
    <note id="GEN.1.FN2" source-id="FN2" type="footnote" marker="‡" verse="29">“Behold”, from “הִנֵּה”, means look at, take notice, observe, see, or gaze at. It is often used as an interjection.</note>
  </notes>
</chapter>
```

### `<chapter>` attributes

| Attribute | Meaning |
| --- | --- |
| `code` | Uppercase book code. |
| `name` | Book display name. |
| `testament` | `ot`, `deut`, or `nt`. |
| `number` | Chapter number. |
| `id` | Canonical chapter ID, `BOOK.CHAPTER`. |

### `<title>`

A human-readable title for the chapter, such as `Genesis 1`, `Psalm 119`, or `Psalm 151`.

### `<verse>`

Each numbered verse is a `<verse>` element.

```xml
<verse number="1" id="GEN.1.1">In the beginning, God<noteref ref="GEN.1.FN1"/> created the heavens and the earth.</verse>
```

| Attribute | Meaning |
| --- | --- |
| `number` | Verse number as an integer string. |
| `id` | Globally unique verse ID: `BOOK.CHAPTER.VERSE`, for example `GEN.1.1` or `PSA.119.105`. |
| `omitted` | Present with value `true` when the verse has no running text in this edition. Such a verse contains only a `<noteref>`; the accompanying note explains the omission or textual variant. |

Verse text is normalized to single spaces. Poetry line breaks are flattened into the verse text; the verse number and paragraph/line boundaries are not part of the text. The text may contain inline elements, described below.

### Inline elements inside verses

| Element | Meaning |
| --- | --- |
| `<noteref ref="..."/>` | A zero-length footnote marker at the exact point where the note belongs. The `ref` value is the `id` of a `<note>` in the same file. |
| `<wj>...</wj>` | Words of Jesus, where the source marks them. |
| `<speaker>...</speaker>` | A dramatic speaker label embedded in the verse, mainly in Song of Solomon. |
| `<ref book="..." chapter="..." verse="...">...</ref>` | A cross-reference to another Bible passage, normally found in notes and non-Bible documents. In verse text it is rare. |

Example with a speaker label:

```xml
<verse number="4" id="SNG.1.4">Take me away with you. Let’s hurry. The king has brought me into his rooms. <speaker>Friends</speaker> We will be glad and rejoice in you. We will praise your love more than wine! <speaker>Beloved</speaker> They are right to love you.</verse>
```

### Headings, introductions, and other non-verse material

Bible chapters also contain headings and introductory material. They are kept in document order but are not numbered verses.

| Element | Meaning |
| --- | --- |
| `<heading kind="book-title">` | Book title material, usually only in the first chapter of a book. |
| `<heading kind="major-section">` | A major division, such as `BOOK 1` in Psalms. |
| `<heading kind="section">` | A section heading. |
| `<heading kind="psalm-title">` | A Psalm superscription, title, or acrostic letter such as `ALEPH`. |
| `<heading kind="speaker">` | A speaker label that is not attached to a verse. Most speaker labels are inline `<speaker>` elements instead. |
| `<intro>` | Non-verse introductory prose in a chapter, such as a Deuterocanon book notice. |

Example:

```xml
<title>Psalm 46</title>
<heading kind="psalm-title">For the Chief Musician. By the sons of Korah. According to Alamoth.<noteref ref="PSA.46.FN1"/></heading>
<verse number="1" id="PSA.46.1">God is our refuge and strength, a very present help in trouble.</verse>
```

Section headings and Psalm titles are deliberately separate from verses so that verse text remains clean and verse numbers remain authoritative.

---

## 4. Notes and footnotes

Notes are stored in a dedicated `<notes>` block at the end of the chapter, not inside the running verse text. This keeps verse text clean while making the association between verse and note explicit and reliable. Chapters with no notes omit the `<notes>` element entirely.

There are two elements:

```xml
<!-- marker in the running text or in a heading -->
<noteref ref="GEN.1.FN1"/>

<!-- note body at the end of the chapter -->
<note id="GEN.1.FN1" source-id="FN1" type="footnote" marker="†" verse="1">
  The Hebrew word rendered “God” is “אֱלֹהִ֑ים” (Elohim).
</note>
```

### `<noteref>`

- Marks the exact position of a note in a verse or heading.
- Is empty; it contributes no text to the verse.
- `ref` points to the `id` of a `<note>` in the same chapter file.
- A verse can contain zero, one, or several `<noteref>` elements.

### `<note>` attributes

| Attribute | Meaning |
| --- | --- |
| `id` | Globally unique note ID: `BOOK.CHAPTER.FNn` (for example `GEN.1.FN1`, `1CO.15.FN4`). Use this to resolve a `<noteref>`. |
| `source-id` | Original per-chapter note identifier from the source (`FN1`, `FN2`, ...). This may repeat in different chapters, so use `id` for identity. |
| `type` | `footnote` for explanatory/textual notes, or `cross-reference` for notes that are primarily references to other passages. |
| `marker` | Original marker symbol (`*`, `†`, `‡`, `§`), omitted if the source has no marker. Markers may repeat within a chapter; use `id` for identity. |
| `verse` | The verse number the note is associated with. Present for Bible notes. Absent for notes in the Preface or Glossary. |

A note in a heading also has a `verse` attribute pointing to the verse it explains. For example, a Psalm title note may have `verse="1"` even though the `<noteref>` is inside `<heading kind="psalm-title">`.

### Note text

The note body is the element's text content. It may contain:

| Element | Meaning |
| --- | --- |
| `<ref book="..." chapter="..." verse="...">...</ref>` | A reference to another Bible passage. `book` is an uppercase book code; `chapter` and `verse` are numeric. For a range, `verse` is the start verse and the element text shows the full range. |
| `<quote>...</quote>` | A quoted reading or quotation inside a note. |
| `<alternative>...</alternative>` | An alternative reading or translation. |
| `<label>...</label>` | A label such as `Note:`, `Greek`, or `Hebrew`. |

Example of a cross-reference note:

```xml
<noteref ref="1CO.15.FN1"/>

<note id="1CO.15.FN1" source-id="FN1" type="cross-reference" marker="*" verse="27">
  <ref book="PSA" chapter="8" verse="6">Psalms 8:6</ref>
</note>
```

Example of a textual footnote with an alternative reading:

```xml
<note id="1MA.5.FN2" source-id="FN2" type="footnote" marker="‡" verse="8">
  Gr. <alternative>daughters. </alternative>Compare <ref book="NUM" chapter="21" verse="25">Numbers 21:25</ref>.
</note>
```

### Omitted verses

Some verse numbers have no running text because the verse is omitted or represented only by a textual note. Such verses are marked:

```xml
<verse number="36" id="LUK.17.36" omitted="true"><noteref ref="LUK.17.FN1"/></verse>
```

The note contains the relevant text or explanation:

```xml
<note id="LUK.17.FN1" source-id="FN1" type="footnote" marker="†" verse="36">
  Some Greek manuscripts add: “Two will be in the field: the one taken, and the other left.”
</note>
```

If a verse has `omitted="true"`, treat its content as being supplied by its note rather than by the verse element itself.

---

## 5. Finding a verse by chapter and verse

### Path formula

Given a book code and chapter number:

1. Look up the code in `bible/toc.xml` (or the book table above) to get its directory.
2. The file is `<directory>/<lowercase-code>_<chapter:03d>.xml`.
3. Inside that file, find `<verse number="...">` or the globally unique `id`.

Examples:

| Reference | File | Verse element |
| --- | --- | --- |
| Genesis 1:1 | `bible/ot/gen/gen_001.xml` | `<verse number="1" id="GEN.1.1">` |
| 1 Chronicles 12:9 | `bible/ot/1ch/1ch_012.xml` | `<verse number="9" id="1CH.12.9">` |
| Psalm 119:105 | `bible/ot/psa/psa_119.xml` | `<verse number="105" id="PSA.119.105">` |
| John 3:16 | `bible/nt/jhn/jhn_003.xml` | `<verse number="16" id="JHN.3.16">` |
| Psalm 151:3 | `bible/deut/ps2/ps2_001.xml` | `<verse number="3" id="PS2.1.3">` |

The canonical verse ID format is:

```text
BOOK.CHAPTER.VERSE
```

where `BOOK` is the uppercase code, and `CHAPTER` and `VERSE` are integers. This ID is unique across the whole corpus.

### XPath examples

```xpath
//verse[@number='1']
//verse[@id='GEN.1.1']
//verse[@number='105' and @id='PSA.119.105']
```

Because each chapter is its own file, `//verse[@number='1']` returns the first verse of the chapter being queried, not the first verse of the Bible.

### Shell search

```bash
# Find chapters containing a phrase
rg -l 'still small voice' bible/ot bible/nt bible/deut

# Show matching verse lines
rg -n 'still small voice' bible

# Find a verse by canonical ID
rg -n 'id="GEN.1.1"' bible/ot/gen/gen_001.xml

# Find a note by canonical note ID
rg -n 'id="GEN.1.FN2"' bible/ot/gen/gen_001.xml
```

### Python with the standard library

```python
from xml.etree import ElementTree as ET

path = "bible/ot/gen/gen_001.xml"
root = ET.parse(path).getroot()

verse = root.find(".//verse[@number='1']")
print("".join(verse.itertext()))
# In the beginning, God created the heavens and the earth.

notes = {note.get("id"): "".join(note.itertext())
         for note in root.findall("notes/note")}

for marker in verse.findall("noteref"):
    note_id = marker.get("ref")
    print(note_id, "=>", notes[note_id])
# GEN.1.FN1 => The Hebrew word rendered “God” is “אֱלֹהִ֑ים” (Elohim).
```

To search every chapter:

```python
from pathlib import Path
from xml.etree import ElementTree as ET

for path in Path("bible").rglob("*.xml"):
    if path.name == "toc.xml":
        continue
    root = ET.parse(path).getroot()
    for verse in root.iter("verse"):
        text = "".join(verse.itertext())
        if "shepherd" in text.lower():
            print(path, verse.get("id"), text)
```

---

## 6. Finding the footnotes for a verse

Because notes are stored at chapter level, there are two equivalent ways to retrieve them.

### By note marker in the verse

```xpath
//verse[@number='29']/noteref/@ref
```

This returns the note IDs referenced from that verse. Then resolve each ID:

```xpath
//notes/note[@id='GEN.1.FN2']
```

### Directly by the note's `verse` attribute

```xpath
//notes/note[@verse='29']
```

This is usually the simplest query when you want all notes associated with a verse, including notes whose markers are in a heading.

### By note type

```xpath
//notes/note[@type='footnote']
//notes/note[@type='cross-reference']
```

### By note text

```xpath
//notes/note[contains(., 'Yahweh')]
```

### Python: verse text plus its notes

```python
from xml.etree import ElementTree as ET

root = ET.parse("bible/ot/gen/gen_001.xml").getroot()
verse = root.find(".//verse[@number='29']")

note_ids = [marker.get("ref") for marker in verse.findall("noteref")]
notes = {note.get("id"): "".join(note.itertext())
         for note in root.findall("notes/note")}

print("VERSE:", "".join(verse.itertext()))
print("NOTES:")
for note_id in note_ids:
    print(f"  [{note_id}] {notes[note_id]}")
```

Important: note text is **not** part of the verse's text content. The `<noteref>` marker is empty. This is intentional: `"".join(verse.itertext())` gives clean verse text, and you explicitly join the note bodies when you want them.

---

## 7. Cross-references

Inside note text and non-Bible documents, Bible references use `<ref>`:

```xml
<ref book="PSA" chapter="8" verse="6">Psalms 8:6</ref>
```

| Attribute | Meaning |
| --- | --- |
| `book` | Uppercase book code, for example `PSA`, `MAT`, `1CO`. |
| `chapter` | Chapter number. |
| `verse` | Start verse number. For a range, this is the first verse; the element text shows the complete range. |

To resolve a reference:

1. Map `book` to its directory using the table above or `bible/toc.xml`.
2. Open `<directory>/<lowercase-book>_<chapter:03d>.xml`.
3. Find `<verse number="...">` or the canonical ID `BOOK.CHAPTER.VERSE`.

Example: `<ref book="PSA" chapter="8" verse="6">Psalms 8:6</ref>` points to:

```text
bible/ot/psa/psa_008.xml
verse id="PSA.8.6"
```

---

## 8. Non-Bible documents

The Preface and Glossary are in `bible/other/`. They use a different root element, `<document>`, but the same note and reference conventions.

```xml
<document code="FRT" name="Preface" type="preface">
  <title>Preface to the World English Bible</title>
  <heading kind="section">What is the Holy Bible?</heading>
  <paragraph>The Holy Bible is a collection of books and letters ...</paragraph>
  <list-item>The order of <ref book="MAT" chapter="23" verse="13">Matthew 23:13</ref> and 14 is reversed in some translations.</list-item>
  <notes>
    <note id="FRT.FN1" source-id="FN1" type="footnote" marker="†">“Christ” means “Anointed One”.</note>
  </notes>
</document>
```

The Glossary additionally uses `<entry>` and `<term>`:

```xml
<entry><term>Abaddon</term> Abaddon is Hebrew for destruction.</entry>
```

| Element | Meaning |
| --- | --- |
| `<title>` | Document title. |
| `<heading kind="section">` | Section heading. |
| `<paragraph>` | Paragraph of prose. |
| `<list-item>` | Item in a list. |
| `<entry>` | Glossary entry. |
| `<term>` | Glossary headword inside an entry. |
| `<notes>` / `<note>` / `<noteref>` | Same note scheme as Bible chapters, except notes have no `verse` attribute. |

The Preface and Glossary are outside the three testament directories and are listed under `<other>` in `bible/toc.xml`.

---

## 9. Conventions and caveats

- **No namespaces.** Elements are in the empty namespace, so simple XPath such as `//verse` works without namespace prefixes.
- **UTF-8.** Files are UTF-8 encoded and contain Unicode curly quotes, Hebrew, and Greek where the source does.
- **Normalized whitespace.** Text runs are normalized to single spaces. There are no meaningful line breaks inside verse or note text.
- **Poetry.** Poetry is flattened into prose-like verse text. Psalm titles and acrostic letters are `<heading>` elements, not verses.
- **Verse numbering.** Verse numbers follow the source edition. Numbers may skip; an `omitted="true"` verse is a deliberate placeholder whose note explains the omission or variant.
- **Chapter 0 pages are not included.** They were navigation pages, not Bible chapters. The first real chapter of every book is chapter 1.
- **Single-chapter books** use the book name as the chapter title (for example `Obadiah`, `Philemon`, `Psalm 151`).
- **Notes are chapter-local.** Note IDs are globally unique because they include the book and chapter, but the note definitions are stored in the chapter file that contains their markers.
- **Note markers may repeat or be absent.** The symbols `*`, `†`, `‡`, and `§` are display markers, not identifiers. A note may have no `marker` attribute when the source supplies no symbol. Always use `noteref/@ref` and `note/@id`.
- **Text search scope.** Searching `<verse>` elements searches Scripture text only. Searching `<note>` elements searches notes only. To search both, search the whole file or iterate all text nodes. A plain-text search of a whole chapter file (for example with `grep` or `rg`) also matches note text; use an XML-aware query when you need to restrict a search to verses.
- **Copyright footers are not present.** Only the Bible text, headings, notes, and the two non-Bible documents are included.

---

## 10. Quick reference

| Task | Query or path |
| --- | --- |
| Open Genesis 1 | `bible/ot/gen/gen_001.xml` |
| Find Genesis 1:1 | `//verse[@id='GEN.1.1']` |
| Find all verses in a chapter | `//verse` |
| Find notes for Genesis 1:29 | `//notes/note[@verse='29']` |
| Find a note by ID | `//notes/note[@id='GEN.1.FN2']` |
| Find cross-reference notes | `//notes/note[@type='cross-reference']` |
| Find omitted verses | `//verse[@omitted='true']` |
| Find verses with notes | `//verse[noteref]` |
| Find all headings | `//heading` |
| Find a book's directory | `bible/toc.xml` → `book/@directory` |
| Find a chapter file | `bible/toc.xml` → `chapter/@file` |
| Find a glossary term | `//entry/term` |

The intended workflow is: use `toc.xml` or the book table to find the chapter file, use `verse/@number` or `verse/@id` to locate the verse, then use `noteref/@ref` or `note/@verse` to retrieve its notes.
