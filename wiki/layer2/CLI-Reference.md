# CLI reference — every command

`doclib.py` has 14 subcommands. All of them read `DOCLIB_ROOT`; none take a
database path.

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py <command> [args]
```

## Ingest

### `add <path> [-c COLLECTION]`

Adds a file or a directory. The path must be inside
`collections/<name>/raw/` — see [Err-Outside-Raw](../layer4/Err-Outside-Raw).

```
افزودن به «office-works» (1 فایل):
  ✓ contract-1405.pdf → 14 تکه (id=1)
تمام. 1 فایل ایندکس شد.
```

Dedupe is by `(collection, sha256)`. Re-adding the same content prints
`= از قبل هست: <name> (id=N)` and writes nothing.

`-c` is optional when the path makes the collection obvious; pass it anyway.

## Query

### `search <query> [-c COLLECTION] [-f NAME] [-n LIMIT]`

```
1 نتیجه برای «جریمه تاخیر»:

[office-works/contract-1405.pdf — ص 3]
  ...به ازای هر ساعت »تاخیر« ۰٫۵ درصد...
```

- `-c` limits to one collection
- `-f` filters by filename fragment
- `-n` caps results (default 10)

Terms are ANDed and prefix-matched. Single-character terms are dropped. See
[Query-Router](Query-Router).

### `list [-c COLLECTION]`

```
=== office-works ===
  [  1] contract-1405.pdf  (pdf, 14 تکه, 412KB, 2026-11-24)
```

A file with `0 تکه` is indexed but not searchable — [Err-Empty-Extract](../layer4/Err-Empty-Extract).

### `show <file_id>`

Prints every chunk of one file, in order, with `ص N` or `تکه N` headers. This is
what you cite from. No per-chunk flag; for one chunk use SQL:

```sql
SELECT text FROM chunks WHERE file_id = 1 AND idx = 4;
```

### `stats`

```
کل: 12 فایل، 130 تکه

  office-works               8 فایل،    96 تکه
  maintenance-learning       3 فایل،    28 تکه
  ai-learning                1 فایل،     6 تکه
```

### `collections`

Lists collections with their scope description, read from each
`COLLECTION.md`. Prints nothing when `DOCLIB_ROOT` is wrong — that is the
single most common "it's broken" report.

## Maintenance

### `rm <file_id>`

Removes the row from `files`; `ON DELETE CASCADE` removes its chunks; the
`chunks_ad` trigger removes the FTS entries. **The file in `raw/` is never
touched.**

### `reindex [-c COLLECTION]`

Deletes each file's chunks and re-extracts them from the source in `raw/`.
Use after changing `CHUNK_SIZE` or the folding maps, or after a schema rebuild.
Slower than the SQL FTS rebuild, but it also repairs `chunks` itself.

```bash
python3 doclib.py reindex -c office-works
```

## Wiki

### `lint [-c COLLECTION]`

Six structural checks: broken link, orphan page, missing from `index.md`,
citation to a missing raw file, page with no citation, duplicate title.
Exit code `1` when there are issues. See [Wiki-Lint](Wiki-Lint).

### `graph [-c COLLECTION]`

Prints in-degree and out-degree per page. In-degree 0 is an orphan; out-degree 0
is a leaf.

### `links <page> -c COLLECTION`

Both link directions for one page — run it before renaming.

```bash
python3 doclib.py links sources/contract-1405 -c office-works
```

`-c` is **required** here, unlike elsewhere.

## Living source

### `ur-new <slug> --title TITLE [-c COLLECTION] [--author] [--year] [--publisher] [--edition] [--isbn] [--lang] [--page-basis] [--started]`

Creates a book-in-progress page under `wiki/sources/User-Reading-<slug>.md`.
`--title` and `-c` are required.

### `ur-add <slug> --page N --quote TEXT [-t TOPIC] [-n NOTE] [-c COLLECTION]`

Appends one quote, with its page, to a living source. Append-only: corrections
are marked `**اصلاح:** <date>` rather than overwriting.

### `ur-list`

Lists every living source with its quote count.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success, or a search with no hits |
| 1 | bad arguments, missing file, unknown `file_id`, lint issues |

A search that finds nothing exits `0` — an empty result is not an error.
