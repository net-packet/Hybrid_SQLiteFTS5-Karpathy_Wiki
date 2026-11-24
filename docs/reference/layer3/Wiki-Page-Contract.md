# What a wiki page must contain

A page that does not meet this contract is not part of the wiki — it is a note
that happens to live in the same directory.

## Required for every `sources/` page

```markdown
# عنوان صفحه

**نوع:** قرارداد · **تاریخ:** ۱۴۰۵/۰۱/۰۱
**منبع:** [contract-1405.pdf](../../raw/files/contract-1405.pdf)

## خلاصه

دو تا چهار خط. چه چیزی در این سند هست و چرا مهم است.

## اعداد کلیدی

| مورد | مقدار | ارجاع |
|---|---|---|
| مبلغ کل | ۴۸۰,۰۰۰,۰۰۰ ریال | ص ۱ |
| جریمه تاخیر | ۰٫۵٪ ماهانه، سقف ۱۰٪ | ص ۳ |

## نکات

- نکته اول — ([ص ۲](../../raw/files/contract-1405.pdf#page=2))
- نکته دوم — ([ص ۳](../../raw/files/contract-1405.pdf#page=3))

## مرتبط

- [budget-1405](budget-1405)
```

## The four rules

### 1. Every number carries a citation

Not "the contract is worth about 480 million" — `۴۸۰,۰۰۰,۰۰۰ ریال | ص ۱`.

Why: this is the only mechanism that makes a wrong number findable. Without it,
a typo is indistinguishable from a fact, forever.

### 2. The `منبع` line points at the raw file

`../../raw/files/contract-1405.pdf` — a relative path from
`wiki/sources/x.md` up to `raw/`. `lint` checks that this file exists
(check 4) and that the page contains at least one such reference (check 5).

### 3. The page is registered in `index.md`

One row. A page not in `index.md` and not linked from anywhere is an orphan.

### 4. No page for a single mention

`entities/` and `concepts/` exist only when a topic appears in **multiple**
sources. One mention gets a line in the `sources/` page, not its own page.

Why: a wiki full of one-sentence pages is harder to navigate than no wiki.

## Language

Write in the language of the source. A Persian contract gets a Persian page. Do
not translate — a translated citation cannot be checked against the original by
someone who reads only the original.

## Length

A `sources/` page is 20–60 lines. Longer means you are summarising the whole
document, which is what the raw file is for. Shorter means you have not read it.

## What a `concepts/` page looks like

Different contract — no `منبع` line, because it synthesises:

```markdown
# جریمه تاخیر

## تعریف
...

## در اسناد این مجموعه

| سند | مقدار | ارجاع |
|---|---|---|
| contract-1405 | ۰٫۵٪/ساعت، سقف ۱۰٪ | [ص ۳](../sources/contract-1405) |
| budget-1405 | فرض ۵٪ | [ص ۱](../sources/budget-1405) |

## تناقض

سقف قرارداد ۱۰٪ است ولی بودجه ۵٪ فرض کرده. ([منبع ۱](../sources/contract-1405)، [منبع ۲](../sources/budget-1405))
```

A concept page cites **pages**, not raw files — and those pages cite raw files.
The chain stays unbroken.

## The check

```bash
python3 doclib.py lint -c office-works
```

Passing lint is necessary, not sufficient. Lint cannot tell whether `ص ۳`
actually says ۱۰ درصد. That requires opening the PDF.
