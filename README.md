# Hybrid SQLite-FTS5 + Karpathy-style Wiki Archive

A document archive that keeps three things apart: the files you were given
(never modified), a search index you can rebuild at any time, and a wiki that
explains and cites them.

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

`VERIFY: PASS` means it works. Anything else means it does not.

- **Agents:** read `AGENTS.md` first, then `CONTRACT.md`.
- **Humans:** read the wiki — start at `wiki/Home.md`.
- **Why it is built this way:** `wiki/layer1/Why-Hybrid.md`.
- **What it is not:** `wiki/layer1/Non-Goals.md`.

## Layout

```
src/         doclib.py (the only executable), setup.py, schema.sql
template/    what setup.py copies into a new archive
demo/        synthetic seed documents + recorded expected output
wiki/        39 pages: why, how it works, how to install, how to repair
docs/        VitePress site (EN at /, FA at /fa/)
```

## Requirements

Python 3.11+ (uses `tomllib`). `ffmpeg` only for audio over 25 MB.
