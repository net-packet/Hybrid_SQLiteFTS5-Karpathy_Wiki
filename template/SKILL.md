---
name: document-archive
description: Use for the user's document archive - ingest or search.
---

# آرشیو اسناد چندمجموعه‌ای / Multi-Collection Document Archive

کاربر یک آرشیو دائمی دارد در `/opt/data/documents/`.
User has a permanent archive at `/opt/data/documents/`.

**هر بار:** (1) فایل/لینک/ویس/عکس جدید رسید، یا (2) کاربر خواست در اسنادش بگردی، یا (3) سؤال درباره قرارداد/بودجه/نگهداشت/یادداشت‌هایش پرسید → اول این را بخوان:

```bash
cat /opt/data/documents/SCHEMA.md
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
/opt/data/documents/
├── SCHEMA.md          ← قانون اساسی آرشیو (اول بخوان)
├── index.db           ← SQLite + FTS5
├── doclib.py          ← اسکریپت استخراج/ایندکس/جستجو
└── collections/<name>/
    ├── COLLECTION.md  ← موضوع این مجموعه
    ├── raw/{files,web,audio,images}
    └── wiki/{index.md,log.md,sources,entities,concepts}
```

مجموعه‌های موجود: `office-works` (کارهای اداری / Admin Works), `maintenance-learning` (آموزش نگهداشت / Maintenance Learning), `ai-learning` (آموزش هوش مصنوعی / AI Learning).

**قاعده مقیاس‌بندی ویکی:** `entities/` و `concepts/` فقط وقتی ساخته می‌شوند که موضوع در **چند منبع** تکرار شده باشد. یک منبع → فقط `sources/` page. این از پر شدن ویکی با صفحات نیمه‌پر جلوگیری می‌کند.

**Wiki scaling rule:** `entities/` and `concepts/` only created when topic appears in **multiple sources**. One source → only `sources/` page. Prevents half-empty wiki pages.

## قواعد سخت / Hard Rules

1. **هرگز محتوای `raw/` را تغییر نده.** منبع حقیقت است.
   **Never modify `raw/` content.** It is the source of truth.
   > تنها استثنا: `raw/files/User-Reading-*.md` — فایل **فقط append + اصلاح علامت‌دار** است (بخش «منبع در حال مطالعه» را ببین).
   > Only exception: `raw/files/User-Reading-*.md` — **append-only + marked corrections** (see "Living Source" section).
1ب. **ابزار یا کتابخانه‌ای را که کار می‌کرد، با فرض «خراب است» عوض نکن.** وقتی فونت یا کتابخانه‌ای قبلاً خروجی درست داده، اولین فرض این است که **لایهٔ خودت** خراب است — نه آن. یک جلسه کامل صرف تعویض فونت شد که علت واقعی دو بار اعمال bidi بود؛ راهنمای مرجع هم با همان فرض غلط بازنویسی شد. تسلسل: علائم را از داده بگیر، از نزدیک‌ترین لایه شروع کن، و تنها وقتی داده ثابت کرد بیرونی خراب است به آن برو.
   **Do not swap out a tool or library that was working, on the assumption that it is broken.** When a font or library has already produced correct output, the first hypothesis is that **your own layer** is wrong, not it. An entire session went into swapping fonts when the real fault was bidi applied twice — and the reference recipe got rewritten carrying the same wrong assumption. Sequence: get the signal from data, start with the innermost layer, and only reach outward once the data proves it.
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
7ب. **دستور «آرشیو کن» پاسخ به سؤال مجموعه نیست.** اگر مجموعه‌ای را پیشنهاد دادی و کاربر جواب ندادی، و بعد گفت «اینو آرشیو کن» — این یعنی «این کار را انجام بده»، نه «و آن سؤال را هم با پیش‌فرض خودت جواب بده». **قبل از کپی، دوباره و به‌تنهایی بپرس: «کدام مجموعه؟»** حتی اگر پیشنهاد قبلی‌ات واضح بود، حتی اگر فایل تکراری همان مجموعه به نظر می‌رسید. پیشنهاد بی‌جواب ≠ تأیید.
   **"Archive it" is not an answer to the collection question.** If you proposed a collection, got no answer, and the user then says "archive this" — that means "do it", not "and answer my earlier question with your own default". **Ask again, on its own, before copying: which collection?** Even if your earlier proposal looked obvious, even if the file seemed to belong to the same collection. An unanswered proposal is not approval.

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
| تصمیم مسیر جستجو (نقطه‌ای vs تحلیلی) | `references/dual-path-query.md` | قبل از پاسخ به سؤال — شامل سه چک حساب قبل از تفسیر «روند» (جمع ستون‌ها vs جمع اعلامی، یکسانی قاعدهٔ محاسبه بین سال‌ها، تعداد نقاط) و ساخت نمودار فارسی با matplotlib: **رشتهٔ خام بده، reshaper/bidi نصب نکن**، سنجش جهت با همبستگی تصویر |
| نرمال‌سازی فارسی + FTS5 | `references/persian-normalization.md` | خطای فولدینگ یا ارقام فارسی در جستجو |
| Lint ساختاری + محتوایی | `references/wiki-lint.md` | قبل از گزارش به کاربر |
| بسته‌بندی آرشیو به‌عنوان قالب قابل انتقال | `references/portability-design.md` | کاربر پرسید «agent کسی دیگر هم بتواند همین سیستم را بسازد؟» یا طراحی repo تازه — شامل تولید `template/SKILL.md`، پیت‌فال `locales`، واگرایی مستندات دست‌نویس، و سنجش دوزبانگی با `diff` |
| نوشتن/بازنویسی README و مستندات ریپو | `references/readme-and-docs.md` | کاربر گفت «README خیلی خلاصه است» یا به README ریپوی دیگری ارجاع داد — شامل ساختار یازده‌بخشی، شمارش هر عدد از دیسک، `curl` روی هر لینک، و ادعاهایی که نباید بی‌چک نقل شوند (مجوز، تعداد صفحه، تعداد دستور) |

## جریان ingest / Ingest Flow

**قواعد مقدم بر جریان:** موضوع را تشخیص بده → **یک** مجموعه پیشنهاد بده → **تأیید بگیر**؛ بدون تأیید هیچ فایلی کپی نمی‌شود. جزئیات کامل هر مرحله و پیت‌فال‌های نوع منبع در `references/ingest-procedures.md`.

**Preconditions:** detect topic → propose **one** collection → get approval. Nothing is copied before approval. Full per-step detail and source-type pitfalls: `references/ingest-procedures.md`.

1. موضوع را تشخیص بده و مجموعه را پیشنهاد بده — **تأیید بگیر**
   Identify topic, propose collection — **get approval**
2. فایل را به پوشه درست `raw/` کپی کن
   Copy file to correct `raw/` folder
3. ایندکس کن:
   ```bash
   python3 /opt/data/documents/doclib.py add <path> -c <collection>
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
9. `python3 /opt/data/documents/doclib.py lint -c <collection>` بزن و ایرادها را درست کن
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

`whisper-large-v3` با زبان `fa`. **نمونه کد:** `/opt/data/cache/scratch/stt_test.py`.

```bash
KEY=$(grep -E '^GROQ_API_KEY=' /opt/data/.env | head -1 | cut -d= -f2- | tr -d '"')
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
python3 /opt/data/documents/doclib.py ur-add <slug> -p 47 -q "متن دقیق جمله" -t "موضوع" -c <collection>
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
python3 /opt/data/documents/doclib.py search "کوئری"              # همه مجموعه‌ها / all collections
python3 /opt/data/documents/doclib.py search "کوئری" -c office-works
python3 /opt/data/documents/doclib.py search "کوئری" -f contract
python3 /opt/data/documents/doclib.py list [-c <collection>]
python3 /opt/data/documents/doclib.py stats
python3 /opt/data/documents/doclib.py show <file_id>
```

**مسیر ۲ — سؤال ترکیبی/تحلیلی / Analytical Query** («روند سه ساله»، «مقایسه کن»، «تناقضی هست؟" / "3-year trend", "compare", "any contradiction?"). ویکی نقطه شروع است، **نه آخرین راه‌حل** / Wiki is the starting point, **not the last resort**:

1. `wiki/index.md` را بخوان / Read `wiki/index.md`
2. صفحه(های) مرتبط را پیدا کن و بخوان / Find & read relevant pages
3. `doclib.py links sources/X -c <coll>` بزن → صفحات مرتبط بعدی / Run → next linked pages
4. ترکیب کن / Combine

**سؤال نقطه‌ای جواب نداد → مسیر ۲. سؤال تحلیلی جواب نداد → جستجوی هدفمند (مسیر ۱).**
Point query fails → Path 2. **Analytical query fails → targeted search (Path 1).**
**سؤال تحلیلی هرگز مستقیم به SQLite نمی‌رود. **بگو از کدام مسیر جواب دادی**.
Analytical query never goes direct to SQLite. **State which path you used.**

**قبل از تفسیر «روند»، حساب سند را چک کن.** جمع ستون‌ها باید با جمع کل اعلامی بخواند؛ اگر نمی‌خواند، اختلاف را بنویس و رشد درصدی را روی عدد مشکوک نساز. و اگر آرشیو فقط دو سال دارد، «مقایسه» است نه «روند» — همان را بگو. جزئیات و ساخت نمودار فارسی در `references/dual-path-query.md`.
**Check the document's arithmetic before interpreting a "trend".** Column totals must match the stated grand total; if they do not, state the gap and do not build a growth percentage on the suspect figure. And with only two years in the archive it is a comparison, not a trend — say so. Detail and Persian chart recipe in `references/dual-path-query.md`.

**در نمودار matplotlib رشتهٔ فارسی خام بده — `arabic-reshaper` و `python-bidi` نصب نکن.** matplotlib خودش با `raqm` می‌چیند؛ آن دو پکیج متن را دو بار پردازش می‌کنند و نتیجه **آینه** می‌شود. نشانه: حروف چسبیده ولی کلمه برعکس. سنجش جهت با مقایسهٔ همبستگی تصویر در برابر نسخهٔ آینه‌شده، نه با چشم — دستور در `references/dual-path-query.md`.
**Feed matplotlib the raw Persian string — do not install `arabic-reshaper` or `python-bidi`.** matplotlib shapes via `raqm` itself; those two packages process the text twice and the result comes out **mirrored**. Tell-tale: letters joined but the word reads backwards. Verify direction by comparing image correlation against the mirrored version, never by eye — recipe in `references/dual-path-query.md`.

**زبان پاسخ = زبان سؤال / Response language = question language**
- سؤال فارسی → جواب فارسی
- English question → English answer
- Mixed → follow the dominant language

## لایه ویکی — ابزارها / Wiki Layer — Tools

```bash
python3 /opt/data/documents/doclib.py links sources/name -c <coll>   # لینک ورودی/خروجی + تشخیص شکستگی
python3 /opt/data/documents/doclib.py lint [-c <coll>]               # بازبینی سلامت / health check
python3 /opt/data/documents/doclib.py graph [-c <coll>]              # نقشه لینک‌ها / link map
```

`lint` شش چیز را می‌گیرد / `lint` catches six things: لینک شکسته (broken links)، منبع گم‌شده (missing source)، صفحه یتیم (orphan page)، صفحه‌ای که در `index.md` نیست (not in index)، صفحه بی‌منبع (no sources)، عنوان تکراری (duplicate title).

**بعد از هر ingest، `lint` بزن.** اگر ایراد داد، قبل از گزارش به کاربر درست کن.
**After every ingest, run `lint`.** Fix all errors before reporting to user.

### Lint محتوایی — کار من است، نه اسکریپت / Content Lint — My Job, Not Script

قبل از نوشتن یا آپدیت یک صفحه که منبع جدیدی برایش آمده: **عددهای صفحه موجود را با منبع جدید مقایسه کن.** اختلاف؟ → گزارش به کاربر، با هر دو عدد و منبعشان. تصمیم با کاربر است. هیچ‌وقت ساکت از روی عدد قدیمی رد نشو.
Before writing/updating a page with new source: **compare existing page numbers with new source.** Discrepancy? → report to user with both numbers + sources. User decides. Never silently overwrite.

### SKILL.md دو نسخه دارد / SKILL.md has two versions

| نسخه / Version | مسیر / Path | مسیر ریشه / Root |
|---|---|---|
| زنده / live | `skills/productivity/document-archive/SKILL.md` | `/opt/data/documents` (این ماشین) |
| قابل حمل / portable | `template/SKILL.md` در ریپوی قالب | `$DOCLIB_ROOT`، پیش‌فرض `~/archive` |

**فقط یک ریپو وجود دارد:** `Hybrid_SQLiteFTS5-Karpathy_Wiki` (قالب قابل نصب). هر اشاره به ریپوی قدیمی حذف شده و نباید برگردد — نه در این فایل، نه در `references/`، نه در `template/`.
**Only one repo exists:** `Hybrid_SQLiteFTS5-Karpathy_Wiki` (the installable template). Every reference to the retired repo was removed and must not return — not here, not in `references/`, not in `template/`.

```bash
# هیچ اشاره‌ای نباید بماند / no reference should remain
grep -rn "Hybrid_SQLite-Karpathy" /opt/data/skills/productivity/document-archive/ \
  /tmp/Hybrid_SQLiteFTS5-Karpathy_Wiki/ --exclude-dir=.git --exclude-dir=node_modules || echo "clean"
```

**قاعدهٔ همگام‌سازی — دوطرفه / Sync rule — bidirectional:** هر تغییری در **قواعد سخت**، **قرارداد صفحه ویکی**، **مسیر دوگانهٔ جستجو**، **living-source**، **فهرست مراحل ingest**، **پیت‌فال‌های Groq**، یا **دستور نمودار فارسی** → همان جلسه در `template/SKILL.md` هم اعمال شود. **و برعکس:** هر تغییری که در `template/SKILL.md` یا در ریپو انجام دادی → همان جلسه در این فایل زنده هم بیاید. یک‌طرفه چک کردن یعنی اسکیل زنده جلو می‌افتد و قالب عقب می‌ماند — و `setup.py` همان قالب عقب‌مانده را نصب می‌کند.
**Sync rule — bidirectional:** any change to the **hard rules**, **wiki page contract**, **dual query path**, **living-source**, **ingest step list**, **Groq pitfalls**, or the **Persian chart recipe** must be applied to `template/SKILL.md` in the same session. **And the reverse:** any change made in `template/SKILL.md` or elsewhere in the repo comes back to this live file the same session. One-directional checking lets the live skill run ahead while the template falls behind — and `setup.py` installs the one that fell behind.

**محتوا از نسخهٔ بهتر، اقتدار در ریپو / Content from the better copy, authority in the repo.** وقتی دو نسخه واگرا شدند، سؤال «کدام ملاک است؟» جواب ساده ندارد — دو سؤال جداست. **محتوا** را از نسخه‌ای بردار که در عمل استفاده می‌شود (معمولاً اسکیل زنده، چون هر روز اجرا می‌شود و اصلاح‌های واقعی را دارد)؛ **اقتدار** را در `template/SKILL.md` نگه دار، چون `setup.py` همان را نصب می‌کند و نسخهٔ زنده بیرون از ریپو و بی‌نسخه است. اگر اسکیل زنده را ملاک اعلام کنی، هر نصب تازه همچنان نسخهٔ ناقص را می‌گیرد — ملاکی که پخش نمی‌شود ملاک نیست. پس جهت درست: محتوا از زنده → قالب، و قالب مرجعِ اعلام‌شده بماند.
**Content from the better copy, authority in the repo.** When the two diverge, "which one is the criterion?" splits into two questions. Take the **content** from the copy actually in use (usually the live skill — it runs daily and carries the real fixes); keep **authority** in `template/SKILL.md`, because `setup.py` installs that one and the live skill sits outside the repo, unversioned. Declaring the live skill the criterion leaves every fresh install shipping the truncated version — a criterion that is not distributed is not a criterion. Correct direction: content live → template, and the template stays the declared reference.

**وقتی کاربر دامنه را به «فقط محتوا» محدود کرد، همان را بده و صریح بگو چه تضمینی از دست می‌رود.** گزینهٔ حداقلی (هم‌تراز کردن محتوا) را اجرا کن، اسکریپت نگهبان/CI را نساز، و در پایان یک خط بنویس که بدون بررسی مکانیکی این واگرایی می‌تواند برگردد. سکوت دربارهٔ ریسک یعنی کاربر فکر می‌کند تضمین دارد.
**When the user scopes it to "content only", deliver that and say plainly what guarantee is lost.** Run the minimal alignment, skip the guard script/CI, and close with one line noting the drift can return without a mechanical check. Silence about the risk reads as a guarantee.

**نسخهٔ قابل حمل را با اسکریپت از فایل زنده تولید کن، نه با بازنویسی دستی** — دست‌نویسی ۴۶۵ خط، قواعد سخت را بی‌صدا تغییر می‌دهد. تبدیل مکانیکی: مسیر → `$DOCLIB_ROOT`، کلید → `$GROQ_API_KEY`. دستور کامل در `references/portability-design.md`.
**Generate the portable version from the live file with a script, never by hand** — hand-writing 465 lines silently alters the hard rules. Mechanical transform: paths → `$DOCLIB_ROOT`, key → `$GROQ_API_KEY`. Full recipe in `references/portability-design.md`.

آنچه **همگام نمی‌شود** (مخصوص همین ماشین است): مسیرهای `/opt/data/...` و فهرست ثابت مجموعه‌ها.
What does **not** sync (machine-specific): `/opt/data/...` paths and the fixed collection list.

**بررسی واگرایی / Drift check:** بلوک قواعد سخت را در دو فایل با هم diff کن — باید یکی باشند. و همان فهرست را با خلاصهٔ `AGENTS.md` بسنج: `AGENTS.md` فقط ۴ قاعده دارد و باید صریح بگوید «فهرست کامل در `SKILL.md` است» — وگرنه agent بقیهٔ قواعد را هرگز نمی‌خواند.
**Drift check:** diff the hard-rules block across both files — they must match. Then check it against the `AGENTS.md` summary: `AGENTS.md` carries only 4 rules and must say explicitly that the full list is in `SKILL.md`, or the agent never learns the rest.

**قبل از diff، توکن‌های عمداً متفاوت را نرمال کن.** مسیر ریشه تنها تفاوت مجاز است؛ اگر نرمال نکنی، diff پر از نویز مسیر می‌شود و تفاوت محتوایی واقعی را نمی‌بینی. `sed 's|\$DOCLIB_ROOT|/opt/data/documents|g'` روی نسخهٔ قالب بزن، بعد diff — خروجی خالی یعنی بلوک‌ها یکی‌اند.
**Normalize the deliberately-different tokens before diffing.** The root path is the only allowed difference; without normalizing, the diff is all path noise and you cannot see a real content difference. Run `sed 's|\$DOCLIB_ROOT|/opt/data/documents|g'` on the template block, then diff — empty output means the blocks match.

```bash
sed -n '/^## جریان ingest/,/^## پردازش انواع/p' template/SKILL.md \
  | sed 's|\$DOCLIB_ROOT|/opt/data/documents|g' > /tmp/tpl
sed -n '/^## جریان ingest/,/^## پردازش انواع/p' \
  /opt/data/skills/productivity/document-archive/SKILL.md > /tmp/live
diff /tmp/tpl /tmp/live && echo "ingest blocks identical"
```

**همگام‌سازی را در سطح بلوک انجام بده، نه فایل کامل.** استخراج بلوک از منبع، جایگزینی همان بلوک در مقصد، و حفظ تفاوت‌های محلی (مسیر، کلید) — کم‌ریسک‌تر از بازنویسی کل فایل است و بقیهٔ بخش‌ها را دست‌نخورده می‌گذارد.
**Sync at block level, not whole-file.** Extract the block from the source, replace the same block in the destination, preserve local differences (path, key) — lower risk than rewriting the file and it leaves every other section untouched.

```python
import pathlib
def block(text, start="## جریان ingest", end="## پردازش انواع"):
    i = text.index(start); j = text.index(end, i)
    return text[i:j]
src = pathlib.Path('template/SKILL.md').read_text(encoding='utf-8')
dst_p = pathlib.Path('/opt/data/skills/productivity/document-archive/SKILL.md')
dst = dst_p.read_text(encoding='utf-8')
dst_p.write_text(dst.replace(block(dst), block(src).replace('$DOCLIB_ROOT', '/opt/data/documents'), 1), encoding='utf-8')
```
```bash
awk '/^## قواعد سخت/,/^## زبان مراجع/' SKILL.md > /tmp/a
awk '/^## قواعد سخت/,/^## زبان مراجع/' /tmp/Hybrid_SQLiteFTS5-Karpathy_Wiki/template/SKILL.md > /tmp/b
diff /tmp/a /tmp/b && echo "hard rules in sync"
# و شمارش قاعده‌ها / and count the rules on each side
grep -cE '^[0-9]+\. \*\*' /tmp/a; grep -cE '^[0-9]+\. \*\*' /tmp/Hybrid_SQLiteFTS5-Karpathy_Wiki/AGENTS.md
```

### قاعدهٔ آینه — `template/` باید با آرشیو زنده یکی باشد / Mirror rule

ریپوی `Hybrid_SQLiteFTS5-Karpathy_Wiki` قالب قابل نصب است. `template/` در آن **آینهٔ** فایل‌های زندهٔ آرشیو است، نه نسخهٔ مستقل.
The `Hybrid_SQLiteFTS5-Karpathy_Wiki` repo is an installable template. Its `template/` is a **mirror** of the live archive files, not an independent copy.

| فایل زنده / Live file | آینه / Mirror |
|---|---|
| `$DOCLIB_ROOT/doclib.py` | `src/doclib.py` |
| `$DOCLIB_ROOT/SCHEMA.md` | `template/SCHEMA.md` |
| `$DOCLIB_ROOT/collections/*/COLLECTION.md` | `template/collections/*/COLLECTION.md` |
| `skills/.../document-archive/references/*.md` | `template/references/*.md` |
| `skills/.../document-archive/SKILL.md` | `template/SKILL.md` (تبدیل‌شده / transformed) |

**قاعده / Rule:** هر تغییر در یک فایل زنده → همان جلسه در آینه‌اش هم اعمال شود، بعد commit و push.
**Any change to a live file syncs to its mirror in the same session, then commit and push.**

**قبل از ادعای «آینه همگام است»، diff کن — از حافظه یا commit message نگو:**
**Before claiming the mirror is in sync, diff it — never report from memory or a commit message:**

```bash
cd /tmp/Hybrid_SQLiteFTS5-Karpathy_Wiki
diff -q src/doclib.py $DOCLIB_ROOT/doclib.py
diff -q template/SCHEMA.md $DOCLIB_ROOT/SCHEMA.md
for f in template/references/*.md; do
  diff -q "$f" /opt/data/skills/productivity/document-archive/references/$(basename "$f")
done
```

`git log` دروغ می‌گوید — یک commit می‌تواند فقط مستندات را بیاورد و کد را نه.
`git log` lies — a commit can carry docs and not the code.

**دو استثنای عمدی — اینها «ناهمگامی» نیستند / Two intentional exceptions — not drift:**

1. **بخش‌های نصب فقط در `template/`:** «اگر آرشیو هنوز نصب نشده» و «این آرشیو از کجا آمده» دستور `git clone` و `setup.py` دارند. برای آرشیو نصب‌شده بی‌معنی‌اند، برای کاربر جدید ضروری. **حذفشان نکن.**
2. **قواعد VitePress فقط در نسخهٔ زنده:** سه خطای بیلد و پیت‌فال `base` مخصوص تولید `docs/` است و به کار آرشیو مربوط نیست. **به `template/` منتقلشان نکن.**

**Install sections live only in `template/`:** they carry `git clone` and `setup.py` — meaningless for an installed archive, essential for a new user. **Do not delete them.**
**VitePress rules live only in the live copy:** the build errors and the `base` pitfall belong to `docs/` generation, not to archiving. **Do not copy them into `template/`.**

### بازبینی یکپارچگی جریان ingest در کل ریپو / Auditing ingest-flow consistency

وقتی کاربر می‌گوید «مراحل ingest را در همهٔ فایل‌ها چک کن»، این نه بررسی را به ترتیب بزن. هیچ‌کدام از حافظه یا از commit message — همه از دیسک.
When the user asks to check ingest steps across every file, run these nine checks in order. None from memory or a commit message — all from disk.

**اگر کاربر گفت «یک بار دیگر چک کن»، یعنی گذر قبلی ناقص بوده — دامنه را باز کن، نه همان grepها را تکرار.** گذر اول معمولاً محتوا را چک می‌کند (آیا `add` دوم هست؟) و شمارش واقعی هر فایل را نمی‌شمارد؛ گذر دوم است که واگرایی نسخه‌ها را پیدا می‌کند. پس در گذر دوم فایل‌هایی را باز کن که عنوانشان «ingest» نیست ولی دنبالهٔ دستور نشان می‌دهند، و **نسخهٔ نصب‌شده** را هم بسنج — نه فقط فایل‌های ریپو.
**If the user says "check again", the previous pass was incomplete — widen the net, do not re-run the same greps.** A first pass usually checks content (is the second `add` there?) and never counts the actual steps per file; the second pass is what finds the version divergence. So on the second pass, open files not titled "ingest" that still show a command sequence, and test the **installed** copy too — not just the repo files.

**۱. محتوا، نه شمارش.** اول ببین `add` دوم (ایندکس کردن صفحهٔ ویکی) در همهٔ روایت‌ها هست:
```bash
grep -rln "add.*wiki\|add.*صفحه" --include="*.md" . --exclude-dir=.git --exclude-dir=dist
```

**۲. شمارش سرفصل‌ها در هر فایل جدا.** عددی که فایل دربارهٔ خودش می‌گوید را با تعداد واقعی مقایسه کن. مرجع رسمی جریان `wiki/layer3/Ingest-Workflow.md` است (۹ مرحله) — اگر فایل دیگری فهرست مراحل کامل دارد، آن یک نسخهٔ موازی است و باید حذف شود، نه همگام:
```bash
for f in wiki/layer3/Ingest-Workflow.md template/SKILL.md \
         template/references/ingest-procedures.md docs/guide/ingest.md docs/fa/guide/ingest.md; do
  echo "$f: $(grep -c '^## Step\|^### Step\|^| [0-9]\|^[0-9]\.' "$f")"
done
```

**۳. ادعاهای عددی را جمع کن.** «eight-step»، «۸ مرحله»، «39 pages» — این‌ها بی‌صدا کهنه می‌شوند:
```bash
grep -rn "eight-step\|8 مرحله\|۸ مرحله\|nine-step\|9 مرحله\|39 pages\|30 pages" \
  --include="*.md" . --exclude-dir=.git --exclude-dir=dist --exclude-dir=node_modules
find wiki -name '*.md' | wc -l   # عدد واقعی
```

**۴. فایل تولیدشده را از دست‌نویس جدا کن.** `docs/reference/` با `tools/build_docs.py` از `wiki/` ساخته می‌شود؛ `docs/guide/` و `docs/fa/guide/` **دست‌نویس**‌اند و هیچ‌چیز آن‌ها را همگام نمی‌کند. پس هر اصلاح در `wiki/` باید **جداگانه** در ده فایل دست‌نویس (`guide/{ingest,cli,install,architecture}.md` × EN/FA) هم اعمال شود. تأیید:
```bash
python3 tools/build_docs.py && git status --porcelain docs/reference   # خالی = تولیدشده همگام است
```

**۴ب. ولی قبل از همگام‌کردن دستی، بپرس آیا آن صفحهٔ دست‌نویس اصلاً باید وجود داشته باشد.** همگام‌کردن دستی یک نسخهٔ تکراری، همان مشکلی را که تازه حل کردی یک لایه بالاتر بازمی‌سازد: صفحه‌ای که شش مرحله از نُه مرحله را با شمارش متفاوت تکرار می‌کند. اگر دلیل حذف یک صفحه «تکرار باعث واگرایی می‌شود» بود، تکرارِ باقی‌مانده را با ویرایش دستی زنده نگه ندار — یا حذفش کن، یا صریح بنویس «این خلاصه است، مرجع X است و در اختلاف آن برنده است» و فهرست مراحلش را بردار.
**4b. But before hand-syncing, ask whether that hand-written page should exist at all.** Hand-syncing a duplicate recreates, one layer up, the exact problem you just solved: a page carrying six of nine steps with different numbering. If the reason for deleting a page was "duplication causes drift", do not keep the surviving duplicate alive by hand-editing it — either delete it, or label it "this is a summary; X is the reference and wins on conflict" and strip its step list.

**۴ج. علت ساختاری وجود مسیر دست‌نویس را چک کن.** اگر `wiki/` هیچ صفحهٔ فارسی ندارد، `build_docs.py` هرگز نمی‌تواند `docs/fa/` را بسازد — پس آن مسیر مجبوراً دست‌نویس است و تا وقتی `wiki/fa/` ساخته نشود، هیچ‌وقت تولیدی نمی‌شود. این را در گزارش بگو، نه اینکه فقط «دست‌نویس است» را به‌عنوان واقعیت تحویل بدهی.
**4c. Check the structural reason the hand-written path exists.** If `wiki/` has no Persian pages, `build_docs.py` can never generate `docs/fa/` — so that path is necessarily hand-written and will stay that way until `wiki/fa/` exists. Say that in the report instead of delivering "it is hand-written" as a bare fact.

**۴د. حذف صفحه از `wiki/` صفحهٔ دست‌نویسِ هم‌نام را حذف نمی‌کند.** اگر `wiki/layer3/First-Ingest.md` را پاک کردی، `docs/guide/ingest.md` با عنوان `# First ingest` سر جایش می‌ماند و روی سایت منتشر می‌شود — کاربر همان را می‌بیند و می‌گوید «هنوز هست». قبل از گزارش «حذف شد»، فایل‌های دست‌نویس را هم با **عنوان** grep کن، نه فقط با نام فایل:
**4d. Deleting from `wiki/` does not delete the same-named hand-written page.** Delete `wiki/layer3/First-Ingest.md` and `docs/guide/ingest.md` keeps its `# First ingest` title and keeps shipping. The user sees it and says "it is still there". Before reporting "deleted", grep the hand-written files by **title**, not just filename:

```bash
grep -rn "^# First ingest\|First-Ingest" docs --include="*.md" --include=".mts" | grep -v docs/reference
```

**۵. ادعای فنی را با اجرا بسنج، نه با خواندن.** اگر فایلی می‌گوید «lint این را می‌گیرد»، همان سناریو را در یک آرشیو تازه بساز و ببین واقعاً می‌گیرد یا نه. در این ریپو دو ادعای غلط این‌طور پیدا شد: «`add` فقط `raw/` را قبول می‌کند» و «ترتیب معکوس را lint می‌بیند» — هر دو با تست رد شدند.

**Check the claim by running it, not by reading it.** If a file says "lint catches this", build that exact scenario in a fresh archive and see. Two false claims in this repo were found that way, both disproved by test.

**بعد از رد کردن یک ادعا، آن را بر اساس «مفهوم» grep کن، نه بر اساس جمله‌ای که اصلاح کردی.** ادعای غلط در فایل‌های دیگر با عبارت دیگری تکرار شده و همان‌جا می‌ماند. «`add` فقط `raw/` را قبول می‌کند» سه بار برگشت: یک بار در `AGENTS.md`، یک بار در `CLI-Reference.md` («must be inside `collections/<name>/raw/`»)، یک بار در `Err-Outside-Raw.md` («a directory … must also be inside `raw/`»). اصلاح فقط در فایلی که دیده بودی، دو نسخهٔ دیگر را زنده نگه می‌دارد.
**After disproving a claim, grep for it by CONCEPT, not by the sentence you fixed.** The same false claim restates itself in other files with different wording and survives. "`add` only accepts `raw/`" came back three times — `AGENTS.md`, `CLI-Reference.md` ("must be inside `collections/<name>/raw/`"), `Err-Outside-Raw.md` ("a directory … must also be inside `raw/`"). Fixing only the file you happened to see leaves the other copies alive.

```bash
grep -rn "inside .*raw/\|داخل .*raw/" --include="*.md" . --exclude-dir=.git --exclude-dir=dist
```

**۶. یک رویه = یک صفحه.** اگر دو صفحهٔ ویکی همان جریان را با شمارش متفاوت دارند، آن تکرار است — نه تقسیم کار. هر دو نسخه را نگه‌داشتن تضمین می‌کند که یک روز واگرا شوند (همین اتفاق باعث شد «هشت مرحله» در چهار فایل بماند و دو فایل در ترتیب `index.md` و `add` مخالف هم شوند). راه‌حل: مرجع را یکی کن، محتوای انحصاری صفحهٔ دیگر را به آن منتقل کن، صفحهٔ دوم را **حذف** کن، و هر صفحهٔ باقی‌مانده را وادار کن صریح بگوید «مرجع آن صفحه است و در اختلاف آن برنده است».

**One procedure = one page.** Two wiki pages carrying the same flow with different numbering is duplication, not division of labour — keeping both guarantees they diverge (that is how "eight steps" survived in four files and two files ended up disagreeing on whether `index.md` or `add` comes first). Collapse to one reference, move the other page's exclusive content into it, **delete** the second, and make every remaining page say explicitly that the reference wins.

**وقتی کاربر می‌پرسد «چرا هم X داریم هم Y؟» — ادعای تقسیم کار را از خود فایل‌ها بخوان، بعد تست کن که واقعاً برقرار است یا نه.** هر دو صفحه معمولاً در خط سومشان تقسیم کار را توضیح می‌دهند («این یکی آموزش است، آن یکی مرجع»). آن جمله را نقل کن، بعد نشان بده که در عمل نقض می‌شود: هر دو فهرست مراحل کامل دارند، با شمارش متفاوت. جواب درست دو بخش دارد — «دلیل طراحیشان این بود» و «ولی در واقعیت کار نمی‌کند، چون…». فقط بخش اول = توجیه وضع موجود، نه جواب.
**When the user asks "why do we have both X and Y?" — read the claimed division of labour from the files themselves, then test whether it actually holds.** Both pages usually state it in their third line ("this one is the tutorial, that one is the reference"). Quote it, then show where it breaks: both carry the full step list, with different numbering. A correct answer has two parts — "this was the design intent" and "but it does not hold, because…". Only the first part is a justification of the status quo, not an answer.

**۷. نسخهٔ ناقص از نسخهٔ تکراری خطرناک‌تر است.** بعد از یکی‌کردن مرجع، صفحاتی می‌مانند که «روایت» هستند و فقط چند مرحله را نشان می‌دهند. خطرناک‌ترین حالت: روایت مراحل ۱ تا ۴ را دارد و بعد مستقیم می‌پرد به `lint` — یعنی **دقیقاً مرحله‌ای را حذف کرده که بقیهٔ ریپو با هشدار پوشش می‌دهد** (`add` دوم). خواننده‌ای که فقط آن صفحه را دنبال کند، صفحه‌ای می‌سازد که `search` پیدایش نمی‌کند. پس در بازبینی، هر صفحه‌ای را که **دنبالهٔ دستور** نشان می‌دهد چک کن، نه فقط صفحاتی که عنوانشان «workflow» یا «ingest» است. روایت ناقص دو راه دارد: مرحلهٔ گم‌شده را اضافه کن، یا همان‌جا که می‌برد صریح بنویس «بقیهٔ مراحل در <مرجع>». سکوت ممنوع.
**A truncated copy is more dangerous than a duplicate.** After collapsing to one reference, narrative pages remain that show only a few steps. Worst case: the narrative covers steps 1–4 then jumps straight to `lint` — deleting exactly the step the rest of the repo warns about (the second `add`). A reader following only that page builds a page `search` cannot find. So audit **every page that shows a command sequence**, not just ones titled "workflow" or "ingest". A truncated narrative has two legal fixes: add the missing step, or say explicitly at the point where it stops "the rest is in <reference>". Silence is not one of them.

**۸. placeholderهای کهنه در بلوک دستور را grep کن.** `add <path-inside-raw/>` از همهٔ grepهای متنی رد می‌شود چون نه جمله است نه دستور واقعی — یک placeholder با کروشه. همین‌طور ادعاهای «چهار دستور» / «four commands» که مثل «هشت مرحله» بی‌صدا کهنه می‌شوند. هر دو را در همان گذر شمارش بگیر:
**Grep for stale placeholders in command blocks.** `add <path-inside-raw/>` slips past every prose grep — it is neither a sentence nor a real command, just an angle-bracket placeholder. Same for "four commands" style claims, which go stale exactly like "eight steps". Catch both in the same count pass:

```bash
grep -rn "inside-raw\|raw/>\|<path" --include="*.md" . --exclude-dir=.git --exclude-dir=dist
grep -rn "four commands\|چهار دستور\|N commands" --include="*.md" . --exclude-dir=.git --exclude-dir=dist
```

**۹. دو نسخهٔ `SKILL.md` را مرحله‌به‌مرحله با هم بسنج — و نسخهٔ نصب‌شده را هم.** بعد از یکی‌کردن مرجع، بزرگ‌ترین خطر این است که `template/SKILL.md` (که `setup.py` کپی می‌کند) از اسکیل زنده عقب بماند و **نصب تازه همان نسخهٔ ناقص را پخش کند**. `git status` تمیز این را نشان نمی‌دهد، چون اسکیل زنده بیرون از ریپو است.
**Diff the two `SKILL.md` copies step by step — and the installed one too.** After collapsing to one reference, the biggest risk is `template/SKILL.md` (which `setup.py` copies) falling behind the live skill, so **every fresh install ships the truncated version**. A clean `git status` does not reveal this — the live skill sits outside the repo.

```bash
# شمارش مرحله در هر سه نسخه — باید یکی باشند
for f in /opt/data/skills/productivity/document-archive/SKILL.md \
         /tmp/Hybrid_SQLiteFTS5-Karpathy_Wiki/template/SKILL.md; do
  echo "$f: $(sed -n '/^## جریان ingest/,/^## پردازش انواع/p' "$f" | grep -c '^[0-9]\.')"
done
# و نسخه‌ای که کاربر واقعاً می‌گیرد
rm -rf /tmp/probe && python3 src/setup.py --root /tmp/probe --skip-install >/dev/null 2>&1
echo "installed: $(sed -n '/^## جریان ingest/,/^## پردازش انواع/p' /tmp/probe/SKILL.md | grep -c '^[0-9]\.')"
grep -c 'show <file_id>' /tmp/probe/SKILL.md   # مرحلهٔ حیاتی که بی‌صدا حذف می‌شود
```

**هم‌شماره بودن کافی نیست — محتوا را هم بسنج.** دو فهرست می‌توانند هر دو ۹ مرحله باشند و یکی `search`+`show` داشته باشد و دیگری «گزارش به کاربر» اضافه کرده باشد. مرحله‌ها را کنار هم بچین (`grep '^[0-9]\.'` روی هر دو) و تفاوت را نام ببر. مرحله‌ای که در مرجع هست و در قالب نیست، **حذف بی‌صدا** است؛ مرحله‌ای که در قالب هست و در مرجع نیست، **افزودهٔ محلی** است — دومی را از فهرست بیرون ببر (مثلاً «گزارش به کاربر» جای آن زیر فهرست است، نه مرحلهٔ ۸).
**Matching counts is not enough — compare content.** Two lists can both have nine steps while one carries `search`+`show` and the other added "report to user". Lay them side by side and name the difference. A step in the reference but missing from the template is a **silent deletion**; a step in the template but not the reference is a **local addition** — move it out of the list (e.g. "report to user" belongs below the list, not as step 8).

**قاعدهٔ همگام‌سازی دوطرفه است.** «هر تغییر در قالب → در زنده هم اعمال شود» نیمی از کار است؛ نیمهٔ دیگر: هر تغییر در زنده → همان جلسه در قالب. اگر فقط یک جهت را چک کنی، اسکیل زنده جلو می‌افتد و قالب عقب می‌ماند — و همان نسخهٔ عقب‌مانده است که نصب می‌شود.
**The sync rule is bidirectional.** "Any change to the template → apply to live" is half of it; the other half: any change to live → the template in the same session. Check one direction only and the live skill runs ahead while the template falls behind — and the one that falls behind is the one that gets installed.

### حذف یک صفحه — سه جا باید پاک شود / Deleting a page — three places to clean

`tools/build_docs.py` فقط **کپی می‌کند**، حذف نمی‌کند. فایل تولیدشده در `docs/reference/` بعد از حذف منبعش باقی می‌ماند و سایت همچنان صفحهٔ مرده را سرو می‌کند. بعد از هر حذف، به ترتیب:
`tools/build_docs.py` only **copies** — it never deletes. The generated file in `docs/reference/` survives its source and the site keeps serving a dead page. After any deletion, in order:

```bash
rm wiki/<path>.md docs/reference/<path>.md   # ۱. منبع + کپی تولیدشده
python3 tools/build_docs.py                  # ۲. بازگشت به حالت همگام
grep -rn "<Page-Name>" --include="*.md" . --exclude-dir=.git --exclude-dir=dist --exclude-dir=node_modules
```

سپس هر ارجاع باقی‌مانده را در `Home.md`، `_Sidebar.md`، و صفحه‌هایی که به آن لینک می‌دادند اصلاح کن — و **شمارش صفحه‌ها را در `Home.md` و `README.md` هم به‌روز کن** (این دو عدد را از خودشان می‌گویند و کهنه می‌مانند). تأیید نهایی:
Then fix every remaining reference in `Home.md`, `_Sidebar.md`, and the pages that linked to it — and **update the page counts in `Home.md` and `README.md`**, which state their own totals and go stale. Final check:

```bash
python3 - <<'EOF'
import pathlib, re
src = {p.stem for p in pathlib.Path('wiki').rglob('*.md')}
ref = {p.stem for p in pathlib.Path('docs/reference').rglob('*.md')}
print("stale in docs/reference:", sorted(ref - src))
EOF
for p in $(find wiki -name '*.md'); do
  python3 -c "import re,sys,pathlib; ..." "$p"   # یا از اسکریپت لینک‌شکن بالا استفاده کن
done
```

گزارش «صفحه حذف شد» بدون این سه بررسی، ادعای بی‌شاهد است (قاعدهٔ ۸).
Reporting "the page is deleted" without these three checks is an unsupported claim (rule 8).

### پیت‌فال: `template/SCHEMA.md` مسیر ثابت دارد / Pitfall: template/SCHEMA.md keeps hardcoded paths

`src/setup.py` فقط `DOCLIB_ROOT` را در محیط ست می‌کند و **هیچ متنی را بازنویسی نمی‌کند**. `template/SCHEMA.md` هفده ارجاع literal به `/opt/data/documents` دارد، پس در نصب تازهٔ `--root ~/archive` هم همان مسیرها می‌مانند و هر دستور کپی‌شده به مسیر اشتباه می‌رود. `template/SKILL.md` درست از `$DOCLIB_ROOT` استفاده می‌کند — `SCHEMA.md` نه. قبل از تحویل قالب به کسی دیگر، این را با `grep -c "/opt/data/documents"` در آرشیو نصب‌شده چک کن.
`src/setup.py` sets `DOCLIB_ROOT` in the environment and rewrites no text. `template/SCHEMA.md` carries seventeen literal `/opt/data/documents` paths, so a fresh `--root ~/archive` install keeps them and every copied command points at the wrong place. `template/SKILL.md` uses `$DOCLIB_ROOT` correctly; `SCHEMA.md` does not. Verify with `grep -c "/opt/data/documents"` on the installed archive before handing the template to anyone.

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

**قاعدهٔ تک‌منبعی برای فهرست‌ها و رویه‌ها / one source per list and per procedure:** فهرست قواعد سخت فقط در `SKILL.md` کامل است. هر فایل دیگر (`AGENTS.md`، صفحات ویکی) باید یا به آن ارجاع بدهد یا صریح بگوید «فهرست کامل آنجاست». دو فهرست ناقص که هر کدام چند مورد دارند، دیر یا زود واگرا می‌شوند — یک قاعده (`index.db` دوریختنی) فقط در `AGENTS.md` بود و در اسکیل نبود. همین برای **رویه** هم صادق است: یک صفحهٔ مرجع برای جریان ingest، بقیه فقط ارجاع.
**One source per list and per procedure:** the complete hard-rules list lives only in `SKILL.md`. Every other file must point at it or say so explicitly. Two partial lists drift apart — one rule existed only in `AGENTS.md` and never reached the skill. The same holds for a **procedure**: one reference page for the ingest flow, everything else points at it.

- **`rel_path_of()` دو شاخه دارد:** مسیر داخل `raw/` نسبت به `raw/` ذخیره می‌شود (`files/x.pdf`)، و مسیر دیگر داخل مجموعه نسبت به ریشهٔ مجموعه (`wiki/sources/x.md`). پس `add` روی صفحهٔ ویکی کار می‌کند و **باید** بزنی — وگرنه صفحه در `search` پیدا نمی‌شود.
   **`rel_path_of()` has two branches:** inside `raw/` it stores relative to `raw/`, elsewhere inside the collection relative to the collection root. So `add` works on a wiki page and **must** be run on it, or `search` cannot find the page.
- **`add` روی پوشه هم کار می‌کند و محدود به `raw/` نیست.** تست شده: `add` روی `collections/<c>/wiki/concepts/` هم می‌پذیرد و فایل‌ها را ایندکس می‌کند. هر مستندی که می‌گوید «پوشه هم باید داخل `raw/` باشد» غلط است.
   **`add` accepts a directory too, and directories are not limited to `raw/`.** Tested: `add` on `collections/<c>/wiki/concepts/` indexes the files inside it. Any doc claiming a directory must also sit under `raw/` is wrong.
- **مسیر ریشه / Root path:** `DOCLIB_ROOT` یا پیش‌فرض `/opt/data/documents`. پوشه اسناد کنار `HOME` نیست (`HOME=/opt/data/home`).
   Not beside `HOME` (`HOME=/opt/data/home`).
   > مسیرهای `/opt/data/documents` در این فایل **مخصوص همین ماشین** هستند. برای آرشیوی که جای دیگری نصب شده، `DOCLIB_ROOT` را ست کن و مسیرها را از آن بساز. نسخهٔ قابل حمل (بدون مسیر ثابت) در `template/SKILL.md` ریپوی قالب است.
   > The `/opt/data/documents` paths in this file are **specific to this machine**. For an archive installed elsewhere, set `DOCLIB_ROOT` and derive paths from it. The portable version (no hardcoded paths) is `template/SKILL.md` in the template repo.
- **نرمال‌سازی فارسی / Persian Normalization:** ذخیره با `normalize()`، ایندکس با `match_fold()`. دومی تهاجمی‌تر است تا «تأخیر» == «تاخیر» و «مسئول» == «مسیول».
   Storage via `normalize()`, indexing via `match_fold()`. Latter aggressive: "تأخیر" == "تاخیر", "مسئول" == "مسیول".
- **`fts_key`** ستون جداگانه در `chunks` است که فرم fold‌شده را نگه می‌دارد — FTS روی آن ایندکس می‌شود، ولی نمایش از `text` اصلی می‌آید.
   Separate `fts_key` column in `chunks` holds folded form — FTS indexes it, display uses original `text`.
- **ابزار تأییدشده را برای بار دوم با فرض «خراب است» عوض نکن.** وقتی یک کتابخانه قبلاً جواب داده (مثلاً فونت فارسی روی نمودار)، اولین فرض عوض‌کردنش نیست؛ فرض درست این است که لایهٔ *خودت* خراب است. یک جلسه صرف تعویض فونت شد که مشکل واقعی دو بار bidi بود — و بدتر: راهنمای مرجع هم با همان فرض غلط بازنویسی شد. علائم را از داده بگیر (همبستگی، پوشش گلیف، شمارش)، نه از احساس «حالا باید درست باشد».
   **Do not replace a tool that already worked on the assumption it is broken.** When a library has produced output before (e.g. a Persian font on a chart), the first hypothesis is not "replace it" — it is "my own layer is wrong". One session went to swapping fonts when the real fault was double-bidi, and worse, the reference recipe was rewritten carrying the same wrong assumption. Get the signal from data (correlation, glyph coverage, counts), not from the feeling that it must be right now.
- ارقام فارسی/عربی در ذخیره به لاتین تبدیل می‌شوند؛ جستجوی «۹۲۲۰» و «9220» هر دو کار می‌کند.
   Persian/Arabic digits → Latin in storage; search works with "۹۲۲۰" and "9220" alike.
- **ارقام فارسی در ویکی:** هر دو صورت عددی را بنویس — `۱۰ (10)` — چون `match_fold` ارقام را تبدیل می‌کند ولی **کلمات عددی را نه** (`ده` جدای از `۱۰` است). تکیه بر `۱۰ ابزار (ده ابزار)` اشتباه است: تست نشان داد `۱۰ ابزار` پیدا نشد.
   **Persian digits in wiki pages:** write both numeral forms — `۱۰ (10)`. `match_fold` converts digits but not number words, so the word form (`ده`) is not a substitute.
- DOCX خراب → fallback به استخراج خام XML (تابع `_docx_raw_xml`).
   Corrupt DOCX → fallback to raw XML extraction (`_docx_raw_xml`).
- **هنگام توضیح مکانیزم دیتابیس، ساختار را از خود دیتابیس بخوان، نه از حافظه.** نام جدول، ستون‌ها، و ترتیب اتصال‌ها سه بار پشت سر هم غلط گفته شد. `PRAGMA table_info(<table>)` + `SELECT sql FROM sqlite_master` + `PRAGMA index_list` بزن و بعد توضیح بده. اگر کاربر گفت «دوباره چک کن»، یعنی توضیح قبلی غلط بوده — همان لحظه دیتابیس را بخوان، نه اینکه همان روایت را بازگو کنی.
   **To explain the DB mechanism, read the schema from the database, not from memory.** Table names, columns, and JOIN keys were each stated wrong in successive turns. Run `PRAGMA table_info(<table>)`, `SELECT sql FROM sqlite_master`, `PRAGMA index_list` first. If the user says "check again", assume the previous explanation was wrong and read the DB.
- **یک تشخیص را بدون شاهد قابل‌اندازه‌گیری به کاربر تحویل نده.** «حالا باید درست شود» تشخیص نیست. قبل از ادعای «مشکل حل شد»، یک سنجه روی خروجی واقعی بگیر (همبستگی دو تصویر، شمارش ردیف، پوشش گلیف) و همان را نشان بده. در این جلسه دو بار «درست شد» گفته شد و هر دو غلط بود، چون شاهد فقط چشمی بود.
   **Never hand the user a diagnosis without a measurable signal.** "It should work now" is not a diagnosis. Before claiming "fixed", take a measurement on the real output (two-image correlation, row counts, glyph coverage) and show it. Twice in one session "fixed" was reported and both were wrong, because the only evidence was eyeballing.

## گزارش وضعیت به کاربر — بدون تغییر / Status Reporting — Read-Only

**اول تشخیص بده کدام حالت است / Decide which mode first:**

| کاربر گفت / User said | جواب / Answer |
|---|---|
| «فقط جواب» / «فقط سؤال جواب بده» / «کاری انجام نده» | **کوتاه: یک تا سه خط.** بدون جدول چندبخشی، بدون بخش‌بندی، بدون سؤال تصمیم پایانی. اگر جواب ادعای فنی است، اول چک کن، بعد کوتاه بگو. |
| «گزارش بده» / «بررسی کن و گزارش بده» | گزارش کامل طبق شش قاعدهٔ زیر، با سؤال تصمیم شماره‌دار در پایان. |
| «پیشنهاد بده» / «راهکارت چیه؟» | ارزیابی صریح پیشنهاد کاربر (کجا درست است، کجا مسدودکننده دارد) + جدول تصمیم + سؤال شماره‌دار. |

**شکل پیشنهاد اصلاح / Shape of a fix proposal.** وقتی کاربر می‌گوید «پیشنهاد اصلاح بده ولی بدون تأیید کاری نکن»، این پنج بخش را به ترتیب بده — نه کمتر، نه با ترتیب دیگر:
When the user says "propose a fix but do nothing without approval", deliver these five parts in this order:

1. **یک تغییر = یک بلوک.** متن دقیق قبل/بعد، آمادهٔ اعمال. اگر متن از نسخهٔ دیگری در همان ریپو می‌آید، بگو «این را از خودم نساختم، نسخهٔ اثبات‌شدهٔ X است».
   **One change = one block.** Exact before/after text, ready to apply. If the text comes from another file in the repo, say so — "not invented, it is the proven version from X".
2. **«چرا لازم است»** زیر هر تغییر، با اشاره به قاعده‌ای که نقض می‌شود (قاعدهٔ سخت ۳، قاعدهٔ ۸…)، نه با «بهتر است».
   **Why it is needed**, tied to the rule it violates — not "it would be nicer".
3. **جدول نتیجهٔ مورد انتظار** — قبل/بعد برای هر فایل، شامل نسخهٔ نصب‌شده.
   **Expected-result table** — before/after per file, including the installed copy.
4. **«چیزی که پیشنهاد نمی‌کنم»** — صریح بگو چه کاری عمداً انجام نمی‌دهی و چرا (مثلاً «مرحلهٔ گزارش را به مرجع اضافه نمی‌کنم چون شمارش را به ۱۰ می‌برد و همه‌جا باید عوض شود»). این بخش بیشتر از بقیه اعتماد می‌سازد.
   **"What I am not proposing"** — state explicitly what you deliberately leave alone and why. This section builds more trust than the rest.
5. **هزینه** — چند ویرایش، چه تأییدی بعدش می‌زنی، و جملهٔ پایانی «منتظر تأییدت می‌مانم».
   **Cost** — how many edits, what verification follows, and end with "waiting for your approval".

**هرگز پیشنهاد را با اجرا قاطی نکن.** حتی وقتی مطمئنی تغییر درست است و کاربر قبلاً موارد مشابه را تأیید کرده، تا «انجام بده» نگیری دست نزن. تأیید قبلی برای مورد قبلی است، نه برای این یکی.
**Never mix proposal with execution.** Even when the change is obviously right and the user approved similar ones before, touch nothing until they say go. Prior approval covers the prior item, not this one.

**«فقط جواب» یعنی کوتاه، نه یعنی حدس بزن.** ادعای فنی را همان لحظه از دیسک/دیتابیس/تاریخچه تأیید کن، بعد در یک پاراگراف جواب بده.
**"Just answer" means short, not guessed.** Verify the technical claim first, then answer in one paragraph.

**وقتی کاربر پیشنهاد تو را با یک سؤال به چالش می‌کشد («اگر X ملاک باشد بهتر نیست؟»)، نه تأیید کن نه رد — دو سؤال را از هم جدا کن.** این سؤال‌ها معمولاً یک مفهوم را در دو نقش قاطی می‌کنند. جواب درست: «به‌عنوان A نه، به‌عنوان B بله» و بعد یک جملهٔ مکانیسم برای هر کدام. اگر فقط تأیید کنی، پیشنهاد غلط را پذیرفته‌ای؛ اگر فقط رد کنی، بخش درستِ حرف کاربر را از دست داده‌ای — و کاربر همان را می‌خواسته.
**When the user challenges your proposal with a question ("wouldn't X be better?"), neither agree nor refuse — split the two questions.** These questions usually conflate one concept in two roles. The right answer is "not as A, but yes as B", then one mechanism sentence for each. Agreeing wholesale accepts a wrong proposal; refusing wholesale discards the correct half of what the user said — which is the half they wanted.

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
6. **پیش از ادعای «این را می‌توان دوباره ساخت»، منبع را نام ببر.** فایل‌های زنده در `/opt/data/documents/` و `skills/` هستند؛ `/tmp` و GitHub فقط کپی‌اند. صفحات ویکی/سایت (`Home.md`، `Architecture.md`، `CLI-Reference.md`، `docs/`) در هیچ منبع زنده‌ای نیستند و باید از روی همان منابع بازنویسی شوند — این را صریح بگو، نه اینکه القا کنی «همه‌چیز در repo است».
   **Before claiming "this can be regenerated", name the source.** Live files are in `/opt/data/documents/` and `skills/`; `/tmp` and GitHub are copies. The wiki/site pages exist in no live source and must be re-authored from those sources — say so explicitly instead of implying the repo holds everything.
7. **ادعایی که نمی‌توانی تأیید کنی را حذف کن، نه تکرار.** وقتی در حال بازنویسی یک سند هستی و به ادعایی می‌رسی که شاهدش را نداری («مجوز MIT» بدون فایل `LICENSE`، «۳۹ صفحه»، «۱۱ دستور»)، آن را از سند بردار و در گزارش صریح بگو چرا. تکرار یک ادعای تأییدنشده بدتر از حذف آن است — خواننده به آن اعتماد می‌کند و بعد کسی باید کشفش کند. همین برای عدد: هر عدد را همان جلسه از دیسک بشمار، نه از نسخهٔ قبلی سند.
   **Delete a claim you cannot verify; do not repeat it.** When rewriting a document and hitting a claim with no evidence ("MIT license" with no `LICENSE` file, "39 pages", "11 commands"), remove it and say why in the report. Repeating an unverified claim is worse than deleting it — the reader trusts it and someone has to discover it later. Same for numbers: count every one from disk in the same session, never from the previous version of the document.

## افزودن مجموعه جدید / Adding New Collection

با کاربر تأیید بگیر، بعد:
Confirm with user, then:

```bash
mkdir -p /opt/data/documents/collections/<new-name>/{raw/{files,web,audio,images},wiki/{sources,entities,concepts}}
```

و `COLLECTION.md`، `wiki/index.md`، `wiki/log.md` بساز (از مجموعه‌های موجود الگو بگیر).
Create `COLLECTION.md`, `wiki/index.md`, `wiki/log.md` (copy from existing collections).
