# Collections — why the archive is split

A collection is a separate universe: its own `raw/`, its own wiki, its own
`index.md`. Search can span all of them or be limited to one.

## The three defaults

| Collection | Scope |
|---|---|
| `office-works` | contracts, letters, circulars, budgets, minutes, org documents |
| `maintenance-learning` | preventive and corrective maintenance, procedures, troubleshooting, standards |
| `ai-learning` | models, tools, papers, prompts, AI in project management |

Each has a `COLLECTION.md` stating its scope. `doclib.py collections` prints
those descriptions, so the boundary is visible at the point of decision.

## Why not one big pile

Three concrete reasons, each learned the hard way:

**1. Ambiguous search results.** A search for `قرارداد` across everything
returns contract clauses next to a paper about contract-management theory. The
user has to disambiguate on every query. With collections, `-c office-works`
removes the noise.

**2. Different citation conventions.** A contract cites a page. A book cites a
page and a quote. A paper cites a section. Keeping them apart means each wiki
can follow its own convention without a global rule that fits none of them.

**3. Different lifetimes.** `ai-learning` will be stale in a year and that is
fine. `office-works` holds contracts that stay authoritative for their whole
term. Mixing them means you cannot tell which is which.

## What a collection contains

```
collections/<name>/
├── COLLECTION.md          scope statement, read by `collections`
├── raw/
│   ├── files/             PDF, DOCX, XLSX, PPTX, TXT, MD, CSV
│   ├── web/               saved pages, with a `source:` header
│   ├── audio/             recording + .transcript.md
│   └── images/            image + .md sidecar
└── wiki/
    ├── index.md           every source listed — the only escape from "orphan"
    ├── log.md             what was added, when
    ├── sources/           one page per source
    ├── entities/          people, orgs, equipment — only if several sources mention them
    └── concepts/          terms — same rule
```

## Cross-collection questions

Sometimes a question spans collections: "does the AI tooling paper change how
we should read the maintenance contract?"

Search both, then write the synthesis in whichever collection owns the
**conclusion**, linking to the source page in the other:

```markdown
| سند | مجموعه | ارجاع |
|---|---|---|
| contract-1405 | office-works | [ص ۳](../../../office-works/wiki/sources/contract-1405) |
| ai-pm-tools | ai-learning | [ص ۱۲](../../../ai-learning/wiki/sources/ai-pm-tools) |
```

Relative paths cross collection boundaries without a special mechanism, because
the layout is identical in every collection.

## The rule for adding one

Ask first. A document in the wrong collection is worse than an unindexed
document, because it will be found in the wrong context later and nobody will
remember why it is there.

If a genuinely new theme appears — say `contracts-1405` as a separate universe
from general office works — that is a new collection. See
[Adding-Collection](Adding-Collection).
