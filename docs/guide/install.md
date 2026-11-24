# Install

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

The last line must be:

```
VERIFY: PASS
```

Anything else means the install failed. Do not report success.

## What it creates

```
~/archive/
├── doclib.py            the only executable
├── SCHEMA.md            the rules, on one page
├── index.db             created empty, user_version = 100
├── references/          9 reference files
└── collections/
    ├── office-works/
    │   ├── COLLECTION.md
    │   ├── raw/{files,web,audio,images}/
    │   └── wiki/{index.md,log.md,sources/,entities/,concepts/}
    ├── maintenance-learning/
    └── ai-learning/
```

## Requirements

| Need | Why |
|---|---|
| Python 3.11+ | `tomllib` is stdlib from 3.11 |
| `pypdf`, `python-docx`, `openpyxl`, `python-pptx` | installed by `setup.py` |
| `ffmpeg` | only for audio over 25 MB |
| `GROQ_API_KEY` | only for audio transcription |

## The five verify checks

| Check | Expectation |
|---|---|
| `collections` | the three collections from `setup.toml` exist |
| `schema` | `files`, `chunks`, `chunks_fts` exist; `user_version = 100` |
| `add` | one seed file indexes; `files` has ≥ 1 row |
| `search` | `search "قرارداد"` returns a hit |
| `lint` | no structural issues |

## Idempotency

Running `setup.py` twice is safe. `index.md` and `log.md` are only created when
missing, and `index.db` is never deleted.

## Uninstall

```bash
rm -rf ~/archive
```

No system packages, no services, no global state.
