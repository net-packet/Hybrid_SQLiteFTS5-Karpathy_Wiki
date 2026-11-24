# The three layers, and the rules each one imposes

## Layer 1 — `raw/` (immutable)

```
collections/<name>/raw/
├── files/     PDF, DOCX, XLSX, PPTX, TXT, MD, CSV
├── web/       blog posts saved as markdown, with a `source:` header
├── audio/     original audio + .transcript.md
└── images/    original image + .md holding the model's reading
```

**Rule:** never modify anything here. Not a typo fix, not a reformat.

Why: every citation in the wiki points into this directory. If a file changes,
every citation that pointed at it becomes unverifiable — and you cannot tell
which ones.

**The one exception:** `raw/files/User-Reading-*.md`. A book you are reading
grows over time, so this file is append-only, and corrections are marked
`**اصلاح:** <date>` rather than overwriting. The `ur-*` commands enforce this.

## Layer 2 — `index.db` (rebuildable)

Three tables plus an FTS5 virtual table. Details in [DB-Files](../layer2/DB-Files.md),
[DB-Chunks](../layer2/DB-Chunks.md), [DB-FTS](../layer2/DB-FTS.md).

**Rule:** treat it as a cache. If it is wrong, delete it and rebuild:

```bash
rm index.db
python3 doclib.py reindex
```

Nothing in this layer is unique information. Every byte came from `raw/`.

## Layer 3 — `wiki/` (derived, but not mechanical)

```
collections/<name>/wiki/
├── index.md      every source listed — the only escape from "orphan"
├── log.md        what was added, when
├── sources/      one page per source
├── entities/     people, orgs, equipment — only when several sources mention them
└── concepts/     terms — same rule
```

**Rule:** every number needs a citation (file + page). No citation, no number.

Why: this layer is the only place where a human writes prose. Prose drifts.
A citation is what makes drift detectable — you can go back and check.

**Scaling rule:** `entities/` and `concepts/` are created only when a topic
appears in **multiple** sources. One source gets a `sources/` page and nothing
else. This prevents a wiki full of half-empty pages.

## How the layers interact

```
ingest:   file ──copy──► raw/ ──extract──► chunks ──► index.db
                                                    │
                                          agent reads chunks
                                                    │
                                                    ▼
                                              wiki/sources/x.md
                                                    │
                                          cite: ../raw/files/x.pdf p.47
```

## What breaks if you violate a layer

| Violation | Consequence |
|---|---|
| edit a file in `raw/` | citations point at text that no longer exists |
| hand-edit `index.db` | FTS5 triggers and content table drift apart; search silently misses rows |
| write a number in the wiki without a citation | nobody can verify it, including you in six months |
| create `entities/` for a single mention | wiki fills with pages that say one sentence |
