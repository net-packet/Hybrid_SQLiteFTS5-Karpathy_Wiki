# demo — recorded, reproducible output

`seed/` holds three synthetic Persian documents (fake contract, fake budget,
fake maintenance-training notes). No real names or figures.

`expected/` holds the output this system actually produced on a clean install.
They were captured, not written by hand:

```bash
rm -rf /tmp/vdemo
python3 src/setup.py --root /tmp/vdemo --skip-install
export DOCLIB_ROOT=/tmp/vdemo
for f in demo/seed/*.md; do cp "$f" /tmp/vdemo/collections/office-works/raw/files/; done
python3 /tmp/vdemo/doclib.py add /tmp/vdemo/collections/office-works/raw/files/01-contract-sample.md -c office-works
# ... repeat for 02 and 03
python3 /tmp/vdemo/doclib.py search "قرارداد" > demo/expected/search-contract.txt
```

## What to compare

| File | Command | Key line |
|---|---|---|
| `collections.txt` | `doclib.py collections` | three collections listed |
| `stats.txt` | `doclib.py stats` | `3 فایل، 3 تکه` |
| `list-office-works.txt` | `doclib.py list -c office-works` | three rows |
| `search-contract.txt` | `search "قرارداد"` | `3 نتیجه` |
| `search-budget.txt` | `search "بودجه"` | `1 نتیجه` |
| `search-oee.txt` | `search "OEE"` | Latin term inside Persian text |
| `show-2.txt` | `show 2` | full chunk text, not a snippet |

Numbers may differ if you add files. The **shape** is what matters: a hit
returns the file name, the chunk index, and the original text.
