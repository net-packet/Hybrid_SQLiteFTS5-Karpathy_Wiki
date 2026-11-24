# `ValueError: ... is not in the subpath of ...`

```
افزودن به «office-works» (1 فایل):
Traceback (most recent call last):
  File "doclib.py", line 377, in rel_path_of
    return str(path.resolve().relative_to(raw.resolve()))
ValueError: '/tmp/x.md' is not in the subpath of '/tmp/archive/collections/office-works'
```

## What happened

`rel_path_of()` has two branches:

```python
raw = COLLECTIONS / collection / "raw"
try:
    return str(path.resolve().relative_to(raw.resolve()))          # inside raw/
except ValueError:
    return str(path.resolve().relative_to((COLLECTIONS / collection).resolve()))
```

A path inside `raw/` is stored relative to `raw/` (`files/x.pdf`). A path
elsewhere **inside the collection** is stored relative to the collection root —
which is how a wiki page gets `wiki/sources/x.md`. A path outside the collection
entirely has no relative form, so the second `relative_to()` raises.

This is a guard, not a bug — but it reports itself badly. A traceback instead of
`این فایل داخل raw نیست` is a rough edge, and it is documented here rather than
hidden.

## Fix

Copy the file into the collection's `raw/` first, then add it from there:

```bash
cp /tmp/x.md ~/archive/collections/office-works/raw/files/
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/files/x.md -c office-works
```

The file must land in the right subdirectory for its type:

| Type | Subdirectory |
|---|---|
| PDF, DOCX, XLSX, PPTX, TXT, MD, CSV | `raw/files/` |
| saved web page | `raw/web/` |
| audio + transcript | `raw/audio/` |
| image + sidecar | `raw/images/` |

## Why the rule exists

`rel_path` is stored relative to `raw/` so the archive can be moved or renamed
without invalidating a single row. An absolute path would break the moment the
archive moved to another machine — and every citation in the wiki points through
these paths.

It also enforces the layer boundary: a file you did not deliberately place in
`raw/` is not part of the archive. `add` cannot be pointed at `~/Downloads`.

## Checking a path before adding

```bash
python3 -c "
from pathlib import Path
raw = Path('$HOME/archive/collections/office-works/raw').resolve()
p = Path('/tmp/x.md').resolve()
print('inside raw:', raw in p.parents)"
```

`True` means `add` will accept it.

## Adding a whole directory

`add` accepts a directory, and it must also be inside the collection —
`raw/files/` for a batch of sources:

```bash
mkdir -p ~/archive/collections/office-works/raw/files/batch-1405-08
cp *.pdf ~/archive/collections/office-works/raw/files/batch-1405-08/
python3 ~/archive/doclib.py add \
  ~/archive/collections/office-works/raw/files/batch-1405-08 -c office-works
```

## If you genuinely need a file outside raw/

Do not patch `rel_path_of`. Copy the file in. The whole design rests on `raw/`
being the complete, self-contained set of evidence — a file that lives elsewhere
is evidence that can vanish without the archive noticing.
