# Persian text: why two columns and two foldings

Persian is written with characters that look identical and are not. Without
folding, `تأخیر` and `تاخیر` are different words to a search engine, and a user
who types one will never find the other.

## The characters that cause trouble

| Same glyph | Different code points |
|---|---|
| ی | `ی` U+06CC (Persian yeh), `ي` U+064A (Arabic yeh) |
| ک | `ک` U+06A9 (Persian kaf), `ك` U+0643 (Arabic kaf) |
| ه | `ه` U+0647, `ۀ` U+06C0 (heh with yeh above) |
| ا | `ا` U+0627, `آ` U+0622, `أ` U+0623, `إ` U+0625 |
| و | `و` U+0648, `ؤ` U+0624 |
| (none) | ZWNJ `‌` U+200C — zero-width non-joiner, used inside `می‌شود` |

Add Arabic diacritics (fatha َ, kasra ِ, shadda ّ) and Persian/Arabic-Indic
digits (۰-۹, ٠-٩), and one document can contain six spellings of one word.

## Two functions, two purposes

### `normalize()` — what gets stored

```python
text = text.replace("\u200c", " ").replace("\u200d", "")   # ZWNJ → space
for a, p in _ARABIC_MAP.items(): text = text.replace(a, p)  # ي→ی, ك→ک
for d in _PERSIAN_DIGITS: text = text.replace(d, latin[d])  # ۴→4
text = re.sub(r"[ \t]+", " ", text)
text = re.sub(r"\n{3,}", "\n\n", text)
```

Conservative: it unifies what is unambiguously the same letter, and stops
there. The result is readable and is what `chunks.text` holds.

### `match_fold()` — what gets indexed

```python
text = normalize(text)
for a, p in _SEARCH_FOLD.items(): text = text.replace(a, p)  # آأإا → ا, ة→ه
text = re.sub(r"[^\w\s]", " ", text)   # punctuation → space
text = re.sub(r"\s+", " ", text)
```

Aggressive: it also collapses `آ/أ/إ/ا` to bare `ا` and strips punctuation.
The result is not pretty — `تأخیر` becomes `تاخیر` — which is exactly why it
lives in a separate column and is never displayed.

## Why not just fold once, aggressively?

Because the user reads `chunks.text`. If you store the folded form, the
displayed text is corrupted: `می‌شود` shows as `می شود`, `۴۸۰` shows as `480`,
and punctuation is gone. The document would no longer look like the document.

Two columns cost one extra string per chunk. That is the whole price.

## The pipeline

```
PDF ──extract──► raw text
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
   normalize()             match_fold()
        │                       │
   chunks.text            chunks.fts_key
        │                       │
   shown to user          indexed by FTS5
```

## What folding does *not* solve

**Synonyms.** `جریمه` and `penalty` are unrelated strings; no folding helps.
This is the documented limit in [Non-Goals](../layer1/Non-Goals.md) — lexical search, by
design.

**Stemming.** `قرارداد` and `قراردادها` are different tokens. FTS5's `porter`
stemmer is English-only. A search for the singular misses the plural.

**Word order.** `نرخ بلیت` and `بلیت نرخ` are different phrases. FTS5 phrase
queries (`"نرخ بلیت"`) require adjacency.

## Testing a folding change

```bash
python3 -c "
import sys; sys.path.insert(0,'.')
from doclib import match_fold, normalize
for w in ['تأخیر','تاخیر','می‌شود','۴۸۰','کتاب','كتاب']:
    print(repr(w), '->', repr(normalize(w)), '|', repr(match_fold(w)))
"
```

Expected: `تأخیر` and `تاخیر` both fold to `تاخیر`; `كتاب` and `کتاب` both
normalize to `کتاب`; `۴۸۰` becomes `480`.

If you change `_SEARCH_FOLD`, you must `reindex` — `fts_key` is stored, not
computed at query time.
