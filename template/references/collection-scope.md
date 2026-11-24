# دامنهٔ مجموعه‌ها / Collection Scope

> در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> When in conflict with `SKILL.md`, **`SKILL.md` wins.**

## قاعدهٔ استفاده

How to use

۱. موضوع منبع را با دامنهٔ زیر تطبیق بده.  
۲. **یک** مجموعه پیشنهاد بده (تصمیم نهایی با کاربر است).  
۳. **تأیید کاربر را بگیر** — پیشنهاد ≠ تصمیم. بدون تأیید، هیچ فایلی اضافه نمی‌شود.  
۴. اگر موضوع در **دو مجموعه** جا داشت → **بپرس**، خودت انتخاب نکن.  
۵. اگر در هیچ مجموعه‌ای جا نشد → **مجموعهٔ جدید** پیشنهاد بده (تأیید بگیر، بعد بخش «افزودن مجموعهٔ جدید» پایین).

1. Match the source topic against the scope below.  
2. Propose **one** collection (the final decision belongs to the user).  
3. **Get the user's approval** — proposal ≠ decision. Without approval, no file is added.  
4. If the topic fits **two** collections → **ask**; do not choose yourself.  
5. If it fits none → propose a **new collection** (get approval, then "Adding New Collection" below).

## office-works / کارهای اداری

**In scope:**

- Contracts & addenda
- Circulars & admin procedures
- Budget tables, supplements, proposals
- Meeting minutes & resolutions
- Performance & progress reports
- Contractor/supplier correspondence
- Decrees, bylaws, forms

**دامنه (فارسی):**

- قراردادها و الحاقیه‌ها
- بخشنامه‌ها و دستورالعمل‌های اداری
- جداول بودجه، متمم، پیشنهاد
- صورت‌جلسات و مصوبات
- گزارش‌های عملکرد و پیشرفت
- مکاتبات پیمانکار / تأمین‌کننده
- احکام، آیین‌نامه‌ها، فرم‌ها

**Out of scope:**

- Maintenance technical learning → `maintenance-learning`
- AI learning content → `ai-learning`

**خارج از دامنه:**

- آموزش فنی نگهداشت → `maintenance-learning`
- محتوای آموزش AI → `ai-learning`

---

## maintenance-learning / آموزش نگهداشت

**In scope:**

- PM procedures
- Troubleshooting & repair
- Equipment catalogs & manuals
- Technical & safety standards
- Failure reports & RCA
- Technical training (electrical, mechanical, signaling, rail)

**دامنه (فارسی):**

- دستورالعمل‌های نگهداشت پیشگیرانه (PM)
- رویه‌های عیب‌یابی و تعمیر
- کاتالوگ و دفترچهٔ تجهیزات
- استانداردهای فنی و ایمنی
- گزارش خرابی و تحلیل ریشه‌ای (RCA)
- آموزش‌های فنی (برق، مکانیک، سیگنالینگ، ریلی)

**Out of scope:**

- Maintenance contracts & financial docs → `office-works`
- Software & AI learning → `ai-learning`

**خارج از دامنه:**

- قراردادها و اسناد مالی نگهداشت → `office-works`
- آموزش نرم‌افزار و AI → `ai-learning`

---

## ai-learning / آموزش هوش مصنوعی

**In scope:**

- AI articles & blog posts
- Tool guides (LLM, RAG, agents)
- Courses & learning notes
- AI applications in PM & maintenance
- Video/podcast transcripts

**دامنه (فارسی):**

- مقاله‌ها و پست‌های بلاگ AI
- راهنماهای ابزار (LLM، RAG، ایجنت)
- دوره‌ها و یادداشت‌های آموزشی
- کاربرد AI در مدیریت پروژه و نگهداشت
- رونویسی ویدیو / پادکست

**Out of scope:**

- Admin docs & contracts → `office-works`
- Maintenance technical procedures → `maintenance-learning`

**خارج از دامنه:**

- اسناد اداری و قراردادها → `office-works`
- رویه‌های فنی نگهداشت → `maintenance-learning`

---

## محل ذخیره‌سازی (همهٔ مجموعه‌ها)

Storage locations (all collections)

| نوع / Type | پوشه / Folder |
|---|---|
| فایل (PDF/Word/Excel/PPT/Text) / Files | `raw/files/` |
| لینک وب و بلاگ / Web & blog | `raw/web/` |
| صدا و ویس / Audio & voice | `raw/audio/` |
| عکس و اسکرین‌شات / Images & screenshots | `raw/images/` |

## افزودن مجموعهٔ جدید

Adding a new collection

۱. تأیید کاربر را بگیر.  
۲. ساخت پوشه‌ها:

1. Get user approval.  
2. Create the folders:

```bash
mkdir -p /opt/data/documents/collections/<new-name>/{raw/{files,web,audio,images},wiki/{sources,entities,concepts}}
```

۳. ساخت `COLLECTION.md` (از یک مجموعهٔ موجود کپی کن، دامنه را ویرایش کن).  
۴. ساخت `wiki/index.md` و `wiki/log.md` خالی (از قالب کپی کن).  
۵. اجرای `doclib.py collections` برای تأیید.

3. Create `COLLECTION.md` (copy from an existing collection, edit the scope).  
4. Create empty `wiki/index.md` and `wiki/log.md` (copy the template).  
5. Run `doclib.py collections` to verify.
