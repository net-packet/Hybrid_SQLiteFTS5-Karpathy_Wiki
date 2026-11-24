# نرمال‌سازی فارسی و جستجو / Persian Normalization & Search

> در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> When in conflict with `SKILL.md`, **`SKILL.md` wins.**

## دو تابع

Two functions

- `normalize(text)` — نرمال‌سازی هنگام ذخیره: نیم‌فاصله→فاصله، ي/ك→ی/ک، حذف اعراب عربی، ارقام→لاتین. **ملایم.**
- `match_fold(text)` — تاشو هنگام جستجو: تاشوی اضافی همزه/ة/ى، نرمال‌سازی ارقام. **تهاجمی.**

- `normalize(text)` — storage normalization: half-space→space, ي/ك→ی/ک, Arabic diacritics removed, digits→Latin. **Moderate.**
- `match_fold(text)` — search-time folding: extra همزة/ة/ى folding, digit normalization. **Aggressive.**

| تابع / Function | هدف / Purpose | شدت / Aggressiveness |
|---|---|---|
| `normalize(text)` | ذخیره / Storage | ملایم / Moderate |
| `match_fold(text)` | جستجو / Search | تهاجمی / Aggressive |

## نگاشت کاراکترها

Character mappings

```python
_ARABIC_MAP = {
    '\u064a': 'ی',  # Arabic yeh  -> Persian yeh
    '\u0643': 'ک',  # Arabic kaf  -> Persian kaf
    '\u0629': 'ه',  # teh marbuta -> heh
    '\u0649': 'ی',  # alef maksura -> yeh
    '\u0623': 'ا',  # alef with hamza above
    '\u0625': 'ا',  # alef with hamza below
    '\u0622': 'ا',  # alef with madda
    '\u0624': 'و',  # waw with hamza
    '\u0626': 'ی',  # yeh with hamza
    # Diacritics removed: \u064b-\u0654
}
_PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'
_ARABIC_DIGITS  = '٠١٢٣٤٥٦٧٨٩'
_LATIN_DIGITS   = '0123456789'
```

## شمای FTS5

FTS5 schema

```sql
ALTER TABLE chunks ADD COLUMN fts_key TEXT NOT NULL DEFAULT '';
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    fts_key,
    content='chunks',
    content_rowid='rowid',
    tokenize="unicode61 remove_diacritics 2"
);
-- Triggers: chunks_ai, chunks_ad, chunks_au sync fts_key on insert/update/delete
```

## رفتار جستجو

Search behavior

- ایندکس، `match_fold(text)` را در `fts_key` ذخیره می‌کند.
- FTS5 روی `fts_key` با `unicode61 remove_diacritics 2` ایندکس می‌زند.
- رتبه‌بندی: `bm25(chunks_fts)`.
- **نمایش از `text` اصلی استفاده می‌کند**، نه تاشویافته — برش متن فارسی واقعی را نشان می‌دهد.
- `make_snippet(text, tokens, width=220)` تطبیق‌ها را در متن اصلی برجسته می‌کند.

- The index stores `match_fold(text)` in `fts_key`.
- FTS5 indexes `fts_key` with `unicode61 remove_diacritics 2`.
- Ranking: `bm25(chunks_fts)`.
- **Display uses the original `text`**, not the folded form — snippets show real Persian.
- `make_snippet(text, tokens, width=220)` highlights matches in the original text.

## هم‌ارزی‌های تست‌شده

Tested equivalences

| جستجو / Query | تطبیق / Matches |
|---|---|
| `تأخیر` | `تاخیر` ✅ |
| `مسئول` | `مسیول` ✅ |
| `جریمه تأخیر` | `جریمه تاخیر` ✅ |
| `۹۲۲۰` | `9220` ✅ |
| `۱۰ ابزار` | `ده ابزار` ❌ (تاشو کلمه→رقم تبدیل نمی‌کند / fold doesn't convert words→digits) |

## قاعدهٔ صفحهٔ ویکی

Wiki page rule

اگر منبع از ارقام فارسی استفاده می‌کند (مثل `۱۰ ابزار`)، **هر دو صورت را در صفحهٔ ویکی بنویس** — ارقام فارسی و لاتین:

If the source uses Persian digits (e.g. `۱۰ ابزار`), **write both forms in the wiki page** — Persian and Latin digits:

```markdown
۱۰ (10) ابزار
```

تست نشان داد `۱۰ ابزار` پیدا **نشد** ولی `ده ابزار` پیدا شد: `match_fold` ارقام را تبدیل می‌کند، نه کلمات عددی. پس هر دو صورت رقمی را بنویس (`۱۰` و `10`)، هرگز به فرم کلمه‌ای (`ده`) تکیه نکن.

The test showed `۱۰ ابزار` was **not** found but `ده ابزار` was: `match_fold` converts digits, not number words. So write both numeral forms (`۱۰` and `10`), never rely on the word form (`ده`).
