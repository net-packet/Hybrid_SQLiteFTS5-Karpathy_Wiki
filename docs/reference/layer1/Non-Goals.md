# Non-goals — what this system deliberately is not

Read this before adding a feature. Most "obvious improvements" are on this
list for a reason, and adding them changes the design rather than extending it.

## Not a search engine

No relevance tuning, no ranking model, no faceting, no query language beyond
FTS5 syntax. It answers "which chunks contain these words" and stops there.
If you need ranking, this is the wrong tool.

## Not multi-user

SQLite is single-writer. Two processes adding files at the same time will
block, and a long `reindex` locks the database. There is no user model, no
permissions, no audit log of who read what.

## No embeddings, no vector search, no RAG

Search is lexical (FTS5 with Persian folding). A synonym that does not share
letters will not be found. `تأخیر` matches `تاخیر` because of folding; `جریمه`
does not match `penalty`.

This is a deliberate trade: lexical search is explainable. You can point at
the exact token that matched. A vector result cannot be audited the same way,
and this system's whole premise is auditable answers.

## No local OCR

Images are read by the model itself, and the reading is written to a `.md`
sidecar beside the image. There is no Tesseract, no PaddleOCR, no local
vision model. This keeps the install to four pip packages.

Consequence: a scanned PDF with no text layer yields empty chunks. The fix is
to read it as an image, not to install an OCR engine.

## No automatic translation

The wiki is written in the language of its source. A Persian source gets a
Persian page. There is no translation step, and no bilingual page generated
from one source.

## No GUI

`doclib.py` is a CLI. There is no web UI, no desktop app, no editor. The wiki
is edited in a text editor.

## No automatic wiki generation

`ur-new` and `ur-add` generate a page for a living source, mechanically, from
the quotes you give them. Nothing else is generated. The rest of the wiki is
written by a human or an agent who read the source.

This is the Karpathy part: the wiki is an interpretation, and an interpretation
that writes itself is just another index.

## Not a sync tool

There is no daemon watching `raw/` for changes, and no automatic reindex. If
you add a file by copying it into `raw/` without running `doclib.py add`, it
will not be searchable. `reindex` exists for the case where you did this a lot.

## What *is* in scope

- Ingest from PDF, DOCX, XLSX, PPTX, TXT, MD, CSV
- Ingest from web pages (saved as markdown, with a `source:` header)
- Ingest from audio (Groq Whisper, transcript stored as a sidecar)
- Ingest from images (model reads, text stored as a sidecar)
- Persian + English text, with Persian orthographic folding
- Chunk-level citations back to file and page
- Structural lint over the wiki
- A living source that grows by append (a book you are reading)
