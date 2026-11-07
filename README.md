# Reading the World English Bible: A Chapter-by-Chapter Commentary

This is the canonical plan for a chapter-by-chapter commentary on the World English Bible (WEB). The commentary is written from a confessing Christian perspective, broadly ecumenical, and hospitable to honest criticism. It is designed for attentive general readers, students, teachers, pastors, and small groups, and it is written to be read aloud. The title is a working title; the file plan and chapter references do not depend on it.

The title and publication metadata live in [metadata.yaml](metadata.yaml). The writing process, evidence standards, chapter architecture, and house style live in [AGENTS.md](AGENTS.md). The structural checker is [check_book.py](check_book.py). The Bible text is the World English Bible Classic (eng-web), converted to per-chapter XML in [`bible/`](bible/) by [convert_bible.py](convert_bible.py); [`bible/toc.xml`](bible/toc.xml) is the authoritative list of books and chapters.

This README is the only maintained plan. It does not outline all 1,402 commentary chapters. It sets the book-level plan, the shape of every chapter, the genre-specific emphases, the page and word budget, the visual register, and the status record. Each chapter receives its detailed brief in its own file at Stage 3.

## The book’s question and argument

**Guiding question:** What does this chapter of Scripture say, what did it mean in its ancient world, and how does it shape Christian faith, worship, and life today?

**Working thesis:** A faithful commentary reads each chapter in its literary, historical, and canonical context; attends to the original languages where they matter; distinguishes the text from interpretation and application; and offers a Christian reading that is generous toward other traditions and honest about difficulties. The commentary does not pretend to neutral scholarship. It states its commitments, shows its evidence, and invites the reader to test the reading against the text.

The commentary serves five purposes, drawn from the ordinary work of Bible commentary:

1. **Clarifying historical and cultural context:** ancient customs, geography, politics, agriculture, money, family life, worship, and idioms that modern readers do not share.
2. **Bridging linguistic gaps:** Hebrew, Aramaic, and Greek words, grammar, and style that ordinary translations cannot fully carry.
3. **Aiding teaching and preaching:** the passage’s structure, central claim, and lines of application, without turning every chapter into a sermon outline.
4. **Preventing interpretive errors:** reading in context, naming interpretive options, and correcting personal or cultural assumptions.
5. **Providing devotional application:** the passage’s claim on the reader’s worship, repentance, hope, and conduct, without forcing a moral lesson from every text.

These purposes are a repertoire, not a checklist. A chapter on a genealogy will not do what a chapter on Psalm 22 or Romans 8 does. The genre modes below govern which purposes receive the most space.

| Purpose | Primary moves | What it looks like in a chapter |
|---|---|---|
| **Clarifying historical and cultural context** | **Context.**, **History.**, **A closer look.** | Ancient customs, geography, politics, money, family life, worship, and idioms that modern readers do not share. |
| **Bridging linguistic gaps** | **Language.**, **Textual note.** | Hebrew, Aramaic, and Greek terms, grammar, translation choices, and manuscript variants, with the original form and a gloss. |
| **Aiding teaching and preaching** | **Exposition.**, **Teaching and application.**, **For reflection.** | The passage’s structure, central claim, and lines of application, without turning every chapter into a sermon outline. |
| **Preventing interpretive errors** | **Exposition.**, **Interpretive options.** | Reading in context, naming the main options, and correcting personal or cultural assumptions. |
| **Providing devotional application** | **Christian reading.**, **Teaching and application.**, **For reflection.** | The passage’s claim on worship, repentance, hope, and conduct, without forcing a moral lesson from every text. |

## Audience, perspective, and limits

**Audience:** readers who know the Bible reasonably well but not the original languages; students and teachers who need a reliable orientation; pastors and small-group leaders who need the passage’s argument and its main interpretive questions; and listeners who encounter the book through reading aloud.

**Perspective:** the commentary is written from a Christian perspective. It treats Scripture as authoritative for faith and life, reads the Old and New Testaments as a unified canon without flattening their differences, and reads everything in relation to Jesus Christ without making every verse a coded prophecy. It does not treat the Old Testament as a puzzle whose only meaning is the New Testament, and it does not use the New Testament to deny God’s faithfulness to Israel. It is ecumenical: it draws on Catholic, Orthodox, Protestant, and Jewish scholarship, and it names the tradition behind a reading when that matters.

**Criticism:** “Christian perspective” does not mean defensive or credulous. The commentary may criticize the text’s reception, the use made of a passage, the behavior of its characters, and the commentary tradition itself. It may state that a historical claim is uncertain, that a moral problem is unresolved, or that a traditional reading is poorly grounded. It must do so fairly, with evidence, and without contempt for the communities that read the text differently.

**Limits:** this is a chapter-level commentary, not a verse-by-verse technical commentary, a systematic theology, a history of interpretation, or a replacement for the biblical text. It does not settle every critical question. It aims to give the reader what is needed to read the chapter well and to know where the disputed questions lie.

## Scope and canonical decisions

### The base text

The base text is the World English Bible Classic (eng-web), a public-domain translation, as supplied in the repository’s XML corpus. The XML preserves verse numbers, verse IDs, section headings, speaker labels, psalm titles, and the translation’s notes. The commentary quotes the WEB exactly when it quotes the translation. When it compares another translation, it names that translation and cites the edition.

The Hebrew, Aramaic, and Greek texts stand behind the translation. The commentary may cite the Biblia Hebraica Stuttgartensia (BHS) or another critical edition for the Hebrew Bible, the Septuagint for the Greek Old Testament, and the Nestle–Aland or United Bible Societies text for the New Testament. It does not claim to collate manuscripts unless it has actually done so.

### The canon

The XML corpus contains 1,402 chapters in three divisions:

| Division | Books | Chapters |
|---|---|---|
| **Old Testament** | 39 | 929 |
| **Deuterocanon** | 15 | 213 |
| **New Testament** | 27 | 260 |
| **Total** | 81 | 1,402 |

The commentary covers all 1,402 chapters, including the Deuterocanon. This is a deliberate decision, not a judgment that every Christian tradition receives every book as canonical. The Deuterocanonical books are treated as Scripture by Catholic and Orthodox readers, as edifying ancient literature by many Protestants, and as important Jewish literature by scholars. The commentary explains the canon-status question at the first chapter of each Deuterocanonical book and then reads the book on its own terms. It does not use the Deuterocanon as a weapon in a canon debate.

The commentary uses “Old Testament” when speaking from within the Christian canon and “Hebrew Bible” when speaking of the Jewish canon or of the scholarly field. It uses “Deuterocanon” for the collection and “deuterocanonical” as an adjective. “Apocrypha” appears only when quoting a source or explaining Protestant usage.

### The one-to-one rule

There is exactly one commentary chapter for each chapter in `bible/toc.xml`. The count is fixed at 1,402. A commentary chapter may be longer or shorter, but it may not be split, merged, or skipped. The only additional manuscript units are the Introduction and Appendices A–E.

The commentary does not add separate book-introduction files. The first chapter of each biblical book carries a short “book at a glance” inside its **Context.** section. That keeps the one-to-one rule intact and prevents 81 extra units from becoming a second, uncontrolled outline.

### Dates and chronology

Use BCE and CE in the commentary’s own prose, not BC and AD, except in quotations and proper names. Give full years at first mention. Where ancient dates are contested, give a range or a conventional date and say so. Do not present a reign date, an exodus date, or a conquest date as settled when the evidence is not. Appendix D is the published chronology; it must agree with the chapters.

### Research cutoff

The planning cutoff for this revision is **November 7, 2026**. Claims about archaeological discoveries, publication details, and current scholarship must be checked against works consulted by that date. A later source may be added only when it has actually been read and the relevant chapter, appendix, and README record are updated together. The cutoff is not a claim that no older work matters; it is a rule against unverified novelty.

## The shape of a commentary chapter

Every commentary chapter is built from the same small set of moves. The moves are marked with bold lead-ins, not headings, so that a one-page chapter does not fill up with typographic scaffolding. A bold label closes after the lead phrase; the paragraph continues in plain text.

### Standard architecture

1. **Title.** One level-one heading with the book name, chapter number, and a short descriptive title: `# Genesis 1 — The God Who Creates`. The reference must be recognizable without the file name.
2. **The text.** A compact summary of the passage’s movement and central claim, normally 40–70 words. This is not a full quotation of the chapter. It tells the reader what happens or what the argument is.
3. **Context.** The historical, cultural, literary, and canonical setting needed to read the chapter, normally 50–90 words. For the first chapter of a biblical book, this includes the “book at a glance.”
4. **Optional form, history, or language.** One or more of **Form.**, **History.**, **Language.**, or **A closer look.** when the chapter needs it. A psalm may need **Form.**; a narrative may need **History.**; a legal text may need **Language.**; an archaeological or textual detail may need **A closer look.**
5. **Exposition.** The heart of the chapter, normally 120–220 words. It follows the passage’s own structure, explains key terms and images, and states the reading the commentary adopts. Contested passages name the main options here.
6. **Optional interpretive options.** **Interpretive options.** when the disagreement is substantial enough to need its own paragraph. State the positions fairly, give the reason for the reading chosen, and leave the question open when it should remain open.
7. **Christian reading.** A required paragraph, normally 50–90 words, that places the passage in the Christian canon and says how it shapes Christian faith. This is deliberately a reading, not a claim that the human author foresaw every later doctrine.
8. **Optional theology or ethics.** **Theology.** or **Ethics.** when the passage calls for a doctrinal synthesis or a moral argument that does not fit inside **Christian reading.**
9. **Optional teaching and application.** **Teaching and application.** when the chapter has a clear use in preaching, teaching, or discipleship. Do not force one.
10. **Optional for reflection.** **For reflection.** One or two questions for personal or group use. They should open the text, not test recall.
11. **Optional further reading.** **Further reading.** At most two items, only when they are genuinely useful to an ordinary reader. The book-level guide is Appendix E.
12. **Optional textual note.** **Textual note.** When a manuscript variant, translation choice, or versification difference affects the reading.
13. **One combined footnote list.** All citations, explanations, textual notes, and editorial checks at the end of the file, using the named-footnote system in AGENTS.md §4.

### Required and optional moves

The required moves are **The text.**, **Context.**, **Exposition.**, and **Christian reading.** Every chapter must have them, in that order. The optional moves are **History.**, **Form.**, **Language.**, **A closer look.**, **Interpretive options.**, **Theology.**, **Ethics.**, **Teaching and application.**, **For reflection.**, **Further reading.**, and **Textual note.** They appear only when they do real work.

The order is fixed:

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

A chapter that needs a different move should propose it in its brief and update this README and `AGENTS.md` before using it. The controlled vocabulary exists so that 1,402 chapters do not drift into 1,402 private formats.

### Word and page targets

A standard chapter is about one typeset page: normally 350–550 words of body text, plus 3–6 footnotes. A chapter marked for emphasis may run to about two pages: normally 550–900 words, plus up to 10 footnotes. A chapter below 250 words is probably a stub; a chapter above 900 words needs a recorded reason in its brief.

These are drafting targets, not a license to pad. A short chapter on Philemon may do its work in 400 words; a long chapter on Romans 8 may need 800. The page budget carries an emphasis reserve for the chapters that need it.

### What no chapter may do

- Invent a scene, a character’s thoughts, a conversation, a crowd, a landscape, or a sensory detail that the text and the evidence do not support.
- Quote a commentary, lexicon, ancient source, or translation that has not been consulted in the edition cited.
- Treat a later doctrine as if it were explicit in the text without labeling it as later reception.
- Use allegory without a warrant from the text, the canon, or a named interpretive tradition.
- Flatten a genuine interpretive disagreement into a single “obvious” reading.
- Use the text to justify antisemitism, racism, violence against outsiders, or the abuse of any person or group.
- Turn every chapter into a moral lesson, an altar call, or a political program.
- Hide an unresolved problem behind devotional language. If the editor has not resolved it, the footnote says so.

### A skeleton

The following skeleton is a planning aid, not a chapter. Angle brackets mark material to be supplied.

```markdown
# <Book> <Chapter> — <Descriptive Title>

**The text.** <The passage’s movement and central claim in 40–70 words.>

**Context.** <Historical, literary, and canonical setting in 50–90 words. For a book’s first chapter, add the book at a glance.>

**Language.** <Optional: a Hebrew, Aramaic, or Greek term, its range, and why it matters.>

**Exposition.** <The main reading, following the passage’s structure, in 120–220 words.>

**Interpretive options.** <Optional: the main positions, stated fairly, and the reading adopted.>

**Christian reading.** <The passage in the Christian canon and its claim on faith, in 50–90 words.>

**Teaching and application.** <Optional: a line of teaching or application, without forcing it.>

**For reflection.** <Optional: one or two questions.>

[^<book>-<chapter>-<descriptive-key>]: <Citation or note>. Used for: <specific claim>. <Limitations.>
```

## Genre modes

The chapters vary in genre, and the commentary varies with them. A narrative chapter asks who acts, what changes, and how the narrator frames it. A psalm asks how the poem works and what it does to the praying community. A law chapter asks what the statute assumes about God, land, family, and neighbor. The following modes are the default starting points; a book may combine two modes.

| Mode | Books and units | What the chapter emphasizes | Common pitfalls |
|---|---|---|---|
| **Narrative** | Genesis, Exodus (prose), Joshua–2 Kings, Ruth, Esther, Daniel’s court tales, Jonah, the Gospels, Acts, Tobit–2 Maccabees, 1 Esdras, 3 Maccabees | Plot, character, setting, point of view, repetition, narrative gaps, covenant and providence | Preaching a moral from every episode; inventing motives or dialogue; ignoring the narrator’s frame and the book’s larger shape |
| **Law** | Exodus 20–40, Leviticus, Numbers, Deuteronomy | Covenant structure, ritual logic, purity and holiness, case law, social ethics, the shape of Israel’s constitution | Reading every statute as a direct modern policy; ignoring the ancient setting; separating law from grace or grace from demand |
| **Poetry** | Psalms, Song of Solomon, Lamentations, Prayer of Manasses, Psalm 151 | Parallelism, imagery, voice, emotion, acrostic form, prayer and praise, the body and desire | Allegorizing without warrant; ignoring the genre; resolving lament too quickly; treating a poem as a doctrinal proposition |
| **Wisdom** | Job, Proverbs, Ecclesiastes, Wisdom, Sirach, Baruch, James, 4 Maccabees | Observation, argument, ambiguity, the fear of the Lord, virtue, friendship, the limits of wisdom | Turning a proverb into a promise; ignoring irony and frame; harmonizing Job’s friends with the book’s verdict; moralizing Ecclesiastes |
| **Prophecy** | Isaiah–Malachi, Lamentations, Baruch, Daniel’s visions, Revelation | Historical address, poetic form, covenant lawsuit, judgment and hope, fulfillment, the prophet’s audience | Reading every prophecy as a code for today; ignoring the original crisis; supersessionism; predicting dates |
| **Gospel** | Matthew, Mark, Luke, John | Narrative sequence, discourse, Christology, kingdom, cross and resurrection, the evangelist’s design | Harmonizing away differences; using John as a flat substitute for the Synoptics; ignoring the evangelist’s ordering of the material |
| **Epistle** | Romans–Jude, Hebrews, 1–3 John | Occasion, argument, rhetoric, theology, ethics, the church’s situation | Quoting verses apart from the argument; ignoring the letter’s occasion; importing later controversies into the first century |
| **Apocalyptic** | Daniel, Revelation, 2 Esdras, parts of Ezekiel and Zechariah | Symbol, vision, historical referent, worship, empire, hope, the new creation | Decoding symbols as a newspaper; ignoring the genre; date-setting; losing the pastoral purpose in speculation |
| **List and genealogy** | 1 Chronicles, Ezra–Nehemiah, 1 Esdras, census and genealogy lists | Structure, purpose, continuity, identity, worship, the meaning of memory | Skimming as irrelevant; treating a list as a modern record; ignoring its rhetorical and theological function |
| **Deuterocanonical** | Tobit–4 Maccabees, Psalm 151 | The book’s own genre, plus a clear note on canon status and Jewish and Christian reception | Ignoring the books; treating them as uniformly secondary; using them as a canon polemic |

A chapter may also combine modes: Exodus is narrative and law; Daniel is narrative and apocalyptic; Hebrews is epistle and sermon; Revelation is prophecy and apocalyptic. The brief names the dominant mode and the secondary mode.

## Book-by-book plan and status

The tables below are the book-level plan and the status record. Every chapter starts at `planned`. The next gate for every book is Stage 2 seeding. When a book is seeded, researched, drafted, checked, or integrated, update its row and the review record. The chapter-level manifest is generated from `bible/toc.xml`; it is not copied into this README.

Each row’s file path follows the stable pattern in “File manifest and status record”: `chapters/{testament}/{book}/{NNN}-{book}-{chapter}.md`. The exact paths are generated by `python3 check_book.py --list`; they are not repeated in every row.

The **Focus and key questions** column is a planning summary, not a claim that every question will receive equal space. A book’s first chapter carries its “book at a glance”; the remaining chapters follow the book’s own order.

### Old Testament

| Book | Chs | Mode | Focus and key questions | Stage |
|---|---|---|---|---|
| **Genesis** | 50 | Narrative | Creation, covenant, and the family of Abraham; primeval history, patriarchal narratives, and the book’s structure; source criticism and genre. | `planned` |
| **Exodus** | 40 | Narrative and law | Deliverance, covenant, law, and divine presence; the divine name, Passover, the golden calf, and the shape of the covenant. | `planned` |
| **Leviticus** | 27 | Law | Holiness, sacrifice, purity, and priesthood; the logic of ritual and the Christian reading of law. | `planned` |
| **Numbers** | 36 | Narrative and law | Wilderness testing, census, and covenant fidelity; judgment, mercy, and the cost of unbelief. | `planned` |
| **Deuteronomy** | 34 | Law | Covenant renewal, love of God, justice, and memory; the shape of Israel’s constitution and its later reception. | `planned` |
| **Joshua** | 24 | Narrative | Land, conquest, and covenant loyalty; violence, allocation, and the book’s rhetorical purpose. | `planned` |
| **Judges** | 21 | Narrative | Cycles of rebellion and rescue; leadership, violence, and the cost of disorder. | `planned` |
| **Ruth** | 4 | Narrative | Loyalty, kinship, and redemption; famine, foreignness, and the genealogy of David. | `planned` |
| **1 Samuel** | 31 | Narrative | Kingship, prophetic authority, and the rise of David; Saul’s tragedy and God’s hidden providence. | `planned` |
| **2 Samuel** | 24 | Narrative | David’s reign, covenant, sin, and succession; power, family, and consequence. | `planned` |
| **1 Kings** | 22 | Narrative | Solomon, the temple, the divided kingdom, and prophetic critique; wealth, idolatry, and empire. | `planned` |
| **2 Kings** | 25 | Narrative | Exile, reform, and prophetic witness; the fall of Samaria and Jerusalem. | `planned` |
| **1 Chronicles** | 29 | Genealogy and narrative | Worship, genealogy, and Davidic hope; the Chronicler’s theological retelling of Israel’s story. | `planned` |
| **2 Chronicles** | 36 | Narrative | Temple, kingship, and repentance; the Chronicler’s case for faithful worship. | `planned` |
| **Ezra** | 10 | Narrative and list | Return, restoration, and covenant identity; Persian policy, intermarriage, and the law. | `planned` |
| **Nehemiah** | 13 | Narrative and list | Rebuilding walls and community; prayer, opposition, and social justice. | `planned` |
| **Esther** | 10 | Narrative | Providence without naming God; diaspora survival, power, and festival. | `planned` |
| **Job** | 42 | Wisdom and poetry | Suffering, theodicy, and divine freedom; the friends’ arguments and God’s answer. | `planned` |
| **Psalms** | 150 | Poetry | Prayer, praise, lament, and trust; genre, parallelism, and the shape of the Psalter. | `planned` |
| **Proverbs** | 31 | Wisdom | Skill for living, the fear of the Lord, and the limits of maxims; wisdom and folly. | `planned` |
| **Ecclesiastes** | 12 | Wisdom | Hevel, mortality, and joy; the limits of wisdom and the fear of God. | `planned` |
| **Song of Solomon** | 8 | Poetry | Desire, covenant love, and interpretation; allegory, literal reading, and the body. | `planned` |
| **Isaiah** | 66 | Prophecy | Judgment, holiness, comfort, and servant hope; Assyria, Babylon, and the shape of the book. | `planned` |
| **Jeremiah** | 52 | Prophecy | Covenant rupture, judgment, and the new covenant; prophet, city, and exile. | `planned` |
| **Lamentations** | 5 | Poetry and prophecy | Grief, protest, and hope; acrostic form and the theology of lament. | `planned` |
| **Ezekiel** | 48 | Prophecy and apocalyptic | Glory, exile, and restoration; vision, symbolism, and the temple. | `planned` |
| **Daniel** | 12 | Narrative and apocalyptic | Faith under empire, visions, and the son of man; court tales and apocalyptic. | `planned` |
| **Hosea** | 14 | Prophecy | Covenant infidelity, judgment, and steadfast love; marriage imagery and the knowledge of God. | `planned` |
| **Joel** | 3 | Prophecy | Locusts, repentance, and the day of the Lord; Spirit and restoration. | `planned` |
| **Amos** | 9 | Prophecy | Justice, worship, and judgment; the prophet from Tekoa and the northern kingdom. | `planned` |
| **Obadiah** | 1 | Prophecy | Edom’s judgment and Zion’s hope; sibling rivalry and the day of the Lord. | `planned` |
| **Jonah** | 4 | Narrative and prophecy | Mercy beyond Israel; flight, repentance, and the prophet’s anger. | `planned` |
| **Micah** | 7 | Prophecy | Justice, mercy, and humble walking; judgment and messianic hope. | `planned` |
| **Nahum** | 3 | Prophecy | Nineveh’s fall and divine justice; violence and the comfort of the oppressed. | `planned` |
| **Habakkuk** | 3 | Prophecy | Complaint, waiting, and faith; the righteous shall live by faith. | `planned` |
| **Zephaniah** | 3 | Prophecy | The day of the Lord, remnant, and restoration; judgment and purified worship. | `planned` |
| **Haggai** | 2 | Prophecy | Temple rebuilding and covenant blessing; postexilic priorities. | `planned` |
| **Zechariah** | 14 | Prophecy and apocalyptic | Visions, priesthood, and messianic hope; restoration and the coming king. | `planned` |
| **Malachi** | 4 | Prophecy | Covenant faithfulness, worship, and the messenger; the book’s closing hope. | `planned` |

### Deuterocanon

| Book | Chs | Mode | Focus and key questions | Stage |
|---|---|---|---|---|
| **Tobit** | 14 | Narrative | Family piety, almsgiving, and providence; diaspora wisdom and the fear of God. | `planned` |
| **Judith** | 16 | Narrative | Courage, piety, and deliverance; gender, violence, and the use of history. | `planned` |
| **Esther (Greek)** | 10 | Narrative | Providence, prayer, and deliverance; the Greek additions and canonical difference. | `planned` |
| **Daniel (Greek)** | 14 | Narrative and apocalyptic | Court tales, visions, and prayer; the Greek additions and apocalyptic symbolism. | `planned` |
| **Wisdom** | 19 | Wisdom | Immortality, wisdom, and idolatry; Hellenistic Judaism and Christian reception. | `planned` |
| **Sirach** | 51 | Wisdom | Instruction, friendship, family, and worship; the wisdom tradition and the canon. | `planned` |
| **Baruch** | 6 | Prophecy and wisdom | Repentance, wisdom, and hope; the letter of Jeremiah and exile. | `planned` |
| **1 Maccabees** | 16 | Narrative | Resistance, covenant, and empire; the Hasmonean rise and historical memory. | `planned` |
| **2 Maccabees** | 15 | Narrative | Martyrdom, temple, and divine intervention; rhetorical history and resurrection hope. | `planned` |
| **1 Esdras** | 9 | Narrative and list | Return and reform; textual relationship to Ezra–Nehemiah. | `planned` |
| **Prayer of Manasses** | 1 | Poetry and prayer | Repentance and divine mercy; the prayer’s setting and theology. | `planned` |
| **Psalm 151** | 1 | Poetry | David’s election and humility; the psalm’s canonical status. | `planned` |
| **3 Maccabees** | 7 | Narrative | Persecution, deliverance, and diaspora identity; rhetoric and history. | `planned` |
| **2 Esdras** | 16 | Apocalyptic | Vision, judgment, and consolation; the Latin Esdras and apocalyptic hope. | `planned` |
| **4 Maccabees** | 18 | Wisdom and rhetoric | Reason, martyrdom, and virtue; Hellenistic Jewish philosophy. | `planned` |

### New Testament

| Book | Chs | Mode | Focus and key questions | Stage |
|---|---|---|---|---|
| **Matthew** | 28 | Gospel | Jesus as Messiah and new Moses; fulfillment, kingdom, and community. | `planned` |
| **Mark** | 16 | Gospel | Suffering Messiah, discipleship, and the cross; urgency and secrecy. | `planned` |
| **Luke** | 24 | Gospel | Salvation for the outcast, the Spirit, and prayer; history, women, and the poor. | `planned` |
| **John** | 21 | Gospel | Signs, glory, and belief; incarnation, love, and the hour of the cross. | `planned` |
| **Acts** | 28 | Narrative | Spirit, mission, and community; Jerusalem to Rome and the growth of the church. | `planned` |
| **Romans** | 16 | Epistle | Gospel, justification, Israel, and new life; Paul’s argument and its coherence. | `planned` |
| **1 Corinthians** | 16 | Epistle | Unity, sexuality, worship, and resurrection; the gospel in a divided church. | `planned` |
| **2 Corinthians** | 13 | Epistle | Apostleship, weakness, and reconciliation; Paul’s defense and the collection. | `planned` |
| **Galatians** | 6 | Epistle | Justification, law, and freedom; Paul’s opponents and the truth of the gospel. | `planned` |
| **Ephesians** | 6 | Epistle | Grace, unity, and the church; the cosmic Christ and household ethics. | `planned` |
| **Philippians** | 4 | Epistle | Joy, humility, and citizenship; the Christ hymn and friendship. | `planned` |
| **Colossians** | 4 | Epistle | Christ’s supremacy, false teaching, and new life; cosmic reconciliation. | `planned` |
| **1 Thessalonians** | 5 | Epistle | Hope, holiness, and the Lord’s return; pastoral encouragement. | `planned` |
| **2 Thessalonians** | 3 | Epistle | Persecution, judgment, and faithful work; the day of the Lord. | `planned` |
| **1 Timothy** | 6 | Epistle | Church order, sound doctrine, and godliness; leadership and wealth. | `planned` |
| **2 Timothy** | 4 | Epistle | Suffering, Scripture, and succession; Paul’s final charge. | `planned` |
| **Titus** | 3 | Epistle | Grace, good works, and community order; sound doctrine on Crete. | `planned` |
| **Philemon** | 1 | Epistle | Reconciliation, slavery, and brotherhood; Paul’s persuasion. | `planned` |
| **Hebrews** | 13 | Epistle and sermon | Christ’s priesthood and better covenant; warning, faith, and perseverance. | `planned` |
| **James** | 5 | Epistle and wisdom | Faith and works, speech, and poverty; wisdom for a scattered church. | `planned` |
| **1 Peter** | 5 | Epistle | Suffering, hope, and holiness; diaspora identity and baptismal imagination. | `planned` |
| **2 Peter** | 3 | Epistle | False teaching, judgment, and patience; the day of the Lord. | `planned` |
| **1 John** | 5 | Epistle | Love, truth, and assurance; tests of faith and the antichrist. | `planned` |
| **2 John** | 1 | Epistle | Truth, love, and hospitality; discernment in the church. | `planned` |
| **3 John** | 1 | Epistle | Hospitality, authority, and conflict; Gaius and Diotrephes. | `planned` |
| **Jude** | 1 | Epistle | Contending for the faith; false teachers and divine judgment. | `planned` |
| **Revelation** | 22 | Apocalyptic | Worship, witness, and hope; symbols, empire, and the new creation. | `planned` |

## Introduction and appendices

### Introduction — 14 pages

The Introduction is a single unnumbered file, `chapters/00-introduction.md`. It has no epigraphs, no In Focus box, and no bridge. Its sections are:

1. Why this commentary, and who it is for.
2. The World English Bible as base text: translation, style, and public-domain status.
3. One chapter at a time: the plan and the limits of a chapter-level commentary.
4. Reading in context: history, literature, and language.
5. A Christian reading, offered with humility: perspective, criticism, and charity.
6. How the notes work: citations, explanations, textual notes, and editorial checks.
7. Canon, translation, and the Deuterocanon.
8. The shape of a commentary chapter, with a guide to the genre modes.
9. Reader’s route and acknowledgments.

The Introduction’s numbered framing claims are:

1. The Bible is a library of books with distinct genres, historical settings, and literary conventions.
2. A Christian reading takes the whole canon seriously without flattening the Testaments into one voice.
3. Historical and literary context serves the text; it does not replace theological reading.
4. The original languages clarify the text but do not create a secret code available only to experts.
5. Every chapter has an argument; not every chapter has the same kind of application.
6. Interpretive disagreement is normal; the commentary states the options and its reasons.
7. The commentary is written from a Christian perspective, welcomes criticism, and refuses to use the text to harm people.
8. The notes are part of the commentary, not an afterthought.

The Introduction carries these claims. It does not preview all 81 books.

### Appendix A — Texts and Documents — 12 pages

A reader’s sourcebook of short, cited texts that illuminate the commentary:

1. The World English Bible preface, glossary, and translation notes.
2. Ancient Near Eastern creation and flood texts, in translation.
3. The Code of Hammurabi and ancient Near Eastern law, in translation.
4. Hittite treaty form and the shape of covenant.
5. The Merneptah Stele and early Israel.
6. The Mesha Stele and the Moabite perspective.
7. The Tel Dan Stele and the house of David.
8. Sennacherib’s annals and the siege of Jerusalem.
9. The Cyrus Cylinder and the Persian restoration.
10. The Elephantine letters and diaspora religion.
11. The Septuagint prologue and the translation of Scripture.
12. The Dead Sea Scrolls and textual pluralism.
13. Josephus and the first-century world.
14. The Pilate inscription and Roman Judea.
15. Early Christian creeds and confessional formulas.
16. A catena of patristic readings on a selected psalm.
17. A medieval Jewish commentary excerpt on Genesis.
18. A Reformation preface on Romans.
19. A modern Catholic and a modern Protestant statement on Scripture.
20. A contemporary Orthodox statement on the Septuagint.

Each selection needs a headnote, a source line, a citation note, and a note on rights. The list is a plan; no selection is considered produced until the text has been collated against a consulted edition.

### Appendix B — Tables and Data — 12 pages

1. Weights and measures, with modern equivalents and uncertainty.
2. Currency, wages, and prices, with the limits of ancient evidence.
3. The biblical calendar and festivals.
4. Kings of Israel and Judah, with regnal dates and co-regencies.
5. High priests from Aaron to the Second Temple.
6. The tribes, their territories, and the geography of the land.
7. A harmony of the Gospels, with the main differences preserved.
8. Paul’s journeys and the cities of the Aegean mission.
9. A New Testament chronology, with contested dates marked.
10. A Second Temple chronology, 516 BCE–70 CE.
11. A table of the Deuterocanonical books, their genres, and their canonical status in major traditions.
12. A glossary of critical terms: source criticism, form criticism, redaction criticism, canonical criticism, and narrative criticism.

Tables use figures, units, definitions, base years, and source locators. A table is not produced until it contains the promised data.

### Appendix C — Maps and Gazetteer — 8 pages

The appendix reproduces Maps 1–12, with captions, source lines, and a gazetteer of place names. The gazetteer gives the biblical name, the modern identification where known, the relevant passages, and a note on uncertainty. Maps state the date of the political boundaries they show and distinguish settled boundaries from contested reconstructions.

### Appendix D — Chronology — 6 pages

A dated chronology in five parts: the ancient Near East and the patriarchal period; the exodus, conquest, and judges; the monarchy; the exile and Second Temple period; and the New Testament era. Contested dates are given as ranges, with the reason. The chronology must agree with the chapters and with Appendix B, Table 4.

### Appendix E — Hermeneutical Essay and Guide to Further Reading — 7 pages

A concise history of interpretation and a selective, annotated guide:

1. Jewish and Christian interpretation from the ancient world to the present.
2. The historical-critical methods and their limits.
3. Literary, canonical, and theological readings.
4. A Christian reading that welcomes criticism.
5. Commentaries and reference works by biblical book.
6. Lexicons, grammars, and textual editions.
7. A short list of works for ordinary readers.

The essay is not a second citation ledger. Works used as evidence are cited in the combined footnotes of the chapters; works recommended for further study are described here.

## Page budget

The base is one page for each of the 1,402 Bible chapters. The emphasis reserve allows selected chapters to run to two pages. The chapter allocations include the chapter’s footnotes, tables, and any visual; the Introduction and appendices are budgeted separately below.

| Component | Chapters | Pages |
|---|---|---|
| **Front and back matter outside manuscript files** | Title, rights, contents, lists | 10 |
| **Introduction** | Unnumbered | 14 |
| **Old Testament** | 929 + 60 emphasis | 989 |
| **Deuterocanon** | 213 + 10 emphasis | 223 |
| **New Testament** | 260 + 55 emphasis | 315 |
| **Chapters subtotal** | 1,402 + 125 emphasis | 1,527 |
| **Appendix A** | Texts and Documents | 12 |
| **Appendix B** | Tables and Data | 12 |
| **Appendix C** | Maps and Gazetteer | 8 |
| **Appendix D** | Chronology | 6 |
| **Appendix E** | Hermeneutical Essay and Further Reading | 7 |
| **Appendices subtotal** | A–E | 45 |
| **Book total** | 10 + 14 + 1,527 + 45 | 1,596 |

This is a planning allowance, not a measured length. A one-page chapter at 350–550 words plus notes is a working estimate; typeset a representative narrative chapter, a poetry chapter, a law chapter, and a table-heavy appendix before committing to the ratio. Reallocate space or compress repetition if necessary. Never shrink away evidence or footnotes to preserve a page total.

The emphasis reserve is not an entitlement. A chapter receives emphasis pages only when its brief records why: canonical weight, interpretive difficulty, or the need to cover a large unit. The reserve is currently allocated as 60 Old Testament pages, 10 Deuterocanonical pages, and 55 New Testament pages. Those numbers may change when the book is typeset, but the total must be reconciled in this table.

## Evidence and footnote conventions

The full rules are in [AGENTS.md](AGENTS.md) §4. The essentials:

- Every factual claim, quotation, linguistic judgment, and historical reconstruction is supported by a named footnote.
- All citations, explanations, textual notes, and editorial questions live in one combined footnote list at the end of each file. There is no separate Sources or References section.
- Citation notes include author or institution, title, date, edition, publisher or host, a direct URL or DOI where one exists, the date accessed, the exact locator, a **Used for:** annotation, and any limitations.
- Explanatory notes begin `Explanation —`. Textual notes begin `Text —`. Editorial questions begin `Editorial check —`. A citation note that also explains uncertainty may carry both a citation and an explanation.
- Footnote keys are descriptive and prefixed by book and chapter: `[^gen-1-creation]`, `[^psa-23-shepherd]`, `[^rom-8-spirit]`, `[^1co-13-love]`. The prefix prevents collisions when the 1,402 files are combined.
- Each file’s notes are self-contained. A reference must resolve to a definition in the same file.
- Do not use “ibid.”, numeric keys, or nested footnote references inside a definition.
- A search result, a publisher’s description, or an AI summary is a lead, not evidence. A work must be read in the edition cited before it supports a checked claim.
- The WEB text is quoted exactly. When the commentary compares a translation or reconstructs a variant, it names the edition and the witness.

### Source hierarchy

1. **Primary biblical text:** the WEB XML for the translation; BHS, the Septuagint, or NA28/UBS5 for the original languages; manuscript images or critical apparatus for variants.
2. **Primary ancient sources:** ancient Near Eastern texts, Second Temple literature, Josephus, Philo, the apostolic fathers, rabbinic literature, and early Christian writers, in identified editions and translations.
3. **Reference works:** lexicons, grammars, textual commentaries, and critical commentaries.
4. **Secondary scholarship:** monographs, articles, and edited collections, read in the edition cited.
5. **Reception and application:** sermons, liturgical texts, and devotional works, used to illustrate how communities have read the text, not to prove what it means.

### A note on original languages

The commentary may discuss Hebrew, Aramaic, and Greek, but it does not assume that the reader knows them. Give the original form in Unicode, a transliteration, and a short gloss. Cite the lexicon entry and the grammar section for a contested grammatical claim. Do not use Strong’s numbers as a substitute for a lexicon. Do not build a doctrine on a word study that ignores the word’s range and context.

### A note on criticism

The commentary is written from a Christian perspective, but it does not treat criticism as an enemy. Historical criticism can clarify the text’s setting, redaction, and reception. Literary criticism can show how a text works. Ideological criticism can expose assumptions the commentary tradition has carried. The commentary should welcome those questions and answer them with evidence, not with anxiety. It should also criticize its own tradition when the tradition has used the text to harm people.

## Visual register

The register covers every table, map, figure, photograph, facsimile, and other image in the commentary, including the Introduction and appendices. No unregistered visual may be added. A planned item may be revised or removed, but the plan and the affected references must change with it.

The one-page chapter does not carry a visual quota. A map or figure belongs to a book or a major unit, not to every chapter. The default is at least one substantive visual for each major unit: the Pentateuch, the Historical Books, the Psalms and Wisdom, the Prophets, the Gospels, Acts and the Letters, the Deuterocanon, and the Introduction and appendices. Shorter books share a unit visual or rely on an appendix map. A table appears in a chapter only when it does real analytical work.

Maps, figures, and images use separate book-wide sequences: “Map 1”, “Figure 1”, “Image 1”. Tables are numbered within their owning file: “Gen 1, Table 1”, “App. B, Table 2”. Planning IDs such as `map-01` and `app-b-table-02` are for the register, not for prose citations.

### Planned maps

| ID | Display | Title | Purpose | Owner | Source and rights plan | Status |
|---|---|---|---|---|---|---|
| **map-01** | Map 1 | The Ancient Near East and the Levant | Orient the reader in the world of Genesis–Exodus | Introduction; Gen 1–11 | Physical geography from public-domain data; ancient boundaries from a licensed atlas | `planned` |
| **map-02** | Map 2 | The Patriarchs and the Exodus | Trace the movements of Genesis 12–Exodus 15 | Gen 12–50; Exod 1–15 | Same base; route reconstructions marked as uncertain | `planned` |
| **map-03** | Map 3 | Wilderness, Conquest, and Settlement | Show the land traditions of Exodus 16–Judges | Exod 16–40; Num; Deut; Josh; Judg | Same base; tribal boundaries distinguished from later claims | `planned` |
| **map-04** | Map 4 | The United Monarchy | Situate Saul, David, and Solomon | 1 Sam–1 Kgs 11 | Same base; regnal dates marked as conventional | `planned` |
| **map-05** | Map 5 | Israel and Judah in the Assyrian Age | Show the divided kingdoms and Assyrian campaigns | 1 Kgs 12–2 Kgs 17 | Same base; campaign arrows and disputed borders labeled | `planned` |
| **map-06** | Map 6 | Judah, Babylon, and the Persian Empire | Follow the exile and return | 2 Kgs 18–Ezra–Neh | Same base; imperial provinces and roads | `planned` |
| **map-07** | Map 7 | The Hellenistic World and the Maccabees | Set the Deuterocanonical narratives in context | 1–2 Maccabees; Dan; Wis; Sir | Same base; Seleucid and Ptolemaic boundaries | `planned` |
| **map-08** | Map 8 | The Roman World in the First Century | Orient the Gospels and Acts | Gospels; Acts; Epistles | Same base; provinces, roads, and sea routes | `planned` |
| **map-09** | Map 9 | Galilee, Judea, and Samaria in the Time of Jesus | Show the immediate setting of the Gospels | Matthew–John | Same base; towns and regions with uncertain identifications marked | `planned` |
| **map-10** | Map 10 | Paul’s Missionary Journeys and the Aegean Churches | Trace the mission and the letters | Acts; Romans–Revelation | Same base; journey reconstructions labeled as reconstructions | `planned` |
| **map-11** | Map 11 | The Seven Churches of Revelation | Locate the churches of Revelation 1–3 | Revelation | Same base; Roman province of Asia | `planned` |
| **map-12** | Map 12 | Jerusalem in the Second Temple Period | Give a detailed plan of the city | Gospels; Acts; Appendix C | Archaeological plan from a public-domain or licensed source; periods distinguished | `planned` |

### Planned figures

| ID | Display | Title | Purpose | Owner | Source and rights plan | Status |
|---|---|---|---|---|---|---|
| **fig-01** | Figure 1 | The Documentary Hypothesis and Its Critics | Explain the source-critical debate without treating it as settled | Genesis–Deuteronomy | Original diagram; positions cited in notes | `planned` |
| **fig-02** | Figure 2 | The Structure of the Sinai Covenant | Show the treaty and covenant pattern | Exodus 19–24 | Original diagram from cited scholarship | `planned` |
| **fig-03** | Figure 3 | The Psalms by Genre and Book | Map the Psalter’s genres and five books | Psalms | Original chart; genre categories explained | `planned` |
| **fig-04** | Figure 4 | Prophetic Books in Historical Context | Place the prophets in their crises | Isaiah–Malachi | Original timeline; dates marked as conventional | `planned` |
| **fig-05** | Figure 5 | The Synoptic Problem | Compare the Gospels’ shared and distinct material | Matthew–Luke | Original diagram; theories named fairly | `planned` |
| **fig-06** | Figure 6 | The Structure of Romans | Show the letter’s argument | Romans | Original outline from the text | `planned` |
| **fig-07** | Figure 7 | The Christ Hymn of Philippians 2 | Display the poem’s structure and movement | Philippians | Original diagram; translation choice noted | `planned` |
| **fig-08** | Figure 8 | The Visions of Revelation | Show the sequence and recurrence of the visions | Revelation | Original diagram; interpretive options noted | `planned` |

### Planned images

| ID | Display | Title | Purpose | Owner | Source and rights plan | Status |
|---|---|---|---|---|---|---|
| **img-01** | Image 1 | A page of Codex Sinaiticus | Show a great manuscript and the material text | Introduction; Appendix A | Public-domain manuscript image; verify the host’s terms | `planned` |
| **img-02** | Image 2 | A Dead Sea Scrolls Isaiah fragment | Illustrate textual witnesses | Isaiah; Appendix A | Image from a museum or digitization project; verify terms | `planned` |
| **img-03** | Image 3 | A Roman denarius | Illustrate currency and imperial imagery | Gospels; Appendix B | Museum image with permission or public-domain status | `planned` |
| **img-04** | Image 4 | A catacomb fresco or early Christian icon | Show early Christian reading and worship | Introduction; Appendix E | Public-domain or licensed image; provenance and credit required | `planned` |

### Table register

Chapter tables are registered when a chapter brief calls for one. The appendices carry the fixed tables listed in the Appendix B plan. No table is considered produced until its data, definitions, source locators, and caption exist. Every table needs a textual reference by number, a bold leading cell in each body row, and a source line.

## File manifest and status record

### Stable paths

| File or directory | Responsibility |
|---|---|
| **`README.md`** | Canonical book plan, chapter shape, page budget, visual register, and book-level status |
| **`metadata.yaml`** | Title, author, rights, and language |
| **`AGENTS.md`** | Process, evidence standards, chapter architecture, and house style |
| **`check_book.py`** | Structural checker |
| **`convert_bible.py`** | Converter for the WEB HTML edition |
| **`bible/toc.xml`** | Authoritative list of 81 books and 1,402 chapters |
| **`bible/{ot,deut,nt}/<book>/<book>_<NNN>.xml`** | The WEB text, one file per Bible chapter |
| **`chapters/00-introduction.md`** | Introduction |
| **`chapters/{ot,deut,nt}/<book>/<NNN>-<book>-<chapter>.md`** | One commentary chapter per Bible chapter |
| **`chapters/51-appendix-a.md` … `chapters/55-appendix-e.md`** | Appendices A–E |

The three-digit prefix in a chapter file name is a zero-padded sort key; the chapter number also appears as the final segment. Examples:

- `chapters/ot/gen/001-gen-1.md`
- `chapters/ot/psa/023-psa-23.md`
- `chapters/deut/sir/051-sir-51.md`
- `chapters/nt/1co/013-1co-13.md`
- `chapters/nt/rev/022-rev-22.md`

The folder names and book codes come from `bible/toc.xml`. Do not rename a file to repair a citation. Repair the citation and the plan.

### Status vocabulary

`planned`, `seeded`, `researched`, `drafted`, `checked`, `integrated`. A substantive later change reopens the affected status. The book table above is the authoritative status record at book level. A generated `status.tsv` may record per-file status once seeding begins; it is a report, not a second plan. The checker’s manifest is the authority for which files exist.

**Last review:** November 7, 2026, for every book. **Review scope:** Stage 1 plan and manifest. **Outstanding blocker:** Stage 2 seeding. When a book moves, update its row’s stage and record the date, scope, and blocker for that change.

### Current status

No manuscript files exist yet. All 81 books are `planned`; all 1,408 manuscript files are unseeded. The next action is Stage 2: seed the Introduction, all 1,402 chapters, and Appendices A–E from this plan. Until then, the default checker run will report all 1,408 files as missing; that is the expected state of a planned repository, not a defect in the plan. Do not draft prose before seeding and without a researched brief.

The Stage 1 exit check for this plan: every Bible chapter in `bible/toc.xml` has a manifest entry; the count is 1,402; the Introduction and five appendices have entries; the page budget reconciles; every planned visual has a register entry; the chapter architecture and genre modes are stated; and the status record is honest about the absence of a draft.

## How to use this plan

1. Read [AGENTS.md](AGENTS.md) before writing.
2. Run `python3 check_book.py --list` to see the manifest, or `python3 check_book.py --book GEN` to check one book.
3. Complete the global Stage 2 seed once, then work in book units: research a book chapter by chapter, draft it, check it, then integrate it with its neighbors.
4. Update this README when scope, the chapter architecture, a visual, a page allocation, or the status of a book changes.
5. Do not create a second outline. Do not maintain a separate `outline.md`. The chapter briefs live in the chapter files; the plan lives here.
6. Do not describe a chapter as checked until every applicable item in AGENTS.md §7 has been completed and the structural checker has passed or its remaining findings are declared blockers.

The commentary is large, but the method is small: read the chapter, state what it says, set it in context, explain what is unclear, offer a Christian reading, cite the evidence, and leave the reader with the text.
