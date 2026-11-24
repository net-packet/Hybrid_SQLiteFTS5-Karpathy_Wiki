# Ingest workflow — the reference

[First-Ingest](First-Ingest.md) walks one file. This page is the full procedure,
including the four non-document source types.

## The eight steps

| # | Step | Who does it |
|---|---|---|
| 1 | identify the topic | human or agent — **ask before assuming** |
| 2 | propose a collection, get confirmation | agent asks, user answers |
| 3 | place the file under `raw/` | `cp` — never edit it afterwards |
| 4 | `doclib.py add <path> -c <collection>` | one command |
| 5 | `doclib.py search "<keyword>"` to confirm | one command |
| 6 | write `wiki/sources/<slug>.md` with citations | human or agent |
| 7 | register in `wiki/index.md` and `wiki/log.md` | two line edits |
| 8 | `doclib.py lint -c <collection>` | one command |

Step 2 is not optional. A document in the wrong collection is worse than an
unindexed document, because it will be found in the wrong context later.

## Documents — PDF, DOCX, XLSX, PPTX, TXT, MD, CSV

```bash
cp file.pdf ~/archive/collections/office-works/raw/files/
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/files/file.pdf -c office-works
```

| Type | Extractor | `page` holds |
|---|---|---|
| PDF | `pypdf` | page number |
| DOCX | `python-docx` | `NULL` |
| XLSX | `openpyxl` | sheet index |
| PPTX | `python-pptx` | slide number |
| TXT / MD / CSV | plain read | `NULL` |

**Scanned PDF:** `pypdf` returns no text. `n_chunks` will be `0`. Do not install
an OCR engine — read the pages as images instead (next section).

## Images and screenshots

There is no local OCR. The model reads the image and the reading is stored as a
markdown sidecar beside it:

```
raw/images/screenshot-1405-08-20.png          the original
raw/images/screenshot-1405-08-20.md           what the model read
```

The sidecar starts with a `source:` header pointing at the image, then the
transcribed content. `doclib.py add` indexes the `.md`, not the `.png` — so the
image stays untouched and the text is searchable.

Why this way: OCR engines fail on Persian handwriting and on charts, and add a
heavy dependency. A vision model handles both, and the sidecar records exactly
what was read, which is auditable.

## Audio and voice

Groq Whisper, because it handles Persian well and is fast.

```bash
# 1. transcribe (the tool does this; the transcript lands beside the audio)
raw/audio/voice-1405-08-20.m4a
raw/audio/voice-1405-08-20.transcript.md

# 2. index the transcript
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/audio/voice-1405-08-20.transcript.md \
  -c office-works
```

**The 25 MB limit.** Groq rejects files over 25 MB. Split first:

```bash
ffmpeg -i long.m4a -f segment -segment_time 600 -c copy part-%03d.m4a
```

Then transcribe each part and concatenate in order. `setup.py` reports whether
`ffmpeg` is present for exactly this reason.

**The `403 error 1010` trap.** Groq returns this when the request carries a
user-agent it does not like, not when the key is wrong. Retrying with a plain
`curl` user-agent fixes it. See [Err-Groq-403](../layer4/Err-Groq-403.md).

## Web pages and blog posts

Save the page as markdown with a `source:` header, then index it:

```markdown
---
source: https://example.com/article
retrieved: 2026-11-24
title: عنوان مقاله
---

# عنوان مقاله

متن...
```

```
raw/web/example-article.md
```

The `source:` line matters: it is the only record of where the text came from,
and `lint` does not check it — so an omission is silent. Always include it.

## The `index.md` trap

Each collection's `wiki/index.md` has a **different column layout**. There is no
shared template. If you generate a row with the wrong number of columns, the
table renders broken and `lint` will not catch it.

Read the existing `index.md` before appending. Copy the header row, then add one
row with the same number of pipes.

## What never to do

| Never | Because |
|---|---|
| edit a file after it is in `raw/` | citations point at text that no longer exists |
| `add` a file from outside `collections/<name>/raw/` | the CLI raises `ValueError: ... is not in the subpath of ...` — see [Err-Outside-Raw](../layer4/Err-Outside-Raw.md) |
| create a collection without asking | wrong-collection documents are worse than none |
| write a number in the wiki without a page reference | unverifiable |
| run `reindex` while another process is writing | SQLite single-writer, it will block |
