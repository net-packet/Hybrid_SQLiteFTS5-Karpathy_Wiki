# A Persian word is not found

The text is in the database, the FTS index is populated, and the search still
misses. Four distinct causes, in order of likelihood.

## 1 — The word is a single character

`fts_query()` drops tokens of length ≤ 1:

```python
tokens = [t for t in q.split() if len(t) > 1]
```

So `search "و"` returns `کوئری خالی است` (empty query). This is deliberate: in
Persian, `و` and `ب` appear in nearly every sentence, so matching them would
return the whole corpus.

**Workaround:** search a two-character fragment of the surrounding phrase.

## 2 — Spelling variant the folding does not cover

Folding handles `ی/ي`, `ک/ك`, `آ/أ/إ/ا`, `ۀ/ه`, ZWNJ, and Persian/Arabic digits.
It does **not** handle:

| Variant | Folds? |
|---|---|
| `تأخیر` / `تاخیر` | ✅ both → `تاخیر` |
| `می‌شود` / `می شود` | ✅ both → `می شود` |
| `۴۸۰` / `480` | ✅ both → `480` |
| `قرارداد` / `قراردادها` | ✅ prefix match (`"قرارداد"*`) |
| `جریمه` / `penalty` | ❌ synonyms — no folding helps |
| `خسارت` / `غرامت` | ❌ different words |
| `بلیت` / `بلیط` | ❌ **different letters** — a real gap |

`بلیت`/`بلیط` is the honest counter-example: two spellings in common use, no
shared fold. Test it:

```bash
python3 -c "
import sys; sys.path.insert(0,'/tmp/x'); from doclib import match_fold
print(match_fold('بلیت'), '|', match_fold('بلیط'))"
```

They differ. Searching one will not find the other. The fix is to search both,
or to add the pair to `_SEARCH_FOLD` — and then `reindex`, because `fts_key` is
stored, not computed at query time.

## 3 — Prefix matching cuts the other way

Every term is a prefix match, so `نرخ` finds `نرخ‌گذاری`. But a **longer** query
does not find a shorter word: `قراردادها` will not match `قرارداد`.

Search the shortest unambiguous stem.

## 4 — The text really is not there

Check before assuming a search bug:

```bash
sqlite3 ~/archive/index.db "select count(*) from chunks where text like '%بلیت%';"
```

- **0** → extraction lost it. Check `n_chunks` and the source file.
- **>0** → the text is present and the index is the problem →
  [Err-FTS-Empty](Err-FTS-Empty.md).

Also possible: the word is inside an image in a PDF. `pypdf` returns no text for
scanned pages, so the word exists visually and not in the database. The fix is
to read the page as an image, not to change the search.

## Testing the folding directly

```bash
python3 -c "
import importlib.util
spec = importlib.util.spec_from_file_location('dl','/tmp/archive/doclib.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for w in ['تأخیر','تاخیر','بلیت','بلیط','می‌شود','۴۸۰']:
    print(repr(w), '|', repr(m.normalize(w)), '|', repr(m.match_fold(w)))
"
```

If `normalize` already differs for two spellings you expected to match, the gap
is in `_ARABIC_MAP`; if only `match_fold` differs, it is in `_SEARCH_FOLD`.

## The order to check

1. Is the query longer than one character? (`fts_query` returns empty otherwise)
2. `select count(*) from chunks where text like '%word%'` — is it in the DB?
3. `select count(*) from chunks_fts` — is the index populated?
4. Does `match_fold` unify the two spellings?
5. Is the word inside an image in the PDF?

Each question eliminates one layer. See [Persian-Normalize](../layer2/Persian-Normalize.md)
for what folding does and does not do.
