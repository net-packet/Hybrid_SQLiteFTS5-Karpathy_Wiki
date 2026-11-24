# راه‌اندازی و همگام‌سازی GitHub / GitHub Setup & Sync

> جزئیات کامل راه‌اندازی و همگام‌سازی GitHub. در تناقض با `SKILL.md`، **`SKILL.md` برنده است**.
>
> Full GitHub setup and sync details. When in conflict with `SKILL.md`, **`SKILL.md` wins.**

## ۱. دو مخزن / Two repositories

- **مخزن اصلی** — کد (`doclib.py`، `setup.py`، `requirements.txt`) + منابع markdown ویکی + پوشهٔ `docs/` (VitePress).
- **مخزن ویکی** — صفحات رندرشدهٔ GitHub Wiki. **فقط بعد از ساخت اولین صفحه از طریق UI ساخته می‌شود.**

- **Main repo** — code (`doclib.py`, `setup.py`, `requirements.txt`) + wiki markdown sources + `docs/` folder (VitePress).
- **Wiki repo** — rendered GitHub Wiki pages. **Only created after the first page is made via the UI.**

| مورد / Item | آدرس / URL |
|---|---|
| مخزن اصلی / Main repo | `https://github.com/net-packet/Hybrid_SQLite-Karpathy_Wiki` |
| مخزن ویکی / Wiki repo | `https://github.com/net-packet/Hybrid_SQLite-Karpathy_Wiki.wiki` |

## ۲. فعال‌سازی اولیهٔ ویکی (یک‌بار، دستی)

Initial wiki activation (once, manual)

۱. مخزن → Settings → Features → تیک **Wikis**.  
۲. رفتن به `https://github.com/net-packet/Hybrid_SQLite-Karpathy_Wiki/wiki`.  
۳. **Create first page** → محتوای `Home.md` را بچسبان → Save.  
۴. تکرار برای ۱۱ صفحهٔ دیگر (فهرست در بخش ۷).  
۵. بعد از اولین صفحه، مخزن `.wiki.git` وجود دارد و cloneable است.

1. Repo → Settings → Features → tick **Wikis**.  
2. Open `https://github.com/net-packet/Hybrid_SQLite-Karpathy_Wiki/wiki`.  
3. **Create first page** → paste `Home.md` content → Save.  
4. Repeat for the other 11 pages (list in section 7).  
5. After the first page, `.wiki.git` exists and is cloneable.

**هیچ API برای ساخت صفحهٔ ویکی وجود ندارد.** فقط محتوا را می‌توان via git sync کرد.

**There is no API to create a wiki page.** Only content can be synced via git.

## ۳. همگام‌سازی ویکی (آپدیت محتوا)

Wiki sync (content update)

```bash
cd /tmp/Hybrid_SQLite-Karpathy_Wiki
cp /opt/data/documents/SCHEMA.md Home.md
cp /opt/data/skills/productivity/document-archive/SKILL.md Ingest-Workflow.md
for c in office-works maintenance-learning ai-learning; do
  cp /opt/data/documents/collections/$c/COLLECTION.md Collection-$c.md
done
git add . && git commit -m "Sync wiki from local" && git push
```

فایل‌های محلی منبع حقیقت‌اند. GitHub Wiki یک **آینهٔ فقط‌خواندنی** است.

Local files are the source of truth. GitHub Wiki is a **read-only mirror**.

### ویکی یک مخزن **جدا** است / The wiki is a **separate** repo

`git push` به مخزن اصلی، صفحات ویکی را آپدیت **نمی‌کند**. ویکی مخزن مستقل `.wiki.git` دارد (شاخهٔ `master`، نه `main`) و باید جدا clone و push شود:

```bash
git clone https://<token>@github.com/<owner>/<repo>.wiki.git /tmp/wiki-sync
cd /tmp/wiki-sync
git config user.email "hermes@local" && git config user.name "Hermes Agent"
```

سپس صفحات را از مخزن اصلی کپی کن (نام صفحه = نام فایل، بدون مسیر):

```bash
for f in Home SCHEMA Architecture CLI-Reference Ingest-Workflow Wiki-Layer \
         Design-Decisions Skills-And-Automation Collection-*; do
  cp /tmp/<main-repo>/$f.md /tmp/wiki-sync/$f.md
done
git add -A && git commit -m "Sync wiki with main repo" && git push origin master
```

**دو فایل ناوبری که فقط در ویکی معنی دارند:** `_Sidebar.md` (منوی کنار هر صفحه) و `_Footer.md` (پایین هر صفحه). بدون `_Sidebar.md` ویکی یک لیست بی‌ترتیب از صفحات است.

**Two navigation files that only exist in the wiki:** `_Sidebar.md` and `_Footer.md`. Without `_Sidebar.md` the wiki is an unordered page list.

**تبدیل لینک قبل از push** — ویکی پسوند `.md` را حذف می‌کند و پوشهٔ `references/` ندارد:

```python
import re, os
for fn in os.listdir(wiki_dir):
    if not fn.endswith('.md'): continue
    p = os.path.join(wiki_dir, fn); s = open(p, encoding='utf-8').read()
    s = re.sub(r'\[([^\]]+)\]\((?!https?:)([\w\-]+)\.md\)', r'[\1](\2)', s)
    s = re.sub(r'\[([^\]]+)\]\((?:\.\./)?references/([\w\-]+)\.md\)',
               r'[\1](https://github.com/<owner>/<repo>/blob/main/references/\2.md)', s)
    open(p, 'w', encoding='utf-8').write(s)
```

**تأیید با clone تازه، نه با خروجی push.** بعد از push یک clone دیگر در پوشهٔ دیگر بگیر و `ls` + `git log --oneline -1` + `wc -l` بزن. پیام `master -> master` فقط یعنی سرور قبول کرد، نه اینکه محتوا همان است که می‌خواستی.

**Verify with a fresh clone, not with the push output.** `master -> master` means the server accepted it, not that the content is what you intended.

**قاعدهٔ گسترده‌تر:** تغییر در `doclib.py` (دستور یا قابلیت جدید) هم یعنی مستندات باید آپدیت شوند — دستور جدید در `CLI-Reference.md`، جریانش در `Ingest-Workflow.md`.

**Broader rule:** a change in `doclib.py` (new command or feature) means the docs must be updated too — the new command in `CLI-Reference.md`, its flow in `Ingest-Workflow.md`.

## ۴. سایت مستندات وب (VitePress + GitHub Pages)

Web docs site (VitePress + GitHub Pages)

**آدرس:** `https://net-packet.github.io/Hybrid_SQLite-Karpathy_Wiki/` — انگلیسی؛ `.../fa/` نسخهٔ فارسی RTL.

**URL:** `https://net-packet.github.io/Hybrid_SQLite-Karpathy_Wiki/` — English; `.../fa/` is the Persian RTL version.

**ساختار:** `docs/` (محتوای VitePress) + `docs/.vitepress/config.mts` (locales: `root`=EN، `fa`=FA با `dir: 'rtl'`) + `docs/package.json` + `.github/workflows/deploy-docs.yml`.

**Structure:** `docs/` (VitePress content) + `docs/.vitepress/config.mts` (locales: `root`=EN, `fa`=FA with `dir: 'rtl'`) + `docs/package.json` + `.github/workflows/deploy-docs.yml`.

**قاعدهٔ همگام‌سازی:** هر تغییری در یک فایل `.md` ریشه باید به معادلش در `docs/` **هر دو زبان** کپی شود:

**Sync rule:** every change to a root `.md` file must be copied to its counterpart in `docs/` for **both languages**:

```bash
cd /tmp/Hybrid_SQLite-Karpathy_Wiki
cp Home.md docs/index.md && cp Home.md docs/fa/index.md
cp CLI-Reference.md docs/guide/cli.md && cp CLI-Reference.md docs/fa/guide/cli.md
cp Architecture.md docs/guide/architecture.md && cp Architecture.md docs/fa/guide/architecture.md
cp Wiki-Layer.md docs/guide/wiki-layer.md && cp Wiki-Layer.md docs/fa/guide/wiki-layer.md
cp Ingest-Workflow.md docs/guide/ingest.md && cp Ingest-Workflow.md docs/fa/guide/ingest.md
cp Design-Decisions.md docs/guide/design-decisions.md && cp Design-Decisions.md docs/fa/guide/design-decisions.md
cp Skills-And-Automation.md docs/guide/skills.md && cp Skills-And-Automation.md docs/fa/guide/skills.md
cp Collection-<name>.md docs/collections/<name>.md && cp Collection-<name>.md docs/fa/collections/<name>.md
```

**هرگز فایل‌های `docs/` را مستقیم ویرایش نکن** — آن‌ها آینه‌اند. ابتدا ریشه را آپدیت کن، بعد کپی.

**Never edit `docs/` files directly** — they are mirrors. Update the root first, then copy.

**پیت‌فال لینک:** اگر فایل ریشه از لینک سبک ویکی (`[x](Architecture)`) استفاده کند، در VitePress **شکسته** می‌شود. برای سایت از مسیر فایل استفاده کن: `[x](/guide/architecture)`.

**Link pitfall:** if a root file uses wiki-style links (`[x](Architecture)`), it **breaks** in VitePress. For the site use file paths: `[x](/guide/architecture)`.

**build محلی قبل از push / Local build before push:**

```bash
cd docs && npm install && npm run docs:build   # output: docs/.vitepress/dist
```

`node_modules/`، `.vitepress/dist/`، `.vitepress/cache/` در `docs/.gitignore` هستند — commit نشوند.

`node_modules/`, `.vitepress/dist/`, `.vitepress/cache/` are in `docs/.gitignore` — do not commit them.

**ورک‌فلوی deploy:** `push` به `main` با تغییر در `docs/**` یا `workflow_dispatch` → `npm install` → `npm run docs:build` → `upload-pages-artifact@v3` → `deploy-pages@v4`.

**Deploy workflow:** `push` to `main` touching `docs/**`, or `workflow_dispatch` → `npm install` → `npm run docs:build` → `upload-pages-artifact@v3` → `deploy-pages@v4`.

`deploy-pages@v4` + مجوزهای `pages: write`، `id-token: write` خودش Pages را فعال می‌کند. **ولی** اگر اولین اجرا با `Pages site not found` شکست خورد، یک‌بار Settings → Pages → Source: **GitHub Actions** را انتخاب کن.

`deploy-pages@v4` with `pages: write` and `id-token: write` permissions enables Pages by itself. **But** if the first run fails with `Pages site not found`, set Settings → Pages → Source: **GitHub Actions** once.

**تأیید وضعیت / Verify status:**

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://api.github.com/repos/net-packet/Hybrid_SQLite-Karpathy_Wiki/actions/runs?per_page=1" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['workflow_runs'][0]; print(d['status'], d['conclusion'])"
curl -s -o /dev/null -w "%{http_code}\n" https://net-packet.github.io/Hybrid_SQLite-Karpathy_Wiki/
```

**هرگز فرض نکن سایت بالاست چون push موفق بود** — Actions اجرا می‌شود، بعد Pages propagate می‌کند (۳۰–۶۰ ثانیه). تا `200` نگرفتی نگو «انجام شد».

**Never assume the site is up because the push succeeded** — Actions runs, then Pages propagates (30–60s). Do not say "done" until you get `200`.

## ۵. پیت‌فال‌های GitHub

GitHub pitfalls

| # | پیت‌فال / Pitfall |
|---|---|
| 1 | **دسترسی فقط با token در URL** — `git push https://<token>@github.com/...` کار می‌کند. credential helper و `gh auth` در دسترس نیستند؛ push بدون token با `could not read Password` (exit 128) شکست می‌خورد. |
| 2 | **`Author identity unknown` (exit 128)** — `git config user.email "hermes@local" && git config user.name "Hermes Agent"` |
| 3 | **`write_file` برای فایل‌های داخل `/tmp/Hybrid_SQLite-Karpathy_Wiki/` رد می‌شود** (`outside HERMES_WRITE`) — از heredoc در `terminal` استفاده کن. نوشتن با `execute_code` روی دیسک `terminal` دیده نمی‌شود؛ همهٔ نوشتن‌های این repo را با `terminal` انجام بده. |

| # | Pitfall |
|---|---|
| 1 | **Access is token-in-URL only** — `git push https://<token>@github.com/...` works. No credential helper and no `gh auth`; push without a token fails with `could not read Password` (exit 128). |
| 2 | **`Author identity unknown` (exit 128)** — `git config user.email "hermes@local" && git config user.name "Hermes Agent"` |
| 3 | **`write_file` is refused for files under `/tmp/Hybrid_SQLite-Karpathy_Wiki/`** (`outside HERMES_WRITE`) — use a heredoc in `terminal`. Writes from `execute_code` are not visible on `terminal`'s disk; do every write in this repo with `terminal`. |

## ۷. بازبینی کهنگی repo / Staleness Audit

هدف: تشخیص اینکه repo واقعاً قابل انتقال است یا فقط مستندات را دارد.
Goal: determine whether the repo is genuinely portable or only has the docs.

### قاعدهٔ پایه / Base rule

repo **آینهٔ** وضعیت زنده است، نه منبع. هفت مقایسه انجام بده و هیچکدام را از حافظه یا از `git log` نگیر:
The repo is a **mirror** of the live state, never the source. Run seven comparisons and take none of them from memory or from `git log`:

| # | مقایسه / Comparison | حکم کهنگی / Stale if |
|---|---|---|
| 1 | `diff -q doclib.py /opt/data/documents/doclib.py` | متفاوتند / they differ |
| 2 | `diff -q Home.md /opt/data/documents/SCHEMA.md` | متفاوتند / they differ |
| 3 | دستورهای `add_parser` در دو `doclib.py` | تعداد یا نام فرق دارد / count or names differ |
| 4 | `Ingest-Workflow.md` vs `SKILL.md` | `wc -l` فرق دارد بیشتر از ~۲۰ خط / line counts diverge |
| 5 | `Skills-And-Automation.md` | قاعده‌ها یا ترتیب مراحل کهنه / rules or step order outdated |
| 6 | `CLI-Reference.md` | دستور `doclib.py` را ندارد / missing a `doclib.py` command |
| 7 | `references/` | در repo نیست یا فایل کم دارد / absent or short |

### فایل‌های آینه / Mirror files

هرکدام یک منبع زنده دارد و باید همان جلسه همگام شود:
Each has one live source and must sync the same session:

| فایل repo / Repo file | منبع زنده / Live source |
|---|---|
| `doclib.py` | `/opt/data/documents/doclib.py` |
| `Home.md` | `/opt/data/documents/SCHEMA.md` |
| `Collection-<name>.md` | `collections/<name>/COLLECTION.md` |
| `Ingest-Workflow.md` | `SKILL.md` |
| `Skills-And-Automation.md` | `SKILL.md` (خلاصه / summary) |
| `CLI-Reference.md` | `add_parser` در `doclib.py` |
| `references/*.md` | `SKILL.md` + `references/` زنده / live |
| `docs/**` | فایل‌های `.md` ریشه / root `.md` files |

### پیت‌فال‌ها / Pitfalls

- **`Skills-And-Automation.md` را در گزارش جا نینداز.** این فایل یک بلوک کد دارد که ادعا می‌کند «Skill Content (Full)» است ولی ۸۰ خط خلاصه است. هر تغییر `SKILL.md` آن را کهنه می‌کند.
  **Do not omit `Skills-And-Automation.md` from the report.** It carries a code block labelled "Skill Content (Full)" that is really an 80-line summary; every `SKILL.md` change makes it stale.
- **`setup.py` نام `Home.md` را hardcode می‌کند** (`schema_src = REPO_ROOT / "Home.md"  # wiki Home.md = SCHEMA.md`). اگر `Home.md` با `SCHEMA.md` زنده فرق کند، هر کاربر جدید **اسکیمای کهنه** نصب می‌کند — دیتابیسش نسازگار می‌شود.
  **`setup.py` hardcodes `Home.md` as the schema source.** If it diverges from the live `SCHEMA.md`, every new user installs an **outdated schema** and gets an incompatible database.
- **`references/` در repo نیست.** راهنمای اسکیل آزاد به `references/*.md` ارجاع می‌دهد؛ بدون آن فایل‌ها هم اسکیل سوراخ است و هم لینک‌های VitePress 404 می‌دهند. تصمیم درست عموماً: کپی به `references/` ریشه + یک کپی در `docs/public/references/` برای سایت.
  **`references/` is absent from the repo.** The guide links to it, so the skill has holes and VitePress links 404. Usual fix: copy to root `references/` plus an extra copy in `docs/public/references/` for the site.
- **commit message ادعای قابلیت می‌کند که کد ندارد.** قبلپذیرش، `add_parser` را grep کن.
  **A commit message can claim a capability the code never got.** Grep `add_parser` before trusting it.
- **تست انتقال در پوشهٔ خالی، نه روی آرشیو زنده.** `python3 setup.py --root /tmp/stagetest` → `add` یک PDF → `search` → `lint`. بدون این، «قابل انتقال» فقط ادعاست.
  **Test portability in an empty directory, not against the live archive.** Without this, "portable" is a claim, not a fact.

### ترتیب اجرای همگام‌سازی / Sync execution order

۱. `doclib.py` (کد اول — بقیه بر آن سوارند) / code first
۲. `SCHEMA.md` → `SCHEMA.md` + `Home.md`
۳. `references/`
۴. `Ingest-Workflow.md` ← `SKILL.md`
۵. `Skills-And-Automation.md`
۶. `CLI-Reference.md` (دستورهای `add_parser` را تطبیق بده / match `add_parser`)
۷. تست در پوشهٔ خالی، بعد build سایت، بعد push

همهٔ کپی‌ها را یک‌جا بزن، بعد `docs/` را از فایل‌های ریشه آینه کن (بخش ۴)، نه برعکس.
Copy once at the root, then mirror into `docs/` (section 4) — never the reverse.

## ۶. بخش About (فقط دستی)

About section (manual only)

Settings → General → About → آیکن چرخ‌دنده (⚙️):

Settings → General → About → gear icon (⚙️):

- **Description:** "Bilingual (fa/en) hybrid document archive: SQLite FTS5 search + Karpathy-style markdown wiki. Multi-collection, multi-source (PDF, audio, images, web), Persian normalization, human-in-the-loop ingest."
- **Website:** `https://github.com/net-packet/Hybrid_SQLite-Karpathy_Wiki/wiki`
- **Topics:** `document-archive`, `sqlite`, `fts5`, `karpathy-wiki`, `persian`, `bilingual`, `groq-stt`, `hermes-agent`

## ۸. نقشهٔ فایل‌های مخزن اصلی

Main repo file map

| صفحهٔ ویکی / Wiki page | فایل منبع / Source file |
|---|---|
| Home | `Home.md` |
| CLI-Reference | `CLI-Reference.md` |
| Architecture | `Architecture.md` |
| Wiki-Layer | `Wiki-Layer.md` |
| Collection-office-works | `Collection-office-works.md` |
| Collection-maintenance-learning | `Collection-maintenance-learning.md` |
| Collection-ai-learning | `Collection-ai-learning.md` |
| Ingest-Workflow | `Ingest-Workflow.md` |
| Design-Decisions | `Design-Decisions.md` |
| Skills-And-Automation | `Skills-And-Automation.md` |
| _Sidebar | `_Sidebar.md` |
| _Footer | `_Footer.md` |

همهٔ فایل‌های منبع بعد از clone در `/tmp/Hybrid_SQLite-Karpathy_Wiki/` هستند، یا از فایل‌های محلی آرشیو با اسکریپت sync بالا تولید می‌شوند.

All source files live in `/tmp/Hybrid_SQLite-Karpathy_Wiki/` after cloning, or are generated from the local archive files by the sync script above.
