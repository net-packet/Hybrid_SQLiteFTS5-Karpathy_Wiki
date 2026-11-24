# `chunks_fts` — the inverted index

```sql
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    fts_key,
    content='chunks',
    content_rowid='rowid',
    tokenize="unicode61 remove_diacritics 2"
);
```

## What `content='chunks'` means

This is an **external-content** FTS5 table. It stores no copy of the text —
only the inverted index (token → rowid list). The text stays in `chunks`.

Two consequences:

1. **It cannot drift silently into being a second source of truth.** There is
   nothing to read from it but the index.
2. **It must be kept in sync by triggers.** FTS5 does not watch `chunks`.

## The three triggers

```sql
CREATE TRIGGER chunks_ai AFTER INSERT ON chunks BEGIN
    INSERT INTO chunks_fts(rowid, fts_key) VALUES (new.rowid, new.fts_key);
END;

CREATE TRIGGER chunks_ad AFTER DELETE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, fts_key)
    VALUES ('delete', old.rowid, old.fts_key);
END;

CREATE TRIGGER chunks_au AFTER UPDATE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, fts_key)
    VALUES ('delete', old.rowid, old.fts_key);
    INSERT INTO chunks_fts(rowid, fts_key) VALUES (new.rowid, new.fts_key);
END;
```

The delete form is FTS5's special syntax: you pass the **old** values so the
index can locate and remove the right entries. Passing only `rowid` is not
enough — FTS5 needs the tokens to know what to unindex.

## The tokenizer

`unicode61 remove_diacritics 2`:

- `unicode61` splits on Unicode word boundaries — works for Persian, unlike
  the default ASCII tokenizer
- `remove_diacritics 2` strips Arabic diacritics (fatha, kasra, shadda…) so
  vocalized and unvocalized text match

It does **not** fold `ی`/`ي`, `ک`/`ك`, or `آ`/`ا`. That folding happens in
Python before the text reaches FTS5 — see [Persian-Normalize](Persian-Normalize.md).

## The shadow tables

`chunks_fts_data`, `chunks_fts_idx`, `chunks_fts_docsize`, `chunks_fts_config`
are created by SQLite. **Never write to them.** They are the physical index;
touching them corrupts it in ways that do not raise an error until much later.

## When the index diverges

Symptom: `files` has rows, `chunks` has rows, `search` returns nothing.

Cause: rows were written to `chunks` with triggers absent — typically because
the database was created before `schema.sql` had them, or because someone
inserted with `PRAGMA recursive_triggers` off and a bulk tool.

Fix — there is no separate repair command, and this is deliberate. `reindex`
deletes each file's chunks and re-extracts them, and because it goes through
`chunks`, the triggers fire and the FTS index follows:

```bash
python3 doclib.py reindex              # every collection
python3 doclib.py reindex -c office-works
```

If the index is so far gone that `reindex` cannot fix it, use FTS5's own
rebuild, which re-reads every row of `chunks` and reconstructs the index:

```sql
INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild');
```

Both are idempotent. `reindex` is slower (it re-extracts from the source file)
but also repairs `chunks` itself; the SQL rebuild only touches the index.

## Checking integrity

```sql
INSERT INTO chunks_fts(chunks_fts) VALUES('integrity-check');
```

Raises an error if the index does not match the content table, silent
otherwise. Run it after any manual database work.

## Why not `content=''` (contentless)

A contentless FTS5 table stores even less, but then `snippet()` and
`highlight()` are unavailable and you must keep the text yourself anyway. Since
`chunks.text` must exist regardless, external-content is the right choice: one
copy of the text, full FTS5 features.
