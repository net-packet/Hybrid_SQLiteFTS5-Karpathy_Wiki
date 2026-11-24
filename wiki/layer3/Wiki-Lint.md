# `lint` — six structural checks

```bash
python3 doclib.py lint                      # every collection
python3 doclib.py lint -c office-works      # one
```

Output on a clean wiki:

```
ویکی: 12 صفحه در 1 مجموعه

✅ هیچ ایرادی پیدا نشد.
```

## The six checks

| # | Check | Flags |
|---|---|---|
| 1 | broken link | `[[target]]` or `[x](target)` where `target.md` does not exist |
| 2 | orphan page | no incoming link **and** not listed in `index.md` |
| 3 | missing from `index.md` | a page under `sources/`, `entities/`, `concepts/` not listed |
| 4 | missing source | a citation to `../raw/...` where the file does not exist |
| 5 | no citation | a `sources/` page containing no reference to `raw/` at all |
| 6 | duplicate title | two pages whose first `# ` heading is identical |

## What lint cannot check

This is the important half.

| Not checked | Why it matters |
|---|---|
| whether a number is **correct** | lint sees a citation exists, not that page 3 says 480 |
| whether the citation points at the **right** page | `ص ۳` is a string |
| whether the prose is **true** | no tool can check that |
| whether `index.md` has the right column count | it is a markdown table, not parsed |
| whether the frontmatter `source:` is present on a web page | not in the schema |

Lint proves **structure**, not **truth**. A wiki can pass lint with every number
wrong. The only defence is the citation rule plus reading the source.

## Reading the output

```
[office-works] لینک شکسته: sources/contract → sources/contract-1405
```

Means: the page `sources/contract.md` links to `sources/contract-1405`, which
does not exist. Usually a rename that missed one link.

```
[office-works] صفحه یتیم: sources/budget-1405
```

Means: nothing links to it and it is not in `index.md`. Fix by adding a row to
`index.md` — or by deleting the page if it was a mistake.

```
[office-works] صفحه بی‌منبع: sources/notes-on-meeting
```

Means: the page cites nothing under `raw/`. Either add the citation or move the
content into a page that has one.

## Exit code

`0` when clean, `1` when there are issues. Usable in a pre-commit hook:

```bash
python3 doclib.py lint || echo "wiki has structural issues"
```

## The graph view

```bash
python3 doclib.py graph -c office-works
```

Prints in-degree and out-degree per page. A page with in-degree 0 is an orphan
by another name; a page with out-degree 0 is a leaf that cites nothing further.

```bash
python3 doclib.py links sources/contract-1405 -c office-works
```

Shows both directions for one page — useful before renaming it.
