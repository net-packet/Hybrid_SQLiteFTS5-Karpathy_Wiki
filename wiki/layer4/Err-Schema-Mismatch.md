# `VERIFY: FAIL` on `schema`

```
  verify:
    PASS  collections
    FAIL  schema       tables ok=True, user_version=0
```

## What the check does

`setup.py --verify` opens `index.db` and asserts two things:

1. the tables `files`, `chunks`, `chunks_fts` all exist
2. `PRAGMA user_version` equals `100` (the `schema_version` in `setup.toml`)

`user_version` is a free integer SQLite stores in the database header. It is
used here as a schema generation marker — nothing reads it at runtime, but it
makes "which version created this database" answerable without guessing.

## The two failure shapes

### `tables ok=False`

A table is missing. Either `index.db` was never created (check it exists at
all), or it was created by something other than `doclib.py`.

```bash
ls -l ~/archive/index.db
sqlite3 ~/archive/index.db "select name from sqlite_master where type='table';"
```

### `tables ok=True, user_version=0`

The tables are there but the version was never stamped — the database was
created by `doclib.py` directly (which creates tables but does not stamp the
version) rather than through `setup.py`.

This is harmless in practice: the schema is correct, only the marker is absent.
Fix it without touching data:

```bash
sqlite3 ~/archive/index.db "PRAGMA user_version = 100;"
python3 src/setup.py --root ~/archive --skip-install --verify
```

## When the schema genuinely differs

If `user_version` is some other non-zero number, the database came from a
different version of this project. Two options:

**Rebuild** — safe, because `index.db` is disposable:

```bash
mv ~/archive/index.db ~/archive/index.db.old
python3 src/setup.py --root ~/archive --skip-install      # creates a fresh one
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py reindex                        # re-extract from raw/
```

`reindex` reads the `files` table — which is gone in a fresh database. So
rebuild in the other order:

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py reindex    # on the OLD db, to confirm raw/ is intact
mv ~/archive/index.db ~/archive/index.db.old
python3 src/setup.py --root ~/archive --skip-install
# then re-add every file from raw/ — see below
```

**Or migrate** — only if you know what changed. Compare `src/schema.sql` against
the live schema:

```bash
sqlite3 ~/archive/index.db ".schema" > /tmp/live.sql
diff /tmp/live.sql src/schema.sql
```

## Re-adding everything after a rebuild

There is no `add-all` command. This is the loop:

```bash
export DOCLIB_ROOT=~/archive
find ~/archive/collections/*/raw -type f \( -name '*.pdf' -o -name '*.docx' \
  -o -name '*.xlsx' -o -name '*.pptx' -o -name '*.txt' -o -name '*.md' -o -name '*.csv' \) \
  -print0 | while IFS= read -r -d '' f; do
    coll=$(echo "$f" | sed -E 's|.*/collections/([^/]+)/raw/.*|\1|')
    python3 ~/archive/doclib.py add "$f" -c "$coll"
done
```

`file_id` values will differ from before. **Citations written as "chunk 7" may
no longer point at the same text** — this is why the wiki contract says to cite
pages for paginated sources.

## Why `user_version` and not a `meta` table

A `meta` table can be dropped, renamed, or shadowed by a user table. `PRAGMA
user_version` lives in the database header, survives `VACUUM`, and cannot be
confused with content.
