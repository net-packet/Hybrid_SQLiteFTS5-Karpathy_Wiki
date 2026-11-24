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
python3 ~/archive/doclib.py collections                    # what exists
python3 ~/archive/doclib.py add <path-inside-raw/> -c <collection>
python3 ~/archive/doclib.py search "query"
python3 ~/archive/doclib.py show <file_id>                 # full text to cite from
python3 ~/archive/doclib.py lint -c <collection>           # after writing a page
```

`collections` printing nothing means `DOCLIB_ROOT` is wrong — check that before
anything else.

`add` accepts any path inside `collections/<name>/` — `raw/` for sources, and
`wiki/` for the pages you write. **Index the wiki page too**, or `search` cannot
find it.

## Diagnosing before you fix

```bash
python3 ~/archive/doclib.py stats
```

Three numbers: files, chunks, and the per-collection split. If `files` has rows
but `search` returns nothing, the FTS index is out of sync — that is
`wiki/layer4/Err-FTS-Empty.md`, not a broken install.

## Where to look when something breaks

| Symptom | Read |
|---|---|
| `VERIFY: FAIL` on `schema` | `wiki/layer4/Err-Schema-Mismatch.md` |
| search returns nothing but files exist | `wiki/layer4/Err-FTS-Empty.md` |
| a Persian word is not found | `wiki/layer4/Err-Persian-Search.md` |
| `index.db` will not open | `wiki/layer4/Err-Corrupt-DB.md` |
| Groq returns `403 error 1010` | `wiki/layer4/Err-Groq-403.md` |
| nothing above fits | `wiki/layer4/Debug-Playbook.md` |

## The skill and the references

`SKILL.md` sits in the archive root. It is the full operating procedure — the
eight-step ingest, the two query paths, the wiki page contract, the Groq
pitfalls, the living-source rules. **Read it before your first ingest.**

```bash
cat $DOCLIB_ROOT/SKILL.md
```

`references/` holds nine deeper files. `SKILL.md` wins on any conflict.

| Need | File |
|---|---|
| ingest detail per source type | `references/ingest-procedures.md` |
| which collection a document belongs to | `references/collection-scope.md` |
| the wiki page contract, with a full example | `references/wiki-page-contract.md` |
| a book the user is reading (grows over time) | `references/living-source.md` |
| point query vs analytical query | `references/dual-path-query.md` |
| Persian folding and FTS5 behaviour | `references/persian-normalization.md` |
| what `lint` checks, and what it cannot | `references/wiki-lint.md` |
| installing a fresh archive | `references/bootstrap.md` |
| packaging this as a portable repo | `references/portability-design.md` |

`SKILL.md` reads its root from `DOCLIB_ROOT` — no path is hardcoded, so it works
wherever the archive was installed.

## Hard rules

The full list — nine rules — is in `SKILL.md` under "Hard Rules". These four are
the ones that matter in every session:

1. **Never modify anything under `raw/`.** It is the source of truth.
2. **Never add a file without the user's confirmation** — propose a collection, wait.
3. **Every number in the wiki needs a citation** (file + page). No citation, no number.
4. **`index.db` is disposable.** If in doubt, delete it and rebuild from `raw/`.

Do not treat this as the complete list. When `SKILL.md` and this file disagree,
`SKILL.md` wins.

## What this is not

Not Elasticsearch. Not multi-user. No embeddings, no local OCR, no GUI, no
automatic translation. See `wiki/layer1/Non-Goals.md` before adding a feature
that assumes otherwise.
