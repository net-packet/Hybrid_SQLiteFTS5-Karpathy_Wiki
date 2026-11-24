# AGENTS.md — read this first

A hybrid document archive: immutable `raw/` files, a rebuildable SQLite FTS5
index, and a markdown wiki that cites its sources. Persian and English both
work, including Persian text search.

## Install

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

The last line of output must be:

```
VERIFY: PASS
```

If it is not, the install failed — do not report success. Read
`wiki/layer4/Debug-Playbook.md`, fix, and run `--verify` again.

## What `--verify` checks

| Check | Expectation |
|---|---|
| `collections` | the three collections from `setup.toml` exist |
| `schema` | `index.db` has `files`, `chunks`, `chunks_fts`; `user_version = 100` |
| `add` | one seed file indexes; `files` table has ≥ 1 row |
| `search` | `search "قرارداد"` returns a hit |
| `lint` | no structural errors |

## After install

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py add <path-inside-raw/> -c <collection>
python3 ~/archive/doclib.py search "query"
python3 ~/archive/doclib.py show <file_id>
```

A file must live under `collections/<name>/raw/` before `add` accepts it.

## Where to look when something breaks

| Symptom | Read |
|---|---|
| `VERIFY: FAIL` on `schema` | `wiki/layer4/Err-Schema-Mismatch.md` |
| search returns nothing but files exist | `wiki/layer4/Err-FTS-Empty.md` |
| a Persian word is not found | `wiki/layer4/Err-Persian-Search.md` |
| `index.db` will not open | `wiki/layer4/Err-Corrupt-DB.md` |
| Groq returns `403 error 1010` | `wiki/layer4/Err-Groq-403.md` |
| nothing above fits | `wiki/layer4/Debug-Playbook.md` |

## Hard rules

1. **Never modify anything under `raw/`.** It is the source of truth.
2. **Never add a file without the user's confirmation** — propose a collection, wait.
3. **Every number in the wiki needs a citation** (file + page). No citation, no number.
4. **`index.db` is disposable.** If in doubt, delete it and re-add from `raw/`.

## What this is not

Not Elasticsearch. Not multi-user. No embeddings, no local OCR, no GUI, no
automatic translation. See `wiki/layer1/Non-Goals.md` before adding a feature
that assumes otherwise.
