# `n_chunks = 0` after a successful add

The file was accepted, a row exists in `files`, and no text came out.

## Confirm

```bash
sqlite3 ~/archive/index.db "select file_id,name,source_type,size,n_chunks from files where n_chunks=0;"
```

## Cause by file type

### PDF — scanned, no text layer

The most common cause by far. `pypdf` reads the text layer; a scan has only
pixels.

Check:

```bash
python3 -c "
from pypdf import PdfReader
r = PdfReader('/path/to/file.pdf')
print('pages:', len(r.pages))
print('chars on page 1:', len(r.pages[0].extract_text() or ''))"
```

`chars on page 1: 0` confirms it.

**Fix:** do not install an OCR engine. Read the pages as images and store the
reading as a sidecar — see [Ingest-Workflow](../layer3/Ingest-Workflow.md), image section.
The reason is that OCR fails on Persian handwriting and on charts, and the
sidecar records exactly what was read.

### DOCX — password-protected or tracked-changes-only

```bash
python3 -c "
import docx
d = docx.Document('/path/to/file.docx')
print('paragraphs:', len(d.paragraphs))"
```

An exception means the file is encrypted or not really a DOCX. A zero count
means the content is in tables, headers, or text boxes — `python-docx` reads
`document.paragraphs` only.

**Fix:** open in Word/LibreOffice, select all, paste into a new document, save.
Or extract tables explicitly.

### XLSX — formulas with no cached values

`openpyxl` in default mode returns formulas, not results, when the file was
written by a tool that did not cache values.

**Fix:** open and save once in Excel/LibreOffice (which caches values), or read
with `data_only=True` after that save.

### PPTX — content only in images

Slides that are one big screenshot have no text frames.

**Fix:** treat as images.

### TXT / MD / CSV — encoding

A file in a non-UTF-8 encoding (Windows-1256 for Persian) may decode to nothing
usable.

```bash
file -i /path/to/file.txt
```

**Fix:** convert first — `iconv -f WINDOWS-1256 -t UTF-8 in.txt > out.txt`.

## What to do with a zero-chunk file

Two honest options:

1. **Remove it from the index** and handle the source another way:
   ```bash
   python3 doclib.py rm <file_id>
   ```
   The file stays in `raw/` — `rm` never touches it.

2. **Leave it** as a marker that the document exists but is not searchable. It
   will show up in `list` with `0 تکه`, which is a useful signal.

Do not leave it silently. A file in `files` with no chunks looks indexed and is
not.

## Why no automatic fallback

`doclib.py` could fall back to OCR, or to a vision model, on zero chunks. It does
not, because both are slow, both fail differently on Persian, and a silent
fallback makes it impossible to know which path produced the text you are
citing. The failure is loud on purpose.
