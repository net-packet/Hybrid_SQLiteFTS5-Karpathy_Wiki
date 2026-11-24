# مسیر دوگانهٔ جستجو / Dual-Path Query

> در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> When in conflict with `SKILL.md`, **`SKILL.md` wins.**

**زبان پاسخ = زبان سؤال.** سؤال فارسی → جواب فارسی؛ سؤال انگلیسی → جواب انگلیسی؛ مختلط → زبان غالب. **همیشه بگو از کدام مسیر جواب دادی.**

**Response language = question language.** Persian question → Persian answer; English question → English answer; mixed → dominant language. **Always state which path you used.**

## قاعدهٔ تصمیم

Decision rule

سؤال **نقطه‌ای** (Point Query) نشانه‌ها: «چقدر؟»، «چه زمانی؟»، «کدام؟»، «چه کسی؟»، «چند درصد؟»، عدد/نام/تاریخ مشخص → **مسیر ۱: SQLite `search`**.

**Point query** indicators: "how much?", "when?", "which?", "who?", "what percentage?", a specific number/name/date → **Path 1: SQLite `search`**.

سؤال **تحلیلی** (Analytical Query) نشانه‌ها: «روند»، «مقایسه»، «تحلیل»، «تناقض»، «الگو»، «چرا»، «چگونه»، ترکیب چند منبع → **مسیر ۲: ویکی**.

**Analytical query** indicators: "trend", "compare", "analyze", "contradiction", "pattern", "why", "how", multi-source synthesis → **Path 2: Wiki**.

سؤال **مبهم** → **از کاربر بپرس** یا مسیر ۱ را شروع کن و اگر کافی نبود به مسیر ۲ برو.

**Ambiguous** → **ask the user**, or start Path 1 and fall back to Path 2 if insufficient.

## مسیر ۱: SQLite (سؤال نقطه‌ای)

Path 1: SQLite (point query)

```bash
python3 /opt/data/documents/doclib.py search "query"           # all collections
python3 /opt/data/documents/doclib.py search "query" -c coll   # specific collection
python3 /opt/data/documents/doclib.py show <file_id>            # full chunks
```

- **خروجی:** تکه‌های رتبه‌بندی‌شده با `file_id`، صفحه، برش متن، ارجاع منبع.
- **سرعت:** آنی (میلی‌ثانیه).
- **کِی:** کاربر یک واقعیت/عدد مشخص از یک سند مشخص می‌خواهد.

- **Output:** ranked chunks with `file_id`, page, snippet, source citation.
- **Speed:** instant (ms).
- **When:** the user wants a specific fact/number from a specific document.

## مسیر ۲: ویکی (سؤال تحلیلی)

Path 2: Wiki (analytical query)

```bash
# 1. Read index
cat /opt/data/documents/collections/<coll>/wiki/index.md
# 2. Read relevant source page(s)
cat /opt/data/documents/collections/<coll>/wiki/sources/<page>.md
# 3. Follow links
python3 /opt/data/documents/doclib.py links sources/<page> -c <coll>
# 4. Read linked pages, synthesize
```

- **خروجی:** پاسخ ترکیبی از صفحات ویکی (که خودشان به منابع خام ارجاع می‌دهند).
- **سرعت:** کندتر (خواندن چند فایل لازم است).
- **کِی:** کاربر روند، مقایسه، تناقض یا الگو در چند منبع می‌خواهد.

- **Output:** synthesized answer from wiki pages (which cite raw sources).
- **Speed:** slower (requires reading multiple files).
- **When:** the user wants trends, comparisons, contradictions, or patterns across sources.

## اجباری: اعلام مسیر

Mandatory: state the path

همیشه در پاسخ بیاور:

Always include in the answer:

- «از **مسیر ۱ (جستجوی SQLite)** جواب دادم — منبع: فایل X، صفحهٔ Y» / "Answered via **Path 1 (SQLite search)** — source: file X, page Y"
- «از **مسیر ۲ (ترکیب ویکی)** جواب دادم — صفحات: A، B، C» / "Answered via **Path 2 (Wiki synthesis)** — pages: A, B, C"

## زنجیرهٔ عقب‌نشینی

Fallback chain

```
سؤال نقطه‌ای → مسیر ۱ → اگر نتیجه نبود → مسیر ۲
سؤال تحلیلی → مسیر ۲ → اگر کافی نبود → مسیر ۱ (جستجوی هدفمند)
```

```
Point query → Path 1 → if no results → Path 2
Analytical query → Path 2 → if insufficient → Path 1 (targeted search)
```

## ضدالگوها

Anti-patterns

| # | ضدالگو / Anti-pattern |
|---|---|
| 1 | سؤال تحلیلی مستقیم به SQLite (ترکیب و زمینه از دست می‌رود) / Analytical query straight to SQLite (loses synthesis and context) |
| 2 | اعلام نکردن مسیر (کاربر نمی‌تواند راستی‌آزمایی کند) / Not stating the path (the user cannot verify) |
| 3 | مسیر ۲ بدون خواندن `index.md` اول (صفحات مرتبط از دست می‌روند) / Path 2 without reading `index.md` first (misses relevant pages) |
| 4 | مسیر ۲ بدون `links` (صفحات متصل از دست می‌روند) / Path 2 without `links` (misses connected pages) |
