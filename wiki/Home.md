# Hybrid SQLite-FTS5 + Karpathy-style Wiki Archive

An archive that keeps three things apart, on purpose:

| Layer | What it holds | Can it be rebuilt? |
|---|---|---|
| `raw/` | the files you were given | **No** — it is the source of truth |
| `index.db` | SQLite FTS5 search index | **Yes** — delete it, re-add from `raw/` |
| `wiki/` | markdown pages that explain and cite | **Yes** — but only from `raw/` |

Most document tools collapse these into one. That is why they cannot answer
"where did this number come from" and cannot survive a database corruption.

## Start here

| If you want to… | Read |
|---|---|
| install it | [Install-Quick](layer3/Install-Quick) |
| see it work in five commands | [Walkthrough-Simple](Walkthrough-Simple) |
| understand why it is built this way | [Why-Hybrid](layer1/Why-Hybrid) |
| know what it deliberately does not do | [Non-Goals](layer1/Non-Goals) |
| fix something that broke | [Debug-Playbook](layer4/Debug-Playbook) |
| hand it to an AI agent | [AGENTS-Page](AGENTS-Page) |

## The one-paragraph version

Files go into `raw/` and are never touched again. `doclib.py` extracts text,
splits it into ~1400-character chunks, folds Persian orthography so `تأخیر` and
`تاخیر` match, and writes three tables: `files`, `chunks`, and the FTS5 virtual
table `chunks_fts`. Search reads `chunks_fts` and returns the original text with
a file and chunk reference. The wiki is written by hand or by an agent, and
every number in it must carry that reference.

## All 29 pages

**Why** — [Why-Hybrid](layer1/Why-Hybrid) · [Three-Layers](layer1/Three-Layers) · [Data-Model](layer1/Data-Model) · [Non-Goals](layer1/Non-Goals)

**How it works** — [DB-Files](layer2/DB-Files) · [DB-Chunks](layer2/DB-Chunks) · [DB-FTS](layer2/DB-FTS) · [Persian-Normalize](layer2/Persian-Normalize) · [Query-Router](layer2/Query-Router) · [CLI-Reference](layer2/CLI-Reference)

**Using it** — [Install-Quick](layer3/Install-Quick) · [Ingest-Workflow](layer3/Ingest-Workflow) · [Collections](layer3/Collections) · [Adding-Collection](layer3/Adding-Collection) · [Dual-Path](layer3/Dual-Path) · [Wiki-Page-Contract](layer3/Wiki-Page-Contract) · [Wiki-Lint](layer3/Wiki-Lint)

**Repair** — [Debug-Playbook](layer4/Debug-Playbook) · [Verify-Checklist](layer4/Verify-Checklist) · [Err-FTS-Empty](layer4/Err-FTS-Empty) · [Err-Persian-Search](layer4/Err-Persian-Search) · [Err-Schema-Mismatch](layer4/Err-Schema-Mismatch) · [Err-Corrupt-DB](layer4/Err-Corrupt-DB) · [Err-Empty-Extract](layer4/Err-Empty-Extract) · [Err-Outside-Raw](layer4/Err-Outside-Raw) · [Err-Groq-403](layer4/Err-Groq-403) · [Err-Broken-DOCX](layer4/Err-Broken-DOCX)

**Agent** — [AGENTS-Page](AGENTS-Page) · [Walkthrough-Simple](Walkthrough-Simple)

## Requirements

Python 3.11+ (`tomllib`), and `ffmpeg` only if you ingest audio over 25 MB.
