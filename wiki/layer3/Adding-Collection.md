# Adding a fourth collection

Collections are directories, not configuration. `doclib.py collections` reads
the filesystem, so a copied directory appears immediately — no restart, no
migration.

## The four steps

### 1 — copy an existing collection

```bash
cd ~/archive/collections
cp -r office-works contracts-1405
```

### 2 — empty it

```bash
cd contracts-1405
rm -rf raw/files/* raw/web/* raw/audio/* raw/images/*
rm -f wiki/sources/*.md wiki/entities/*.md wiki/concepts/*.md
```

Keep the directories. `add` expects `raw/files/` to exist.

### 3 — rewrite the scope statement

`COLLECTION.md` is what `doclib.py collections` prints. If it still describes
office works, the next person will file documents in the wrong place.

```markdown
# contracts-1405

قراردادهای سال ۱۴۰۵ و الحاقیه‌های آنها.

## در این مجموعه چه چیزی هست
- قرارداد اصلی و الحاقیه‌ها
- صورت‌جلسات تحویل
- ضمانت‌نامه‌ها

## چه چیزی نیست
- مکاتبات عمومی → office-works
- رویه‌های فنی → maintenance-learning
```

### 4 — reset the wiki skeleton

`wiki/index.md` and `wiki/log.md` still hold the old collection's rows. Empty
them but keep the headers — **each collection's `index.md` has its own column
layout, and there is no shared template.** Copy the header from the file you
just emptied, not from another collection.

```bash
: > wiki/log.md && printf '# Log\n\n| Date | Action | Detail |\n|---|---|---|\n' > wiki/log.md
```

### 5 — record it in `setup.toml`

So a future re-install creates it too:

```toml
[collections]
default = ["office-works", "maintenance-learning", "ai-learning", "contracts-1405"]
```

Without this, the collection works today and disappears the next time someone
bootstraps a fresh archive from the repo.

## Verify

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py collections      # the new one is listed
python3 ~/archive/doclib.py stats            # it appears with 0 files
```

Then ingest one file into it to prove the path works end to end:

```bash
cp test.pdf ~/archive/collections/contracts-1405/raw/files/
python3 ~/archive/doclib.py add \
  ~/archive/collections/contracts-1405/raw/files/test.pdf -c contracts-1405
python3 ~/archive/doclib.py search "تست" -c contracts-1405
```

## What not to do

| Don't | Because |
|---|---|
| create a collection without asking the user | the boundary is a judgement call, not a technical one |
| copy `index.db` rows between collections | `file_id` is global; `rel_path` is per-collection; the combination breaks |
| rename a collection directory | every `files.collection` value becomes stale; there is no rename command |
| share a `raw/` directory between two collections | dedupe is per-collection, so the same file in two collections is two rows — deliberate, but only when you meant it |

## Why there is no `collection add` command

Because the interesting part is the scope statement, not the directory copy.
A command would create the structure and let you skip the part that decides
whether the collection should exist.
