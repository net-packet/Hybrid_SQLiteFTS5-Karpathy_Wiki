# `files` — one row per document

```sql
CREATE TABLE files (
    file_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    collection  TEXT NOT NULL,
    name        TEXT NOT NULL,
    rel_path    TEXT NOT NULL,
    source_type TEXT NOT NULL,
    size        INTEGER,
    sha256      TEXT,
    n_chunks    INTEGER DEFAULT 0,
    added_at    TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(collection, rel_path)
);
CREATE INDEX idx_files_coll ON files(collection);
```

## Column by column

| Column | Meaning | Why it exists |
|---|---|---|
| `file_id` | integer identity | every chunk points here; stable across renames |
| `collection` | `office-works`, `maintenance-learning`, … | collections are separate universes |
| `name` | `contract-1405.pdf` | display only, never used for lookup |
| `rel_path` | `files/contract-1405.pdf` | path **relative to `raw/`** — survives moving the archive |
| `source_type` | `pdf`, `docx`, `xlsx`, `pptx`, `txt`, `md`, `csv`, `web`, `audio`, `image` | decides which extractor ran |
| `size` | bytes | sanity check: 0 bytes means extraction will fail |
| `sha256` | content hash | dedupe key |
| `n_chunks` | count | avoids `COUNT(*)` on every listing |
| `added_at` | UTC timestamp | ordering, and "what did I add last week" |

## The two constraints that matter

**`UNIQUE(collection, rel_path)`** — a path is unique *within* a collection.
Adding a different file at the same path is a conflict. `doclib.py add`
reports it rather than silently overwriting, because silently overwriting
`raw/` breaks every citation pointing at that page.

**`sha256` is not unique in the schema, but `add` checks it.** The check is
`(collection, sha256)`: the same PDF in `office-works` and in
`maintenance-learning` is two rows with two `file_id`s. That is correct —
the same document can be evidence in two different arguments.

## Queries you will actually run

```sql
-- everything in one collection, newest first
SELECT file_id, name, n_chunks, added_at
FROM files WHERE collection = 'office-works'
ORDER BY added_at DESC;

-- files whose extraction produced nothing
SELECT file_id, name, source_type FROM files WHERE n_chunks = 0;

-- duplicate content in one collection
SELECT collection, sha256, COUNT(*) c
FROM files GROUP BY collection, sha256 HAVING c > 1;

-- total size per collection
SELECT collection, COUNT(*) files, SUM(size)/1048576 AS mb
FROM files GROUP BY collection;
```

## Deleting a file

```bash
python3 doclib.py rm <file_id>
```

Deletes the `files` row; `ON DELETE CASCADE` removes its chunks; the `chunks_ad`
trigger removes the FTS entries. **The file in `raw/` is not touched** — that is
intentional, and why `rm` is safe to run by mistake.

## What `n_chunks = 0` means

Extraction produced no text. Causes, in order of likelihood:

1. Scanned PDF with no text layer → read it as an image instead
2. Password-protected DOCX → decrypt first
3. XLSX with only formulas and no cached values → open and save once
4. Empty file → check `size`

See [Err-Empty-Extract](../layer4/Err-Empty-Extract.md).
