# Working on this commentary

This is a collaborative, single-authored chapter-by-chapter commentary on the World English Bible (WEB), written from a confessing Christian perspective and intended to be read aloud. The title, author, rights statement, and language live in `metadata.yaml`. This file governs the writing process, evidence standards, chapter architecture, and house style; `README.md` governs the book’s plan.

The deliverable is a commentary on **1,402 biblical chapters** — 929 Old Testament, 213 Deuterocanon, and 260 New Testament — plus an unnumbered Introduction and Appendices A–E. There is exactly one commentary chapter for each chapter in `bible/toc.xml`. The count is fixed. The page count is an estimate, not a reason to pad or omit evidence.

The chapter is the unit of writing, but the **book** is the unit of work. Do not write a chapter in isolation from the book it belongs to, and do not let a one-page chapter become a fragment with no argument.

## 1. Repository and sources of truth

| File or directory | Responsibility |
|---|---|
| **`README.md`** | Canonical book plan, chapter architecture, genre modes, page budget, visual register, and book-level status |
| **`metadata.yaml`** | Title, author, rights, and language |
| **`AGENTS.md`** | Process, evidence standards, chapter architecture, and house style |
| **`check_book.py`** | Pre-render structural checker |
| **`convert_bible.py`** | Converter from the WEB HTML edition to the XML corpus |
| **`bible/toc.xml`** | Authoritative list of 81 books and 1,402 chapters |
| **`bible/{ot,deut,nt}/<book>/<book>_<NNN>.xml`** | The WEB text, one file per Bible chapter |
| **`chapters/00-introduction.md`** | Introduction |
| **`chapters/{ot,deut,nt}/<book>/<NNN>-<book>-<chapter>.md`** | One commentary chapter per Bible chapter |
| **`chapters/51-appendix-a.md` … `chapters/55-appendix-e.md`** | Appendices A–E |

### Stable file names

- The Introduction is exactly `chapters/00-introduction.md`.
- A commentary chapter is `chapters/{testament}/{book}/{NNN}-{book}-{chapter}.md`.
  - The testament is `ot`, `deut`, or `nt`.
  - The book code and folder come from `bible/toc.xml` and are lowercase in the path: `gen`, `1sa`, `psa`, `1co`, `rev`.
  - The three-digit prefix is a zero-padded sort key; the chapter number also appears as the final segment.
  - Examples: `chapters/ot/gen/001-gen-1.md`, `chapters/ot/psa/023-psa-23.md`, `chapters/deut/sir/051-sir-51.md`, `chapters/nt/1co/013-1co-13.md`.
- Appendices are exactly `chapters/51-appendix-a.md` through `chapters/55-appendix-e.md`. The prefixes 51–55 identify appendices, not commentary chapters 51–55.
- Never rename or renumber a file to repair a mistaken citation. Repair the citation and any affected planning record.
- Use relative links in `README.md` and in chapter files to the actual manuscript and XML paths.

### One plan, not competing plans

`README.md` is the only maintained plan. Chapter files contain the local, more detailed development of the README’s chapter shape and book plan; Appendix C is a reader-facing map catalog, not a competing visual plan; Appendix D is the published chronology and must agree with the chapters.

When scope, chapter structure, a book-level emphasis, a visual, a page allocation, or a status changes during writing, update the relevant README record and every affected chapter or appendix together. Resolve contradictions by checking the text and the evidence and making an explicit decision, not by assuming either the older plan or the newer prose must be right.

### Applying these rules to this repository

This repository began with a plan and tooling adapted from a different book, a history of the United States. That book’s apparatus — epigraphs, opening scenes, In Focus boxes, formal debates, Legacies sections, chapter summaries, study questions, Further Reading sections, closing notes, and bridges — is **retired** here. It does not fit a one-page commentary chapter, and importing it would produce padding rather than commentary.

The four adapted files are `AGENTS.md`, `README.md`, `check_book.py`, and `metadata.yaml`. The XML corpus and `convert_bible.py` are this repository’s own. Do not reintroduce history-book conventions by habit. If a convention from the older project is still useful, adapt it explicitly in this file and in the checker.

There is no manuscript draft yet. The current stage is `planned`. Do not describe a chapter as drafted, checked, or integrated until its file exists and the relevant stage checks have been performed.

### Repository checks

`check_book.py` is the pre-render structural checker. Run it from the repository root:

```bash
python3 check_book.py
python3 check_book.py --strict
python3 check_book.py --json
python3 check_book.py --quiet
python3 check_book.py --book GEN
python3 check_book.py chapters/ot/gen/001-gen-1.md
python3 check_book.py --list
```

With no arguments it checks the full manifest derived from `bible/toc.xml`, plus `chapters/00-introduction.md` and the five appendix files: 1,408 files. `--book GEN` checks one biblical book’s chapters. Positional paths check only those files. `--list` prints the expected paths and exits without checking. `--strict` treats warnings as failures; `--json` emits a machine-readable report; `--quiet` suppresses individual findings and prints the summary. Exit status is 0 when the check passes, 1 when it fails, and 2 for invalid usage or a missing manifest. At Stage 2, run the checker without `--strict`; the short-seed warnings are expected. Use `--strict` from Stage 4 onward.

The checker verifies the manifest against `bible/toc.xml`; the expected file path for every Bible chapter; one level-one heading per file; the title’s reference to the book and chapter; heading levels and any numbered section/subsection order; the required and optional bold labels and their order; chapter word-count targets; the combined footnote namespace, including missing, duplicate, unused, numeric, and wrongly prefixed keys, nested references, `ibid.`, citation notes without a “Used for:” annotation, explanatory notes without an allowed label, content after the definitions, and a separate Sources, References, Notes, or Footnotes heading; pipe-table header, separator, row width, empty tables, captions, textual references, and bold leading cells; local Markdown links and heading anchors; curly quotation marks and apostrophes, the ellipsis character, ordinary spaces, hard breaks, tabs, hyphenated number ranges, Scripture verse ranges written with hyphens, and double hyphens; and body word counts excluding notes and code.

The checker does not verify that a citation supports a claim, that a quotation matches its edition, that a historical reconstruction is sound, that an exegetical judgment is correct, that a visual register matches actual assets, that a table fits a typeset page, or that rendered note links and return links work. Those remain Stage 5 and Stage 7 checks. A passing run means the Markdown is structurally sound, not that the chapter is checked.

Before Stage 2, the default run reports 1,408 missing files. That is the expected state of a planned repository, not a checker failure to investigate.

Report codes such as `note-missing-definition`, `label-order`, and `table-ragged` are stable identifiers and may be cited in review notes. `INFO` findings, such as a chapter that may need emphasis review, are reported but never fail the run.

There is no separate test suite yet. If tests are added, put them beside the checker and document the command here.

## 2. The writing process: plan → seed → research → draft → check → integrate → release

These are separate writing steps with saved outputs. Do not turn a short plan into supposedly finished prose in one pass. For this commentary, finish the book-level plan before seeding, seed every file before expanding a book, and complete a book’s research and drafting before moving to the next book.

Work only within the requested scope. If asked to plan, stop with a plan; if asked to seed, do not draft; if asked to draft, do not describe the result as checked. Report the stage reached, checks actually performed, and remaining blockers. A request to revise one chapter is not authorization to rewrite the rest of the commentary.

### Stage 1 — Plan the whole commentary in `README.md`

Write the complete plan before drafting. It must contain:

1. The guiding question, working thesis, audience, Christian perspective, and the limits that perspective imposes.
2. The five purposes of the commentary and where each appears in the chapter architecture.
3. The canon and scope decision: all 1,402 chapters in `bible/toc.xml`, including the Deuterocanon, with the canon-status question handled honestly.
4. The one-to-one rule and the stable file manifest.
5. The shape of a commentary chapter: required and optional moves, word targets, and the rules against padding and invention.
6. The genre modes and the books or units assigned to each, with the common pitfalls of each mode.
7. A book-by-book plan: file path, title, chapter count, mode, focus and key questions, and status. This is not a 1,402-chapter outline. It is the book-level plan that every chapter brief will follow.
8. For the Introduction and each appendix: contents, purpose, scope, and page allocation. List promised documents, datasets, maps, and other reference material individually, not merely as categories.
9. A complete visual register as specified in §3, including maps, figures, images, and appendix tables.
10. A page budget and a status record for each biblical book.

Budget the whole book, not just the prose. Include titles, the Introduction, the combined notes and citations, tables, maps, figures, images, appendix tables, front matter, and back matter. The working allocation is 1,596 pages: 10 for front/back matter, 14 for the Introduction, 1,527 for the 1,402 commentary chapters plus 125 emphasis pages, and 45 for Appendices A–E. A standard chapter is one page; an emphasis chapter is up to two. These are planning allowances, not measured lengths.

Page counts depend on layout. Record word counts as a working measure, calibrate them against a representative typeset chapter, and revise the budget after actual builds. Do not silently equate a Markdown page or an assumed words-per-page ratio with a finished page.

**Exit check:** every Bible chapter in `bible/toc.xml` has a manifest entry; the count is 1,402; the Introduction and five appendices have entries; the page budget reconciles; coverage has no unexplained gaps or duplication; every planned visual has a register entry; the chapter architecture and genre modes are stated; and the status record is honest about the absence of a draft.

### Stage 2 — Seed every manuscript file from the plan

Create the Introduction, all 1,402 commentary chapters, and the five appendix files using the stable names in §1. Because the manifest is large, seed it deterministically from `bible/toc.xml` with a script or a template; do not hand-create 1,402 inconsistent files.

Each chapter seed contains:

- The level-one heading with the book name, chapter number, and a working descriptive title.
- The passage reference and the corresponding XML path, so the writer can open the text immediately. Put these in a plain line or blockquote, not in a bold label; the bold vocabulary is reserved for the chapter moves in §5.
- The book-level plan from `README.md`, copied into the chapter brief.
- The standard label skeleton from §5, with placeholders rather than prose.
- The chapter’s assigned genre mode and any book-level emphasis.
- Empty or clearly marked slots for the passage structure, key terms, context, interpretive options, Christian reading, sources, and editorial checks.

Do not replace the copied plan with a generic template that loses the book’s focus. Do not write prose in Stage 2. A seed is a plan, not a draft. The checker’s `chapter-short` warning is expected on a seed; it becomes a blocker only when the chapter is presented as drafted.

Track stages in the README book-level status record using `planned`, `seeded`, `researched`, `drafted`, `checked`, and `integrated`. Record the last review date, review scope, and outstanding blockers. A generated `status.tsv` may record per-file status; it is a report, not a second plan. Unfinished material is not `checked`; a substantive later change reopens the affected checks.

**Exit check:** all 1,408 manuscript files exist; each matches its README book entry; the chapter seed contains the required labels and the passage reference; and no file is empty or represented only by a title.

### Stage 3 — Expand one chapter into a researched brief

This is a distinct deliverable, not prose drafting. In the chapter file, expand the seed into a short, bullet-level brief:

- The passage’s structure and movement.
- The historical, cultural, literary, and canonical context that the chapter needs.
- The key Hebrew, Aramaic, or Greek terms, with lexicon and grammar locators.
- The main interpretive options, stated fairly, and the reading the commentary will adopt.
- The Christian reading and its canonical warrant.
- The teaching or application the passage actually supports, if any.
- The sources to be cited, with exact locators.
- The open questions and planned checks, as editorial notes.

For each substantive claim, attach a named citation footnote with the precise supporting passage, page, document identifier, verse ID, lexicon entry, or database locator. Plan quotations, statistics, chronology, visuals, and cross-references with the same care as the prose. Identify what each source cannot establish.

Use primarily accessible, stable, document-specific sources so another reader can check the evidence. This includes the XML text, digitized manuscripts, critical editions, scholarly articles and books, institutional collections, and original datasets. A search result, a catalog listing, a publisher’s description, or an unread book is not evidence for a claim. Search for leads, then open and read the actual source.

Build the chapter’s single annotated footnote list now, using §4. Citations and other notes belong together, not in a separate Sources list.

Do not manufacture a scene, a historical detail, a character’s motive, or a quotation to fill the architecture. Where the text or the evidence does not establish a detail, omit it, qualify the inference, or choose another emphasis. Never invent thoughts, composite witnesses, overheard remarks, or sensory details.

**Exit check:** the chapter has a usable evidence trail; quotations have been transcribed from identified editions; the original-language claims have lexicon or grammar support; the interpretive options are stated fairly; visuals have sources and production plans; and gaps are explicitly marked. An unsupported central claim blocks drafting it as fact; it does not become true because the chapter needs it.

### Stage 4 — Write from the researched brief

Expand the brief into prose, following §§5–6. Keep the named citation references immediately beside the claims they support. Remove planning bullets as they become prose; retain unresolved questions as editorial footnotes rather than letting them disappear.

Drafting may expose new research needs. Return to Stage 3 for those claims, read the sources, and add or update their citation notes before asserting them. Do not write from memory and attach plausible citations afterward. New visuals or scope changes require a README update during the same change, not at the end of the book.

Keep the book open when writing a chapter. Match the book’s argument, recurring terms, and canonical connections. When the previous or next chapter is still provisional, record that dependency rather than inventing a transition. Avoid repeating an earlier chapter’s full explanation when a checked cross-reference will do.

**Exit check:** the complete chapter architecture is present; the labels are in the required order; the word count is within the one-page target or the recorded emphasis allowance; notes and source records remain traceable; and the status is `drafted`, not `checked`.

### Stage 5 — Check the chapter in separate passes

Do not substitute a stylistic reread for verification. Use the checklist in §7 in distinct passes: text and translation; history and culture; exegesis and theology; genre and rhetoric; notes and citations; prose and rendering. Reopen the cited sources and the biblical text. Record what was checked, what changed, and what remains unresolved.

When a source fails to support a claim, correct, qualify, replace, or remove the claim. Do not merely remove its citation and leave it unsupported. Preserve permanent evidence notes; remove editorial notes only when their questions have actually been resolved. If access or tooling prevents a check, say so and leave the relevant blocker open.

**Exit check:** all chapter-level checks pass; no unsupported central assertion, invented detail, unresolved factual correction, or missing required visual remains; the WEB quotation matches the XML; the original-language claims are sound; and a bounded scholarly uncertainty is accurately described in the prose and the permanent note.

### Stage 6 — Integrate across the book and the whole commentary

After chapter checks, read and check the book as a whole. Reconcile `README.md`, the Introduction, the book’s chapters, and the appendices for scope, chronology, recurring terms, claims, statistics, numbering, and cross-references. Search for duplicate explanations, contradictory accounts, dangling links, and promised material that was never supplied.

Check Appendix A’s excerpts against the cited editions; Appendix B’s actual tables against every data reference; Appendix C against the README visual register and actual assets; Appendix D against chapter dates and events; and Appendix E against the interpreters and works the commentary discusses. A list of intended tables or maps is not the promised table or map.

Read the openings, transitions, and closings of adjacent chapters in sequence. Check the Introduction’s stated method, canon decision, and language conventions against the manuscript and this file, locating the actual sections rather than assuming old section numbers. The commentary on Revelation 22 closes the biblical canon; it must not claim to know the date or manner of the end, and it must not confuse the text’s hope with a political forecast.

**Exit check:** book boundaries and appendices agree; the README registers and status records are current; and all affected chapter checks have been rerun after integration edits.

### Stage 7 — Build and release

Use the repository’s actual build tooling; discover it rather than inventing commands or claiming that a nonexistent pipeline passed. If no build is available, report that limitation. Inspect rendered output for the single combined note list, citation links and return links, tables, images, captions, emphasis, and page breaks. Resolve build warnings and inspect both representative pages and known difficult passages.

Reconcile the measured page count with the 1,596-page budget. Confirm exactly 1,402 commentary chapters, one Introduction, and Appendices A–E. Remove planning debris and resolve editorial blockers before release. Do not delete permanent citations or scholarly caveats to make the commentary look finished. Report build results, remaining limitations, and any deliberate departures from the plan.

## 3. The visual register

Maintain the register in `README.md` from Stage 1 onward. It covers **every table, map, figure, photograph, facsimile, and other image**, including those in the Introduction and appendices. No unregistered item may be added to the manuscript. Planned items may be revised or removed, but the plan and affected references must change with them.

For each item, record:

- A unique, stable planning ID, its type, and its display number.
- A short title, its analytical purpose, and the claim it supports.
- Its owning file or book, plus other places that reproduce or reference it.
- Its chronological and geographic coverage; for data, units, denominators, definitions, and base years.
- Source keys and exact source locators; any transformations or calculations. When a source is cited in the manuscript, map its planning key to the named citation note in the owning file; a register key alone is not a reader-facing citation.
- Asset path or table location, caption, source/credit line, and alt text for images. Detailed production information may live with the asset, linked from the register.
- Rights or license evidence, required attribution, and permission status. The WEB text is public domain, but a manuscript image, museum photograph, map, or atlas may not be. Do not assume that a host’s license covers all material it displays.
- Production and verification status: `planned`, `sourced`, `produced`, or `verified`, with specific blockers where necessary.

Use separate book-wide sequences for maps, figures, and images: “Map 12”, “Figure 3”, “Image 2”. Tables are numbered within their owning file: “Gen 1, Table 1”, “App. B, Table 2”. Planning IDs such as `map-01` and `app-b-table-02` disambiguate records; they are not prose citations. Assign planned numbers centrally, not independently in chapter drafts. Freeze released numbering; any necessary renumbering is a coordinated change to the register, manuscript, captions, and references.

The one-page chapter does not carry a visual quota. A map or figure belongs to a book or major unit, not to every chapter. The default is at least one substantive visual for each major unit: the Pentateuch, the Historical Books, the Psalms and Wisdom, the Prophets, the Gospels, Acts and the Letters, the Deuterocanon, and the Introduction and appendices. Shorter books share a unit visual or rely on an appendix map. Additional tables and images must earn their space and fit the budget. A shared visual has one owner and number, with its other uses recorded; Appendix C’s catalog entry is not a new visual.

Every item needs a short caption, a source line, and an explicit textual reference by number. Data drawn from an appendix must point to the actual supporting table, not a convenient number. Maps must state the relevant date and distinguish boundaries, claims, and uncertain reconstructions. A placeholder caption, a map description, or a link to an image is not a finished asset. Tables must contain the promised data or comparison, not merely their titles.

## 4. Evidence and the combined footnote list

### Source selection and verification

- Prefer accessible, stable, document-specific sources: the WEB XML, critical editions, digitized manuscripts, scholarly publishers, university presses, museum and archive catalogs, and peer-reviewed journals. Judge the particular source, its provenance, context, and limits; a prestigious domain alone does not verify a claim.
- Use the biblical text for what it says, primary ancient sources for what ancient writers said, and scholarship for interpretation and context. A primary source can establish that someone made a claim without establishing that the claim was true.
- Distinguish the text, its translation, its interpretation, and its application. “The text says” is not the same as “this commentary reads” or “Christians have applied.”
- Prefer digitized editions and open scholarly texts where possible. Necessary print or restricted sources are allowed only when actually consulted; identify the edition and locator, and state access limitations. A publisher’s description verifies bibliographic details, not an unread book’s argument or a quotation’s wording.
- Distinguish `discovered`, `read`, and `verified for this claim`. Only the last supports a checked assertion. Search snippets and AI summaries are leads, not final verification. If access fails, find an accessible authoritative edition or flag the check as blocked; do not claim to have read it.
- Corroborate disputed, consequential, or surprising claims where possible with independent evidence. Repeated copies of one report are not independent sources. Represent the strongest competing interpretation fairly before answering it.
- Never invent an author, title, URL, page number, quotation, access date, manuscript shelfmark, or verification result. A link that opens is not proof that its contents support the sentence.

### The biblical text and original languages

- Quote the WEB exactly from the XML, including its curly quotation marks, capitalization, and punctuation. Record the verse ID and the XML file. If the commentary modernizes or repunctuates, say so and show the source wording.
- When quoting Hebrew, Aramaic, or Greek, give the text in Unicode, a transliteration, and a translation. Identify the edition (BHS, LXX, NA28, UBS5, or another) and the exact verse or section.
- For a lexical claim, cite the lexicon entry (BDB, HALOT, BDAG, Louw–Nida, or another) and the relevant sense. For a grammatical claim, cite the grammar and section (GKC, Joüon–Muraoka, Waltke–O’Connor, Wallace, Smyth, or another). Do not use Strong’s numbers as a substitute for a lexicon.
- For a textual variant, cite the witness, the apparatus, and the edition. Distinguish a variant from a translation choice. Do not claim that a reading is “original” without argument.
- For an ancient source, cite the edition, book, chapter, section, and translation. “Josephus says” is not a locator; “Josephus, *Antiquities of the Jews* 18.5.2” is.
- For a chronological or archaeological claim, cite the excavation report, the inscription, the dataset, or the scholarly synthesis, and state the uncertainty.

### One list for citations and other notes

**All source citations, explanatory notes, textual notes, scholarly qualifications, and working editorial questions use the same named-footnote system and appear in one list.** Do not split citations into a separate `## Sources`, References, or bibliography list. A citation note can also explain uncertainty; there is no need to create two notes for one evidentiary problem.

Put a named footnote reference immediately after the assertion, quotation, statistic, or caption it supports. The reference must take the reader directly to the citation and its locator, not merely to a source key that requires a second lookup. A note may cover a clearly bounded cluster of related facts, but must identify which source supports which claim. Cite the chapter’s opening, its close reading, its Christian reading, and every visual source line as carefully as the body.

Appendix E is a selective, annotated reader’s guide, not a second citation ledger or a substitute for citation notes. A work may appear there as a recommendation and also be cited in a footnote. README production-source records may remain planning metadata; when used in the manuscript, their evidence must be cited through the combined footnotes.

### Note types

Every footnote definition begins with one of the following, or contains a `Used for:` annotation:

- A **citation note**, which contains `Used for:` and gives the full source details and locator.
- An **explanatory note**, beginning `Explanation —`, for a qualification, definition, or background fact that does not rest on a new source.
- A **textual note**, beginning `Text —`, for a manuscript variant, versification difference, or translation choice.
- An **editorial check**, beginning `Editorial check —`, for an unresolved question, a source still to be consulted, or a dependency on another chapter.

A note that cites evidence and also explains uncertainty should include both the citation and the `Used for:` annotation. Do not use an editorial note to smuggle in an unsupported claim; an editorial note is a task, not evidence.

### Named references, reuse, and file-end order

- Use descriptive named references such as `[^gen-1-creation]`, `[^psa-23-shepherd]`, `[^rom-8-spirit]`, or `[^1co-13-love]`, not numbered keys such as `[^1]`.
- Prefix keys with the book and chapter: `gen-1-`, `1sa-16-`, `psa-23-`, `1co-13-`, `rev-22-`. The prefix prevents collisions when the files are combined.
- Give each key exactly one definition and at least one reference. Citation, explanatory, textual, and editorial notes share one sequence in order of first reference; they are not grouped into separate lists by type.
- Reuse a key when the same source passage and the same qualification support more than one occurrence. If another claim needs a different page, passage, version, or qualification, create a distinct descriptive key rather than silently changing what an existing note supports.
- Give the first citation of a work or version in each chapter its full details. Later notes may use author, short title, and the new exact locator if the full citation is unambiguous within that chapter. Do not use “ibid.”, hard-coded note numbers, or footnote references nested inside note definitions. If the first full citation is removed or moved later, promote the earliest remaining citation so the details are not lost.
- Each file’s notes are self-contained. A reference must resolve to a definition in the same file, not in another chapter or appendix.
- After the chapter’s last paragraph, place all definitions together at the very end of the file as plain Markdown footnote definitions. Do not add a manual heading, bullets, or numbering; separate definitions with blank paragraphs and indent continuation paragraphs when needed. Leave note numbering and any rendered heading to the build. The Introduction and appendices follow the same rule after their main text.
- Check that rendered references, repeated references, note order, and return links work in the combined book. Source-file order alone does not establish correct rendering.

### Required citation-note fields

The first full citation of each work or version includes:

- Author or responsible institution; exact title; original date and publication or hosting institution.
- Edition, translator or editor, document or collection identifier, and other bibliographic details needed to identify the version actually used.
- A direct URL or DOI link to the consulted text or data, and the date actually accessed. For an offline source, give its full print or archive locator and state that it was consulted offline; do not invent a URL.
- The exact page, passage, document, verse, table, dataset variables, or timestamp supporting the attached claim. An entire website or a book title without a usable locator is insufficient.
- **Used for:** a concise description of the specific claim, quotation, translation, dataset, or visual supported, with bold-label or visual IDs where useful. Keep this annotation inside the citation note; “background” or “general reference” alone is inadequate.
- Relevant limitations: conflicting editions, uncertain attribution, translation issues, incomplete data, or restricted access.

Each shortened citation still needs its own precise locator, a clear “Used for” description, and any qualification particular to that claim. A note citing several sources must distinguish their contributions. Explanatory notes without external claims need no invented bibliography; explanatory or editorial notes that rely on evidence include its citation in that same note.

### Templates

The following are structural templates only. Bracketed fields and the example URL are placeholders, not real citations.

```markdown
[The WEB wording of the chapter’s central command].[^gen-1-web]

[A claim about the Hebrew term and its range].[^gen-1-image]

[An unresolved question about the book’s date].[^gen-1-date-check]

[^gen-1-web]: World English Bible Classic, Genesis 1:26–28, in [bible/ot/gen/gen_001.xml](../../../bible/ot/gen/gen_001.xml), verse IDs GEN.1.26–GEN.1.28. Public domain. Used for: the wording and sequence of the creation command. Limitations: the XML is a derived transcription; check it against the WEB edition named in Appendix A.

[^gen-1-image]: [Author], [title], [edition], [publisher], [year], [page or entry]. [Consulted text](https://example.org/replace-with-source). Accessed [actual date]. Used for: **Exposition**, the lexical range of [term] and the translation choice. Limitations: [if applicable].

[^gen-1-date-check]: Editorial check — [the specific unresolved question and the evidence needed to resolve it].
```

Link paths in the notes are relative to the chapter file; from `chapters/ot/gen/` the XML corpus is three levels up (`../../../bible/`).

For an ancient source, the locator should identify the edition and the section:

```markdown
[^rom-8-augustine]: Augustine, *On the Spirit and the Letter*, [chapter and section], trans. [translator], in [edition], [page]. [Consulted text](https://example.org/replace-with-source). Accessed [actual date]. Used for: the history of interpretation summarized in **Christian reading.** Limitations: the translation is [name and date].
```

Build and maintain this single list during research, drafting, and checking. In a researched brief, put unread candidates in a clearly labeled editorial note attached to the research question: `discovered — not yet consulted`. Such a note is a task, not verified support. Resolve these tasks before calling the chapter checked; remove unused leads, but retain evidence citations when editorial questions are answered. Becoming confident does not make attribution unnecessary.

### Quotations and numbers

Quote exactly from the consulted edition, checking spelling, capitalization, punctuation, and omissions character by character. Record a page, verse, section, or equivalent locator for every quotation, including the WEB text and ancient sources. Use square brackets for insertions and spaced ellipsis for omissions. If modernizing or translating a passage, say so and identify the version or translator. Never silently repair the source.

Statistics carry a source, observation year or period, units, population or denominator, and the series or table locator. State rounding, uncertainty, and calculations. For ancient measures, give the biblical measure, the probable modern equivalent, and the range of scholarly estimates. For currency, do not convert ancient sums into modern money without naming the method and its limits. For chronology, give the conventional date, the range, and the reason for the choice. Do not combine incompatible estimates or change definitions without explanation.

## 5. The shape of a finished chapter

The researched brief supplies the argument; the architecture supports it rather than replacing it. The chapter’s total allowance includes its footnotes, tables, and any visual. The standard chapter is about one page; an emphasis chapter may run to about two.

1. **Title.** One level-one heading with the book name, chapter number, and a short descriptive title: `# Genesis 1 — The God Who Creates`. The title must make the reference recognizable without the file name.
2. **The text.** A required bold lead-in and a compact summary of the passage’s movement and central claim, normally 40–70 words. This is not a full quotation of the chapter.
3. **Context.** A required bold lead-in and the historical, cultural, literary, and canonical setting needed to read the chapter, normally 50–90 words. The first chapter of a biblical book includes a short “book at a glance.”
4. **Optional history, form, language, or closer look.** One or more of **History.**, **Form.**, **Language.**, or **A closer look.** when the chapter needs it. A psalm may need **Form.**; a narrative may need **History.**; a legal text may need **Language.**; an archaeological or textual detail may need **A closer look.**
5. **Exposition.** The required heart of the chapter, normally 120–220 words. It follows the passage’s structure, explains key terms and images, and states the reading the commentary adopts.
6. **Optional interpretive options.** **Interpretive options.** when the disagreement is substantial enough to need its own paragraph. State the positions fairly, give the reason for the reading chosen, and leave the question open when it should remain open.
7. **Christian reading.** A required paragraph, normally 50–90 words, placing the passage in the Christian canon and saying how it shapes Christian faith. Label later doctrine as later reception.
8. **Optional theology or ethics.** **Theology.** or **Ethics.** when the passage calls for a doctrinal synthesis or a moral argument that does not fit inside **Christian reading.**
9. **Optional teaching and application.** **Teaching and application.** when the chapter has a clear use in preaching, teaching, or discipleship. Do not force one.
10. **Optional for reflection.** **For reflection.** One or two questions for personal or group use. They should open the text, not test recall.
11. **Optional further reading.** **Further reading.** At most two items, only when genuinely useful to an ordinary reader. Appendix E is the book-level guide.
12. **Optional textual note.** **Textual note.** When a manuscript variant, translation choice, or versification difference affects the reading.
13. **One combined footnote list.** The named definitions for all citations, explanations, textual notes, qualifications, and editorial questions, following §4. Do not add a separate Sources list.

### Required and optional moves

The required moves are **The text.**, **Context.**, **Exposition.**, and **Christian reading.** They appear in that order. The optional moves are **History.**, **Form.**, **Language.**, **A closer look.**, **Interpretive options.**, **Theology.**, **Ethics.**, **Teaching and application.**, **For reflection.**, **Further reading.**, and **Textual note.** They appear only when they do real work.

The fixed order is:

1. **The text.**
2. **Context.**
3. **History.** / **Form.** / **Language.** / **A closer look.** (any order among these)
4. **Exposition.**
5. **Interpretive options.**
6. **Christian reading.**
7. **Theology.** / **Ethics.**
8. **Teaching and application.**
9. **For reflection.**
10. **Further reading.** / **Textual note.**

A chapter that needs a different move must propose it in its brief and update this file and the checker before using it. The controlled vocabulary exists so that 1,402 chapters do not drift into 1,402 private formats.

### Retired apparatus

The older history-book architecture does not apply here. Do not add epigraphs, a staged opening scene, an In Focus box, a formal Debate section with four subsections, a Legacies section, a separate Summary section, a Study Questions section, a formal Further Reading section, a closing note, or a bridge to the next chapter. (The optional **Further reading.** label is a short note, not a section.) Their work is done, when needed, by:

- **Context.** and **History.** for setting.
- **Exposition.** and **Interpretive options.** for argument and dispute.
- **Christian reading.** for canonical and theological connection.
- **Teaching and application.** and **For reflection.** for use.
- **Further reading.** and Appendix E for bibliography.
- A single closing sentence, when it helps, for transition. A bridge is not a required section.

This is a deliberate simplification, not a lower standard. The chapter must still have an argument, evidence, and a Christian reading. It simply does not need the older book’s scaffolding to have them.

### Emphasis chapters

A chapter may receive emphasis pages when its brief records why: canonical weight, interpretive difficulty, the size of the unit, or the need to cover a book’s introduction and first chapter together. The standard emphasis allowance is up to two pages and about 900 words. An emphasis chapter may use the optional moves more fully — **Interpretive options.**, **Theology.**, **Ethics.**, or **A closer look.** — but it may not add a second chapter’s worth of material or repeat the previous chapter.

### The Introduction

The Introduction has its own outlined structure in `README.md`, without epigraphs, an In Focus box, or a bridge. Its framing section carries the book’s numbered claims. It explains the method, the canon decision, the base text, the use of the original languages, the notes, the genre modes, and the reader’s route. It does not preview all 81 books or mechanically inherit the commentary chapter’s labels.

### The appendices

The appendices are reference material: A, Texts and Documents; B, Tables and Data; C, Maps and Gazetteer; D, Chronology; E, Hermeneutical Essay and Guide to Further Reading. They have no commentary chapter labels, roadmap, summary, or reflection questions. They use the same evidence and typography rules, include actual promised material, and each ends with one combined footnote list for citations and other notes. Every table, map, and image needs a source line with a citation reference where full evidence details are required.

## 6. House style

These conventions apply to the commentary’s own prose, headings, tables, and captions. Quotations and titles retain the source’s spelling and wording. Technical examples, file paths, URLs, and source identifiers retain their literal characters.

### Prose and theological reasoning

- Write to be read aloud. Read at least a representative page aloud, or use text-to-speech if available, and check every revised passage for cadence. Do not claim a listening check that was not performed.
- Give each sentence a main idea; keep most under 25 words. A longer sentence earns its length through a clear turn, not stacked clauses.
- Give each paragraph one job. Vary length with the argument; do not force every paragraph into a word quota. Cut paragraphs that merely repeat a claim or roadmap.
- Use past tense for historical narrative, not the historic present. Present tense is appropriate for the text’s wording, the commentary’s argument, and clearly identified present conditions. Do not use the historic present to create false immediacy.
- Prefer concrete nouns and active verbs. Cut “it is important to note”, “arguably”, “of course”, “in many ways”, and “the fact that”. Define technical terms at first use: covenant, eschatology, apocalyptic, justification, atonement, canon, Septuagint, Masoretic Text, and so on.
- Mark inference as inference: “the text suggests”, “probably”, “the evidence does not show”. Give contested dates and reconstructions as ranges or estimates.
- Distinguish what the text says, what the human author likely intended, what the canon or the Christian tradition reads, and what the commentary applies. These are different claims and need different warrants.
- Do not give biblical characters knowledge of later events. A narrative may use irony or foreshadowing, but the commentary must not attribute the later outcome to the character’s mind.
- Where no voice survives, name the silence. Do not ventriloquize women, enslaved people, children, foreigners, or defeated enemies. Do not infer consensus from an absent record.
- Use historical place names, adding the modern identification where useful. Explain genuinely contested names.
- The commentary is Christian, but it is not sectarian. Name the tradition behind a reading when it matters; do not present one party’s interpretation as the plain sense of Scripture.
- Welcome criticism. A chapter may say that a text is difficult, that a traditional reading has caused harm, or that the evidence is insufficient. It must not use criticism as a substitute for reading the text.

### Difficult texts

- **Violence and conquest:** describe what the text says and what the ancient world assumed. Distinguish the narrative’s claim from the historical reconstruction. Do not glory in violence or sanitize it. State the interpretive options and the commentary’s reading.
- **Slavery:** use “enslaved person” in the commentary’s prose; retain “slave” in quotations and in the description of ancient institutions. Explain the range of Hebrew and Greek terms. Do not claim that the Bible endorses modern slavery or that every biblical text is a critique of it.
- **Gender and sexuality:** attend to the ancient setting, the text’s rhetoric, and the history of interpretation. State the main readings fairly. Do not use the text to demean people or to score a modern political point.
- **Imprecation and lament:** let the psalms protest. Do not rush to resolve a lament or explain away a curse. Distinguish the psalm’s voice from the commentary’s moral judgment.
- **Antisemitism and supersessionism:** do not treat “the Jews” as a monolithic antagonist. Distinguish characters, parties, crowds, and later reception. Do not use the New Testament to deny God’s faithfulness to Israel. When a text has been used to harm Jewish people, say so and explain the interpretive alternatives.
- **Canon and the Deuterocanon:** explain the status of the book in the relevant traditions. Do not use the Deuterocanon as a polemic for or against another tradition.
- **Historicity:** distinguish the text’s claim, the historical evidence, and the commentary’s judgment. Do not claim that a narrative is historical or fictional without argument. Do not invent archaeological confirmation.

### Typography and spelling

- Use curly quotation marks and apostrophes: “ ” and ’.
- Use spaced em dashes for breaks — like this — and en dashes for ranges and coordinated compounds: “Gen 1:1–3”, “1 Cor 13:4–7”, “chs. 1–3”, “North–South”. Never use a hyphen between numbers to mean a range.
- Use the ellipsis character “…”, not three periods; a marked omission within a quotation uses spaced ellipsis.
- Use American date order for modern dates: “November 7, 2026”. For biblical chronology, use “586 BCE” and “70 CE”. Give full years at first mention. Write “the 1950s” for modern decades; use “the 50s CE” only when the context is clear, and prefer “the 50s” or “the 50s CE” in technical discussion.
- Spell out one through nine in prose; use figures for 10 and above. Exceptions include proper names, dates, Scripture chapter and verse numbers, statistics, populations, money, measurements, and item numbers. Tables, data, and appendices use figures.
- Use ordinary spaces, not non-breaking spaces, hyphenation tricks, or Markdown hard breaks within paragraphs.
- Use American English: -ize/-ization, behavior, defense, center, program, labor, analyze, judgment; license as noun and practice as noun and verb. Quotations and work titles keep their original spelling.
- Use “Hebrew”, “Aramaic”, and “Greek” as language names; italicize a foreign term only at first occurrence or when discussing the word itself.

### Titles, italics, and bold

- Biblical book titles are roman, not italic: Genesis, 1 Samuel, Psalms, Matthew, Romans. Do not italicize Bible book names.
- Italicize commentary titles, monographs, journals, newspapers, ancient works, and named long documents: *The New International Commentary on the Old Testament*, *Antiquities of the Jews*, *Against Apion*, *The Chicago Manual of Style*.
- Put articles, essays, chapters, sermons, and titled short documents in quotation marks: “The Historical-Critical Method”, “The Sermon on the Mount”, “The Song of the Sea”.
- Ancient inscriptions, laws, and collections are roman and capitalized: the Code of Hammurabi, the Mesha Stele, the Tel Dan Stele, the Dead Sea Scrolls, the Cyrus Cylinder. A book about them is italicized.
- Other italics are for a technical or foreign term at first occurrence, a word discussed as a word, deliberate emphasis, and the fixed labels. A chapter carries no more than a dozen emphasis italics; title italics do not count toward that limit.
- Bold names a move and closes after the lead phrase: **The text.** The paragraph continues in plain text. The controlled vocabulary is **The text.**, **Context.**, **History.**, **Form.**, **Language.**, **A closer look.**, **Exposition.**, **Interpretive options.**, **Christian reading.**, **Theology.**, **Ethics.**, **Teaching and application.**, **For reflection.**, **Further reading.**, and **Textual note.** Do not invent extra labels without changing this file and the checker.
- Bold also marks the leading cell of table rows and the numbered claims in the Introduction. Do not bold whole paragraphs. Check paired emphasis markers and rendered output; a mechanical count alone cannot prove correct rendering.

### Names and house words

- Use “God” capitalized. The WEB renders the divine name as “Yahweh.” Use “Yahweh” when quoting the WEB or discussing the Hebrew name. Use “LORD” only when quoting a translation that uses it or when explaining the convention.
- Do not capitalize divine pronouns (he, him, his) except at the start of a sentence. This follows the base text and modern scholarly style.
- Capitalize “Messiah”, “Christ”, “Son of God”, “Son of Man”, “Holy Spirit”, “Spirit” when referring to the Holy Spirit, and “Word” when referring to Christ in John 1. Lowercase “messianic”, “spirit” when referring to a human spirit, and “word of God” when referring to the message or Scripture, except in titles.
- Capitalize “Satan” as a name; lowercase “the devil”. Capitalize “Gentile(s)”, “Jew(s)”, “Jewish”, “Israelite(s)”, “Judean(s)”, “Samaritan(s)”, “Pharisee(s)”, “Sadducee(s)”, “Essene(s)”, and “Zealot(s)”.
- Use “church” lowercase for the community of believers; capitalize “Church” only in a denomination’s name or a building’s proper name. Use “the early church”, “the New Testament church”, and “the church at Corinth”.
- Use “gospel” lowercase for the message; capitalize “Gospel” for the literary genre or a book title: “the Gospel of Matthew”, “the four Gospels”.
- Use “epistle” lowercase for a letter; capitalize “Epistles” when referring to the New Testament collection.
- Use “Old Testament”, “New Testament”, and “Hebrew Bible” as defined in `README.md`. Use “Deuterocanon” for the collection and “deuterocanonical” as an adjective. Use “Apocrypha” only when quoting or explaining Protestant usage.
- Use “Second Temple” capitalized, “Second Temple Judaism”, “early Judaism”, and “rabbinic Judaism”.
- Use “the land of Israel” for the land in biblical and Second Temple contexts when the text or the tradition uses that frame. Use “Judea”, “Samaria”, “Galilee”, “Idumea”, “Perea”, “the Decapolis”, and “the Levant” for specific regions. Use “Palestine” for the Roman province after 135 CE and for modern geography, and explain the term’s history when it matters. Do not make a modern political claim by choosing a name.
- Use “Judeans” for the people of the province of Judea in the Second Temple period when the geographic or political sense is meant; use “Jews” for the religious and ethnic community and in quotations. Explain the distinction at first use in a chapter.
- Use “enslaved people” in the commentary’s prose; retain “slave” in quotations and historical proper names. Explain the range of Hebrew `ʿebed` and Greek `doulos` when the passage turns on it.
- Use “the nations” or “Gentiles” as the context requires; do not use “the nations” as a decorative synonym for “Gentiles” when the text has a specific term.
- Slurs and degrading period language appear only in quotation, only when necessary to the historical or exegetical argument, and with an explanation in the same paragraph of why they are reproduced.

### Cross-references and tables

- Cite Scripture by book, chapter, and verse: “Gen 1:1–3”, “1 Sam 16:7”, “Ps 23:1–6”, “Matt 5:3–12”, “Rom 8:1–11”. Use full book names in prose at first mention and standard abbreviations in notes and cross-references. There is no space after the colon or around the en dash in a verse range: “Gen 1:1–3”, not “Gen 1: 1–3”.
- Cite a commentary chapter by its Bible reference, not by a sequential number: “the commentary on Gen 1”, “the chapter on Romans 8”. Do not write “Ch. 1” for a commentary chapter; “chapter” is reserved for the Bible’s chapters and can confuse the reader.
- Cite a section within a commentary chapter by its bold label: “**Context** in the commentary on Gen 1”.
- Cite appendices as “App. B, Table 3”, “App. D (Chronology)”; visuals as “Map 2”, “Figure 4”, “Image 1”.
- Before citing a section, table, or visual, open it and confirm that it supports the attributed claim, not merely the general topic. A missing or provisional target is an unresolved dependency, not a checked reference.
- Use pipe tables with a header and a separator such as `|---|---|`. Bold each body row’s leading cell. Keep cells short; comparisons belong in tables, sustained argument in prose. Give each table its registered caption and source line. The caption begins `**Caption.**` and includes the table number.

## 7. Acceptance checklist

Before calling a chapter checked, complete every applicable item. Whole-book items are required again at integration and release.

- [ ] **Plan and scope:** the README book entry, actual title, file path, chapter count, mode, page allowance, status, and registered items agree. The chapter is one of exactly 1,402.
- [ ] **Text and translation:** every WEB quotation matches `bible/` character by character, with the verse ID and XML path; every comparison translation is identified; every versification difference is noted.
- [ ] **Evidence:** every factual assertion is traceable to consulted evidence through a named citation note; citations retain full identification, exact locators, “Used for” annotations, and limitations as specified in §4; access problems and uncertainty are explicit. No unread-source attribution or unsupported correction remains.
- [ ] **Original languages:** every Hebrew, Aramaic, and Greek form is correct; transliteration and gloss are supplied; lexical and grammatical claims cite a lexicon or grammar; no claim rests on Strong’s numbers alone.
- [ ] **Quotations:** every quotation matches the identified edition character by character, with a precise locator and marked omissions and insertions. Ancient-source quotations identify the edition and translation.
- [ ] **Exegesis:** the reading follows the text’s structure and genre; the main interpretive options are stated fairly; the Christian reading is labeled as a reading and does not pretend to be the text’s only sense; allegory has a named warrant.
- [ ] **Reasoning:** historical and cultural claims are supported; inference is marked; later doctrine is distinguished from the text; no biblical character is given later knowledge; no scene or motive is invented.
- [ ] **Difficult texts:** violence, slavery, gender, sexuality, imprecation, and anti-Jewish readings are handled according to §6; no antisemitism, racism, or abuse is left unaddressed.
- [ ] **Chronology:** dates, reigns, and historical reconstructions agree with Appendix D and Appendix B, Table 4; contested dates are given as ranges with the reason; no event is asserted beyond the evidence.
- [ ] **Statistics and measures:** source series, dates, units, denominators, base years, rounding, estimates, and calculations are stated and checked; ancient measures and currency are not converted without a named method.
- [ ] **References:** every cited section, table, and visual exists and supports the claim; relative links resolve; every named footnote has exactly one definition and at least one reference in the same file. Reused notes support the same passage and qualification; shortened citations resolve unambiguously.
- [ ] **Visuals:** the README register matches every actual table, map, figure, and image, its number, placement, caption, credit, source, rights status, and textual reference. Required assets and appendix datasets actually exist; placeholders are not counted as finished.
- [ ] **Architecture and length:** the title, required labels, optional labels, and their order are correct; the chapter is within the one-page target or the recorded emphasis allowance; the book-at-a-glance appears in the book’s first chapter; the retired apparatus has not crept back in.
- [ ] **Language and sound:** terminology, names, tense, spelling, quotation marks, dashes, ellipses, and emphasis follow §6. Cadence has been checked; repetitions and mechanical scaffolding have been cut.
- [ ] **Notes and citations:** citations, explanations, textual notes, qualifications, and editorial questions appear in one named-footnote list, ordered by first reference; no separate Sources or citation list remains. Editorial questions are resolved or remain declared blockers; permanent citations are retained; Appendix E is not being used as an evidence ledger.
- [ ] **Integration:** the Introduction, README, book chapters, appendices, recurring terms, chronology, and visual counts agree; no obsolete second outline or contradictory register is being maintained.
- [ ] **Structural checks:** `python3 check_book.py --strict` passes for the chapter, or every reported error and warning is resolved or declared as a blocker. This does not replace the evidence, quotation, exegesis, visual, or rendering checks above.
- [ ] **Rendering and budget:** available builds pass without unresolved warnings; the combined notes, citation and return links, tables, images, and emphasis have been inspected; measured length has been reconciled with the budget. Unavailable checks are reported, not asserted as passed.

## 8. Web research with TinyFish

TinyFish Search and Fetch are the project’s default web research tools. Use them for source discovery, reading, and verification; record bibliographic evidence in the manuscript, not just in a tool transcript. Use local read and edit tools for repository files. Tool signatures can change, so the live catalog is authoritative; do not guess parameter names.

### Discover tools, then search and read

Inside code mode, discover the exact paths and signatures before first use:

```js
const catalog = search({ query: "tinyfish search fetch_content" });
return catalog.items;
```

Then call the discovered search tool with a focused question and purpose:

```js
const results = await tools.tinyfish.search({
  query: "SBL Handbook of Style abbreviation Bible citations",
  purpose: "Find the standard abbreviation and citation conventions for biblical books and ancient sources"
});
return results;
```

Open relevant results with `fetch_content`. Always pass `format`, `links`, `image_links`, `iframe_links`, and `page_metadata` explicitly:

```js
const content = await tools.tinyfish.fetch_content({
  urls: ["https://www.bibleodyssey.org/"],
  purpose: "Read a scholarly introduction to the biblical world, not just a search snippet",
  format: "markdown",
  links: false,
  image_links: false,
  iframe_links: false,
  page_metadata: false
});
return content;
```

Keep output focused on the passages and metadata needed for the check rather than dumping entire long documents. Inspect both `results` and `errors`; a successful result for one URL does not mean every URL succeeded.

- Run independent searches or fetches in parallel with `Promise.allSettled`. A search followed by reading its result is a dependency, not an independent pair.
- For academic discovery, prefer `domain_type: "research_paper"` where appropriate; use `pub_year_min` and `pub_year_max` for its publication-year filters. For web or news searches, use date windows or `recency_minutes`, not both together.
- Fetch up to 10 URLs per request when the live signature permits it. Keep the consulted edition, locator, and actual access date in the source record.
- If a page blocks access or a PDF does not extract, try another accessible authoritative edition or supported fetch format. Search snippets may guide that search but do not complete a quotation or claim check. Record unresolved access limitations.
- Search and Fetch are free; interactive browser automation is metered. Use automation only when interaction is needed. For authenticated work, use the authorized profile and vault options. After an automation error or timeout, check the existing run rather than retrying blindly; it may still be running. Use asynchronous automation only on an explicit request for background execution.
- Deep research and datasets are slow, billed, and opt-in. Do not start them merely because a chapter needs research. Scheduled monitors and usage-history tools are also only for explicit requests.
- If a tool returns an insufficient-credit or subscription message, show the exact top-up or upgrade link as a clickable Markdown link and ask the user to open it. Show any returned “Add money” link immediately. Do not hide the error, silently substitute a weaker tool, or retry the metered operation blindly.
