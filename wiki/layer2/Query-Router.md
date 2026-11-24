# How a query becomes an answer

One command, four steps, no magic.

```bash
python3 doclib.py search "جریمه تاخیر"
```

## Step 1 — fold the query

```
"جریمه تاخیر"  ──match_fold()──►  "جریمه تاخیر"
```

The query goes through the **same** `match_fold()` as the documents. This is
the only reason `تأخیر` finds `تاخیر`: both sides arrive at the index in the
same shape. Fold one side and not the other and nothing matches.

## Step 2 — build an FTS5 expression

`fts_query()` turns the folded string into a safe MATCH expression:

```python
q = match_fold(q)
tokens = [t for t in q.split() if len(t) > 1]
return " AND ".join(f'"{t}"*' for t in tokens)
```

| Input | Expression | Meaning |
|---|---|---|
| `جریمه تاخیر` | `"جریمه"* AND "تاخیر"*` | both terms, prefix-matched |
| `قرارداد` | `"قرارداد"*` | matches `قرارداد` and `قراردادها` |
| `a` | `` (empty) | single-character tokens are dropped |

Two decisions worth knowing:

- **Every term is a prefix match** (`*`), so a search for `قرارداد` also finds
  `قراردادها`. The cost: `نرخ` also matches `نرخ‌گذاری` and any word starting
  with those letters.
- **Single-character tokens are dropped.** In Persian, `و` and `ب` are common
  enough that keeping them would match nearly every chunk.

Each term is quoted, so FTS5 operators inside a word (`-`, `:`, `^`) cannot
break the query. This is why a search for `PM-01` does not raise a syntax error.

## Step 3 — the SQL

```sql
SELECT f.collection, f.name, c.page, c.idx, c.text,
       bm25(chunks_fts) AS rank
FROM chunks_fts
JOIN chunks c ON c.rowid = chunks_fts.rowid
JOIN files  f ON f.file_id = c.file_id
WHERE chunks_fts MATCH ?
ORDER BY rank
LIMIT ?;
```

`bm25()` is FTS5's built-in ranking. It is not tuned, and it is not the point —
the point is that a hit is a real chunk of a real file.

Optional filters are appended to the `WHERE`: `-c <collection>` and
`-f <name-fragment>`.

## Step 4 — the answer

```
2 نتیجه برای «جریمه تاخیر»:

[office-works/01-contract-sample.md — تکه 4]
  ## جریمه تاخیر در صورت تاخیر در پاسخ اضطراری، به ازای هر ساعت تاخیر ۰٫۵
  درصد مبلغ ماهانه کسر می‌شود. سقف جریمه: ۱۰ درصد مبلغ قرارداد.

[office-works/03-maintenance-training-sample.md — تکه 2]
  ...
```

Three facts per hit: **which file**, **which chunk or page**, **the text
around the match**. That is enough to cite, and enough to go read the source.

## Why a snippet and not the whole chunk

`make_snippet()` returns ~220 characters centred on the first matching term,
with the terms wrapped in `»…«`. It does not use FTS5's `snippet()`, because
that function works on the indexed `fts_key` — which is folded and would show
the user `تاخیر` where the document says `تأخیر`.

The custom snippet cuts from `chunks.text`, so the displayed text is the
original. To read a whole chunk, use `show`:

```bash
python3 doclib.py show <file_id>      # every chunk of that file, in order
```

`show` has no per-chunk flag — it prints the whole file. For one chunk, the SQL
is one line:

```sql
SELECT text FROM chunks WHERE file_id = 1 AND idx = 4;
```

## The two-path rule

There are two ways to answer a question, and they are not interchangeable:

| Question | Path | Command |
|---|---|---|
| "where is this word" | index | `search` |
| "what does the corpus say about X" | wiki | read `wiki/`, then `search` to verify |

The index cannot synthesise. The wiki cannot be trusted without the index.
Using one where the other belongs is the most common mistake — see
[Dual-Path](../layer3/Dual-Path.md).
