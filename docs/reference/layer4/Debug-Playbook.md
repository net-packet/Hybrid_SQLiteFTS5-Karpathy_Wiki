# Debug playbook — start here when something is wrong

Work down the list. Each entry is a symptom, the one command that distinguishes
causes, and the page that explains the fix.

## The first three commands, always

```bash
python3 doclib.py collections        # does it see the archive at all?
python3 doclib.py stats              # how many files, how many chunks?
python3 doclib.py lint               # is the wiki structurally sound?
```

Most problems are visible here. `collections` returning nothing means
`DOCLIB_ROOT` is wrong, not that the archive is broken — that is the single
most common cause, and it accounts for about half of all "broken" reports.

## Symptom → page

| Symptom | Likely cause | Page |
|---|---|---|
| `VERIFY: FAIL` on `schema` | `index.db` from an older version | [Err-Schema-Mismatch](Err-Schema-Mismatch.md) |
| search returns nothing, files exist | FTS index out of sync | [Err-FTS-Empty](Err-FTS-Empty.md) |
| a Persian word is not found | folding, or prefix, or spelling | [Err-Persian-Search](Err-Persian-Search.md) |
| `index.db` will not open | corruption | [Err-Corrupt-DB](Err-Corrupt-DB.md) |
| `n_chunks = 0` after add | extraction produced no text | [Err-Empty-Extract](Err-Empty-Extract.md) |
| `ValueError: ... not in the subpath of ...` | file added from outside `raw/` | [Err-Outside-Raw](Err-Outside-Raw.md) |
| Groq `403 error 1010` | user-agent, not the key | [Err-Groq-403](Err-Groq-403.md) |
| a DOCX opens as binary garbage | corrupt zip / wrong extension | [Err-Broken-DOCX](Err-Broken-DOCX.md) |
| `collections` prints nothing | `DOCLIB_ROOT` unset or wrong | [Install-Quick](../layer3/Install-Quick.md) |
| `lint` reports orphans | missing `index.md` row | [Wiki-Lint](../layer3/Wiki-Lint.md) |

## The isolation rule

When a search fails, do not debug search first. Establish which layer broke:

```bash
# 1. is the row in files?
sqlite3 ~/archive/index.db "select file_id,name,n_chunks from files;"

# 2. are the chunks there?
sqlite3 ~/archive/index.db "select count(*) from chunks;"

# 3. is the FTS index there?
sqlite3 ~/archive/index.db "select count(*) from chunks_fts;"
```

| 1 | 2 | 3 | Diagnosis |
|---|---|---|---|
| empty | empty | empty | ingest never happened |
| rows | rows | **empty** | FTS triggers never fired → [Err-FTS-Empty](Err-FTS-Empty.md) |
| rows | **empty** | empty | extraction produced nothing → [Err-Empty-Extract](Err-Empty-Extract.md) |
| rows | rows | rows, search still fails | the query, not the data → [Err-Persian-Search](Err-Persian-Search.md) |

Three queries localise the fault to one layer. Everything after that is that
layer's page.

## What not to do

| Don't | Because |
|---|---|
| delete `index.db` first | it is rebuildable, but you lose the diagnosis; run the three queries first |
| re-run `setup.py` over a working archive | it will not fix a data problem and may overwrite templates |
| edit `chunks_fts_*` shadow tables | corrupts the index in ways that raise no error |
| reinstall the Python packages | extraction problems are almost never dependency problems |
| assume the query is correct | test with a single common word first (`search "قرارداد"`) |

## Getting help efficiently

Report these five facts, and most problems answer themselves:

```
DOCLIB_ROOT = ...
python3 doclib.py stats          → output
sqlite3 index.db "pragma user_version;"
sqlite3 index.db "select count(*) from chunks_fts;"
the exact command and the exact output
```
