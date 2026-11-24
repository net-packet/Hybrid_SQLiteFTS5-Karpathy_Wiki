# Ingest workflow — the reference

**This is the only procedure.** Every other page that describes ingest defers to
this one; if something disagrees with this page, this page wins.

## The nine steps

| # | Step | Who does it |
|---|---|---|
| 1 | identify the topic | human or agent — **ask before assuming** |
| 2 | propose a collection, get confirmation | agent asks, user answers |
| 3 | place the file under `raw/` | `cp` — never edit it afterwards |
| 4 | `doclib.py add <raw path> -c <collection>` | one command |
| 5 | `doclib.py search` to confirm, `show` to read the chunk you will cite | two commands |
| 6 | write `wiki/sources/<slug>.md` with citations | human or agent |
| 7 | **`doclib.py add <wiki page> -c <collection>`** | one command — **do not skip** |
| 8 | register in `wiki/index.md` and `wiki/log.md` | two line edits |
| 9 | `doclib.py lint -c <collection>` | one command |

Step 7 is the one that gets forgotten. The page exists on disk and looks
finished, but until it is indexed `search` cannot find it — and `lint` does not
check searchability, only structure.

Step 1 has its own page: [Collections](Collections.md) lists what belongs in
each one. If no collection fits, **stop and ask** — do not create one on the fly.

## What each command prints

### Step 4 — `add` the raw file

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/files/contract-1405.pdf \
  -c office-works
```

```
✓ افزوده شد: contract-1405.pdf → 14 تکه (file_id=1)
```

`14 تکه` means the extractor found text. **`0` means it found none** — a scanned
PDF with no text layer. Do not install OCR; read the pages as images instead
(see the images section below).

If instead you see `قبلاً افزوده شده`, the `sha256` matched an existing row.
Nothing was duplicated — that is the dedupe working, not an error.

### Step 5 — confirm, then read

```bash
python3 ~/archive/doclib.py search "جریمه تاخیر"
```

```
2 نتیجه برای «جریمه تاخیر»:

[office-works/contract-1405.pdf — ص 3]
  ...در صورت تاخیر در پاسخ اضطراری، به ازای هر ساعت »تاخیر« ۰٫۵ درصد...
```

Note what the output carries: **which file**, **which page**, **the original
text**. That is the whole output contract.

Nothing back but step 4 succeeded? The FTS table did not receive the rows — see
[Err-FTS-Empty](../layer4/Err-FTS-Empty.md).

`search` gives you a snippet. To cite, you need the full chunk:

```bash
python3 ~/archive/doclib.py show 1
```

Prints every chunk of `file_id=1` with its page or index. **This is what you
quote from** — not the search snippet, which is truncated.

### Step 6 — write the page

`collections/office-works/wiki/sources/contract-1405.md`:

```markdown
# قرارداد نگهداشت ۱۴۰۵

**نوع:** قرارداد · **تاریخ:** ۱۴۰۵/۰۱/۰۱ · **منبع:** [contract-1405.pdf](../../raw/files/contract-1405.pdf)

## خلاصه
...

## اعداد کلیدی

| مورد | مقدار | ارجاع |
|---|---|---|
| مبلغ کل | ۴۸۰,۰۰۰,۰۰۰ ریال | ص ۱ |
| جریمه تاخیر | ۰٫۵٪ ماهانه، سقف ۱۰٪ | ص ۳ |

## نکات
...
```

Every number carries a page. **No page, no number** — that is the rule that makes
the wiki checkable six months later. The full shape, the four rules, and the
`concepts/` variant are in [Wiki-Page-Contract](Wiki-Page-Contract.md).

### Step 7 — index the wiki page too

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/wiki/sources/contract-1405.md \
  -c office-works
```

The wiki is indexed as a source like any other file — `rel_path` becomes
`wiki/sources/contract-1405.md` instead of `files/contract-1405.pdf`.

**Without this the page is invisible to `search`.** This is not optional and it
is easy to forget, because the page already exists on disk and looks finished.
It is not finished until `search` can find it.

Verify — you should now get **two** hits, the PDF and the page:

```bash
python3 ~/archive/doclib.py search "قرارداد نگهداشت"
```

### Step 8 — register it

One row in `collections/office-works/wiki/index.md`:

```markdown
| 1 | [contract-1405](sources/contract-1405) | قرارداد | 2026-11-24 |
```

A page not listed here and not linked from anywhere else is an **orphan**, and
`lint` will say so. Read the existing `index.md` first — see
[the `index.md` trap](#the-indexmd-trap) below.

One line in `collections/office-works/wiki/log.md`:

```markdown
| 2026-11-24 | ingest | contract-1405.pdf → 14 chunks |
```

### Step 9 — `lint`

```bash
python3 ~/archive/doclib.py lint -c office-works
```

Expect `✅ هیچ ایرادی پیدا نشد`. Six checks run: broken links, orphan pages,
pages missing from `index.md`, citations to a raw file that does not exist,
pages with no citation at all, and duplicate titles. See
[Wiki-Lint](Wiki-Lint.md).

`lint` checks **structure, not searchability**. A page that was never `add`ed
passes lint and is still invisible to `search`.

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

Seven steps. The header is the part people skip, and it is the part that makes
the page citable six months later.

### 1 — fetch and clean

Extract the article, then strip navigation, ads, and footers. Site-specific
noise to remove: on dev.to, every line after a `* * *` separator is an ad block.

### 2 — save to `raw/web/`

```
raw/web/YYYY-MM-DD-slug.md
```

### 3 — write the full header

```yaml
---
source: https://example.com/article
title: the actual article title
author: the actual author
published: the actual publish date
retrieved: 2026-11-24
lang: en          # or fa
---
```

All six fields. `source` is mandatory — it is the only record of where the text
came from, and **`lint` does not check it**, so an omission is silent and
permanent. The other five are what let you answer "who said this and when"
without re-fetching a page that may have changed or vanished.

### 4 — index the raw file

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/web/2026-11-24-example-article.md \
  -c office-works
```

### 5 — write the wiki page

`wiki/sources/<short-english-name>.md`. **The wiki page is written in the
language of the source** — a Persian article gets a Persian page, an English one
gets English. Do not translate; a translated citation cannot be checked against
the original by someone who reads only the original.

### 6 — index the wiki page too

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/wiki/sources/example-article.md \
  -c office-works
```

Skipping this is the most common ingest mistake: the page exists, looks
finished, and `search` cannot find it.

### 7 — register and lint

One row in `wiki/index.md`, one in `wiki/log.md`, then:

```bash
python3 ~/archive/doclib.py lint -c office-works
```

### Why the header is not optional

A web page is the only source type that can change or disappear after you saved
it. Without `retrieved` you cannot say whether you read this version or an
earlier one. Without `published` you cannot tell whether it predates the
contract it discusses.

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
| `add` a file from outside `collections/<name>/` | the CLI raises `ValueError: ... is not in the subpath of ...` — see [Err-Outside-Raw](../layer4/Err-Outside-Raw.md) |
| create a collection without asking | wrong-collection documents are worse than none |
| write a number in the wiki without a page reference | unverifiable |
| run `reindex` while another process is writing | SQLite single-writer, it will block |

## The whole thing, condensed

```bash
cp file.pdf ~/archive/collections/office-works/raw/files/
python3 ~/archive/doclib.py add ~/archive/collections/office-works/raw/files/file.pdf -c office-works
python3 ~/archive/doclib.py search "کلیدواژه"
python3 ~/archive/doclib.py show <file_id>          # read the chunk you will cite
# write wiki/sources/file.md
python3 ~/archive/doclib.py add ~/archive/collections/office-works/wiki/sources/file.md -c office-works
# update wiki/index.md and wiki/log.md
python3 ~/archive/doclib.py lint -c office-works
```

Nine steps, two of which are writing prose. The rest is one command each.

**The step everyone forgets is the second `add`.** A wiki page that is not
indexed cannot be found, and nothing warns you — `lint` checks structure, not
searchability.
