# Walkthrough — one document, four commands

No theory. A single Persian contract, from a file on disk to a searchable,
cited page.

## 1 — put it in the collection

```bash
cp ~/Downloads/contract-1405.pdf \
   ~/archive/collections/office-works/raw/files/
```

Nothing else goes in `raw/`. No editing, no renaming to something prettier —
the filename is part of the citation.

## 2 — index it

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

Fourteen chunks. If the number is `0`, the PDF has no text layer — see
[Err-Empty-Extract](layer4/Err-Empty-Extract).

## 3 — search it

```bash
python3 ~/archive/doclib.py search "جریمه تاخیر"
```

```
1 نتیجه برای «جریمه تاخیر»:

[office-works/contract-1405.pdf — ص 3]
  ...در صورت »تاخیر« در پاسخ اضطراری، به ازای هر ساعت »تاخیر« ۰٫۵ درصد
  مبلغ ماهانه کسر می‌شود. سقف جریمه: ۱۰ درصد مبلغ قرارداد...
```

Note what the answer contains: **which file**, **which page**, **the original
text**. That is the whole output contract.

## 4 — write the page

`collections/office-works/wiki/sources/contract-1405.md`:

```markdown
# قرارداد نگهداشت ۱۴۰۵

**نوع:** قرارداد · **منبع:** [contract-1405.pdf](../../raw/files/contract-1405.pdf)

## خلاصه

قرارداد نگهداشت پیشگیرانه تاسیسات، ۱۲ ماهه، با جریمه تاخیر در پاسخ اضطراری.

## اعداد کلیدی

| مورد | مقدار | ارجاع |
|---|---|---|
| مبلغ کل | ۴۸۰,۰۰۰,۰۰۰ ریال | ص ۱ |
| جریمه تاخیر | ۰٫۵٪ ماهانه، سقف ۱۰٪ | ص ۳ |
| زمان پاسخ اضطراری | ۴ ساعت | ص ۳ |
```

Then one row in `wiki/index.md` and one in `wiki/log.md`, then:

```bash
python3 ~/archive/doclib.py lint -c office-works
```

## What you have now

| Question | Answer comes from |
|---|---|
| "where does it mention penalties" | `search` — step 3 |
| "what are the key numbers" | the page — step 4 |
| "where did ۴۸۰,۰۰۰,۰۰۰ come from" | `ص ۱` of the PDF, cited in the table |

Three different questions, three different paths, one document. That is the
system.

## The next document

Same four steps. The only judgement call is step 1: which collection. If the
answer is not obvious, stop and ask — a document in the wrong collection is
worse than one that is not indexed yet.

This page shows one document with real output. The procedure itself — all nine
steps, plus audio, images and web pages — is
[Ingest-Workflow](layer3/Ingest-Workflow). Where the two differ, that page wins.
