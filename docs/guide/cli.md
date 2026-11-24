# CLI

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py <command> [args]
```

## Ingest

| Command | Does |
|---|---|
| `add <path> [-c COLL]` | index a file or directory inside `raw/` |
| `rm <file_id>` | remove from the index; the file in `raw/` is untouched |
| `reindex [-c COLL]` | re-extract every file from `raw/` |

## Query

| Command | Does |
|---|---|
| `search <query> [-c] [-f NAME] [-n LIMIT]` | ANDed, prefix-matched FTS5 search |
| `list [-c COLL]` | files with chunk counts |
| `show <file_id>` | every chunk of one file, in order |
| `stats` | totals per collection |
| `collections` | collections with their scope statements |

## Wiki

| Command | Does |
|---|---|
| `lint [-c COLL]` | six structural checks, exit 1 on issues |
| `graph [-c COLL]` | in/out degree per page |
| `links <page> -c COLL` | both link directions for one page |

## Living source

| Command | Does |
|---|---|
| `ur-new <slug> --title T -c COLL` | create a book-in-progress page |
| `ur-add <slug> -p N -q TEXT -c COLL` | append one quote with its page |
| `ur-list` | list living sources with quote counts |

## Exit codes

`0` success or empty search · `1` bad arguments, missing file, lint issues.

Full detail: [CLI-Reference](../reference/layer2/CLI-Reference).
