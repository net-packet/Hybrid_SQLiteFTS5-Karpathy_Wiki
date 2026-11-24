# Hybrid SQLite-FTS5 + Karpathy-style Wiki Archive

**An archive that keeps three things apart on purpose: the files you were given,
a search index you can throw away, and a wiki where every number has a page
reference.**

[![docs](https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki/actions/workflows/docs.yml/badge.svg)](https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki/actions/workflows/docs.yml)

**[Documentation](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/)** ·
**[مستندات فارسی](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/fa/)** ·
[Wiki source](wiki/Home.md) · [For agents](AGENTS.md) · [Portability contract](CONTRACT.md)

---

## The problem

You have a folder of contracts, budgets, meeting notes, and training material.
You need to answer two different kinds of question:

- *"What is the late-delivery penalty?"* — a fact, somewhere on page 3
- *"Do these three contracts contradict each other?"* — a judgement across files

Most tools answer one and fake the other. A chat-with-your-PDF tool returns a
paragraph with no page number, so you cannot check it. A folder of notes has no
search. And when the database corrupts, everything is gone — including the
originals, if you let the tool "import" them.

This archive refuses to collapse those jobs.

## The three layers

| Layer | What it holds | Rebuildable? |
|---|---|---|
| `raw/` | the files exactly as you received them | **No** — it is the source of truth |
| `index.db` | SQLite + FTS5: extracted text, chunked | **Yes** — delete it, re-add from `raw/` |
| `wiki/` | markdown that explains and cites | **Yes** — but only from `raw/` |

Corrupt the database and nothing is lost: `rm index.db && reindex`. Edit a wiki
page into nonsense and the evidence is untouched. That separation is the whole
design, and everything below follows from it.

## Quick start

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

The last line must be `VERIFY: PASS`:

```
archive root: /home/you/archive
installing:
  deps: installed
  ffmpeg: found
  collections: 3 (office-works, maintenance-learning, ai-learning)

  verify:
    PASS  collections  office-works
    PASS  schema       tables ok=True, user_version=100
    PASS  add          files rows=1
    PASS  search       query 'قرارداد' -> hit
    PASS  lint         ✅ هیچ ایرادی پیدا نشد.

VERIFY: PASS
```

Anything else means the install failed. **Do not report success on a different
last line** — see [Debug-Playbook](wiki/layer4/Debug-Playbook.md).

Then:

```bash
export DOCLIB_ROOT=~/archive
python3 ~/archive/doclib.py add ~/archive/collections/office-works/raw/files/contract.pdf -c office-works
python3 ~/archive/doclib.py search "جریمه تاخیر"
python3 ~/archive/doclib.py show 1
```

Requirements: **Python 3.11+** (uses `tomllib`), the four extractors in
`src/requirements.txt`, and `ffmpeg` only for audio over 25 MB. `setup.py`
installs the Python deps; `--skip-install` skips that step on a machine with no
network.

## What you get

```
~/archive/                          DOCLIB_ROOT
├── doclib.py                       the only executable — 14 commands
├── SCHEMA.md                       the rules, on one page
├── SKILL.md                        the full operating procedure
├── index.db                        SQLite + FTS5, user_version = 100
├── references/                     9 reference files
└── collections/
    ├── office-works/               contracts, letters, budgets, minutes
    │   ├── COLLECTION.md
    │   ├── raw/{files,web,audio,images}/    ← never modified
    │   └── wiki/{index.md,log.md,sources/,entities/,concepts/}
    ├── maintenance-learning/       procedures, troubleshooting, standards
    └── ai-learning/                models, tools, papers, AI in PM
```

Collections are the unit of separation. A contract *about* maintenance belongs
in `office-works`; `maintenance-learning` holds training material, not the
paperwork. If a document fits two, the agent asks — it does not guess.

## The nine-step ingest

This is the only procedure. Every other page defers to it
([Ingest-Workflow](wiki/layer3/Ingest-Workflow.md)).

| # | Step | Who |
|---|---|---|
| 1 | identify the topic | ask before assuming |
| 2 | propose one collection, get confirmation | agent asks, you answer |
| 3 | place the file under `raw/` | `cp` — never edit it after |
| 4 | `doclib.py add <raw path> -c <collection>` | one command |
| 5 | `search` to confirm, `show` to read the chunk you will cite | two commands |
| 6 | write `wiki/sources/<slug>.md` with citations | prose |
| 7 | **`doclib.py add <wiki page> -c <collection>`** | one command — **do not skip** |
| 8 | register in `wiki/index.md` and `wiki/log.md` | two line edits |
| 9 | `doclib.py lint -c <collection>` | one command |

**Step 7 is the one everyone forgets.** The page exists on disk and looks
finished, but until it is indexed `search` cannot find it — and `lint` will not
warn you, because it checks structure, not searchability.

**Step 5 is the one everyone shortcuts.** A search result is a ~200-character
snippet. Cite from the snippet and you can cite the wrong page. `show` prints
the whole chunk; that is what you quote from.

## Two query paths, not one

| Question | Path | Why |
|---|---|---|
| "what is the penalty %" | `search` → `show` → answer with file + page | a fact lives in one chunk |
| "compare the three contracts" | read `wiki/index.md` → follow links → then `search` to verify | a judgement lives across files |

The analytical path **starts at the wiki**, not at SQLite. The wiki is the map
you built while reading; the database is the evidence. Going straight to SQL for
an analytical question gives you fragments with no argument.

The answer must say which path it took, and name every source.

## Commands

Fourteen, all in one file, no dependencies beyond the extractors.

| Command | What it does |
|---|---|
| `add <path> [-c COLL]` | index a file or directory inside the collection |
| `search "<query>" [-c COLL] [-f FILTER]` | FTS5 search — returns file, page, text |
| `show <file_id>` | every chunk of one file — what you cite from |
| `list [-c COLL]` | indexed files |
| `rm <file_id>` | remove from the index (the raw file stays) |
| `reindex [-c COLL]` | rebuild the index from `raw/` |
| `stats` | counts per collection |
| `collections` | what exists — run this first if `DOCLIB_ROOT` is in doubt |
| `links <page> [-c COLL]` | in/out links of a wiki page |
| `lint [-c COLL]` | six structural checks |
| `graph [-c COLL]` | link map of the wiki |
| `ur-new` / `ur-add` / `ur-list` | "source in progress" — a book you are reading, quote by quote |

`lint` checks: broken links, orphan pages, pages missing from `index.md`,
citations to a raw file that does not exist, pages with no citation at all, and
duplicate titles. It does **not** check whether a number is true — that is the
reader's job, which is why every number carries a page.

## Persian, treated as a first-class case

`تأخیر` and `تاخیر` are the same word. So are `کتاب` and `كتاب`, and `۴۸۰` and
`480`. Folding happens **before the index is written**, not after the query — so
the index itself is normalized and a search for either form matches both.

That is not a nicety. A Persian contract will use both spellings, sometimes on
the same page.

## What it deliberately does not do

| Not | Because |
|---|---|
| embeddings / vector search / RAG | FTS5 plus a curated wiki answers the questions this is for, and you can read why it matched |
| local OCR | engines fail on Persian handwriting and charts; a vision model reads the image and its reading is stored as a `.md` sidecar you can audit |
| automatic translation | a translated citation cannot be checked against the original |
| a GUI | it is a CLI and a folder of markdown; both survive |
| multi-user concurrency | SQLite is single-writer, and pretending otherwise corrupts data |

Full list: [Non-Goals](wiki/layer1/Non-Goals.md).

## Is it actually portable?

[`CONTRACT.md`](CONTRACT.md) states five conditions, each testable. `setup.py
--verify` automates three of them on every run. The repo ships a
[demo](demo/README.md) with three synthetic Persian documents and the output
this system actually produced on a clean install — compare the shape, not the
line wrapping.

An agent can install this from `AGENTS.md` alone, without asking a question.
That is condition 5, and it is the one that breaks silently when the docs drift.

## Documentation

The site is generated from `wiki/` plus four hand-written guides, in two
languages:

| | English | فارسی |
|---|---|---|
| Install | [guide/install](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/guide/install) | [fa/guide/install](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/fa/guide/install) |
| First ingest | [guide/ingest](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/guide/ingest) | [fa/guide/ingest](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/fa/guide/ingest) |
| CLI | [guide/cli](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/guide/cli) | [fa/guide/cli](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/fa/guide/cli) |
| Architecture | [guide/architecture](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/guide/architecture) | [fa/guide/architecture](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/fa/guide/architecture) |
| Reference (30 pages) | [/reference/Home](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/reference/Home) | — |

Where to start in the repo:

- **Why it is built this way** — [Why-Hybrid](wiki/layer1/Why-Hybrid.md)
- **See it work, one document** — [Walkthrough-Simple](wiki/Walkthrough-Simple.md)
- **Hand it to an agent** — [AGENTS.md](AGENTS.md), then [AGENTS-Page](wiki/AGENTS-Page.md)
- **Something broke** — [Debug-Playbook](wiki/layer4/Debug-Playbook.md)

## Repo layout

```
src/         doclib.py (the only executable), setup.py, schema.sql
template/    what setup.py copies into a new archive
demo/        synthetic seed documents + recorded expected output
wiki/        32 pages: why, how it works, how to install, how to repair
docs/        VitePress site (EN at /, FA at /fa/)
tools/       build_docs.py — generates docs/reference from wiki/
```

`docs/reference/` is **generated**. Edit `wiki/`, then run
`python3 tools/build_docs.py`. CI fails the build if the two disagree.

## Credits

- **Karpathy's LLM-wiki method** — [the gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): interlinked markdown as a knowledge base an LLM can navigate
- **SQLite FTS5** — full-text search with no server
- **Groq Whisper** — Persian speech-to-text
- **Hermes Agent** — the platform this was built on

---

<div dir="rtl">

## خلاصهٔ فارسی

**یک آرشیو که عمداً سه چیز را از هم جدا نگه می‌دارد:** فایل‌هایی که به شما
داده‌اند، ایندکسی که هر وقت خواستید می‌توانید دور بیندازید، و ویکی‌ای که هر
عدد در آن ارجاع به فایل و صفحه دارد.

| لایه | چه چیزی نگه می‌دارد | قابل بازسازی؟ |
|---|---|---|
| `raw/` | فایل اصلی، دست‌نخورده | **نه** — منبع حقیقت است |
| `index.db` | SQLite + FTS5، متن استخراج‌شده | **بله** — پاک کن، از `raw/` بساز |
| `wiki/` | صفحات مارک‌داون با ارجاع | **بله** — ولی فقط از `raw/` |

اگر دیتابیس خراب شود چیزی از دست نمی‌رود: `rm index.db && reindex`.

### شروع

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

آخرین خط باید `VERIFY: PASS` باشد. هر چیز دیگری یعنی نصب نشده — موفقیت گزارش
نکنید.

### جریان ingest — نُه مرحله

۱. تشخیص موضوع · ۲. پیشنهاد و **تأیید** مجموعه · ۳. کپی به `raw/` ·
۴. `add` فایل خام · ۵. `search` و `show` · ۶. نوشتن صفحهٔ ویکی ·
۷. **`add` صفحهٔ ویکی** · ۸. `index.md` و `log.md` · ۹. `lint`

**مرحلهٔ ۷ را همه فراموش می‌کنند.** صفحه روی دیسک هست و تمام‌شده به نظر
می‌رسد، ولی تا ایندکس نشود `search` پیدایش نمی‌کند — و `lint` هشدار نمی‌دهد،
چون ساختار را چک می‌کند نه قابل‌جستجو بودن را.

**مرحلهٔ ۵ را همه میان‌بر می‌زنند.** نتیجهٔ `search` یک تکهٔ ~۲۰۰ کاراکتری است.
اگر از آن نقل کنی، ممکن است صفحهٔ اشتباه را ارجاع بدهی. `show` تکهٔ کامل را
چاپ می‌کند.

### دو مسیر پرسش

- **سؤال نقطه‌ای** («جریمه چند درصد؟») → `search` → `show` → جواب با نام فایل و صفحه
- **سؤال تحلیلی** («این سه قرارداد تناقض دارند؟») → `wiki/index.md` → لینک‌ها → بعد `search` برای تأیید

مسیر تحلیلی **از ویکی شروع می‌شود**، نه از SQLite. و جواب باید بگوید از کدام
مسیر آمده و همهٔ منابع را نام ببرد.

### فارسی

`تأخیر` و `تاخیر` یک کلمه‌اند. `کتاب` و `كتاب` هم. `۴۸۰` و `480` هم.
نرمال‌سازی **قبل از نوشتن ایندکس** انجام می‌شود، نه بعد از کوئری — پس خود
ایندکس نرمال است و هر دو شکل را پیدا می‌کند.

### چه کاری عمداً نمی‌کند

بدون embedding و vector search · بدون OCR محلی (مدل تصویر را می‌خواند و
خوانده‌اش در یک فایل `.md` کنار تصویر ذخیره می‌شود) · بدون ترجمهٔ خودکار ·
بدون GUI · بدون چند کاربر همزمان (SQLite تک‌نویسنده است).

**مستندات کامل فارسی:** [net-packet.github.io/…/fa/](https://net-packet.github.io/Hybrid_SQLiteFTS5-Karpathy_Wiki/fa/)

</div>

---

**Built with [Hermes Agent](https://hermes-agent.nousresearch.com)** — local-first,
no server, no account, no telemetry. Your documents never leave the machine.
