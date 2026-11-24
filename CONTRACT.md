# CONTRACT — what "portable" means here

This repository is portable when **all five** hold. Each one is testable;
none is a claim.

| # | Condition | How to test | Pass looks like |
|---|---|---|---|
| 1 | Installs into an empty directory | `python3 src/setup.py --root /tmp/empty --skip-install` | three collections created, no error |
| 2 | Works with no network | `--skip-install`, then `doclib.py add` a local file | file indexed, `search` finds it |
| 3 | Self-verifies | `python3 src/setup.py --root /tmp/empty --verify` | `VERIFY: PASS` |
| 4 | Persian search works | `doclib.py search "قرارداد"` | at least one hit with a chunk reference |
| 5 | A fresh agent can do it | new session, only `AGENTS.md` read | installs without extra questions |

## What is deliberately out of scope

- Multiple concurrent writers (SQLite single-writer)
- Embeddings / vector search / RAG
- Local OCR (images are read by the model, not by a local engine)
- Automatic translation
- A GUI

## How the contract is checked today

Condition 3 is automated inside `setup.py --verify` (five checks:
collections, schema, add, search, lint). Conditions 1, 2 and 4 are covered by
the same run. Condition 5 is manual and must be re-run whenever `AGENTS.md`
changes — see `wiki/layer3/Verify-Checklist.md`.

## Known gaps

- `--verify` proves the plumbing, not the correctness of extraction for every
  file type. A broken DOCX still needs the fallback described in
  `wiki/layer4/Err-Broken-DOCX.md`.
- `demo/expected/` records one machine's output. Line wrapping may differ on
  another; the field names and counts are the stable part.
