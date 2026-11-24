---
name: document-archive
description: Use for a hybrid SQLite-FTS5 + wiki document archive - ingest, search, cite.
---

# آرشیو اسناد چندمجموعه‌ای / Multi-Collection Document Archive

این اسکیل روی **هر** آرشیوی کار می‌کند. ریشه را از `DOCLIB_ROOT` بخوان (پیش‌فرض `~/archive`).
This skill works on **any** archive. Read the root from `DOCLIB_ROOT` (default `~/archive`).

```bash
export DOCLIB_ROOT="${DOCLIB_ROOT:-$HOME/archive}"
```

**هرگز مسیر مطلق را hardcode نکن.** اگر `DOCLIB_ROOT` خالی بود، `collections` را بزن؛ اگر خروجی خالی داد، ریشه غلط است — قبل از هر کار دیگری آن را درست کن.
**Never hardcode an absolute path.** If `DOCLIB_ROOT` is empty, run `collections`; empty output means the root is wrong — fix that before anything else.

**هر بار:** (1) فایل/لینک/ویس/عکس جدید رسید، یا (2) کاربر خواست در اسنادش بگردی، یا (3) سؤال درباره قرارداد/بودجه/نگهداشت/یادداشت‌هایش پرسید → اول این را بخوان:

```bash
cat $DOCLIB_ROOT/SCHEMA.md
```

**Every time:** (1) new file/link/voice/image arrives, or (2) user wants to search, or (3) question about contracts/budgets/maintenance/notes → read SCHEMA.md first.

## اگر آرشیو هنوز نصب نشده / If the archive is not installed yet

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

آخرین خط باید `VERIFY: PASS` باشد. اگر نبود، نصب نشده — موفقیت گزارش نکن؛ `wiki/layer4/Debug-Playbook.md` را بخوان.
The last line must be `VERIFY: PASS`. If it is not, the install failed — do not report success; read `wiki/layer4/Debug-Playbook.md`.

## ساختار

```
$DOCLIB_ROOT/
├── SCHEMA.md          ← قانون اساسی آرشیو (اول بخوان)
├── index.db           ← SQLite + FTS5
├── doclib.py          ← اسکریپت استخراج/ایندکس/جستجو
└── collections/<name>/
    ├── COLLECTION.md  ← موضوع این مجموعه
    ├── raw/{files,web,audio,images}
    └── wiki/{index.md,log.md,sources,entities,concepts}
```

**فهرست مجموعه‌ها را از خود آرشیو بخوان، نه از این فایل:** `python3 $DOCLIB_ROOT/doclib.py collections`. پیش‌فرض قالب سه مجموعه است (`office-works`، `maintenance-learning`، `ai-learning`)، ولی کاربر می‌تواند مجموعه اضافه کند — فهرست ثابت را فرض نکن.
**Read the collection list from the archive, not from this file:** `collections`. The template defaults to three, but the user can add more — never assume a fixed list.

**قاعده مقیاس‌بندی ویکی:** `entities/` و `concepts/` فقط وقتی ساخته می‌شوند که موضوع در **چند منبع** تکرار شده باشد. یک منبع → فقط `sources/` page. این از پر شدن ویکی با صفحات نیمه‌پر جلوگیری می‌کند.

**Wiki scaling rule:** `entities/` and `concepts/` only created when topic appears in **multiple sources**. One source → only `sources/` page. Prevents half-empty wiki pages.

## قواعد سخت / Hard Rules

1. **هرگز محتوای `raw/` را تغییر نده.** منبع حقیقت است.
   **Never modify `raw/` content.** It is the source of truth.
   > تنها استثنا: `raw/files/User-Reading-*.md` — فایل **فقط append + اصلاح علامت‌دار** است (بخش «منبع در حال مطالعه» را ببین).
   > Only exception: `raw/files/User-Reading-*.md` — **append-only + marked corrections** (see "Living Source" section).
2. **هیچ فایلی بدون تأیید کاربر اضافه نمی‌شود.** اول موضوع را تشخیص بده، مجموعه را پیشنهاد بده، تأیید بگیر.
   **No file added without user confirmation.** Detect topic, propose collection, get approval.
3. **هر عدد در `wiki/` باید ارجاع داشته باشد** (فایل + صفحه). بدون ارجاع، عدد ننویس.
   **Every number in `wiki/` must have a citation** (file + page). No citation = no number.
4. **Extend, don't create** — قبل از ساخت صفحه جدید، جستجو کن صفحه‌ای هست یا نه.
   **Extend, don't create** — search before making a new page.
5. **`entities/` و `concepts/` فقط وقتی لازم شد** — نه از ابتدا.
   **`entities/` and `concepts/` only when needed** — not upfront.
6. **فایل `.md` همراه در `raw/`:** عکس → `<name>.md` (متنی که مدل خواند)، صدا → `<name>.transcript.md`.
   **Sidecar `.md` in `raw/`:** images → `<name>.md` (model's reading), audio → `<name>.transcript.md`.
7. **پیشنهاد ≠ تصمیم.** وقتی مجموعه‌ای را پیشنهاد می‌دهی و نمی‌پرسی، این «تأیید ضمنی» نیست. هرگز جملاتی مثل «نمی‌پرسَم، تک‌گزینگی روشن است» ننویس — همان لحظه بپرس، یا صریح بنویس «پیش‌فرض: X، اگر اعتراضی داری بگو» و منتظر بمان.
   **Proposing ≠ deciding.** A unilateral proposal is not implicit approval. Never write "I won't ask, the fit is obvious" — ask, or state "default: X, object if wrong" and wait.
8. **گزارش «انجام شد» فقط با شاهد واقعی.** قبل از گفتن «ویکی ساخته شد / فایل ایندکس شد / lint پاس شد» یا برعکس «ساخته نشده»، همان لحظه وضعیت دیسک را چک کن (فهرست پوشه با `search_files`، جستجوی متن در `index.md`، خروجی `lint`). تست موفق یک مرحله (استخراج PDF یا `add`) به معنی ساخته شدن کل صفحه ویکی نیست.
   **Report "done" only with fresh evidence.** Check the disk (`ls`, `grep` in `index.md`, `lint` output) immediately before claiming a page/file exists — or that it is missing. A passing extraction step is not a built wiki page.
9. **`index.db` دورریختنی است.** اگر شک داری، پاکش کن و از `raw/` دوباره بساز. هرگز با SQLite دستی تعمیرش نکن.
   **`index.db` is disposable.** If in doubt, delete it and rebuild from `raw/`. Never repair it by hand.

## زبان مراجع — دوزبانه با حفظ خوانایی / Reference Language — Bilingual, Readable

مراجع `references/` **دوزبانه**اند، ولی دوزبانگی نباید خوانایی را خراب کند. فارسی و انگلیسی هرگز در یک خط قاطی نمی‌شوند.
References are **bilingual**, but bilingual must not hurt legibility. Persian and English never interleave on one line.

| لایه / Layer | قاعده / Rule |
|---|---|
| عنوان `#` و `##` | یک خط با «فارسی / English» / One line: `فارسی / English` |
| متن توضیحی | **فارسی بالا، انگلیسی پایین، دو خط جدا** / Persian line, then English line |
| فهرست‌ها | دو فهرست جدا: `**In scope:**` (EN) و `**دامنه (فارسی):**` — نه آیتم دوزبانه درون‌خطی / Two lists, never `- Contracts / قراردادها` |
| جدول‌ها | **فقط انگلیسی**، سرستون دوزبانه: `| مورد / Item | مقدار / Value |` / English body, bilingual header |
| بلوک کد و کامنت‌ها | انگلیسی فقط؛ توضیح فارسی بیرون کد / English only; Persian explanation outside the fence |
| گام‌های شماره‌دار | دو بلوک جدا (۱. فارسی، بعد 1. انگلیسی) / Two blocks, not one mixed list |

سنجش پس از ویرایش / Measure after editing:

```python
# خطی که هم فارسی طولانی دارد و هم ۱۰+ کلمهٔ لاتین = مخلوط سنگین
if len(re.findall(r'[\u0600-\u06FF]', line)) > 18 and len(re.findall(r'[A-Za-z]{3,}', line)) > 10:
    report(line)
```

هدف: صفر خط مخلوط سنگین بیرون از جدول و بلوک کد. بعد از تأیید نهایی، حجم می‌تواند دو برابر شود — این مشکل نیست، خوانایی هدف است.
Goal: zero heavy-mixed lines outside tables and code blocks. Doubling file size is expected and fine.

## نقشهٔ مراجع / Reference Map

`SKILL.md` منبع نهایی است. مراجع فقط دانش تکمیلی دارند. **در تناقض، `SKILL.md` برنده است.**

| موضوع | فایل | کِی بخوان |
|---|---|---|
| راه‌اندازی آرشیو جدید | `references/bootstrap.md` | ساخت آرشیو برای کاربر جدید |
| دامنهٔ مجموعه‌ها (In/Out scope) | `references/collection-scope.md` | قبل از پیشنهاد مجموعه به کاربر |
| جریان کامل ingest + پیت‌فال‌ها | `references/ingest-procedures.md` | شروع هر ingest |
| قرارداد صفحهٔ ویکی + نمونهٔ کامل | `references/wiki-page-contract.md` | قبل از نوشتن صفحهٔ `sources/` |
| منبع در حال مطالعه (User-Reading) | `references/living-source.md` | کاربر گفت «کتاب X را شروع کردم» |
| تصمیم مسیر جستجو (نقطه‌ای vs تحلیلی) | `references/dual-path-query.md` | قبل از پاسخ به سؤال |
| نرمال‌سازی فارسی + FTS5 | `references/persian-normalization.md` | خطای فولدینگ یا ارقام فارسی در جستجو |
| Lint ساختاری + محتوایی | `references/wiki-lint.md` | قبل از گزارش به کاربر |
| بسته‌بندی آرشیو به‌عنوان قالب قابل انتقال | `references/portability-design.md` | کاربر پرسید «agent کسی دیگر هم بتواند همین سیستم را بسازد؟» یا طراحی repo تازه |

## جریان ingest / Ingest Flow

**قواعد مقدم بر جریان:** موضوع را تشخیص بده → **یک** مجموعه پیشنهاد بده → **تأیید بگیر**؛ بدون تأیید هیچ فایلی کپی نمی‌شود. جزئیات کامل هر مرحله و پیت‌فال‌های نوع منبع در `references/ingest-procedures.md`.

**Preconditions:** detect topic → propose **one** collection → get approval. Nothing is copied before approval. Full per-step detail and source-type pitfalls: `references/ingest-procedures.md`.

1. موضوع را تشخیص بده و مجموعه را پیشنهاد بده — **تأیید بگیر**
   Identify topic, propose collection — **get approval**
2. فایل را به پوشه درست `raw/` کپی کن
   Copy file to correct `raw/` folder
3. ایندکس کن:
   ```bash
   python3 $DOCLIB_ROOT/doclib.py add <path> -c <collection>
   ```
   Index it
4. تأیید جستجو + خواندن تکه‌ای که ارجاع می‌دهی: `search "<کلیدواژه>"` بعد `show <file_id>`
   Confirm search + read the chunk you will cite: `search` then `show`
5. صفحه ویکی بساز در `wiki/sources/<short-english-name>.md` — با قرارداد کامل (پایین)
   Create wiki page at `wiki/sources/<short-english-name>.md` — full contract (below)
6. **`doclib.py add` روی صفحه ویکی هم بزن** — وگرنه ویکی در `search` پیدا نمی‌شود
   **`doclib.py add` the wiki page too** — or wiki invisible to search
7. به صفحه جدید در `wiki/index.md` لینک بده — وگرنه lint آن را یتیم می‌بیند
   Link in `wiki/index.md` — or lint marks it orphan
8. `wiki/log.md` را آپدیت کن
   Update `wiki/log.md`
9. `python3 $DOCLIB_ROOT/doclib.py lint -c <collection>` بزن و ایرادها را درست کن
   Run `lint`, fix all errors

پس از `lint`، نتیجه را به کاربر گزارش بده — قالب در بخش «گزارش وضعیت به کاربر».
After `lint`, report the result to the user — format in "Status Reporting".

مرجع رسمی همین جریان در `wiki/layer3/Ingest-Workflow.md` است. این فهرست و آن صفحه باید **هم‌شماره** بمانند؛ اگر یکی را تغییر دادی، دیگری را همان جلسه همگام کن.
The canonical version of this flow is `wiki/layer3/Ingest-Workflow.md`. This list and that page must stay **identically numbered**; change one, sync the other the same session.

## پردازش انواع منبع / Source Type Processing

| نوع / Type | روش / Method |
|---|---|
| PDF/DOCX/XLSX/PPTX/TXT/MD/CSV | `doclib.py add` (pypdf, python-docx, openpyxl, python-pptx) |
| عکس/اسکرین‌شات / Image/Screenshot | **خود مدل می‌خواند** — صفر نصب. متن را در `.md` کنار عکس بنویس، بعد ایندکس کن
   **Model reads directly** — zero install. Write text to `.md` beside image, then index |
| صدا/ویس / Voice/Audio | Groq Whisper → رونویسی را در `.transcript.md` بنویس، بعد ایندکس کن
   Groq Whisper → write transcript to `.transcript.md`, then index |
| لینک/بلاگ / Link/Blog | `web_extract` → markdown در `raw/web/YYYY-MM-DD-slug.md` با خط `source: <URL>`
   `web_extract` → markdown in `raw/web/YYYY-MM-DD-slug.md` with `source: <URL>` |

### گام‌های ingest برای لینک/بلاگ / Web Ingest Steps

1. `web_extract` — HTML را بگیر، تبلیغات/منو/فوتر را حذف کن (dev.to: خطوط بعد از `* * *` که ad است)
   `web_extract` — fetch HTML, strip ads/nav/footer (dev.to: lines after `* * *`)
2. فایل ذخیره در `raw/web/YYYY-MM-DD-slug.md` با هدر YAML:
   Save to `raw/web/YYYY-MM-DD-slug.md` with YAML header:
   ```yaml
   source: <URL>
   title: <actual article title>
   author: <actual author>
   published: <actual publish date>
   retrieved: <today>
   lang: <en|fa>
   ```
3. `doclib.py add` روی فایل خام
   `doclib.py add` on raw file
4. صفحه ویکی بساز در `wiki/sources/<short-english-name>.md` — **زبان ویکی = زبان منبع**
   Create wiki page — **wiki language = source language**
5. `doclib.py add` **روی صفحه ویکی هم بزن** — وگرنه صفحه ویکی در جستجو پیدا نمی‌شود (باگ واقعی، در تست پیدا شد)
   `doclib.py add` **on wiki page too** — or wiki invisible to search (real bug found in testing)
6. به `wiki/index.md` لینک بده + `wiki/log.md` آپدیت کن
   Link in `wiki/index.md` + update `wiki/log.md`
7. `lint` بزن
   Run `lint`

### رونویسی صدا با Groq / Groq STT

`whisper-large-v3` با زبان `fa`. کلید از `$GROQ_API_KEY` خوانده می‌شود.

```bash
KEY="${GROQ_API_KEY:?set GROQ_API_KEY first}"
curl -sS https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer $KEY" \
  -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36" \
  -F "file=@<audio>" -F "model=whisper-large-v3" -F "language=fa" -F "response_format=json"
```

**پیت‌فال‌ها / Pitfalls:**
- بدون یوزر-ایجنت مرورگر → `HTTP 403 error 1010` (Cloudflare). حتماً `-A` بده.
   No browser UA → `HTTP 403 error 1010`. Must use `-A`.
- سقف حجم ~۲۵ مگابایت. فایل بزرگ‌تر را با `ffmpeg` به تکه‌های ۱۰ دقیقه‌ای بشکن، با ۵ ثانیه همپوشانی، بعد به هم بچسبان.
   ~25 MB limit. Split larger files with `ffmpeg` into 10-min chunks, 5s overlap, concat.
- `whisper-large-v3-turbo` سریع‌تر و ارزان‌تر است؛ برای فارسی ابتدا `large-v3` را امتحان کن.
   `whisper-large-v3-turbo` faster/cheaper; try `large-v3` first for Persian.
- رونویسی ممکن است اصطلاح تخصصی را غلط بنویسد؛ **متن خام را به کاربر نشان بده** تا تصحیح کند.
   Transcript may miswrite technical terms; **show raw to user** for correction.
- `prompt` پارامتر پشتیبانی می‌شود — لیست اصطلاحات تخصصی را آنجا بده.
   `prompt` param supported — put domain terms there.

**Voice command vs question detection:** The model cannot distinguish from audio alone. Use speech markers ("اضافه کن", "ثبت کن" vs "چیه؟", "معلومه؟") + file accompaniment. **Always confirm before ingest** — show transcript, ask "Add to <collection>?". In doubt, show transcript and ask briefly.

## منبع در حال مطالعه / Living Source

**کاربر می‌گوید «کتاب X را شروع کردم».** این یک مسیر جدا از ingest عادی است: فایل خام می‌تواند رشد کند.
**User says "I started book X".** Separate path from normal ingest: the raw file may grow.

### جریان اجباری / Mandatory Flow

1. **جستجو** — `ur-list` و `search "<عنوان>"` بزن. کتاب از قبل هست؟
   **Search** — run `ur-list` and `search`. Does the book already exist?
   - هست → همان را ادامه بده (`ur-add`)، فایل جدید نساز
   - Exists → continue it (`ur-add`), do not create a new file
2. **موضوع → مجموعه** — پیشنهاد بده. اگر در دو مجموعه جا داشت، **بپرس**.
   **Topic → collection** — propose. If it fits two, **ask**.
3. **فیلدهای گم‌شده** — فقط چیزهایی که کاربر نداد و برای پیش‌نمایش لازم است بپرس (عنوان، نویسنده، زبان حتماً؛ ناشر/سال/ISBN اختیاری).
   **Missing fields** — ask only what's needed (title, author, lang required; publisher/year/ISBN optional).
4. **پیش‌نمایش + تأیید** — جدول زیر را نشان بده. **تا «تأیید» نگرفتی، هیچ فایلی نساز.**
   **Preview + confirm** — show the table below. **Create nothing before "approved".**

```
📖 پیش‌نمایش منبع جدید / New source preview

عنوان / Title      ...
نویسنده / Author   ...
سال / Year         ...
ناشر / Publisher   ...
زبان / Language    ...
مجموعه / Collection ...
نام فایل / Filename User-Reading-<slug>.md
صفحه ویکی / Wiki    wiki/sources/user-reading-<slug>.md
```

5. **ساخت** — `ur-new` (فایل خام + صفحه ویکی + ثبت در `index.md` خودکار)
   **Create** — `ur-new` (raw + wiki page + `index.md` entry, all automatic)
6. **هر نقل‌قول بعدی** — `ur-add`، بدون پیش‌نمایش مجدد
   **Each later quote** — `ur-add`, no re-preview

### نام‌گذاری / Naming

```
raw/files/User-Reading-<english-slug>.md
wiki/sources/user-reading-<english-slug>.md
```

slug **انگلیسی** است. عنوان کتاب (فارسی/انگلیسی) در frontmatter می‌رود، نه در نام فایل.
slug is **English**. Book title goes in frontmatter, never in filename.

### نقل‌قول‌ها / Quotes

```bash
python3 $DOCLIB_ROOT/doclib.py ur-add <slug> -p 47 -q "متن دقیق جمله" -t "موضوع" -c <collection>
```

- `q001`, `q002`... خودکار شماره می‌گیرند
- `q-NNN` **شناسه ثبات است، نه ترتیب** — ترتیب افزودن و ترتیب صفحه جدا نمایش داده می‌شوند
- `q-NNN` is a **stability ID, not ordering**

### مجاز و ممنوع / Allowed vs Forbidden

| عمل / Action | مجاز / Allowed |
|---|---|
| افزودن نقل‌قول / Add quote | ✅ |
| اصلاح تایپی / Fix typo | ✅ با `**اصلاح:** <تاریخ>` |
| افزودن فیلد خالی frontmatter | ✅ |
| حذف نقل‌قول / Delete quote | ❌ — `**لغو:** دلیل` بنویس، اسکریپت از نمای اصلی خارجش می‌کند |
| تغییر فیلد موجود frontmatter | ❌ |
| شماره‌گذاری مجدد / Renumber | ❌ |

### ایندکس / Indexing

هر نقل‌قول **یک تکه جدا** در `index.db` است، با شماره صفحه. جستجوی نقطه‌ای مستقیم نقل‌قول را با ارجاع برمی‌گرداند:
```
[کتاب X · نویسنده · ص 47 · q001] متن جمله | موضوع: ...
```

صفحه ویکی خودکار بازتولید می‌شود (دو نما + موضوعات + لغو‌شده‌ها). دستی ویرایشش نکن.
Wiki page auto-regenerated (two views + topics + cancelled). Do not hand-edit.

**`q-NNN` را دستی نشمار و تولید نکن.** همیشه `ur-add` بزن؛ شماره بعدی از فایل خام خوانده می‌شود. اگر خودت شماره بگذاری، لغوها و فاصله‌ها باعث برخورد می‌شود.
**Never hand-pick `q-NNN`.** Always go through `ur-add`; it derives the next number from the raw file.

### پیت‌فال: `index.md` هر مجموعه قالب متفاوتی دارد / Pitfall: index.md formats differ per collection

بعضی `wiki/index.md`ها **جدول** دارند و بعضی **فهرست بولت**. `_ur_index_ensure` هر دو را می‌شناسد، ولی اگر قالب جدیدی اضافه کردی دو قاعده را رعایت کن: (1) ردیف موجود خودمان **جایگزین** شود نه تکرار، (2) شماره ردیف جدول از ردیف‌های **غیرخودمان** شمرده شود.

Some `wiki/index.md` files are **tables**, others **bulleted lists**. Both are handled — but when adding a format: (1) replace our own row instead of appending a second one, (2) compute the table row number from rows that are **not ours**, or every `ur-add` bumps the number.

**تست تکرارپذیری بعد از تغییر `_ur_index_ensure`:** یک `ur-add` دوم بزن و مطمئن شو (a) قالب درست است، (b) برچسب ردیف تغییر نکرده، (c) هنوز فقط یک ردیف وجود دارد.
After editing `_ur_index_ensure`, run a second `ur-add` and verify one row, correct format, stable row label.

### پیت‌فال: آرتیفکت تست را پاک کن / Pitfall: clean test artifacts

بعد از تست کتاب ساختگی، سه جا باید برگردد: فایل `raw/files/User-Reading-*.md`، صفحه `wiki/sources/user-reading-*.md`، و **ردیف‌های `files`/`chunks` در `index.db`** (حذف دستی در SQLite). بعد `stats` بزن و با baseline مقایسه کن، و `lint` بزن تا خط یتیم نماند.
Test books leave DB rows behind, not just files — delete from both tables, re-check `stats` against baseline, then `lint`.

## جستجو — دو مسیر، نه یکی / Query — Two Paths, Not One

**قاعده صفر — انتخاب مجموعه / Rule zero — collection choice:** پیش‌فرض `search` را **بدون `-c`** بزن (همه مجموعه‌ها). فقط وقتی کاربر خودش مجموعه را نام برد محدود کن. هرگز از نام مجموعه حدس نزن — کلمهٔ «نگهداری/تعمیرات» در «پیمانکار نگهداری» یعنی `office-works` (قرارداد/پرداخت)، نه `maintenance-learning` (که فقط آموزش است). در شک → همه.

**Default:** run `search` **without `-c`** (all collections). Narrow only when the user names a collection. Never infer the collection from the collection's own name.

**`search` فایل را پیدا می‌کند؛ `show` جواب می‌دهد.** snippet فقط یک تکه (~۲۰۰ کاراکتر) است؛ جدول یا لیست تقریباً همیشه در تکه‌های دیگر است. برای هر سؤال «لیست/چند تا/همه»: `list -c` → `show <file_id>` → همهٔ تکه‌ها را بخوان، بعد جواب بده. جواب از snippet = ردیف‌های گم‌شده.

**`search` finds the file; `show` answers the question.** A snippet is one chunk (~200 chars) — a list or table almost always lives in other chunks. For any "list / how many / all" question: `list -c` → `show <file_id>` → read every chunk before answering.

**`search` خالی بود ≠ داده نیست.** اول `list -c <collection>` بزن تا «واژهٔ اشتباه» از «دادهٔ نبودن» تفکیک شود.

**مسیر ۱ — سؤال نقطه‌ای / Point Query** («بودجه چقدر بود؟»، «جریمه چند درصد؟» / "What was the budget?", "Penalty %?"):

```bash
python3 $DOCLIB_ROOT/doclib.py search "کوئری"              # همه مجموعه‌ها / all collections
python3 $DOCLIB_ROOT/doclib.py search "کوئری" -c office-works
python3 $DOCLIB_ROOT/doclib.py search "کوئری" -f contract
python3 $DOCLIB_ROOT/doclib.py list [-c <collection>]
python3 $DOCLIB_ROOT/doclib.py stats
python3 $DOCLIB_ROOT/doclib.py show <file_id>
```

**مسیر ۲ — سؤال ترکیبی/تحلیلی / Analytical Query** («روند سه ساله»، «مقایسه کن»، «تناقضی هست؟" / "3-year trend", "compare", "any contradiction?"). ویکی نقطه شروع است، **نه آخرین راه‌حل** / Wiki is the starting point, **not the last resort**:

1. `wiki/index.md` را بخوان / Read `wiki/index.md`
2. صفحه(های) مرتبط را پیدا کن و بخوان / Find & read relevant pages
3. `doclib.py links sources/X -c <coll>` بزن → صفحات مرتبط بعدی / Run → next linked pages
4. ترکیب کن / Combine

**سؤال نقطه‌ای جواب نداد → مسیر ۲. سؤال تحلیلی جواب نداد → جستجوی هدفمند (مسیر ۱).**
Point query fails → Path 2. **Analytical query fails → targeted search (Path 1).**
سؤال تحلیلی هرگز مستقیم به SQLite نمی‌رود. **بگو از کدام مسیر جواب دادی**.
Analytical query never goes direct to SQLite. **State which path you used.**

**زبان پاسخ = زبان سؤال / Response language = question language**
- سؤال فارسی → جواب فارسی
- English question → English answer
- Mixed → follow the dominant language

## لایه ویکی — ابزارها / Wiki Layer — Tools

```bash
python3 $DOCLIB_ROOT/doclib.py links sources/name -c <coll>   # لینک ورودی/خروجی + تشخیص شکستگی
python3 $DOCLIB_ROOT/doclib.py lint [-c <coll>]               # بازبینی سلامت / health check
python3 $DOCLIB_ROOT/doclib.py graph [-c <coll>]              # نقشه لینک‌ها / link map
```

`lint` شش چیز را می‌گیرد / `lint` catches six things: لینک شکسته (broken links)، منبع گم‌شده (missing source)، صفحه یتیم (orphan page)، صفحه‌ای که در `index.md` نیست (not in index)، صفحه بی‌منبع (no sources)، عنوان تکراری (duplicate title).

**بعد از هر ingest، `lint` بزن.** اگر ایراد داد، قبل از گزارش به کاربر درست کن.
**After every ingest, run `lint`.** Fix all errors before reporting to user.

### Lint محتوایی — کار من است، نه اسکریپت / Content Lint — My Job, Not Script

قبل از نوشتن یا آپدیت یک صفحه که منبع جدیدی برایش آمده: **عددهای صفحه موجود را با منبع جدید مقایسه کن.** اختلاف؟ → گزارش به کاربر، با هر دو عدد و منبعشان. تصمیم با کاربر است. هیچ‌وقت ساکت از روی عدد قدیمی رد نشو.
Before writing/updating a page with new source: **compare existing page numbers with new source.** Discrepancy? → report to user with both numbers + sources. User decides. Never silently overwrite.

### این آرشیو از کجا آمده / Where this archive came from

این سیستم از یک قالب قابل نصب ساخته می‌شود: `https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki`
This system is installed from an installable template: `https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki`

اگر آرشیو از قبل نصب شده، به آن ریپو نیاز نداری — `doclib.py` و `references/` کنار خود آرشیو هستند.
If the archive is already installed, you do not need that repo — `doclib.py` and `references/` sit beside the archive.

**مرجع کامل طراحی و پیت‌فال‌های بسته‌بندی:** `references/portability-design.md`
**Full design rationale and packaging pitfalls:** `references/portability-design.md`

## قرارداد صفحه ویکی / Wiki Page Contract

**قاعده برتری منابع / Source precedence:** `SKILL.md` تنها منبع حقیقت است. `references/*.md` فقط دانش تکمیلی‌اند؛ در تناقض، `SKILL.md` برنده است. اگر تناقض واقعی و مهم بود، از کاربر بپرس — حدس نزن و آخرین فایل خوانده‌شده را مبنا نگیر.
**Source precedence:** `SKILL.md` is the single source of truth. `references/*.md` are supplementary; on conflict `SKILL.md` wins. On a real conflict, ask the user — never let "last file read" silently win.

**هشدار کهنگی مراجع / Reference staleness:** بعد از هر تغییر در `SKILL.md`، مراجع مرتبط را همان جلسه همگام کن. نشانهٔ کهنگی: یک بلوک در `SKILL.md` کامل است ولی معادلش در `references/` ناقص یا با ترتیب متفاوت — مثلاً فهرست مراحل ingest یا قاعدهٔ `index.md`. قبل از اتکا، مرجع را با بخش مربوط مقایسه کن و در اختلاف `SKILL.md` را اجرا کن.
**Staleness:** whenever `SKILL.md` changes, sync the related `references/` file in the same session. Symptom of drift: a block is complete in `SKILL.md` but thin or differently ordered in `references/` (ingest step order, simplified `index.md` rules). Compare before relying; on disagreement follow `SKILL.md`.

### قاعده ویرایش مراجع / Reference Editing Rule

فایل مرجع جدید نساز و فایل موجود را **بدون درخواست کاربر** تغییر نده. اگر دیدی جزئیاتی در مرجع جا افتاده: اول به کاربر بگو (چه فایل، چه محتوا، چرا)، تأیید بگیر، بعد بنویس. `SKILL.md` تنها مرجعی است که خودت نگه می‌داری؛ `references/` با اجازهٔ کاربر رشد می‌کند.
Do not create reference files or restructure `references/` unprompted — propose the exact change (file, content, reason), get approval, then write.

**بازنویسی کامل مرجع موجود را با `write_file` انجام بده، نه `patch`.** ابزار `write_file` روی فایل مرجعی که در همین نوبت کامل خوانده نشده رد می‌شود (`stale_write_blocked`)؛ حتی خواندن صفحه‌ای (`offset`/`limit`) هم کافی نیست. الگوی کارآمد: `read_file` بدون `limit` (کل فایل) → `write_file` یک‌جا. اگر باز هم رد شد، نوشتن با پایتون در `browser_exec` کار می‌کند. قبل از هر بازنویسیِ دسته‌ای، `cp -r references /tmp/refs_backup_$(date +%s)` بگیر — برگشت‌پذیر بمان.
**Rewrite an existing reference with `write_file`, not many `patch` calls.** `write_file` refuses a file not fully read in the same turn (`stale_write_blocked`); a paginated read does not satisfy it. Read the whole file (no `limit`) then write once. If it is still refused, writing from Python in `browser_exec` works. Snapshot with `cp -r` before a batch rewrite so you can roll back.

**ترتیب امن / Safe order:** اول مرجع را **کامل** کن (تکرار با `SKILL.md` این مرحله مجاز است)، بعد اگر خواستی بلوک تکراری را از `SKILL.md` به لینک خلاصه کن — و آن خلاصه‌سازی تأیید جداگانه لازم دارد. برعکسش (حذف از `SKILL.md` قبل از کامل‌شدن مرجع) دانش را از دست می‌دهد.
**Safe order:** fill the reference in completely first (duplication with `SKILL.md` is fine at that stage), then — with separate approval — collapse the now-duplicated block in `SKILL.md` to a pointer. Never delete from `SKILL.md` before the reference is complete.

**هر فایل در `references/` باید در Reference Map درج شود.** فایلی که در نقشه نیست عملاً مرده است (هیچ‌وقت خوانده نمی‌شود). بعد از افزودن/حذف مرجع، نقشه را همان جلسه آپدیت کن و با `grep -c "<filename>" SKILL.md` بررسی کن که هر فایل حداقل یک ارجاع دارد.
**Every file in `references/` must appear in the Reference Map.** An unlisted file is dead — never read. Update the map in the same session; verify with `grep -c "<filename>" SKILL.md` that each file has at least one hit.

هر صفحه در `wiki/sources/` باید داشته باشد / Every page in `wiki/sources/` must have:
`# عنوان` / `# Title` · `> یک‌خط` / `> One-line` · `## خلاصه` / `## Summary` · `## محتوا` / `## Content` · `## منابع` / `## Sources` · `## مرتبط` / `## Related`.

- مسیر نسبی از محل فایل: `../entities/x.md` و `../../raw/files/y.pdf`
   Relative paths from file location
- `## منابع` اجباری است — نبودش = «صفحه بی‌منبع» در lint
   `## Sources` mandatory — missing = "no sources" in lint
- `index.md` **باید** به همه صفحات `sources/` لینک بدهد — تنها نجات‌دهنده از یتیمی
   `index.md` **must** link all `sources/` pages — only escape from orphan status
- بخش `مرتبط` همان چیزی است که ویکی را ویکی می‌کند؛ بدون آن هر صفحه یک جزیره است
   `## Related` is what makes wiki a wiki; without it every page is an island

ساختار کامل در `SCHEMA.md` → «قرارداد صفحه ویکی».
Full structure in `SCHEMA.md` → "Wiki Page Contract".

## نکات فنی مهم / Technical Notes

- **مسیر ریشه / Root path:** `DOCLIB_ROOT`، پیش‌فرض `~/archive`. هیچ مسیر ثابتی در این فایل نیست.
   `DOCLIB_ROOT`, default `~/archive`. No hardcoded path anywhere in this file.
- **نرمال‌سازی فارسی / Persian Normalization:** ذخیره با `normalize()`، ایندکس با `match_fold()`. دومی تهاجمی‌تر است تا «تأخیر» == «تاخیر» و «مسئول» == «مسیول».
   Storage via `normalize()`, indexing via `match_fold()`. Latter aggressive: "تأخیر" == "تاخیر", "مسئول" == "مسیول".
- **`fts_key`** ستون جداگانه در `chunks` است که فرم fold‌شده را نگه می‌دارد — FTS روی آن ایندکس می‌شود، ولی نمایش از `text` اصلی می‌آید.
   Separate `fts_key` column in `chunks` holds folded form — FTS indexes it, display uses original `text`.
- ارقام فارسی/عربی در ذخیره به لاتین تبدیل می‌شوند؛ جستجوی «۹۲۲۰» و «9220» هر دو کار می‌کند.
   Persian/Arabic digits → Latin in storage; search works with "۹۲۲۰" and "9220" alike.
- **ارقام فارسی در ویکی:** هر دو صورت عددی را بنویس — `۱۰ (10)` — چون `match_fold` ارقام را تبدیل می‌کند ولی **کلمات عددی را نه** (`ده` جدای از `۱۰` است). تکیه بر `۱۰ ابزار (ده ابزار)` اشتباه است: تست نشان داد `۱۰ ابزار` پیدا نشد.
   **Persian digits in wiki pages:** write both numeral forms — `۱۰ (10)`. `match_fold` converts digits but not number words, so the word form (`ده`) is not a substitute.
- DOCX خراب → fallback به استخراج خام XML (تابع `_docx_raw_xml`).
   Corrupt DOCX → fallback to raw XML extraction (`_docx_raw_xml`).
- **هنگام توضیح مکانیزم دیتابیس، ساختار را از خود دیتابیس بخوان، نه از حافظه.** نام جدول، ستون‌ها، و ترتیب اتصال‌ها سه بار پشت سر هم غلط گفته شد. `PRAGMA table_info(<table>)` + `SELECT sql FROM sqlite_master` + `PRAGMA index_list` بزن و بعد توضیح بده. اگر کاربر گفت «دوباره چک کن»، یعنی توضیح قبلی غلط بوده — همان لحظه دیتابیس را بخوان، نه اینکه همان روایت را بازگو کنی.
   **To explain the DB mechanism, read the schema from the database, not from memory.** Table names, columns, and JOIN keys were each stated wrong in successive turns. Run `PRAGMA table_info(<table>)`, `SELECT sql FROM sqlite_master`, `PRAGMA index_list` first. If the user says "check again", assume the previous explanation was wrong and read the DB.

## گزارش وضعیت به کاربر — بدون تغییر / Status Reporting — Read-Only

**اول تشخیص بده کدام حالت است / Decide which mode first:**

| کاربر گفت / User said | جواب / Answer |
|---|---|
| «فقط جواب» / «فقط سؤال جواب بده» / «کاری انجام نده» | **کوتاه: یک تا سه خط.** بدون جدول چندبخشی، بدون بخش‌بندی، بدون سؤال تصمیم پایانی. اگر جواب ادعای فنی است، اول چک کن، بعد کوتاه بگو. |
| «گزارش بده» / «بررسی کن و گزارش بده» | گزارش کامل طبق شش قاعدهٔ زیر، با سؤال تصمیم شماره‌دار در پایان. |
| «پیشنهاد بده» / «راهکارت چیه؟» | ارزیابی صریح پیشنهاد کاربر (کجا درست است، کجا مسدودکننده دارد) + جدول تصمیم + سؤال شماره‌دار. |

**«فقط جواب» یعنی کوتاه، نه یعنی حدس بزن.** ادعای فنی را همان لحظه از دیسک/دیتابیس/تاریخچه تأیید کن، بعد در یک پاراگراف جواب بده.
**"Just answer" means short, not guessed.** Verify the technical claim first, then answer in one paragraph.

کاربر غالباً می‌گوید «فقط گزارش بده، منتظر تأیید من بمون». در این حالت:
The user often says "just report, wait for my approval". In that case:

1. **اول ساختار را از دیسک بخوان، بعد گزارش بده.** فهرست فایل‌ها، `git ls-files`، `diff`، `wc -l` — نه از حافظه.
   **Read the structure from disk first** — `git ls-files`, `diff`, `wc -l` — not from memory.
2. **فهرست کامل بده، نه نمونه.** اگر ۶ فایل کهنه است، هر ۶ را نام ببر. جا انداختن یک فایل در گزارش بدتر از گزارش ندادن است.
   **Give the complete list.** Missing one file is worse than no report.
3. **بعد از هر گزارش، سؤال تصمیم صریح بپرس** — گزینه‌ها را شماره‌گذاری کن (الف/ب/ج) و مشخص کن کدام را توصیه می‌کنی و چرا.
   **End every report with explicit numbered decision questions** and say which you recommend.
4. **حتی وقتی «فقط جواب» می‌خواهد، اگر جواب یک ادعای فنی است، اول چک کن.** جملهٔ «فقط جواب» مجوز حدس زدن نیست.
   **Even when the user says "just answer", verify first if the answer is a technical claim.** "Just answer" is not permission to guess.
5. **سؤال «این را از کجا می‌دانی / چطور ساختی» → از تاریخچه بخوان، نه از حافظه.** `git log --reverse --format='%h %ad %s' --date=iso` و `git ls-tree -r --name-only <first-commit>` بزن و دقیق بگو کدام فایل **کپی** شد و کدام را **نوشتی**.
   **"How do you know / how did you build this" → read the history, not memory.** Run `git log --reverse` + `git ls-tree -r <first-commit>` and state exactly which files were **copied** from a live source and which you **authored**.
6. **پیش از ادعای «این را می‌توان دوباره ساخت»، منبع را نام ببر.** فایل‌های زنده در `$DOCLIB_ROOT/` و `skills/` هستند؛ `/tmp` و GitHub فقط کپی‌اند. صفحات ویکی/سایت (`Home.md`، `Architecture.md`، `CLI-Reference.md`، `docs/`) در هیچ منبع زنده‌ای نیستند و باید از روی همان منابع بازنویسی شوند — این را صریح بگو، نه اینکه القا کنی «همه‌چیز در repo است».
   **Before claiming "this can be regenerated", name the source.** Live files are in `$DOCLIB_ROOT/` and `skills/`; `/tmp` and GitHub are copies. The wiki/site pages exist in no live source and must be re-authored from those sources — say so explicitly instead of implying the repo holds everything.

## افزودن مجموعه جدید / Adding New Collection

با کاربر تأیید بگیر، بعد:
Confirm with user, then:

```bash
mkdir -p $DOCLIB_ROOT/collections/<new-name>/{raw/{files,web,audio,images},wiki/{sources,entities,concepts}}
```

و `COLLECTION.md`، `wiki/index.md`، `wiki/log.md` بساز (از مجموعه‌های موجود الگو بگیر).
Create `COLLECTION.md`, `wiki/index.md`, `wiki/log.md` (copy from existing collections).
