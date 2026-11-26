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
| 5 | گزارش «روند» بدون چک کردن اینکه جمع‌های اعلامی سند با هم می‌خوانند / Reporting a "trend" without first checking that the document's own stated totals add up |

## گزارش تحلیلی عددی — حساب را قبل از تفسیر چک کن / Numeric Report — Check the Arithmetic Before Interpreting

سؤال «روند/مقایسه/چقدر بوده» با جدول و نمودار جواب می‌گیرد، ولی **قبل از هر تفسیری** سه چک حساب را بزن. سندی که جمع ستون‌هایش با جمع کل اعلامی نمی‌خواند، مبنای رشد درصدی نیست.
A "trend / compare / how much" question gets a table and a chart — but **before any interpretation** run three arithmetic checks. A document whose column totals disagree with its stated grand total is not a base for percentage growth.

1. **جمع ستون‌ها = جمع کل اعلامی؟** اگر نه، اختلاف را به ریال/تومان بنویس و بگو کدام عدد را نمی‌توان تأیید کرد. رشد درصدی را روی عدد مشکوک نساز — یا هر دو سناریو را بده.
   **Do the column totals equal the stated grand total?** If not, state the gap in absolute currency and say which figure you cannot vouch for. Do not build a growth percentage on the suspect figure — give both scenarios, or neither.
2. **جمع ردیف‌ها = جمع اعلامی جدول؟** اگر برابر است، آن جدول سالم است؛ اگر نه، ردیف گم‌شده یا عدد غلط تایپی هست.
   **Do the row values sum to the table's stated total?** Equal means the table is sound; unequal means a missing row or a typo.
3. **آیا قاعدهٔ محاسبهٔ ستون بین سال‌ها یکی است؟** اگر نسبت یک ستون (مثلاً «تعدیل ÷ ماهانه») در یک سال ۰.۵۲ و در سال دیگر ۰.۶۱ باشد، بخشی از رشد از **تغییر نرخ** آمده نه افزایش حجم کار — این را در تفسیر جدا کن، وگرنه رشد را بیش از واقع نشان می‌دهی.
   **Is the column's computation rule the same across years?** If a ratio (e.g. adjustment ÷ monthly) is 0.52 one year and 0.61 the next, part of the growth is a **rate change**, not more work — separate that in the interpretation or you overstate growth.

**فرضیه را با داده تست کن، با منطق نه.** «ماهانه = قرارداد ÷ مدت» فرضیهٔ معقولی بود و غلط درآمد؛ نسبت `monthly/(contract/12)` بین ردیف‌ها از ۰.۴۵ تا ۲.۲۲ پراکنده بود. یک محاسبهٔ ستونی روی همهٔ ردیف‌ها این را در ۵ ثانیه نشان می‌دهد.
**Test a hypothesis against the data, not by plausibility.** "monthly = contract ÷ duration" looked reasonable and was wrong; the ratio ranged 0.45–2.22 across rows. One column-wide calculation shows this in five seconds.

**تعداد نقاط را صریح بگو.** دو سال «روند» نیست، «مقایسه» است. اگر آرشیو فقط دو سال دارد، همین را بنویس و بگو برای روند سه‌نقطه‌ای چه سندی لازم است — تفسیر دو نقطه به‌عنوان روند، ادعای بی‌پشتوانه است.
**State the number of data points.** Two years is a comparison, not a trend. If the archive holds only two, say so and name what document would make it three — interpreting two points as a trend is an unsupported claim.

## نمودار فارسی با matplotlib / Persian Chart with matplotlib

**رشتهٔ خام بده — `arabic_reshaper` و `python-bidi` را نصب نکن.** matplotlib از نسخهٔ ۳.۸ به بعد با موتور `raqm`/harfbuzz خودش حروف فارسی را می‌چسباند و راست‌به‌چپ می‌چیند. اعمال `get_display(arabic_reshaper.reshape(s))` یعنی **دو بار** شکل‌دهی: متن درست چیده می‌شود و بعد آینه می‌شود.
**Pass the raw string — do not install `arabic-reshaper` or `python-bidi`.** matplotlib ≥3.8 shapes and bidi-orders Persian itself via `raqm`/harfbuzz. Wrapping the text in `get_display(arabic_reshaper.reshape(s))` shapes it **twice** and mirrors the result.

```python
# غلط / wrong — double processing, text comes out mirrored
import arabic_reshaper
from bidi.algorithm import get_display
ax.set_title(get_display(arabic_reshaper.reshape("پرداخت ماهانه")))

# درست / right
ax.set_title("پرداخت ماهانه")
```

**نشانهٔ تشخیص: چسبیده ولی برعکس = bidi دو بار. جدا از هم = bidi هرگز.** اگر حروف به هم چسبیده‌اند ولی کلمه آینه است، reshaper را بردار (نه اینکه اضافه کنی). اگر حروف جدا از هم‌اند، نسخهٔ matplotlib قدیمی است — اول `matplotlib.__version__` را چک کن.
**Diagnostic: connected but mirrored = bidi applied twice. Disconnected = bidi never applied.** If the letters join but the word reads backwards, remove the reshaper — do not add one. If the letters stand apart, matplotlib is too old — check `matplotlib.__version__` first.

**سنجش جهت با کد، نه با چشم.** بعد از ساخت تصویر، هر رشتهٔ فارسی را با خروجی PIL (که raqm دارد و مرجع است) مقایسه کن؛ اگر همبستگیِ آینه‌شده از همبستگیِ مستقیم بیشتر بود، متن برعکس است:
**Test direction in code, not by eye.** After building the image, compare each Persian string against a PIL render (PIL has raqm and is the reference); if the mirrored correlation beats the direct one, the text is reversed:

```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np

fnt = ImageFont.truetype(FONT, 34)
def pil_ref(t):
    im = Image.new("RGB", (1400, 90), "white")
    ImageDraw.Draw(im).text((700, 45), t, font=fnt, fill="black", anchor="mm")
    return np.array(im)

def crop(a):                                   # bounding box of ink only
    g = np.array(Image.fromarray(a).convert("L"))
    c = np.argwhere(g < 128)
    y0, x0 = c.min(0); y1, x1 = c.max(0)
    return g[y0:y1+1, x0:x1+1]

# for each label: render via matplotlib, crop both, resize to the same shape, then
# same = corrcoef(mpl, pil)   mirrored = corrcoef(mpl, pil[:, ::-1])
# PASS requires same > mirrored on EVERY label.
```

فونت وزیرماتن را با `addfont` از فایل `.ttf` بارگذاری کن؛ نیازی به نصب سیستمی نیست. **گلیف‌های Presentation Form (U+FB50–U+FEFF) را هم باید داشته باشد**، وگرنه متن دوباره می‌شکند:
Load Vazirmatn with `addfont` straight from the `.ttf`; system install is unnecessary. **It must also carry the Presentation Forms block (U+FB50–U+FEFF)**, or the text breaks again:

```bash
curl -sL -o fonts/Vazirmatn-Regular.ttf \
  https://github.com/rastikerdar/vazirmatn/raw/master/fonts/ttf/Vazirmatn-Regular.ttf
```

```python
from fontTools.ttLib import TTFont
cmap = TTFont("fonts/Vazirmatn-Regular.ttf").getBestCmap()
for ch in "شپیک۰٪":                      # Persian letters + digits + percent
    assert ord(ch) in cmap, ch
for cp in (0xFE96, 0xFEAE, 0xFB58):     # presentation forms used by the font itself
    assert cp in cmap, hex(cp)
```

**گلیف غایب را در متن رها نکن.** فلش `←`/`→` در وزیرماتن نیست و به‌جای آن مربع خالی رندر می‌شود؛ عبارت را کلامی کن («۱۴۰۴ تا ۱۴۰۵»). `grep` گلیف‌های غیرفارسیِ متن را قبل از رسم چک کن.
**Never leave a missing glyph in the string.** Vazirmatn has no `←`/`→` and renders an empty box; phrase it in words ("1404 to 1405"). Check every non-Persian symbol in the strings before drawing.

**اعداد را در نمودار هم با ارقام فارسی بنویس** و واحد را در محور بگذار («میلیارد تومان در ماه»)، نه در تیتر هر میله. میله‌های گروهی (اجزا کنار هم) + یک پنل جدا برای درصد رشد، خواناتر از یک نمودار انباشته است.
**Use Persian digits in the chart too**, and put the unit on the axis ("billion toman per month"), not on every bar. Grouped bars (components side by side) plus a separate growth panel read better than one stacked chart.
