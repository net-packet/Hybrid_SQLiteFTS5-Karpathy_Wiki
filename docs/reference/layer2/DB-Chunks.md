# `chunks` — the text, split

```sql
CREATE TABLE chunks (
    file_id INTEGER NOT NULL,
    idx     INTEGER NOT NULL,
    page    INTEGER,
    text    TEXT NOT NULL,
    fts_key TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (file_id, idx),
    FOREIGN KEY (file_id) REFERENCES files(file_id) ON DELETE CASCADE
);
CREATE INDEX idx_chunks_file ON chunks(file_id);
```

## Why chunks at all

A 200-page PDF is one row of 400 KB. Searching it returns the whole document
and you still have to find the sentence. Chunking gives:

- a citation you can point at (`contract-1405.pdf, chunk 7, page 3`)
- a result small enough to read
- bounded memory during extraction

## How the split works

`chunkify()` in `doclib.py`:

| Parameter | Value | Meaning |
|---|---|---|
| `CHUNK_SIZE` | 1400 chars | target maximum |
| `CHUNK_OVERLAP` | 200 chars | how much of the tail repeats into the next chunk |

The splitter prefers a **sentence boundary** inside the last half of the
window, trying in order: blank line, `. `, `؟ `, `! `, newline. If none is
found it cuts at 1400. Overlap exists so a sentence straddling a boundary is
still findable in full from at least one chunk.

Consequence: **chunk boundaries are not stable across edits of `doclib.py`.**
Change `CHUNK_SIZE` and every `idx` shifts. Citations written as "chunk 7"
survive only until the next `reindex` with a different size — cite the page
when the source has pages.

## `page` is nullable on purpose

| Source type | `page` |
|---|---|
| PDF | page number, from the extractor |
| DOCX / TXT / MD / CSV | `NULL` |
| XLSX | sheet index |
| PPTX | slide number |
| web / audio / image | `NULL` |

A citation falls back to the chunk index when `page` is `NULL`. Do not write
"page 3" for a DOCX — write "chunk 3".

## `text` vs `fts_key`

Two columns holding nearly the same string. `text` is what a human reads;
`fts_key` is the aggressively folded version that FTS5 indexes. They differ
because folding loses information you do not want to display:

| Original | `fts_key` |
|---|---|
| `تأخیر` | `تاخیر` |
| `می‌شود` | `می شود` |
| `۴۸۰` | `480` |

Search matches against `fts_key`; the result shows `text`. Details in
[Persian-Normalize](Persian-Normalize.md).

## Queries

```sql
-- read one chunk in full
SELECT text FROM chunks WHERE file_id = 1 AND idx = 7;

-- all chunks of a file in order
SELECT idx, page, substr(text,1,80) FROM chunks
WHERE file_id = 1 ORDER BY idx;

-- chunks with no page number (non-paginated sources)
SELECT f.name, COUNT(*) FROM chunks c JOIN files f USING(file_id)
WHERE c.page IS NULL GROUP BY f.name;

-- biggest chunks, to check the splitter
SELECT file_id, idx, length(text) FROM chunks
ORDER BY length(text) DESC LIMIT 10;
```

## The overlap trap

Because of the 200-char overlap, the same sentence can appear in two chunks.
A search for a distinctive phrase may therefore return two hits from one file.
That is not a bug and not a duplicate file — check the `idx` before concluding
anything. `search` reports the chunk index for exactly this reason.
