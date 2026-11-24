# جریان ingest / Ingest Procedures

> جزئیات کامل جریان ingest. در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> Full ingest flow details. When in conflict with `SKILL.md`, **`SKILL.md` wins.**

## جریان کامل ingest (۸ مرحله)

Complete ingest flow (8 steps)

| # | اقدام / Action | دستور / Command |
|---|---|---|
| 1 | کپی به پوشهٔ درست `raw/` / Copy to correct `raw/` folder | `cp <file> /opt/data/documents/collections/<coll>/raw/<type>/` |
| 2 | ایندکس فایل خام / Index raw file | `python3 /opt/data/documents/doclib.py add <path> -c <coll>` |
| 3 | ساخت صفحهٔ ویکی / Create wiki page | `wiki/sources/<short-english-name>.md` |
| 4 | لینک در `index.md` / Link in `index.md` | به صفحهٔ جدید لینک بده، وگرنه **یتیم** می‌شود |
| 5 | ایندکس صفحهٔ ویکی / Index wiki page | `doclib.py add <wiki-page-path> -c <coll>` — **حیاتی** |
| 6 | آپدیت `log.md` / Update `log.md` | منبع + تاریخ + اعداد کلیدی |
| 7 | اجرای `lint` / Run `lint` | `doclib.py lint -c <coll>` — **صفر خطا** |
| 8 | گزارش به کاربر / Report | `file_id` + مسیر ویکی + اعداد |

**ترتیب ۴ و ۵ الزامی است:** ابتدا `index.md`، بعد `add` روی صفحهٔ ویکی. اگر برعکس شود، `lint` صفحه را «در index است ولی یتیم» می‌بیند.

Steps 4 and 5 must stay in this order: `index.md` first, then `add` the wiki page. Reversed, `lint` reports the page as indexed-but-orphan.

## پیش‌نیاز قبل از مرحله ۱

Prerequisites before step 1

- موضوع تشخیص داده شد؟ / Topic identified?
- مجموعه **پیشنهاد** و **تأیید** شد؟ / Collection **proposed** and **approved**?
- اگر در دو مجموعه جا داشت → **بپرس** / If it fits two, **ask**

## PDF / DOCX / XLSX / PPTX / TXT / MD / CSV

| مورد / Item | مقدار / Value |
|---|---|
| موتورها / Engines | `pypdf`, `python-docx`, `openpyxl`, `python-pptx` |
| تکه‌بندی / Chunking | ۱۴۰۰ کاراکتر، ۲۰۰ همپوشانی، page-aware / 1400 chars, 200 overlap, page-aware |
| DOCX خراب / Corrupt DOCX | fallback به `_docx_raw_xml()` (zipfile + regex) |

```bash
python3 /opt/data/documents/doclib.py add "collections/<coll>/raw/files/doc.pdf" -c <coll>
```

## عکس / اسکرین‌شات — Images / Screenshots

۱. **خود مدل عکس را می‌خواند** — بدون OCR لوکال، صفر نصب.  
۲. متن استخراج‌شده را در sidecar بنویس: `raw/images/<name>.md`.  
۳. `doclib.py add` روی همان `.md`.  
۴. صفحهٔ ویکی **هر دو** را ارجاع می‌دهد: `../../raw/images/<name>.jpg` و `../../raw/images/<name>.md`.  
۵. اگر جدول/ارقام دارد → ارقام فارسی را حفظ کن و فرم لاتین را هم در پرانتز بنویس: `۱۰ (10)`.

1. **The model reads the image directly** — no local OCR, zero install.  
2. Write extracted text to a sidecar: `raw/images/<name>.md`.  
3. `doclib.py add` on that `.md`.  
4. The wiki page cites **both**: `../../raw/images/<name>.jpg` and `../../raw/images/<name>.md`.  
5. Tables/numbers: keep Persian digits and add the Latin form in parentheses: `۱۰ (10)`.

## صدا / ویس (Groq Whisper) — Audio / Voice

```bash
KEY=$(grep -E '^GROQ_API_KEY=' /opt/data/.env | head -1 | cut -d= -f2- | tr -d '"')
curl -sS https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $KEY" \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36" \
  -F "file=@<audio>" -F "model=whisper-large-v3" -F "language=fa" -F "response_format=json"
```

۱. رونویسی با `whisper-large-v3`، `language=fa`.  
۲. ذخیره در sidecar: `raw/audio/<name>.transcript.md`.  
۳. `doclib.py add` روی transcript.  
۴. **متن خام را به کاربر نشان بده** تا اصطلاحات تخصصی را تصحیح کند — قبل از ساخت صفحهٔ ویکی.  
۵. صفحهٔ ویکی به transcript ارجاع می‌دهد.

1. Transcribe with `whisper-large-v3`, `language=fa`.  
2. Save the sidecar: `raw/audio/<name>.transcript.md`.  
3. `doclib.py add` on the transcript.  
4. **Show the raw transcript to the user** for technical-term correction, before building the wiki page.  
5. The wiki page cites the transcript sidecar.

### پیت‌فال‌های Groq — Groq Pitfalls

| # | پیت‌فال / Pitfall |
|---|---|
| 1 | بدون `-A` مرورگر → `HTTP 403 error 1010` (Cloudflare) / No browser UA → `HTTP 403 error 1010` |
| 2 | سقف ~۲۵ مگابایت → `ffmpeg` به تکه‌های ۱۰ دقیقه، ۵ ثانیه همپوشانی / ~25 MB cap → split with `ffmpeg`, 10-min chunks, 5s overlap |
| 3 | `large-v3` برای فارسی بهتر از `large-v3-turbo` / `large-v3` beats turbo for Persian |
| 4 | پارامتر `prompt` را با اصطلاحات تخصصی پر کن / Fill the `prompt` param with domain terms |
| 5 | تشخیص «فرمان vs سؤال» از صدا ممکن نیست — نشانه‌های گفتاری + همیشه تأیید / Cannot tell command from question in audio — use speech markers + always confirm |

## لینک / بلاگ — Web / Blog Links

۱. `web_extract` — HTML را بگیر؛ تبلیغات/منو/فوتر را حذف کن (نمونه dev.to: خطوط بعد از `* * *` تبلیغ است).  
۲. ذخیره در `raw/web/YYYY-MM-DD-slug.md` با هدر YAML.  
۳. `doclib.py add` روی فایل خام.  
۴. ساخت صفحهٔ ویکی در `wiki/sources/<short-name>.md` — **زبان ویکی = زبان منبع**.  
۵. `doclib.py add` **روی صفحهٔ ویکی هم بزن** — وگرنه در جستجو پیدا نمی‌شود (باگ واقعی).  
۶. لینک در `wiki/index.md` + آپدیت `wiki/log.md`.  
۷. `lint`.

1. `web_extract` — fetch HTML, strip ads/nav/footer (dev.to: lines after `* * *` are ads).  
2. Save to `raw/web/YYYY-MM-DD-slug.md` with a YAML header.  
3. `doclib.py add` on the raw file.  
4. Create the wiki page at `wiki/sources/<short-name>.md` — **wiki language = source language**.  
5. `doclib.py add` **on the wiki page too** — otherwise it stays invisible to `search` (real bug).  
6. Link in `wiki/index.md` + update `wiki/log.md`.  
7. `lint`.

هدر YAML / YAML header:

```yaml
source: <URL>
title: <title>
author: <author>
published: <publish date>
retrieved: <today>
lang: <en/fa>
```

## پیت‌فال `index.md` — هر مجموعه قالب متفاوتی دارد

Pitfall: `index.md` format differs per collection

بعضی `wiki/index.md`ها **جدول** دارند و بعضی **فهرست بولت**. `_ur_index_ensure` هر دو را می‌شناسد.

Some `wiki/index.md` files are **tables**, others **bulleted lists**. `_ur_index_ensure` handles both.

| # | قاعده / Rule |
|---|---|
| 1 | ردیف موجودِ خودمان **جایگزین** شود نه تکرار / Replace our own row, never append a duplicate |
| 2 | شمارهٔ ردیف جدول از ردیف‌های **غیرخودمان** شمرده شود / Compute the row number from rows that are **not ours** |

**تست تکرارپذیری:** یک `ur-add` دوم بزن و مطمئن شو (a) قالب درست، (b) برچسب ردیف تغییر نکرده، (c) هنوز فقط یک ردیف وجود دارد.

**Repeatability test:** run a second `ur-add` and verify (a) format is correct, (b) row label unchanged, (c) still exactly one row.

## باگ‌های واقعی که رفع شده‌اند (برنگردان)

Real bugs already fixed (do not regress)

| # | باگ / Bug |
|---|---|
| 1 | صفحهٔ ویکی ایندکس نشده → مرحلهٔ ۵ الزامی / Wiki page not indexed → step 5 is mandatory |
| 2 | ارقام فارسی در ویکی جستجو نمی‌شوند → هر دو صورت را بنویس `۱۰ (10)` / Persian digits unsearchable → write both forms `۱۰ (10)` |
| 3 | DOCX خراب → `_docx_raw_xml()` / Corrupt DOCX → `_docx_raw_xml()` |
| 4 | Groq 403 بدون UA → `-A "Mozilla/5.0..."` الزامی / Groq 403 without UA → `-A` required |
| 5 | سقف ۲۵MB Groq → `ffmpeg` split / Groq 25 MB cap → `ffmpeg` split |

## پاک‌سازی آرتیفکت تست

Cleaning up test artifacts

بعد از تست با کتاب/فایل ساختگی، **سه جا** باید برگردد:

After testing with a fake book/file, **three places** must be reverted:

۱. فایل `raw/files/*`.  
۲. صفحهٔ `wiki/sources/*.md`.  
۳. **ردیف‌های `files` و `chunks` در `index.db`** (حذف دستی در SQLite).

1. The `raw/files/*` file.  
2. The `wiki/sources/*.md` page.  
3. The **`files` and `chunks` rows in `index.db`** (manual SQLite delete).

بعد `stats` بزن و با baseline مقایسه کن، و `lint` بزن تا خط یتیم نماند.

Then run `stats` and compare with the baseline, and `lint` so no orphan link remains.
