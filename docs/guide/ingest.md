# First ingest

One file, four commands.

## 1 — place it under `raw/`

```bash
cp ~/Downloads/contract-1405.pdf \
   ~/archive/collections/office-works/raw/files/
```

The path must be inside `collections/<name>/`. `raw/` holds sources; `wiki/`
holds the pages you write. A path outside the collection is refused.

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

`0 تکه` means extraction produced no text — usually a scanned PDF.

## 3 — search it

```bash
python3 ~/archive/doclib.py search "جریمه تاخیر"
```

```
1 نتیجه برای «جریمه تاخیر»:

[office-works/contract-1405.pdf — ص 3]
  ...به ازای هر ساعت »تاخیر« ۰٫۵ درصد مبلغ ماهانه کسر می‌شود...
```

## 4 — write the page

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

## 5 — index the wiki page too

```bash
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/wiki/sources/contract-1405.md \
  -c office-works
```

**Without this the page is invisible to `search`.** It exists on disk and looks
finished, but the index does not know about it. `lint` will not warn you —
it checks structure, not searchability.

Prove it:

```bash
python3 ~/archive/doclib.py search "قرارداد نگهداشت"
```

Two hits now: the PDF and the wiki page.

## 6 — register and lint

One row in `wiki/index.md`, one in `wiki/log.md`, then:

```bash
python3 ~/archive/doclib.py lint -c office-works
```

## Other source types

| Type | Where | What gets indexed |
|---|---|---|
| PDF / DOCX / XLSX / PPTX / TXT / MD / CSV | `raw/files/` | the file |
| web page | `raw/web/` | the saved `.md`, with a `source:` header |
| audio | `raw/audio/` | the `.transcript.md` sidecar |
| image | `raw/images/` | the `.md` sidecar holding the model's reading |

There is no local OCR. Images are read by the model and the reading is stored
beside the image, so the original stays untouched and the text is searchable.
