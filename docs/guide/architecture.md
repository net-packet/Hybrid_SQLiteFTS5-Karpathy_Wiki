# Architecture

## Three layers

```
raw/       immutable    ← the evidence
index.db   rebuildable  ← exact retrieval over the evidence
wiki/      derived      ← interpretation, citing the evidence
```

| Layer | Fails when | Recovery |
|---|---|---|
| `raw/` | disk loss | restore from backup — nothing else helps |
| `index.db` | corruption, schema change | delete and rebuild from `raw/` |
| `wiki/` | staleness, wrong numbers | re-read `raw/`, fix the citation |

Because `index.db` is disposable, a schema change is cheap. Because `wiki/` must
cite, a wrong number is findable. Because `raw/` is untouched, both can be
rebuilt.

## One file through the system

```
contract-1405.pdf
      │  sha256, size, path
      ▼
files ──── 1 row
      │  file_id
      ▼
chunks ─── 14 rows (text + fts_key + page)
      │  rowid
      ▼
chunks_fts ── inverted index only, no text copy
```

`chunks_fts` is an external-content FTS5 table: `content='chunks'`,
`content_rowid='rowid'`. It stores no text, so it must be kept in sync by three
triggers (`chunks_ai`, `chunks_ad`, `chunks_au`). Bypass them and the index
diverges silently — no error, search just returns nothing.

## Persian folding

Two functions, two purposes:

| Function | Output | Used for |
|---|---|---|
| `normalize()` | `تأخیر` → `تاخیر`, `۴۸۰` → `480`, ZWNJ → space | `chunks.text`, what the user reads |
| `match_fold()` | also `آ/أ/إ/ا` → `ا`, punctuation → space | `chunks.fts_key`, what FTS5 indexes |

Folding once, aggressively, would corrupt the displayed text. Two columns cost
one extra string per chunk.

What folding does **not** solve: synonyms (`جریمه`/`penalty`), stemming
(`قرارداد`/`قراردادها` — handled by prefix matching), and spelling variants with
different letters (`بلیت`/`بلیط`).

## Query path

```
query ──match_fold()──► tokens ──"a"* AND "b"*──► FTS5 MATCH
                                                      │
                                          join chunks, files
                                                      │
                                    file · page/chunk · original text
```

The query goes through the same `match_fold()` as the documents. That is the
only reason `تأخیر` finds `تاخیر`.

## The wiki is indexed too

A wiki page is a source like any other. After writing
`wiki/sources/contract-1405.md`, run `add` on it:

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/wiki/sources/contract-1405.md -c office-works
```

Its `rel_path` becomes `wiki/sources/contract-1405.md` — the second branch of
`rel_path_of()`, which stores anything inside the collection relative to the
collection root. Without this step the page is invisible to `search`, and
nothing warns you: `lint` checks structure, not searchability.

Why index the wiki at all? Because the two paths are meant to reinforce each
other. A search for a term should surface both the evidence and the
interpretation of it — otherwise you read the contract and never learn that a
wiki page already noticed a contradiction in it.

## Non-goals

No embeddings, no vector search, no local OCR, no GUI, no multi-user, no
automatic wiki generation. Each is on the list because adding it changes the
design rather than extending it. See [Non-Goals](../reference/layer1/Non-Goals).
