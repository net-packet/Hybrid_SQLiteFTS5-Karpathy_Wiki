# A DOCX will not open or extracts garbage

```
zipfile.BadZipFile: File is not a zip file
docx.opc.exceptions.PackageNotFoundError: Package not found at 'file.docx'
```

## Why DOCX fails this way

A `.docx` is a ZIP archive containing XML. Every one of these produces a file
with a `.docx` extension that is not a ZIP:

| What it actually is | How to tell |
|---|---|
| legacy `.doc` (OLE2, Word 97–2003) | `file` says `Composite Document File V2` |
| RTF renamed to `.docx` | starts with `{\rtf` |
| an HTML file saved as `.docx` | starts with `<html` |
| a 0-byte file | `size` is 0 in `files` |
| a truncated download | `unzip -t` fails partway |

## Diagnose

```bash
file /path/to/file.docx
unzip -t /path/to/file.docx
head -c 8 /path/to/file.docx | xxd
```

| Result | Fix |
|---|---|
| `Microsoft Word 2007+` and `unzip -t` OK | not a DOCX problem — check extraction, [Err-Empty-Extract](Err-Empty-Extract.md) |
| `Composite Document File V2` | convert: `libreoffice --headless --convert-to docx file.doc` |
| `Rich Text Format` | convert: `libreoffice --headless --convert-to docx file.rtf` |
| `HTML document` | save from a browser as `.html`, then treat as a web page |
| `empty` | re-download the file |

## Converting legacy `.doc`

```bash
libreoffice --headless --convert-to docx --outdir /tmp old.doc
```

`antiword` and `catdoc` also read `.doc`, but they lose tables and produce
plain text with no structure. LibreOffice preserves the document, which matters
because the citation will point at page numbers.

If LibreOffice is not available, the honest fallback is to open the file
manually, export to PDF, and ingest the PDF — page numbers survive that path.

## A DOCX that opens but yields nothing

`python-docx` reads `document.paragraphs`. Content in these places is invisible
to it:

- tables (`document.tables`)
- headers and footers (`section.header`, `section.footer`)
- text boxes and shapes
- footnotes

Check:

```bash
python3 -c "
import docx
d = docx.Document('/path/to/file.docx')
print('paragraphs:', len(d.paragraphs))
print('tables:', len(d.tables))
print('sections:', len(d.sections))"
```

`paragraphs: 0, tables: 5` means the document is entirely tabular.

**Fix:** open in LibreOffice and export to PDF, then ingest the PDF. Tables come
through as text with page numbers, which is what a citation needs. A custom
table extractor is possible but produces text with no page reference — worse for
this system's purpose.

## Truncated downloads

```bash
unzip -t file.docx | tail -3
```

`unexpected end of central directory` means the download stopped early. Compare
`size` against the source. Re-download; do not try to repair the ZIP — a
partially recovered DOCX loses exactly the content you cannot verify.

## The rule this page enforces

When a DOCX is broken, **convert it and keep the original in `raw/`**. Do not
replace the original with the converted file.

```
raw/files/report.docx              the original, broken, untouched
raw/files/report-converted.pdf     the working copy, ingested
```

The wiki cites the converted PDF and notes the conversion. If someone later
questions a number, both files are there: the original as received, and the copy
that was actually read.
