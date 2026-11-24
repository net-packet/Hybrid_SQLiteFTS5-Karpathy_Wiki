# `index.db` will not open

```
sqlite3.DatabaseError: file is not a database
sqlite3.OperationalError: database disk image is malformed
```

## First: is it actually corrupt?

```bash
sqlite3 ~/archive/index.db "pragma integrity_check;"
```

| Output | Meaning |
|---|---|
| `ok` | not corrupt — the problem is elsewhere, check `DOCLIB_ROOT` |
| `*** in database main ***` lines | genuinely corrupt |
| `file is not a database` | not a SQLite file at all (wrong path? a git LFS pointer? empty?) |

Check the file is a real database and not a 0-byte placeholder:

```bash
ls -l ~/archive/index.db
file ~/archive/index.db          # expect "SQLite 3.x database"
head -c 16 ~/archive/index.db    # expect "SQLite format 3"
```

## Cause

In order of likelihood:

1. **Two writers at once.** SQLite is single-writer. Two `doclib.py add` runs in
   parallel, or an `add` during a `reindex`, can leave a hot journal that a
   later reader misreads.
2. **The filesystem lied about fsync.** A container or network mount that
   acknowledges writes it has not flushed. Common on some overlay filesystems.
3. **Copied mid-write.** `cp index.db` while a write was in flight.
4. **Disk full** during a commit.

## Fix — and this is the good news

`index.db` holds **no unique information**. Every byte came from `raw/`. So
corruption is an inconvenience, not a loss.

```bash
export DOCLIB_ROOT=~/archive
mv ~/archive/index.db ~/archive/index.db.corrupt
python3 src/setup.py --root ~/archive --skip-install      # fresh empty db
find ~/archive/collections/*/raw -type f \( -name '*.pdf' -o -name '*.docx' \
  -o -name '*.xlsx' -o -name '*.pptx' -o -name '*.txt' -o -name '*.md' -o -name '*.csv' \) \
  -print0 | while IFS= read -r -d '' f; do
    coll=$(echo "$f" | sed -E 's|.*/collections/([^/]+)/raw/.*|\1|')
    python3 ~/archive/doclib.py add "$f" -c "$coll"
done
```

Time: proportional to the corpus, typically under a minute for a few hundred
files. **The wiki is untouched** — only `file_id` values change.

## Try recovery before rebuilding

If the corpus is large, attempt a dump first:

```bash
sqlite3 ~/archive/index.db ".recover" | sqlite3 ~/archive/recovered.db
```

`.recover` is more aggressive than `.dump` and works on partially damaged files.
Then check:

```bash
sqlite3 ~/archive/recovered.db "pragma integrity_check;"
sqlite3 ~/archive/recovered.db "select count(*) from files;"
```

If `files` and `chunks` are intact but `chunks_fts` is not, you do not need the
recovered file at all — rebuild the index in place:

```bash
sqlite3 ~/archive/index.db "INSERT INTO chunks_fts(chunks_fts) VALUES('rebuild');"
```

## Preventing it

| Habit | Why |
|---|---|
| never run two `add`s in parallel | single-writer |
| `cp index.db` only when nothing is running | avoid mid-write copies |
| keep `raw/` on a local disk | network mounts and fsync do not mix |
| back up `raw/`, not `index.db` | the index is derived; the raw files are not |

That last row is the whole design in one line. Back up `raw/` and `wiki/`.
Never bother backing up `index.db`.

## If `raw/` is also gone

Then there is nothing to rebuild from. That is the one unrecoverable failure,
and it is why `raw/` is the only layer that needs a real backup. See
[Three-Layers](../layer1/Three-Layers.md).
