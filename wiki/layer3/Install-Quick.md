# Install — five commands

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py collections
```

The third command must end with `VERIFY: PASS`. If it does not, the install
failed — read [Debug-Playbook](../layer4/Debug-Playbook.md) before doing anything else.

## What `setup.py` does

It reads `setup.toml` and nothing else. It holds no knowledge of the archive
layout, so changing the layout means editing the TOML, not the script.

| Step | Action |
|---|---|
| 1 | `pip install --user -r src/requirements.txt` (skip with `--skip-install`) |
| 2 | check for `ffmpeg` (only needed for audio > 25 MB) |
| 3 | create `collections/<name>/` with `raw/{files,web,audio,images}` and `wiki/{sources,entities,concepts}` |
| 4 | seed `wiki/index.md` and `wiki/log.md` |
| 5 | copy `src/doclib.py`, `template/SCHEMA.md`, `template/references/` |
| 6 | create `index.db` and stamp `PRAGMA user_version = 100` |

## Requirements

| Need | Why |
|---|---|
| Python 3.11+ | `tomllib` is stdlib from 3.11 |
| `pypdf`, `python-docx`, `openpyxl`, `python-pptx` | extraction, installed by step 1 |
| `ffmpeg` | audio over 25 MB must be split before Groq accepts it |
| `GROQ_API_KEY` | only for audio. Everything else works without it |

## The layout you get

```
~/archive/
├── doclib.py            the only executable
├── SCHEMA.md            the rules, in one page
├── index.db             created empty, ready
├── references/          9 reference files
└── collections/
    ├── office-works/
    │   ├── COLLECTION.md
    │   ├── raw/{files,web,audio,images}/
    │   └── wiki/{index.md,log.md,sources/,entities/,concepts/}
    ├── maintenance-learning/
    └── ai-learning/
```

## Choosing a different root

```bash
python3 src/setup.py --root /srv/archive --verify
```

`--root` accepts `~` and relative paths. `DOCLIB_ROOT` must point at the same
place, or `doclib.py` will look in the wrong directory and report zero
collections.

## Adding a fourth collection later

```bash
python3 ~/archive/doclib.py add ... -c new-name     # fails: collection unknown
```

Collections are declared in `setup.toml`. To add one:

```bash
cp -r ~/archive/collections/office-works ~/archive/collections/contracts
rm -rf ~/archive/collections/contracts/raw/* ~/archive/collections/contracts/wiki/sources/*
# edit COLLECTION.md to describe the new scope
```

Then add the name to `setup.toml` so a future re-install creates it too. The
`collections` command reads the directory, not the TOML, so the new collection
appears immediately.

## Idempotency

Running `setup.py` twice is safe. Existing files are copied over; existing
`index.md` and `log.md` are **not** overwritten (they are only created if
missing). `index.db` is never deleted.

## Uninstall

```bash
rm -rf ~/archive
```

That is the whole thing — no system packages, no services, no global state.
