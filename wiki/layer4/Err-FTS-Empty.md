# `chunks` has rows but `search` returns nothing

The most common real failure. `files` and `chunks` are populated; FTS5 finds
nothing.

## Diagnose

```bash
sqlite3 ~/archive/index.db "select count(*) from files;"      -- e.g. 12
sqlite3 ~/archive/index.db "select count(*) from chunks;"     -- e.g. 130
sqlite3 ~/archive/index.db "select count(*) from chunks_fts;" -- 0   ← the fault
```

Also check that the triggers exist:

```bash
sqlite3 ~/archive/index.db "select name from sqlite_master where type='trigger';"
```

Expected: `chunks_ai`, `chunks_ad`, `chunks_au`. If they are missing, every
insert into `chunks` since they went missing is absent from the index.

## Cause

`chunks_fts` is an **external-content** FTS5 table. It stores no text — only the
inverted index. Nothing copies rows into it except the three triggers. If a row
reaches `chunks` without a trigger firing, the text and the index diverge
silently: no error, no warning, search just returns nothing.

Real ways this happens:

1. The database was created by an older version of `doclib.py` before the
   triggers existed, then rows were added.
2. A bulk import wrote to `chunks` with `PRAGMA recursive_triggers = OFF`.
3. Someone restored an old `chunks` table into a newer database.
4. `index.db` was copied from another machine mid-write.

## Fix

First try the cheap repair — FTS5 rebuilds its index from the content table:

```bash
sqlite3 ~/archive/index.db "INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild');"
```

Then:

```bash
sqlite3 ~/archive/index.db "select count(*) from chunks_fts;"
python3 doclib.py search "قرارداد"
```

If that worked, stop. If the triggers were the cause, `reindex` also re-creates
them through the schema — but `reindex` re-extracts from the source files, which
is slower:

```bash
python3 doclib.py reindex -c office-works
```

## Verify the fix held

```bash
sqlite3 ~/archive/index.db "INSERT INTO chunks_fts(chunks_fts) VALUES('integrity-check');"
```

Silent means consistent; an error means the index still does not match.

## Prevent it

- Never write to `chunks` by hand. Use `doclib.py add`.
- After restoring a database from a backup, run the integrity check.
- `setup.py --verify` catches this: its `search` check fails when
  `chunks_fts` is empty while `chunks` is not.

## Why not use a contentless FTS5 table

A contentless table has the same trigger requirement and loses `snippet()` and
`highlight()`. External-content was chosen so the text lives exactly once, in
`chunks.text`, and the index can always be rebuilt from it — which is what
saves you here.
