# قرارداد صفحهٔ ویکی / Wiki Page Contract

> قرارداد کامل صفحهٔ ویکی. منبع اصلی: `/opt/data/documents/SCHEMA.md` → «قرارداد صفحه ویکی». در تناقض، **`SKILL.md` برنده است**.
>
> Full wiki page contract. Primary source: `/opt/data/documents/SCHEMA.md` → "Wiki page contract". In conflict, **`SKILL.md` wins.**

## ساختار اجباری (۶ بخش)

Mandatory structure (6 sections)

هر صفحه در `wiki/sources/` **باید** این بخش‌ها را داشته باشد. `lint` نبودش را گزارش می‌دهد.

Every page in `wiki/sources/` **must** have these sections. `lint` reports any that are missing.

```markdown
# عنوان / Title

> یک خط توضیح — این خط در `index.md` استفاده می‌شود.
> One-line description — used in `index.md`.

## خلاصه / Summary
دو تا پنج خط: این سند چیست، طرفین/موضوع، بازهٔ زمانی، مهم‌ترین عددها.

## محتوا / Content
جزئیات ساختاریافته. جدول برای اعداد. هر عدد با ارجاع.

## منابع / Sources
- [نام فایل](../../raw/files/contract.pdf) — ص ۳، ۷
- [عکس بودجه](../../raw/images/2026-11-20-budget.md)

## مرتبط / Related
- [پارس فولاد](../entities/pars-steel.md)
- [تأخیر و جریمه](../concepts/delay-penalty.md)
```

## قواعد لینک‌دهی

Linking rules

- **مسیر نسبی از محل فایل.** صفحه در `wiki/sources/` است → `../entities/x.md` برای موجودیت‌ها و `../../raw/files/y.pdf` برای فایل خام.
- **`## مرتبط` اجباری نیست** اگر واقعاً چیزی مرتبط نیست — ولی اگر هست و ننویسی، صفحه **یتیم** می‌شود و `lint` می‌گیردش.
- **صفحه بدون `## منابع` = صفحه بی‌منبع.** `lint` علامت می‌زند. فقط `index.md`، `log.md`، `entities/` و `concepts/` معاف‌اند.

- **Relative paths from the file's location.** A page in `wiki/sources/` uses `../entities/x.md` for entities and `../../raw/files/y.pdf` for raw files.
- **`## Related` is not mandatory** if nothing is genuinely related — but if something is and you omit it, the page becomes an **orphan** and `lint` catches it.
- **A page without `## Sources` is a sourceless page.** `lint` flags it. Only `index.md`, `log.md`, `entities/` and `concepts/` are exempt.

## قواعد محتوایی

Content rules

- **هر عدد باید ارجاع داشته باشد** (فایل + صفحه). بدون ارجاع، عدد ننویس.
- **ارقام فارسی:** هر دو صورت را بنویس — `۱۰ (10)` — چون `match_fold` ارقام را تبدیل می‌کند ولی کلمات عددی را نه.
- **زبان صفحه = زبان منبع.** منبع انگلیسی → صفحهٔ انگلیسی. منبع فارسی → صفحهٔ فارسی.
- **Extend, don't create:** قبل از ساخت صفحهٔ جدید، جستجو کن صفحه‌ای هست یا نه.
- **`entities/` و `concepts/` فقط وقتی** موضوع در چند منبع تکرار شده باشد. یک منبع → فقط `sources/`.

- **Every number needs a citation** (file + page). No citation, no number.
- **Persian digits:** write both forms — `۱۰ (10)` — because `match_fold` converts digits but not number words.
- **Page language = source language.** English source → English page. Persian source → Persian page.
- **Extend, don't create:** search for an existing page before creating a new one.
- **`entities/` and `concepts/` only when** a topic recurs across several sources. One source → `sources/` only.

## ساختار `index.md`

`index.md` structure

`index.md` **باید** به همهٔ صفحات `sources/` لینک بدهد. این تنها راهی است که صفحه از «یتیم» بودن نجات پیدا می‌کند.

`index.md` **must** link every page in `sources/`. This is the only thing that keeps a page from being an orphan.

دو قالب مجاز (بر اساس مجموعه):

Two allowed formats (per collection):

**قالب بولت / Bulleted format:**

```markdown
# فهرست منابع — <نام مجموعه>

> توضیح مجموعه

## منابع
- [عنوان فارسی](sources/short-english-name.md) — نوع، تاریخ

## موضوعات
- [پارس فولاد](entities/pars-steel.md)
```

**قالب جدول / Table format:**

```markdown
| # | منبع | نوع | تاریخ افزودن | صفحه ویکی |
|---|---|---|---|---|
| 1 | عنوان | PDF | 2026-11-23 | [slug](sources/slug.md) |
```

**پیت‌فال:** ردیف موجود خودمان **جایگزین** شود نه تکرار؛ شمارهٔ ردیف از ردیف‌های **غیرخودمان** شمرده شود.

**Pitfall:** replace our existing row, never duplicate it; count the row number from rows that are **not ours**.

## مثال کامل (PDF قرارداد)

Full example (contract PDF)

```markdown
# قرارداد نگهداشت سالانه — پارس فولاد

> قرارداد سه‌سالهٔ نگهداشت پیشگیرانه با پارس فولاد، از ۱۴۰۴ تا ۱۴۰۶.

## خلاصه / Summary
قرارداد بین کارفرما و پارس فولاد برای نگهداشت پیشگیرانهٔ خط تولید. مدت ۳۶ ماه، شروع ۱۴۰۴/۰۱/۰۱. مبلغ کل ۱۲٬۵۰۰ میلیون ریال (ص ۲). جریمهٔ تأخیر ۰٫۵٪ روزانه، سقف ۱۰٪ (ص ۵).

## محتوا / Content

| مورد | مقدار | ارجاع |
|---|---|---|
| مبلغ کل | ۱۲٬۵۰۰ میلیون ریال | ص ۲ |
| مدت | ۳۶ ماه | ص ۲، ۳ |
| جریمهٔ تأخیر | ۰٫۵٪ روزانه (۰.۵) | ص ۵ |

## منابع / Sources
- [قرارداد-پارس-فولاد.pdf](../../raw/files/contract-pars-steel-1404.pdf) — ص ۲، ۳، ۵

## مرتبط / Related
- [پارس فولاد](../entities/pars-steel.md)
- [تأخیر و جریمه](../concepts/delay-penalty.md)
```
