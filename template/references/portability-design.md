# بسته‌بندی آرشیو به‌عنوان ریپوی قابل نصب / Packaging the Archive as an Installable Repo

هدف: یک agent ناشناس، با خواندن فقط `AGENTS.md`، همان سیستم را روی ماشین خودش راه بیندازد و به `VERIFY: PASS` برسد.
Goal: an unknown agent, reading only `AGENTS.md`, installs the same system on its own machine and reaches `VERIFY: PASS`.

## ساختار تأییدشدهٔ ریپو / Verified repo shape

```
AGENTS.md          ← تنها فایل ورودی agent (نه README)
CONTRACT.md        ← شرایط قابل‌آزمون قابل‌حمل بودن
README.md          ← برای انسان
setup.toml         ← نقشهٔ نصب؛ تنها جایی که چیدمان تعریف می‌شود
src/doclib.py      ← تنها فایل اجرایی (کپی بایت‌به‌بایت از منبع زنده)
src/setup.py       ← TOML را می‌خواند، هیچ دانشی از چیدمان ندارد
src/schema.sql     ← آینهٔ رشتهٔ SCHEMA در doclib.py
template/          ← SCHEMA.md + collections/*/COLLECTION.md + references/
demo/seed/         ← ۳ سند جعلی فارسی برای smoke test
demo/expected/     ← خروجی واقعی ضبط‌شده روی نصب تمیز
wiki/              ← ویکی چندلایه (why / how / use / repair)
docs/              ← VitePress
```

## قاعدهٔ طلایی: `setup.py` نباید چیدمان بداند / Golden rule

هر چیزی که کپی می‌شود در `setup.toml` اعلام می‌شود (`[[copy]]`، `[[dir]]`، `[[file]]`). تغییر چیدمان = ویرایش TOML، نه اسکریپت. اگر روزی مجبور شدی برای افزودن یک فایل `setup.py` را دست بزنی، طراحی را شکسته‌ای.
Every copied path is declared in `setup.toml`. Changing the layout means editing the TOML, never the script.

## `--verify` باید داده را بسنجد، نه stdout را / Verify the data, not the message

پیت‌فال واقعی: نسخهٔ اول `"file_id" in output` را چک می‌کرد و با پیام خوش‌بینانه ولی بدون ردیف، PASS می‌داد.
Real pitfall: the first version asserted `"file_id" in output` and passed on a cheerful message with no row.

```python
# غلط / wrong
ok = code == 0 and "file_id" in out.lower()
# درست / right
rows = con.execute("select count(*) from files").fetchone()[0]
ok = code == 0 and rows >= 1
```

پنج بررسی حداقلی / Five minimum checks: `collections`، `schema` (جدول‌ها + `PRAGMA user_version`)، `add` (ردیف در `files`)، `search` (هیت واقعی)، `lint` (کد خروج ۰).

## پیت‌فال: `add` فایل بیرون از `raw/` را با traceback رد می‌کند / add outside raw/ raises

`rel_path_of()` مسیر را نسبت به `raw/` ذخیره می‌کند، پس مسیر بیرون `ValueError: ... is not in the subpath of ...` می‌دهد — نه پیام تمیز. در `--verify` فایل seed را **اول داخل مجموعه کپی کن**، بعد `add` بزن:

```python
staged = root / "collections" / coll / "raw" / "files" / probe.name
shutil.copy2(probe, staged)
run("add", str(staged), "-c", coll)
```

## پیت‌فال: `doclib.py` جدول‌ها را می‌سازد ولی `user_version` را نمی‌زند

`doclib.py` با اولین اجرا (`stats`) جدول‌ها را می‌سازد، ولی `PRAGMA user_version` صفر می‌ماند. `setup.py` باید بعد از ساخت، مهر بزند:

```python
con.execute(f"PRAGMA user_version = {plan['archive']['schema_version']}")
```

## SKILL.md خودش قابل حمل نیست — بزرگ‌ترین شکاف / SKILL.md is not portable

`skills/productivity/document-archive/SKILL.md` حدود ۲۵ بار مسیر `/opt/data/documents` را hardcode کرده. اگر آن را در `template/` بگذاری و کپی کنی، روی آرشیوی که در `~/archive` نصب شده **همهٔ دستورهایش به مسیر غلط اشاره می‌کنند**.
The live SKILL.md hardcodes `/opt/data/documents` ~25 times. Copying it into a portable repo produces a skill whose every command points at the wrong path.

اگر خواستی SKILL.md را هم بفرستی: مسیر را از `DOCLIB_ROOT` بخوان، نه literal. و `setup.toml` یک `[[copy]]` برای `template/SKILL.md` بگیرد. تا آن زمان، `AGENTS.md` باید صریح بگوید رویهٔ کامل در `references/` است — وگرنه agent نمی‌داند ۹ فایل مرجع وجود دارد.
If you ship SKILL.md, read the root from `DOCLIB_ROOT` and add a `[[copy]]` entry. Until then `AGENTS.md` must explicitly point at `references/`, or the agent never learns those nine files exist.

## `AGENTS.md` باید هر subcommand را نام ببرد / AGENTS.md must name every subcommand

با مقایسهٔ مکانیکی پیدا می‌شود، نه با بازخوانی:

```bash
for c in add search show rm reindex list stats collections lint graph links ur-new ur-add ur-list; do
  grep -q "doclib.py $c" AGENTS.md && echo "  ok $c" || echo "  MISSING $c"
done
```

فایل‌های خطا را هم همین‌طور چک کن: هر صفحهٔ `wiki/layer4/Err-*.md` باید در جدول «symptom → page» باشد.

## شرط پنجم قابل‌حمل بودن، دستی است / Condition 5 is manual

چهار شرط اول با یک `--verify` سنجیده می‌شوند. شرط پنجم («یک agent تازه می‌تواند») فقط با تست واقعی سنجیده می‌شود: نشست تازه، فقط `AGENTS.md`، و اگر سؤالی پرسید که `AGENTS.md` باید جوابش را می‌داد، **باگ در `AGENTS.md` است نه در agent**. این شرط بی‌صدا کهنه می‌شود.

## VitePress: `locales` باید سطح بالا باشد / locales must be top-level

پیت‌فال پرهزینه: اگر `locales` را داخل `themeConfig` بگذاری، فقط `nav`/`sidebar` اعمال می‌شود و `lang`/`title`/`description` **بی‌صدا نادیده** گرفته می‌شوند — بیلد سبز است و `/fa/` هنوز `<html lang="en-US">` و عنوان انگلیسی دارد.

```ts
// غلط / wrong — lang and title ignored
export default defineConfig({ themeConfig: { locales: { fa: { lang: 'fa-IR', title: '…' } } } })
// درست / right
export default defineConfig({ locales: { fa: { lang: 'fa-IR', title: '…', themeConfig: { nav, sidebar } } } })
```

سنجش بعد از بیلد / verify after build:

```bash
grep -o 'lang="[^"]*"' dist/index.html dist/fa/index.html
grep -o '<title>[^<]*</title>' dist/index.html dist/fa/index.html
```

`lang="en"` برای ریشه و `lang="fa-IR"` + عنوان فارسی برای `/fa/`. اگر هر دو `en-US` بود، `locales` جای غلطی است.

## پیت‌فال: فایل‌های chrome ویکی گیت‌هاب نباید صفحهٔ سایت شوند / skip _Sidebar and _Footer

`_Sidebar.md` و `_Footer.md` مخصوص GitHub Wiki هستند. اگر اسکریپت همگام‌سازی همهٔ `*.md` را کپی کند، به صفحهٔ سایت تبدیل می‌شوند. در حلقهٔ کپی:

```python
if rel.name.startswith("_"):
    continue
```

## لینک‌ها: مسیر نسبی، و یک checker واقعی / Relative links plus a real checker

لینک‌های سبک ویکی (`[x](Architecture)`) در VitePress شکسته می‌شوند. به مسیر نسبی تبدیلشان کن. بعد با یک checker بسنج — نه با چشم:

```python
import re, pathlib
stems = {f.stem for f in pathlib.Path('.').rglob('*.md')}
for f in pathlib.Path('.').rglob('*.md'):
    for _, href in re.findall(r'\[([^\]]+)\]\(([^)]+)\)', f.read_text(encoding='utf-8')):
        h = href.split('#')[0].strip()
        if not h or h.startswith(('http','mailto')) or h.endswith(('.pdf','.png','.jpg')): continue
        base = h[:-3] if h.endswith('.md') else h
        if '/' in base:
            if not (f.parent/h).exists() and not (f.parent/(h+'.md')).exists(): print('BAD', f, href)
        elif base not in stems: print('BAD', f, href)
```

**مثال‌های درون بلوک کد را استثنا کن.** یک checker ساده‌لوح، مسیرهای نمونه مثل `sources/contract-1405` را «لینک شکسته» گزارش می‌کند و تو را دنبال باگ ناموجود می‌فرستد.
Exempt paths inside fenced code blocks — a naive checker flags example paths as dead links.

## مستندات تولیدشده نباید از منبع جدا بیفتند / Generated docs must not drift

`docs/reference/` از `wiki/` تولید می‌شود. CI باید fail کند اگر کپی کهنه است:

```yaml
- run: python3 tools/build_docs.py
- run: |
    if [ -n "$(git status --porcelain docs/reference)" ]; then
      echo "docs/reference is out of date"; exit 1
    fi
```

و **هرگز `docs/reference/` را دستی ویرایش نکن** — منبع `wiki/` است. اگر بیلد لینک شکسته گرفت، در `wiki/` درستش کن و دوباره تولید کن.

## مستندسازی باید با کد واقعی سنجیده شود / Document against the running code

سه بار در یک جلسه، صفحه‌ای دستوری را مستند کرد که وجود نداشت: `remove` (واقعی: `rm`)، `rebuild-fts` (واقعی: `reindex`)، `show -i` (چنین فلگی نیست). قبل از نوشتن هر صفحهٔ CLI:

```bash
python3 doclib.py --help
grep -oE 'add_parser\("[a-z-]+"' doclib.py | sort
grep -n 'add_argument' doclib.py
```

و اگر رفتاری واقعاً زشت است (مثل traceback به‌جای پیام خطا)، **مستندش کن، پنهانش نکن** — یک صفحهٔ `Err-*` که می‌گوید «این guard است ولی بد گزارش می‌شود» صادقانه‌تر از سکوت است.
