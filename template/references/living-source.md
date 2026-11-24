# منبع در حال مطالعه / Living Source (User-Reading)

> مسیر جدا از ingest عادی: فایل خام کتاب **می‌تواند رشد کند**. در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> A path separate from normal ingest: the raw book file **may grow**. In conflict with `SKILL.md`, **`SKILL.md` wins.**

## تعریف

Definition

کاربر می‌گوید «کتاب X را شروع کردم». این تنها **استثنای** قاعدهٔ «هرگز `raw/` را تغییر نده» است — فایل `raw/files/User-Reading-*.md` فقط **append** می‌شود.

The user says "I started book X". This is the only **exception** to the "never modify `raw/`" rule — the `raw/files/User-Reading-*.md` file is **append-only**.

## جریان اجباری (۶ مرحله)

Mandatory flow (6 steps)

### ۱. جستجو — کتاب از قبل هست؟

Step 1: Search — does the book already exist?

```bash
python3 /opt/data/documents/doclib.py ur-list
python3 /opt/data/documents/doclib.py search "<عنوان>"
```

- **هست** → همان را ادامه بده (`ur-add`)، فایل جدید نساز.
- **نیست** → برو به مرحلهٔ ۲.

- **Exists** → continue it (`ur-add`); do not create a new file.
- **Does not exist** → go to step 2.

### ۲. موضوع → مجموعه

Step 2: Topic → collection

مطابق `references/collection-scope.md` پیشنهاد بده. اگر در **دو مجموعه** جا داشت → **بپرس**.

Propose per `references/collection-scope.md`. If it fits **two** collections → **ask**.

### ۳. فیلدهای گم‌شده

Step 3: Missing fields

فقط چیزهایی که کاربر نداد و برای پیش‌نمایش **لازم** است بپرس:

Ask only for what the user did not give and what the preview **needs**:

| فیلد / Field | الزامی؟ / Required? |
|---|---|
| عنوان / Title | ✅ الزامی / required |
| نویسنده / Author | ✅ الزامی / required |
| زبان / Language | ✅ الزامی / required |
| ناشر / Publisher | اختیاری / optional |
| سال / Year | اختیاری / optional |
| ISBN | اختیاری / optional |

**قاعده:** کاربر ممکن است خودش مشخصات کتاب را بدهد — از آن استفاده کن، و اگر موردی جا افتاد **سؤال بپرس**. هرگز فیلد الزامی را حدس نزن.

**Rule:** the user may supply the book details themselves — use them, and **ask** if something is missing. Never guess a required field.

### ۴. پیش‌نمایش + تأیید

Step 4: Preview + approval

**تا «تأیید» نگرفتی، هیچ فایلی نساز.** این جدول را نشان بده:

**Create no file before you get "approved".** Show this table:

```
📖 پیش‌نمایش منبع جدید / New source preview

عنوان / Title       ...
نویسنده / Author    ...
سال / Year          ...
ناشر / Publisher    ...
زبان / Language     ...
مجموعه / Collection ...
نام فایل / Filename User-Reading-<slug>.md
صفحه ویکی / Wiki    wiki/sources/user-reading-<slug>.md
```

### ۵. ساخت

Step 5: Create

```bash
python3 /opt/data/documents/doclib.py ur-new <slug> --title "<عنوان>" --author "<نویسنده>" --lang <fa|en> -c <collection>
```

این دستور **سه کار** را خودکار انجام می‌دهد:

This command does **three things** automatically:

۱. ساخت `raw/files/User-Reading-<slug>.md` با frontmatter.  
۲. ساخت صفحهٔ ویکی `wiki/sources/user-reading-<slug>.md`.  
۳. ثبت ردیف در `wiki/index.md` مجموعه.

1. Creates `raw/files/User-Reading-<slug>.md` with frontmatter.  
2. Creates the wiki page `wiki/sources/user-reading-<slug>.md`.  
3. Registers a row in the collection's `wiki/index.md`.

### ۶. هر نقل‌قول بعدی

Step 6: Each subsequent quote

**بدون پیش‌نمایش مجدد** — مستقیم `ur-add`:

**No preview again** — straight to `ur-add`:

```bash
python3 /opt/data/documents/doclib.py ur-add <slug> -p 47 -q "متن دقیق جمله" -t "موضوع" -c <collection>
```

## نام‌گذاری

Naming

```
raw/files/User-Reading-<english-slug>.md
wiki/sources/user-reading-<english-slug>.md
```

- slug **انگلیسی** است (کوتاه‌شده، kebab-case).
- عنوان کتاب (فارسی/انگلیسی) در **frontmatter** می‌رود، نه در نام فایل.
- مثال: کتاب «مهندسی نگهداری» → `User-Reading-maintenance-engineering.md`.

- The slug is **English** (short, kebab-case).
- The book title (Persian/English) goes in **frontmatter**, not in the filename.
- Example: the book «مهندسی نگهداری» → `User-Reading-maintenance-engineering.md`.

## نقل‌قول‌ها

Quotes

- `q001`، `q002`، ... خودکار شماره می‌گیرند.
- `q-NNN` **شناسهٔ ثابت است، نه ترتیب** — ترتیب افزودن و ترتیب نمایش در صفحه جدا هستند.
- هر نقل‌قول **یک تکهٔ جدا** در `index.db` است، با شمارهٔ صفحه.
- جستجوی نقطه‌ای مستقیم نقل‌قول را با ارجاع برمی‌گرداند.

- `q001`, `q002`, ... are numbered automatically.
- `q-NNN` is a **stable identifier, not an order** — insertion order and display order on the page are independent.
- Each quote is a **separate chunk** in `index.db`, with its page number.
- A point query returns the quote directly with its citation.

```
[کتاب X · نویسنده · ص 47 · q001] متن جمله | موضوع: ...
```

## مجاز و ممنوع

Allowed and forbidden

| عمل / Action | مجاز / Allowed |
|---|---|
| افزودن نقل‌قول / Add a quote | ✅ `ur-add` |
| اصلاح تایپی / Typo fix | ✅ با ثبت `**اصلاح:** <تاریخ>` / with an `**اصلاح:** <date>` entry |
| افزودن فیلد خالی frontmatter / Add an empty frontmatter field | ✅ |
| حذف نقل‌قول / Delete a quote | ❌ — `**لغو:** دلیل` بنویس؛ اسکریپت از نمای اصلی خارجش می‌کند / write `**لغو:** reason`; the script drops it from the main view |
| تغییر فیلد موجود frontmatter / Change an existing frontmatter field | ❌ |
| شماره‌گذاری مجدد `q-NNN` / Renumber `q-NNN` | ❌ |

## ایندکس‌گذاری

Indexing

- صفحهٔ ویکی **خودکار بازتولید** می‌شود (دو نما + موضوعات + لغو‌شده‌ها). **دستی ویرایشش نکن.**
- **`q-NNN` را دستی نشمار و تولید نکن.** همیشه `ur-add` بزن؛ شمارهٔ بعدی از فایل خام خوانده می‌شود. اگر خودت شماره بگذاری، لغوها و فاصله‌ها باعث برخورد می‌شوند.

- The wiki page is **regenerated automatically** (two views + topics + cancelled). **Do not edit it by hand.**
- **Do not count or generate `q-NNN` yourself.** Always use `ur-add`; the next number is read from the raw file. Manual numbering collides with cancellations and gaps.

## پیت‌فال: `index.md` هر مجموعه قالب متفاوتی دارد

Pitfall: `index.md` format differs per collection

بعضی `wiki/index.md`ها **جدول**، بعضی **بولت**. `_ur_index_ensure` هر دو را می‌شناسد.

Some `wiki/index.md` files are **tables**, others **bulleted**. `_ur_index_ensure` handles both.

| # | قاعده / Rule |
|---|---|
| 1 | ردیف موجود خودمان **جایگزین** شود، نه تکرار / Replace our own row, never duplicate it |
| 2 | شماره ردیف جدول از ردیف‌های **غیرخودمان** شمرده شود / Count the row number from rows that are **not ours** |

**تست تکرارپذیری:** بعد از تغییر `_ur_index_ensure`، یک `ur-add` دوم بزن و مطمئن شو (a) قالب درست، (b) برچسب ردیف تغییر نکرده، (c) هنوز فقط یک ردیف وجود دارد.

**Repeatability test:** after changing `_ur_index_ensure`, run a second `ur-add` and verify (a) format is correct, (b) row label unchanged, (c) still exactly one row.

## پیت‌فال: سایت و ویکی

Pitfall: site and wiki

هر تغییری در `raw/files/User-Reading-*.md` که frontmatter را عوض کند باید صفحهٔ ویکی را بازتولید کند (`ur-add` یا regenerate)، وگرنه ویکی و منبع ناهمخوان می‌شوند.

Any change to `raw/files/User-Reading-*.md` that alters frontmatter must regenerate the wiki page (`ur-add` or regenerate); otherwise the wiki and the source drift apart.
