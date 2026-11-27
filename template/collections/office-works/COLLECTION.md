# کارهای اداری — `office-works` / Admin Works

> مکاتبات، قراردادها، بخشنامه‌ها، بودجه، صورت‌جلسات و اسناد سازمانی.
> Correspondence, contracts, circulars, budgets, minutes, and organizational documents.

## چه چیزی داخل این مجموعه می‌رود / What Goes In

- قراردادها و الحاقیه‌ها / Contracts and addenda
- بخشنامه‌ها و دستورالعمل‌های اداری / Circulars and admin procedures
- جداول بودجه، متمم بودجه، پیشنهاد بودجه / Budget tables, supplements, proposals
- صورت‌جلسات و مصوبات / Meeting minutes and resolutions
- گزارش‌های عملکرد و پیشرفت / Performance and progress reports
- مکاتبات با پیمانکاران و تأمین‌کنندگان / Contractor/supplier correspondence
- احکام، آیین‌نامه‌ها، فرم‌ها / Decrees, bylaws, forms

## چه چیزی داخل این مجموعه نمی‌رود / What Does NOT Go In

- مطالب آموزشی فنی نگهداشت (→ maintenance-learning) / Maintenance technical learning
- محتوای یادگیری هوش مصنوعی (→ ai-learning) / AI learning content

## محل‌های استقرار / Storage Locations

| نوع / Type | پوشه / Folder |
|---|---|
| فایل (PDF/Word/Excel/PPT/متنی) | `raw/files/` |
| لینک و بلاگ‌پست / Link & Blog | `raw/web/` |
| صدا و ویس / Voice & Audio | `raw/audio/` |
| عکس و اسکرین‌شات / Images & Screenshots | `raw/images/` |

## قواعد اعتبارسنجی / Validation Rules

این مجموعه سند مالی و قراردادی دارد. **هر صفحه‌ای که جدول عددی دارد**، قبل از ثبت، سه محاسبه روی آن اجرا شود.
This collection holds financial and contractual documents. **Every page containing a numeric table** gets three checks before it is written.

**۱. جمع ستون‌ها با جمع اعلامی سند.** ستون‌هایی که ماهیت جمع‌شدنی دارند (مبلغ، تعداد) جمع بزن و با «جمع/مجموع/کل» اعلامی مقایسه کن. اختلاف → هر دو عدد و اختلاف دقیق در بخش `## تناقض‌های داخلی` همان صفحه.
**Column totals vs the document's stated total.** Sum the additive columns (amount, count) and compare against the stated total. Gap → both figures and the exact difference in `## Internal Inconsistencies` on that page.

**۲. جمع ردیف‌ها با جمع اعلامی همان جدول.** اگر نخواند، صفحه ساخته می‌شود ولی با هشدار. عدد را حدس نزن و جای خالی نگذار.
**Row values vs the table's own stated total.** If it does not add up, the page is still written but carries the warning. Never guess a number; never leave a blank.

**۳. نسبت ستون‌های وابسته در همهٔ ردیف‌ها.** اگر ستونی از ستون دیگر مشتق می‌شود (تعدیل از ماهانه، ماهانه از قرارداد)، نسبت را در **همهٔ ردیف‌ها** حساب کن. پراکندگی (مثلاً ۰.۴۵ تا ۲.۲۲) یعنی آن ستون قاعدهٔ یکسان ندارد — در صفحه بنویس و در گزارش‌های بعدی مبنای مقایسه قرار نده.
**Dependent-column ratio across every row.** If one column derives from another (adjustment from monthly, monthly from contract), compute the ratio in **every row**. A spread (say 0.45–2.22) means the column has no single rule — record that, and never use it as a comparison base later.

**۴. اجرا با پایتون، نه با چشم.** ارقام فارسی و جداکنندهٔ فارسی اول به لاتین تبدیل شوند، بعد جمع زده شوند.
**Run it in Python, not by eye.** Convert Persian digits and separators to Latin first, then sum.

**۵. جای نتیجه.** بخش `## تناقض‌های داخلی` در همان صفحهٔ منبع — نه فقط در پیام به کاربر. پیام گم می‌شود، صفحه می‌ماند.
**Where the result goes.** `## Internal Inconsistencies` on the source page itself — not only in the chat reply. Messages are lost; pages persist.

**چرا این قواعد:** گزارش ۱۴۰۴ جمع اعلامی ۲۲۶,۵۹۱,۶۳۶,۷۹۴ ریال دارد، ولی صورت‌وضعیت ماهانه (۱۳۱,۶۳۶,۶۲۴,۱۸۶) و تعدیل (۶۸,۱۷۹,۲۸۰,۵۹۱) جمعاً ۱۹۹,۸۱۵,۹۰۴,۷۷۷ می‌شوند — اختلاف ۲۶,۷۷۵,۷۳۲,۰۱۷ ریال. صفحهٔ ویکی این عدد را نقل کرده بود بدون اینکه با اجزایش بسنجد.
**Why these rules:** the 1404 report states 226,591,636,794 rials while its own components (131,636,624,186 + 68,179,280,591) sum to 199,815,904,777 — a 26,775,732,017 rial gap. The wiki page copied the total without testing it against the parts.

## وضعیت / Status

خالی — هنوز منبعی اضافه نشده.
Empty — no sources added yet.
