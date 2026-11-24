# اولین افزودن

یک فایل، چهار دستور.

## ۱ — فایل را داخل `raw/` بگذار

```bash
cp ~/Downloads/contract-1405.pdf \
   ~/archive/collections/office-works/raw/files/
```

مسیر باید داخل `collections/<name>/raw/` باشد. `add` هر مسیر دیگری را رد
می‌کند.

## ۲ — ایندکس کن

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/files/contract-1405.pdf \
  -c office-works
```

```
افزودن به «office-works» (1 فایل):
  ✓ contract-1405.pdf → 14 تکه (id=1)
تمام. 1 فایل ایندکس شد.
```

`0 تکه` یعنی استخراج متنی پیدا نکرد — معمولاً PDF اسکن‌شده.

## ۳ — جستجو کن

```bash
python3 ~/archive/doclib.py search "جریمه تاخیر"
```

```
1 نتیجه برای «جریمه تاخیر»:

[office-works/contract-1405.pdf — ص 3]
  ...به ازای هر ساعت »تاخیر« ۰٫۵ درصد مبلغ ماهانه کسر می‌شود...
```

## ۴ — صفحهٔ ویکی را بنویس

`collections/office-works/wiki/sources/contract-1405.md`:

```markdown
# قرارداد نگهداشت ۱۴۰۵

**نوع:** قرارداد · **منبع:** [contract-1405.pdf](../../raw/files/contract-1405.pdf)

## اعداد کلیدی

| مورد | مقدار | ارجاع |
|---|---|---|
| مبلغ کل | ۴۸۰,۰۰۰,۰۰۰ ریال | ص ۱ |
| جریمه تاخیر | ۰٫۵٪ ماهانه، سقف ۱۰٪ | ص ۳ |
```

بعد یک ردیف در `wiki/index.md`، یک ردیف در `wiki/log.md`، و:

```bash
python3 ~/archive/doclib.py lint -c office-works
```

## انواع دیگر منبع

| نوع | کجا | چه چیزی ایندکس می‌شود |
|---|---|---|
| PDF / DOCX / XLSX / PPTX / TXT / MD / CSV | `raw/files/` | خود فایل |
| صفحهٔ وب | `raw/web/` | فایل `.md` ذخیره‌شده، با هدر `source:` |
| صدا | `raw/audio/` | فایل `.transcript.md` |
| عکس | `raw/images/` | فایل `.md` که خواندهٔ مدل را دارد |

OCR محلی وجود ندارد. عکس را مدل می‌خواند و خوانده‌اش کنار عکس ذخیره می‌شود،
تا اصل دست‌نخورده بماند و متن قابل جستجو باشد.
