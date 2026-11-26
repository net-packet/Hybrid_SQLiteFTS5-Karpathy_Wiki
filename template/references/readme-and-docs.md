# README و مستندات ریپو / Repo README and Docs

> وقتی کاربر می‌گوید «README خیلی خلاصه است، بهترش کن» یا «README ریپوی قدیمی را ببین و ایده بگیر».
> When the user says the README is too thin, or points at another repo's README as inspiration.

## چرا README معمولاً بد است / Why a README usually fails

READMEهای کوتاه معماری را توصیف می‌کنند، نه مشکل را. خواننده می‌فهمد «سه لایه دارد» ولی نمی‌فهمد چرا باید اهمیت بدهد. README خوب با **مشکل** شروع می‌شود و بعد نشان می‌دهد معماری جواب آن مشکل است.
A short README describes architecture instead of the problem. The reader learns "it has three layers" but not why that matters. A good README opens with the problem, then shows the architecture is the answer to it.

## ساختار / Structure

1. **یک خط بولد** که خودِ ادعای طراحی است، نه فهرست ویژگی.
2. **The problem** — دو نوع سؤال واقعی که کاربر دارد، و چرا ابزارهای دیگر یکی را جواب می‌دهند و دیگری را تقلید می‌کنند.
3. **جدول لایه‌ها** با ستون «قابل بازسازی؟» — این ستون خودِ استدلال است، نه تزئین.
4. **Quick start** با **خروجی واقعی** `VERIFY: PASS`، نه وعده. به‌علاوه: «اگر آخرین خط چیز دیگری بود، موفقیت گزارش نکن».
5. **درخت خروجی نصب** — چه چیزی ساخته می‌شود، با کامنت کنار هر خط.
6. **جدول مراحل** با نام‌بردن از مراحلی که همه رد می‌کنند و **دلیل** رد شدنشان.
7. **جدول دستورها** — همه، نه نمونه.
8. **«عمداً نمی‌کند»** با یک دلیل برای هر ردیف.
9. **بخش قابل‌سنجش بودن** — ارجاع به `CONTRACT.md` و `demo/`، نه ادعا.
10. **لینک مستندات** — سایت، ویکی، `AGENTS.md`.
11. **خلاصهٔ فارسی** داخل `<div dir="rtl">` تا واقعاً خوانا باشد.

## قاعدهٔ سخت: هر عدد را همان جلسه بشمار / Every number gets counted

**هیچ عددی را از README قبلی، از حافظه، یا از commit message نقل نکن.** هر عدد را از دیسک بشمار و در همان جلسه:
**Never carry a number over from the old README, memory, or a commit message.** Count it from disk, same session:

```bash
# تعداد دستورهای CLI
grep -c "add_parser(" src/doclib.py
# صفحات ویکی و مراجع
find wiki -name '*.md' | wc -l
ls template/references | wc -l
find docs/reference -name '*.md' | wc -l
ls demo/seed | wc -l
wc -l < src/requirements.txt
```

عددی که README دربارهٔ خودش می‌گوید (مثل «39 pages») بی‌صدا کهنه می‌شود — همان کلاس باگ «eight-step». اگر عددی را نتوانستی بشماری، در README ننویس.
A number the README states about itself goes stale silently — the same bug class as "eight-step". If you cannot count it, do not write it.

## قاعدهٔ سخت: هر لینک را با curl بسنج / Every URL gets curl'd

لینک سایت را از README قبلی کپی نکن — ممکن است هرگز وجود نداشته باشد. هر آدرس را جدا تست کن:
Do not copy site links from the old README — they may never have existed. Test each one:

```bash
for p in guide/install guide/ingest guide/cli guide/architecture \
         fa/guide/install fa/guide/ingest fa/guide/cli fa/guide/architecture \
         reference/Home; do
  echo -n "$p -> "; curl -s -o /dev/null -w "%{http_code}\n" -m 12 \
    "https://<user>.github.io/<repo>/$p"
done
```

و لینک‌های نسبی داخل ریپو را با پایتون چک کن، نه با چشم:
And check relative links inside the repo with Python, not by eye:

**`200` ثابت می‌کند صفحه وجود دارد، نه اینکه کار می‌کند.** اگر VitePress بدون `base` بیلد شده باشد، هر لینک README `200` می‌دهد ولی خود سایت بی‌استایل و با لینک‌های شکسته باز می‌شود. پس قبل از نوشتن لینک سایت در README، یک دارایی را هم تست کن:
**`200` proves the page exists, not that it works.** A VitePress build without `base` returns `200` for every README link while the site itself renders unstyled with broken links. Before putting site links in a README, test one asset too:

```bash
curl -s "https://<user>.github.io/<repo>/" | grep -o '/<repo>/assets/[^"]*' | head -1
# خالی = base غایب است؛ لینک‌های README گمراه‌کننده‌اند
```

```python
import re, pathlib
s = pathlib.Path('README.md').read_text(encoding='utf-8')
bad = [m for m in re.findall(r'\]\(([^)]+)\)', s)
       if not m.startswith(('http', '#', 'mailto'))
       and not pathlib.Path(m.split('#')[0]).exists()]
print(bad or "all relative links resolve")
```

## ادعاهایی که نباید بی‌چک نقل شوند / Claims never to carry over blindly

| ادعا / Claim | چرا خطرناک است / Why |
|---|---|
| «License: MIT» | اگر فایل `LICENSE` در ریپو نیست، ادعا دروغ است. بخش را **حذف** کن، نه تکرار — و به کاربر بگو فایل ندارد. |
| تعداد صفحات / page count | بی‌صدا کهنه می‌شود. بشمار. |
| «N commands» | با هر دستور جدید کهنه می‌شود. `grep -c "add_parser("`. |
| لینک سایت / site URL | شاید هرگز deploy نشده باشد. `curl` بزن. |
| «همه‌چیز در repo است» | صفحات ویکی/سایت در هیچ منبع زنده‌ای نیستند؛ باید از منابع بازنویسی شوند. |

**اگر ادعایی را نمی‌توانی تأیید کنی، حذفش کن و در گزارش بگو چرا.** تکرار یک ادعای تأییدنشده بدتر از حذف آن است.
**If you cannot verify a claim, delete it and say why in the report.** Repeating an unverified claim is worse than removing it.

## ایده گرفتن از README دیگر / Taking inspiration from another README

README قدیمی را **کامل** بخوان (`web_extract` روی `raw.githubusercontent.com/...`)، بعد به سه سبد تقسیم کن:
Read the old README **in full**, then sort its content into three buckets:

1. **بگیر** — ساختار، جدول ویژگی‌ها، Credits، بلوک فارسی.
2. **بازنویسی کن** — فهرست ویژگی‌های بی‌دلیل → استدلال با دلیل.
3. **دور بریز** — هر عدد، هر لینک، هر ادعای مجوز که نمی‌توانی تأیید کنی.

README قدیمی معمولاً دستورهایی دارد که در نسخهٔ فعلی وجود ندارند (`setup.py` در ریشه، `requirements.txt` در ریشه). قبل از کپی، مسیر واقعی را چک کن.
The old README usually has commands that no longer exist (setup.py at root, requirements.txt at root). Check the real path before copying.

## گزارش پایانی / Final report

جدول «بود → شد» برای ادعاهای اصلاح‌شده، و یک بلوک تأیید که هر عدد را با دستور شمارشش نشان می‌دهد. عدد بی‌شاهد در گزارش ننویس (قاعدهٔ سخت ۸).
A before/after table for the corrected claims, plus a verification block showing the counting command for each number. No unsupported numbers in the report (hard rule 8).
