# Why SQLite *and* a wiki, not one of them

## The problem with search alone

A search index answers "which file contains this word". It does not answer:

- "What was the penalty clause, and does it contradict the other contract?"
- "Is the budget figure in this month's report consistent with the contract?"
- "Which of these three documents is the authoritative one?"

Those are synthesis questions. A snippet cannot answer them, because the
answer is not in one chunk — it is in the relationship between chunks.

## The problem with a wiki alone

A wiki answers synthesis questions well. It fails at:

- exact retrieval ("find every page that mentions ۴۸۰,۰۰۰,۰۰۰")
- provenance ("which page 47 of which PDF did this come from")
- scale (nobody writes a wiki page per invoice)

## Why both, kept apart

```
raw/       immutable    ← the evidence
index.db   rebuildable  ← exact retrieval over the evidence
wiki/      derived      ← interpretation, citing the evidence
```

Each layer has one job and one failure mode:

| Layer | Fails when | Recovery |
|---|---|---|
| `raw/` | disk loss | restore from backup — nothing else can help |
| `index.db` | corruption, schema change | delete and rebuild from `raw/` |
| `wiki/` | staleness, wrong numbers | re-read `raw/`, fix the citation |

Because `index.db` is disposable, a schema change is cheap. Because `wiki/`
must cite, a wrong number is findable. Because `raw/` is untouched, both can
be rebuilt.

## What this costs

- Two things to maintain instead of one. The wiki does not update itself.
- An ingest is two writes (raw file, then index), not one.
- Every claim needs a citation, which is slower than writing freely.

The trade: you can always answer "where did this come from", and a corrupted
database is an inconvenience rather than a loss.

## The alternative that was rejected

Store everything in the wiki and search it with `grep`. Simple, and it works
until the corpus is large enough that `grep` returns 200 lines and you cannot
tell which one is the current version. FTS5 with chunk-level references is
what makes the result usable.
