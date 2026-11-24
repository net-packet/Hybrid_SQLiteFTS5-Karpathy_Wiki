# Your first ingest, step by step

One file, start to finish, with the real output at each step. This is the
sequence to follow the first time; after that, [Ingest-Workflow](Ingest-Workflow.md)
is the reference.

## Step 0 — decide the collection

Before touching anything, answer: **which collection does this belong to?**

| Collection | Belongs here |
|---|---|
| `office-works` | contracts, letters, circulars, budgets, minutes |
| `maintenance-learning` | equipment procedures, troubleshooting, standards, training |
| `ai-learning` | models, tools, papers, prompts, project-management AI use |

If none fits, stop and ask. Do not create a collection on the fly — a document
in the wrong collection is worse than an unindexed document.

## Step 1 — put the file in `raw/`

```bash
cp ~/Downloads/contract-1405.pdf \
   ~/archive/collections/office-works/raw/files/
```

`raw/files/` for documents, `raw/web/` for saved pages, `raw/audio/` for
recordings, `raw/images/` for screenshots.

`doclib.py add` accepts any path inside `collections/<name>/` — `raw/` for
sources, and `wiki/` for the pages you write in step 6. A path outside the
collection raises `ValueError` (see [Err-Outside-Raw](../layer4/Err-Outside-Raw.md)).

## Step 2 — add it to the index

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/files/contract-1405.pdf \
  -c office-works
```

Output:

```
✓ افزوده شد: contract-1405.pdf → 14 تکه (file_id=1)
```

If instead you see `قبلاً افزوده شده` (already added), the `sha256` matched an
existing row. Nothing was duplicated; that is the dedupe working.

## Step 3 — confirm it is searchable

```bash
python3 ~/archive/doclib.py search "جریمه تاخیر"
```

```
2 نتیجه برای «جریمه تاخیر»:

[office-works/contract-1405.pdf — ص 3]
  ...در صورت تاخیر در پاسخ اضطراری، به ازای هر ساعت »تاخیر« ۰٫۵ درصد...
```

If this returns nothing but step 2 succeeded, the FTS index did not receive the
rows — see [Err-FTS-Empty](../layer4/Err-FTS-Empty.md).

## Step 4 — read a chunk in full

```bash
python3 ~/archive/doclib.py show 1
```

Prints every chunk with its page or index. This is what you cite from.

## Step 5 — write the wiki page

```
collections/office-works/wiki/sources/contract-1405.md
```

Minimum shape:

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

Every number carries a page. No page, no number — that is the rule that makes
the wiki checkable six months later.

## Step 6 — index the wiki page too

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/wiki/sources/contract-1405.md \
  -c office-works
```

**Without this the page is invisible to `search`.** The wiki is indexed as a
source like any other file — `rel_path` becomes `wiki/sources/contract-1405.md`
instead of `files/contract-1405.pdf`.

This is not optional and it is easy to forget, because the page already exists
on disk and looks finished. It is not finished until `search` can find it.

Verify:

```bash
python3 ~/archive/doclib.py search "قرارداد نگهداشت"
```

You should now get **two** hits: the original PDF and the wiki page.

## Step 7 — register it in `index.md`

Add one row to `collections/office-works/wiki/index.md`:

```markdown
| 1 | [contract-1405](sources/contract-1405) | قرارداد | 2026-11-24 |
```

A page not listed here and not linked from anywhere else is an **orphan**, and
`lint` will say so.

## Step 8 — log it

Append to `collections/office-works/wiki/log.md`:

```markdown
| 2026-11-24 | ingest | contract-1405.pdf → 14 chunks |
```

## Step 9 — lint

```bash
python3 ~/archive/doclib.py lint -c office-works
```

Expect `بدون مشکل` (no issues). Six checks run: broken links, orphan pages,
pages missing from `index.md`, citations to missing raw files, pages with no
citation at all, and duplicate titles. See [Wiki-Lint](Wiki-Lint.md).

## The whole thing, condensed

```bash
cp file.pdf ~/archive/collections/office-works/raw/files/
python3 ~/archive/doclib.py add ~/archive/collections/office-works/raw/files/file.pdf -c office-works
python3 ~/archive/doclib.py search "کلیدواژه"
# write wiki/sources/file.md
python3 ~/archive/doclib.py add ~/archive/collections/office-works/wiki/sources/file.md -c office-works
# update wiki/index.md and wiki/log.md
python3 ~/archive/doclib.py lint -c office-works
```

Nine steps, two of which are writing prose. The rest is one command each.

**The step everyone forgets is the second `add`.** A wiki page that is not
indexed cannot be found, and nothing warns you — `lint` checks structure, not
searchability.
