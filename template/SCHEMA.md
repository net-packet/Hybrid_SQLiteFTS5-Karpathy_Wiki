# SCHEMA — قواعد آرشیو اسناد / Archive Constitution

این فایل «قانون اساسی» آرشیو است. هر سشن جدیدی که با آرشیو کار می‌کند باید اول این را بخواند.
This file is the archive constitution. Every new session working with the archive must read this first.

## ساختار / Structure

```
documents/
├── SCHEMA.md                       همین فایل / This file
├── index.db                        SQLite — index جستجو (خودکار ساخته می‌شود) / Search index (auto-created)
├── doclib.py                       اسکریپت استخراج/ایندکس/جستجو / Extract/index/search script
├── doclib.single-collection.py.bak نسخه قدیمی (استفاده نمی‌شود) / Old version (unused)
└── collections/<name>/
    ├── COLLECTION.md               موضوع این مجموعه، چه چیزی داخلش می‌شود / Collection scope
    ├── raw/                        منبع حقیقت — هرگز تغییر نمی‌کند / Source of truth — never modified
    │   ├── files/                  PDF, DOCX, XLSX, PPTX, TXT, MD, CSV
    │   ├── web/                    نسخه markdown بلاگ‌پست‌ها / Blog posts as markdown
    │   ├── audio/                  فایل صوتی اصلی + رونویسی / Original audio + transcript
    │   └── images/                 عکس اصلی + متنی که مدل خوانده / Original image + model reading
    └── wiki/
        ├── index.md                فهرست همه منابع این مجموعه / All sources index
        ├── log.md                  تاریخچه عملیات (چه چیزی کِی اضافه شد) / Operation history
        ├── sources/                یک صفحه per منبع / One page per source
        ├── entities/               افراد، سازمان‌ها، تجهیزات (فقط وقتی لازم شد) / People, orgs, equipment (only when needed)
        └── concepts/               مفاهیم، اصطلاحات (فقط وقتی لازم شد) / Concepts, terms (only when needed)
```

## سه لایه / Three Layers

1. **`raw/`** — فایل اصلی، دست‌نخورده. مرجع نهایی. **هرگز ویرایش یا حذف نمی‌شود.**
   **Original files, untouched. Source of truth. Never edited or deleted.**
2. **`index.db`** — متن استخراج‌شده، تکه‌تکه‌شده، برای جستجوی سریع نقطه‌ای.
   **Extracted, chunked text for fast point queries.**
3. **`wiki/`** — صفحات markdown که *من* نوشتم. نقشه و تحلیل، نه کپی خام.
   **Markdown pages I write. Map & analysis, not raw copy.**

## قواعد سخت / Hard Rules

### ۱. اصل فایل تغییر نمی‌کند / Raw Immutable
هرگز محتوای `raw/` را ویرایش نکن. اگر منبع جدیدی نسخه بهتری داشت، فایل جدید با نام جدید اضافه می‌شود.
Never edit `raw/` content. If a new source has a better version, add as new file with new name.

**تنها استثنا / Only exception:** فایل‌های `raw/files/User-Reading-*.md` — منبع زنده، فقط append. جزئیات در بخش «منبع در حال مطالعه».
**Only exception:** `raw/files/User-Reading-*.md` — living source, append-only. See "Living Source" section.

### ۲. هر عدد و ادعای عددی باید ارجاع داشته باشد / Every Number Must Be Cited
در صفحات `wiki/`، هر عدد باید به منبع و جای مشخصش اشاره کند:
In `wiki/` pages, every number must cite source + location:
`بودجه ۴۵ میلیارد ریال (`raw/files/contract.pdf`، ص ۳)`

بدون ارجاع، عدد نوشته نمی‌شود.
No citation = no number written.

### ۳. Extend, don't create
قبل از ساختن صفحه جدید در `wiki/`، جستجو کن آیا صفحه‌ای درباره همان موضوع هست. اگر هست، **همان را گسترش بده**، نه اینکه صفحه دوم بسازی.
Before creating a new `wiki/` page, search if one exists for that topic. If yes, **extend it**, don't create a second page.

### ۴. ویکی حداقلی / Minimal Wiki
`sources/` همیشه ساخته می‌شود (یک صفحه per منبع).
`sources/` always created (one page per source).
`entities/` و `concepts/` **فقط وقتی** ساخته می‌شوند که واقعاً موضوعی تکرار شده باشد که ارزش صفحه مستقل داشته باشد.
`entities/` and `concepts/` **only when** a topic repeats across sources enough to warrant its own page.

### ۵. زبان / Language Rules
- زبان محتوای `wiki/` = زبان منبع اصلی (فارسی→فارسی، انگلیسی→انگلیسی) / Wiki content language = source language (fa→fa, en→en)
- متن دوزبانه → فارسی با اصطلاحات فنی به انگلیسی در پرانتز / Mixed → Persian with English terms in parentheses
- **نام فایل‌های ویکی همیشه انگلیسی و کوتاه** (مثلاً `steel-plant-contract.md`) / Wiki filenames always English short
- **زبان پاسخ = زبان سؤال** / **Response language = question language**: سؤال فارسی → جواب فارسی، English question → English answer
- پرسش ترکیبی دوزبانه → زبان غالب / Mixed query → dominant language

### ۶. آپلود بدون تأیید ممنوع / No Upload Without Confirmation
هیچ فایلی بدون اینکه اول موضوعش تشخیص داده شود، مجموعه‌اش پیشنهاد شود و کاربر تأیید کند، اضافه نمی‌شود.
No file added without: detect topic → propose collection → get user confirmation.

## قرارداد صفحه ویکی / Wiki Page Contract

هر صفحه در `wiki/sources/` **باید** این ساختار را داشته باشد. `lint` نبودش را گزارش می‌دهد.
Every page in `wiki/sources/` **must** have this structure. `lint` reports missing sections.

```markdown
# عنوان فارسی / Persian Title

> یک خط توضیح — این خط در `index.md` و `collections` استفاده می‌شود.
> One-line description — used in `index.md` and `collections`.

## خلاصه / Summary
دو تا پنج خط: این سند چیست، طرفین/موضوع، بازه زمانی، مهم‌ترین عددها.
2–5 lines: what is this doc, parties/topic, date range, key numbers.

## محتوا / Content
جزئیات ساختاریافته. جدول برای اعداد. هر عدد با ارجاع.
Structured details. Tables for numbers. Every number cited.

## منابع / Sources
- [نام فایل](../../raw/files/contract.pdf) — ص ۳، ۷
- [عکس بودجه](../../raw/images/2026-11-20-budget.md)

## مرتبط / Related
- [پارس فولاد](../entities/pars-steel.md)
- [تأخیر و جریمه](../concepts/delay-penalty.md)
```

### قواعد لینک‌دهی / Linking Rules

- **مسیر نسبی از محل فایل.** صفحه در `wiki/sources/` است → `../entities/x.md` و `../../raw/files/y.pdf`.
  **Relative paths from file location.** Page in `wiki/sources/` → `../entities/x.md` and `../../raw/files/y.pdf`.
- **بخش `مرتبط` اجباری نیست** اگر واقعاً چیزی مرتبط نیست — ولی اگر هست و ننویسی، صفحه یتیم می‌شود و `lint` می‌گیردش.
  **`## Related` not mandatory** if truly nothing related — but if related pages exist and you don't list them, page becomes orphan and `lint` catches it.
- **صفحه بدون `## منابع` = صفحه بی‌منبع.** `lint` علامت می‌زند. فقط `index.md`، `log.md`، `entities/` و `concepts/` معاف‌اند.
  **Page without `## Sources` = no-sources page.** `lint` flags it. Only `index.md`, `log.md`, `entities/`, `concepts/` exempt.

### ساختار `index.md` / `index.md` Structure

`index.md` **باید** به همه صفحات `sources/` لینک بدهد. این تنها راهی است که یک صفحه از «یتیم» بودن نجات پیدا می‌کند:
`index.md` **must** link all `sources/` pages. This is the only way a page escapes orphan status:

```markdown
# فهرست منابع — <نام مجموعه> / Sources Index — <Collection Name>

> توضیح مجموعه / Collection description

## منابع / Sources
- [عنوان فارسی](sources/short-english-name.md) — نوع، تاریخ / Type, Date

## موضوعات / Topics
- [پارس فولاد](entities/pars-steel.md)
```

## سه عملیات ویکی / Three Wiki Operations

| عملیات / Op | چه کسی / Who | ابزار / Tools |
|---|---|---|
| **Ingest** | من + `add` / Me + `add` | تشخیص موضوع → تأیید → کپی به `raw/` → `doclib.py add` (فایل خام) → نوشتن صفحه ویکی → **`doclib.py add` (صفحه ویکی)** → آپدیت `index.md` و `log.md` |
| **Query** | من + `search`/`links` / Me + `search`/`links` | زیر را ببین / See below |
| **Lint** | `doclib.py lint` + من / `doclib.py lint` + Me | ساختاری با اسکریپت، محتوایی با خواندن / Structural via script, content via reading |

### Query — دو مسیر / Query — Two Paths

1. **نقطه‌ای / Point Query** («بودجه چقدر بود؟»، «جریمه چند درصد؟») → `doclib.py search` → جواب + نام فایل + صفحه.
2. **ترکیبی/تحلیلی / Analytical Query** («روند سه ساله»، «مقایسه کن»، «تناقضی هست؟») → این مسیر / This path:
   1. `wiki/index.md` را بخوان / Read `wiki/index.md`
   2. صفحه(های) مرتبط را پیدا کن / Find relevant page(s)
   3. `doclib.py links <page> -c <coll>` بزن تا صفحات مرتبط بعدی را ببینی / Run to see next linked pages
   4. آن صفحات را بخوان و ترکیب کن / Read & combine those pages
3. **مسیر ۱ جواب نداد** → برو مسیر ۲. **مسیر ۲ کافی نبود** → `search` بزن.
   **Path 1 fails** → go Path 2. **Path 2 insufficient** → `search`.
4. **در پاسخ بگو از کدام مسیر جواب دادی** و همه منابع را ذکر کن.
   **In answer, state which path you used** and cite all sources.

**قاعده:** سؤال تحلیلی هرگز مستقیم به SQLite نمی‌رود. ویکی نقطه شروع است، نه آخرین راه‌حل.
**Rule:** Analytical query never goes direct to SQLite. Wiki is the starting point, not the last resort.

**زبان پاسخ = زبان سؤال / Response language = question language**

### Lint — دو لایه / Lint — Two Layers

**لایه ساختاری (اسکریپت) / Structural (Script):** لینک شکسته (broken links)، صفحه یتیم (orphan page)، منبع گم‌شده (missing source)، صفحه بی‌منبع (no sources)، عنوان تکراری (duplicate title)، صفحه‌ای که در `index.md` نیست (not in index).

**لایه محتوایی (من، نه اسکریپت) / Content Layer (Me, Not Script):**

> هر بار که منبع جدیدی مربوط به صفحه‌ای موجود است، **قبل از نوشتن**، عددهای صفحه موجود را با منبع جدید مقایسه کن. اگر اختلاف بود، **به کاربر گزارش بده** — هیچ‌وقت ساکت از روی عدد قدیمی رد نشو. تصمیم با کاربر است، نه من.
> Every time a new source relates to an existing page, **before writing**, compare existing page numbers with new source. If discrepancy, **report to user** — never silently overwrite old numbers. User decides, not me.

کهنگی هم همین‌طور: اگر منبعی که صفحه بر آن بنا شده عوض شد، صفحه باید بازخوانی شود.
Staleness same: if source a page was built on changed, page must be re-read.

## نوع منبع (`source_type`) / Source Types

| نوع / Type | مسیر / Path | نحوه پردازش / Processing |
|---|---|---|
| `pdf` | `raw/files/` | pypdf، صفحه‌به‌صفحه / Page by page |
| `docx` | `raw/files/` | python-docx، پاراگراف + جدول / Paragraphs + tables |
| `xlsx` | `raw/files/` | openpyxl، شیت‌به‌شیت با `\|` / Sheet by sheet with `\|` |
| `pptx` | `raw/files/` | python-pptx، اسلاید‌به‌اسلاید / Slide by slide |
| `text` | `raw/files/` یا `raw/web/` | مستقیم / Direct |
| `image` | `raw/images/` | **مدل خودش می‌خواند** — صفر نصب / **Model reads directly** — zero install |
| `audio` | `raw/audio/` | Groq Whisper large-v3 (STT) |
| `user-reading` | `raw/files/User-Reading-<slug>.md` | **منبع زنده** — append-only، هر نقل‌قول یک تکه / **Living source** — append-only, one chunk per quote |

## منبع در حال مطالعه (`user-reading`) / Living Source

**استثنای یگانه بر قاعده «raw تغییرناپذیر».** / **The only exception to raw immutability.**

فایلی که نامش با `User-Reading-` شروع می‌شود، تنها فایلی است که بعد از ساخت می‌تواند تغییر کند — و آن هم فقط با **افزودن**.
A file whose name starts with `User-Reading-` is the only file that may change after creation — and only by **appending**.

### چه زمانی / When

کاربر می‌گوید «کتاب X را شروع کردم» و مشخصات می‌دهد. **هیچ فایلی بدون تأیید صریح ساخته نمی‌شود.**
User says "I started book X" and gives details. **No file is created without explicit confirmation.**

### جریان / Flow

1. تشخیص موضوع → پیشنهاد مجموعه / Detect topic → propose collection
2. `doclib.py ur-list` و `search` → کتاب قبلاً هست؟ / Check if book already exists
3. پر کردن جاهای خالی با سؤال از کاربر (فقط فیلدهای لازم) / Fill gaps by asking (only needed fields)
4. **پیش‌نمایش** (عنوان، نویسنده، سال، ناشر، زبان، مجموعه، نام فایل، مسیرها) → تأیید / **Preview** → confirmation
5. `doclib.py ur-new` → ساخت فایل خام + صفحه ویکی + ثبت در `index.md`
6. هر نقل‌قول بعدی: `doclib.py ur-add` (بدون پیش‌نمایش مجدد) / Each later quote: `ur-add` (no re-preview)

### نام‌گذاری / Naming

```
raw/files/User-Reading-<english-slug>.md
wiki/sources/user-reading-<english-slug>.md
```

- **slug انگلیسی** — عنوان کتاب (فارسی یا انگلیسی) در frontmatter می‌آید، نه در نام فایل
- **slug انگلیسی** — book title goes in frontmatter, never in filename

### frontmatter اجباری / Required Frontmatter

```yaml
source_type: user-reading
mutable: append-only
book_title: <عنوان اصلی>
author: <نویسنده>
year: <سال چاپ>
publisher: <ناشر>
edition: <چاپ>
isbn: <ISBN>
lang: fa | en
page_ref_basis: <مبنای شماره صفحه>
collection: <نام مجموعه>
started: <YYYY-MM-DD>
```

`source_type: user-reading` منبع حقیقت است، نه نام فایل. اگر فایل تغییر نام دهد، رفتار append-only حفظ می‌شود.
`source_type: user-reading` is the source of truth, not the filename. Renaming preserves append-only behavior.

### ساختار بدنه / Body Structure

```markdown
## q001 — ص ۴۷
> متن دقیق جمله

**موضوع:** نگهداشت پیشگیرانه
**یادداشت:** (اختیاری)
**افزوده:** 2026-11-22
```

### مجاز و ممنوع / Allowed vs Forbidden

| عمل / Action | مجاز / Allowed |
|---|---|
| افزودن `q-NNN` جدید / Add new `q-NNN` | ✅ |
| اصلاح غلط تایپی در `q-NNN` / Fix typo in existing | ✅ با `**اصلاح:** <تاریخ>` |
| افزودن فیلد خالی frontmatter / Add empty field | ✅ |
| حذف نقل‌قول / Delete quote | ❌ — `**لغو:** دلیل` بنویس |
| تغییر فیلد موجود frontmatter / Modify existing field | ❌ |
| شماره‌گذاری مجدد `q-NNN` / Renumber | ❌ — شناسه ثابت است |

`q-NNN` **شناسه ثبات است، نه ترتیب**. ترتیب افزودن و ترتیب صفحه جدا نگه داشته می‌شوند.
`q-NNN` is a **stability ID, not ordering**. Insertion order and page order tracked separately.

### صفحه ویکی / Wiki Page

یک صفحه per کتاب، خودکار بازتولید می‌شود. سه بخش:
One page per book, auto-regenerated. Three sections:

1. **نمای ۱ — به ترتیب افزودن** / In reading order
2. **نمای ۲ — به ترتیب صفحه** / By page
3. **موضوعات پوشش‌داده‌شده** / Topics covered

هیچ `entities/` یا `concepts/` برای کتاب ساخته نمی‌شود مگر موضوعی در چند منبع تکرار شود.
No `entities/` or `concepts/` for a book unless a topic repeats across sources.

### ایندکس / Indexing

هر نقل‌قول **یک تکه جدا** در `index.db` است، با شماره صفحه. جستجوی نقطه‌ای مستقیماً نقل‌قول را با ارجاع برمی‌گرداند:
Each quote is **one separate chunk** in `index.db`, with its page number. Point query returns the quote with citation:

```
[کتاب X · نویسنده · ص ۴۷ · q001] متن جمله | موضوع: نگهداشت پیشگیرانه
```

### دستورها / Commands

```bash
python3 doclib.py ur-new <slug> --title "<عنوان>" -a "<نویسنده>" -y <سال> -c <collection>
python3 doclib.py ur-add <slug> -p <صفحه> -q "<متن>" [-t "<موضوع>"] [-n "<یادداشت>"] -c <collection>
python3 doclib.py ur-list
```

## فایل‌های مرتبط در `raw/` / Sidecar Files in `raw/`

هر فایل غیرمتنی یک فایل `.md` همراه دارد:
Every non-text file has a companion `.md`:

- `raw/images/2026-11-20-budget-table.jpg` ← عکس اصلی / Original image
- `raw/images/2026-11-20-budget-table.md` ← متن استخراج‌شده توسط مدل / Model-extracted text

- `raw/audio/2026-11-20-meeting.ogg` ← صدا / Audio
- `raw/audio/2026-11-20-meeting.transcript.md` ← رونویسی Groq / Groq transcript

فایل `.md` همراه هم در `index.db` ایندکس می‌شود (چون `.md` یعنی `text`).
Sidecar `.md` also indexed in `index.db` (since `.md` = `text`).

**صفحات `wiki/` هم باید ایندکس شوند.** پس از نوشتن صفحه در `wiki/sources/`، اجرا کن:
**`wiki/` pages must also be indexed.** After writing page in `wiki/sources/`, run:

```bash
python3 /opt/data/documents/doclib.py add "wiki/sources/name.md" -c <collection>
```

بدون این، صفحه ویکی نوشته شده در جستجو پیدا نمی‌شود (فایل خام می‌شود، تحلیل نمی‌شود).
Without this, written wiki page invisible to search (raw file indexed, analysis not).

## دستورهای اسکریپت / Script Commands

```bash
python3 /opt/data/documents/doclib.py collections
python3 /opt/data/documents/doclib.py add <file> -c <collection>
python3 /opt/data/documents/doclib.py search "کوئری" -c <collection>
python3 /opt/data/documents/doclib.py search "کوئری"          # همه مجموعه‌ها / All collections
python3 /opt/data/documents/doclib.py list [-c <collection>]
python3 /opt/data/documents/doclib.py stats
python3 /opt/data/documents/doclib.py show <file_id>
python3 /opt/data/documents/doclib.py rm <file_id>
python3 /opt/data/documents/doclib.py reindex [-c <collection>]

# لایه ویکی / Wiki Layer
python3 /opt/data/documents/doclib.py links sources/name -c <collection>   # لینک ورودی/خروجی / In/out links
python3 /opt/data/documents/doclib.py lint [-c <collection>]               # بازبینی سلامت / Health check
python3 /opt/data/documents/doclib.py graph [-c <collection>]              # نقشه لینک‌ها / Link map

# منبع در حال مطالعه / Living Source
python3 /opt/data/documents/doclib.py ur-new <slug> --title "<عنوان>" -a "<نویسنده>" -y <سال> -c <collection>
python3 /opt/data/documents/doclib.py ur-add <slug> -p <صفحه> -q "<متن>" [-t "<موضوع>"] [-n "<یادداشت>"] -c <collection>
python3 /opt/data/documents/doclib.py ur-list
```

## افزودن مجموعه جدید / Adding New Collection

```bash
mkdir -p /opt/data/documents/collections/<new-name>/{raw/{files,web,audio,images},wiki/{sources,entities,concepts}}
# سپس COLLECTION.md و wiki/index.md و wiki/log.md بساز / Then create COLLECTION.md, wiki/index.md, wiki/log.md
```

قبل از ساخت، با کاربر تأیید بگیر.
Confirm with user before creating.