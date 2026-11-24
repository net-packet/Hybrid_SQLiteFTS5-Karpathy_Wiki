# One file, from disk to three rows

This page follows a single PDF through the system. Every table and column
name below was read from the database, not remembered.

## Step 0 — the file on disk

```
collections/office-works/raw/files/contract-1405.pdf      (412 KB)
```

## Step 1 — a row in `files`

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
```

One row:

| column | value |
|---|---|
| `file_id` | `1` |
| `collection` | `office-works` |
| `name` | `contract-1405.pdf` |
| `rel_path` | `files/contract-1405.pdf` (relative to `raw/`) |
| `source_type` | `pdf` |
| `size` | `421888` |
| `sha256` | `9f2c…` |
| `n_chunks` | `14` |
| `added_at` | `2026-11-24 16:43:02` |

**Why `sha256`:** adding the same file twice returns the existing `file_id`
instead of duplicating it. The check is `(collection, sha256)`, so the same
document in two collections is two rows — deliberately.

**Why `UNIQUE(collection, rel_path)`:** a path is unique within a collection.
Re-adding a changed file at the same path is a conflict, not a silent overwrite.

## Step 2 — rows in `chunks`

```sql
CREATE TABLE chunks (
    file_id INTEGER NOT NULL,
    idx     INTEGER NOT NULL,
    page    INTEGER,
    text    TEXT NOT NULL,
    fts_key TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (file_id, idx),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);
```

Fourteen rows for a fourteen-chunk PDF:

| `file_id` | `idx` | `page` | `text` | `fts_key` |
|---|---|---|---|---|
| 1 | 0 | 1 | `# قرارداد نگهداشت…` | `قرارداد نگهداشت…` (folded) |
| 1 | 1 | 2 | `## تعهدات…` | `تعهدات…` |
| … | … | … | … | … |

**`page` is nullable** — DOCX and TXT have no pages, so it stays `NULL` and
citations fall back to the chunk index.

**`fts_key` is the folded form.** `text` holds what the reader sees; `fts_key`
holds the aggressively normalized version that FTS5 indexes. See
[Persian-Normalize](../layer2/Persian-Normalize.md) for why these are two columns and not one.

**`PRIMARY KEY (file_id, idx)`** — chunk order is part of the identity. Two
chunks with the same index cannot exist for one file.

**`ON DELETE CASCADE`** — deleting the `files` row deletes its chunks, because
`PRAGMA foreign_keys = ON` is set on every connection.

## Step 3 — rows in `chunks_fts`

```sql
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    fts_key,
    content='chunks',
    content_rowid='rowid',
    tokenize="unicode61 remove_diacritics 2"
);
```

This is an **external-content** FTS5 table: it stores no copy of the text, only
the inverted index. `content='chunks'` tells it where the text lives;
`content_rowid='rowid'` tells it which column identifies a row.

Because it holds no text of its own, it must be kept in sync by triggers —
`chunks_ai`, `chunks_ad`, `chunks_au` — defined in `src/schema.sql`. Insert a
chunk and `chunks_ai` inserts into `chunks_fts`; delete one and `chunks_ad`
issues the FTS5 `'delete'` command. **Bypass the triggers (write to `chunks`
with triggers dropped, or edit `index.db` by hand) and the index silently
diverges from the text.**

## The whole picture

```
contract-1405.pdf
      │  sha256, size, path
      ▼
files ──── 1 row
      │  file_id
      ▼
chunks ─── 14 rows (text + fts_key + page)
      │  rowid
      ▼
chunks_fts ── inverted index only, no text copy
```

Search reads `chunks_fts`, joins back to `chunks` for the original `text`, and
to `files` for the name. Three tables, one answer.
