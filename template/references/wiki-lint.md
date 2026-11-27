# Lint ویکی / Wiki Lint

> در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> When in conflict with `SKILL.md`, **`SKILL.md` wins.**

**بعد از هر ingest، `lint` بزن. صفر خطا قبل از گزارش به کاربر.**

**Run `lint` after every ingest. Zero errors before reporting to the user.**

## لینت ساختاری (اسکریپت `doclib.py lint`)

Structural lint (script: `doclib.py lint`)

| بررسی / Check | توضیح / Description | رفع / Fix |
|---|---|---|
| **لینک شکسته** / Broken links | لینک `## Related` یا `## Sources` به فایل ناموجود / links to a non-existent file | صفحهٔ هدف را بساز یا مسیر را درست کن / Create the target or correct the path |
| **منبع گم‌شده** / Missing source | `## Sources` به فایلی اشاره می‌کند که در `raw/` نیست یا ایندکس نشده / cites a file not in `raw/` or not indexed | فایل را در `raw/` بگذار و `doclib.py add` کن / Add the file to `raw/` and `doclib.py add` it |
| **صفحهٔ یتیم** / Orphan page | صفحه در `sources/` که `index.md` به آن لینک نداده / not linked from `index.md` | لینک در جدول `index.md` اضافه کن / Add the link in the `index.md` table |
| **در index نیست** / Not in index | صفحه هست ولی در `index.md` فهرست نشده / exists but unlisted | مثل یتیم — به `index.md` اضافه کن / Same as orphan |
| **بدون منبع** / No sources | صفحهٔ `sources/` بدون بخش `## Sources` / missing `## Sources` | `## Sources` با حداقل یک ارجاع بگذار / Add `## Sources` with at least one citation |
| **عنوان تکراری** / Duplicate title | دو صفحه با `# Title` یکسان / two pages with the same title | یکی را تغییر نام بده و `index.md` را آپدیت کن / Rename one and update `index.md` |

```bash
python3 /opt/data/documents/doclib.py lint -c <collection>
```

## لینت محتوایی (انسانی، نه اسکریپت)

Content lint (human, not script)

**قاعده:** قبل از نوشتن/آپدیت صفحهٔ ویکی با منبع جدید، **اعداد صفحهٔ موجود را با منبع جدید مقایسه کن**. اگر اختلاف بود → با هر دو عدد و منبع به کاربر گزارش بده. تصمیم با کاربر است. هرگز بی‌صدا بازنویسی نکن.

**Rule:** before writing/updating a wiki page with a new source, **compare the existing page's numbers with the new source**. If they differ → report to the user with both numbers and sources. The user decides. Never silently overwrite.

**کهنگی:** اگر منبعی که صفحه بر آن ساخته شده تغییر کرد، صفحه باید دوباره خوانده و آپدیت شود.

**Staleness:** if a source a page was built on changed, the page must be re-read and updated.

## تناقض‌های عددی در صفحه — قالب / Numeric contradictions on a page — template

وقتی یک سند با حساب خودش نمی‌خواند، آن را **در صفحه بنویس**، نه فقط در پاسخ به کاربر. پیام گم می‌شود؛ صفحه می‌ماند و دفعهٔ بعد که کسی (یا خودت) صفحه را می‌خواند، هشدار را می‌بیند.
When a source disagrees with its own arithmetic, **write it on the page**, not only in the chat reply. Messages are lost; the page persists and the next reader sees the warning.

بخش اختیاری `### تناقض‌های داخلی / Internal Inconsistencies` را بلافاصله قبل از `**نکات مهم**` (یا قبل از `## منابع` اگر آن بخش نیست) بگذار. سه چیز باید باشد:
Put the optional `### Internal Inconsistencies` section just before the notes list (or before `## Sources` if there is none). It must carry three things:

1. **هر دو عدد + اختلاف دقیق.** جدول کوچک: جزء، جزء، جمع اجزا، جمع اعلامی، اختلاف. خواننده باید بتواند خودش جمع بزند.
   **Both figures plus the exact gap.** A small table: component, component, computed sum, stated total, difference — the reader must be able to re-add it.
2. **کجا اختلاف هست، کجا نیست.** اگر همهٔ ستون‌ها با ردیف‌هایشان می‌خوانند، این را بنویس: یعنی اشکال در جمع نهایی است نه در ردیف‌ها. این تشخیص ارزش گزارش را چند برابر می‌کند.
   **Say where the fault is and where it is not.** If every column reconciles with its rows, state that — it localizes the fault to the grand total, not the rows.
3. **هشدار عملی برای استفادهٔ بعدی.** یک نقل‌قول کوتاه: «این عدد را به‌عنوان مقدار تأییدشده به کار نبر؛ اگر لازم شد هر دو سناریو را بده.» بدون این، نسخهٔ بعدیِ خودت دوباره همان عدد را نقل می‌کند.
   **An actionable warning for later use.** A short quote: do not treat this figure as verified; if needed, present both scenarios. Without it, your next self quotes the same number again.

**قاعدهٔ ستون با ضریب نایکنواخت را هم بنویس.** اگر عنوان ستون یک قاعده می‌گوید (مثل «تعدیل ۴۵٪») و فقط بعضی ردیف‌ها آن را رعایت می‌کنند، جدول انحراف‌ها را بیاور: هر ردیف، مقدار ثبت‌شده، مقدار مورد انتظار، اختلاف با علامت. این نشان می‌دهد ستون مشتق است ولی از یک قاعدهٔ واحد، پس مقایسهٔ بین‌سالی روی آن معتبر نیست.
**Record columns whose multiplier is not uniform too.** If a column's heading states a rule (e.g. "adjustment 45%") and only some rows obey it, table the deviations: row, recorded value, expected value, signed difference. It proves the column is derived but not by one rule, so year-over-year comparison on it is invalid.

**اعداد داخل این بخش را بعد از نوشتن دوباره حساب کن.** عنوان بخش و جدول زیرش باید یک عدد بدهند؛ اختلاف یک‌ریالی بین تیتر و جدول، همان دسته خطایی است که این بخش برای گرفتنش ساخته شد.
**Re-compute the figures inside this section after writing it.** The heading and the table beneath it must agree; a one-rial difference between heading and table is exactly the class of error the section exists to catch.

## دستور `links` (برای سؤال‌های مسیر ۲)

Links command (for Path 2 queries)

```bash
python3 /opt/data/documents/doclib.py links sources/<page> -c <coll>
```

**خروجی / Output:**

- لینک‌های خروجی (✓ موجود، ✗ شکسته) / Outgoing links (✓ exists, ✗ broken)
- بک‌لینک‌های ورودی / Incoming backlinks
- ورودی‌های گم‌شدهٔ `## Related` / Missing `## Related` entries

## دستور `graph`

Graph command

```bash
python3 /opt/data/documents/doclib.py graph [-c <coll>]
```

**خروجی:** نقشهٔ ASCII با صفحه | درجهٔ ورودی (نوار ←) | درجهٔ خروجی (نوار →).

**Output:** ASCII map with page | in-degree (← bar) | out-degree (→ bar).

## قرارداد صفحهٔ ویکی (اجبارشده توسط lint)

Wiki page contract (enforced by lint)

هر صفحهٔ `wiki/sources/` **باید** داشته باشد:

Every `wiki/sources/` page MUST have:

```markdown
# Title
> One-line description
## Summary
## Content
## Sources          # MANDATORY
## Related
```

- مسیر نسبی از محل فایل: `../entities/x.md`، `../../raw/files/y.pdf`.
- `index.md` **باید** به همهٔ صفحات `sources/` لینک بدهد — تنها راه خروج از یتیمی.
- `## Related` همان چیزی است که ویکی را ویکی می‌کند؛ بدون آن هر صفحه یک جزیره است.

- Relative paths from the file location: `../entities/x.md`, `../../raw/files/y.pdf`.
- `index.md` MUST link every `sources/` page — the only escape from orphan status.
- `## Related` is what makes a wiki a wiki; without it every page is an island.

## مقیاس‌پذیری ویکی حداقلی

Minimal wiki scaling

- `sources/` — همیشه ساخته می‌شود (یکی به ازای هر منبع).
- `entities/` — فقط وقتی موضوع در **چند منبع** آمده باشد.
- `concepts/` — فقط وقتی اصطلاح در **چند منبع** آمده باشد.
- یک منبع → فقط صفحهٔ `sources/`. جلوی صفحه‌های نیمه‌خالی ویکی را می‌گیرد.

- `sources/` — always created (one per source).
- `entities/` — only when a topic appears in **multiple sources**.
- `concepts/` — only when a term appears in **multiple sources**.
- One source → only the `sources/` page. Prevents half-empty wiki pages.
