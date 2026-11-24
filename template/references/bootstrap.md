# راه‌اندازی آرشیو / Bootstrap

> فقط برای **راه‌اندازی آرشیو جدید**. برای استفادهٔ روزمره به `SKILL.md` رجوع کن.
>
> Only for **bootstrapping a new archive**. For day-to-day use, go to `SKILL.md`.

## فایل‌های مخزن اصلی

Files in the main repo

| فایل / File | کاربرد / Purpose |
|---|---|
| `doclib.py` | اسکریپت مستقل: extract/index/search/links/lint/graph / Standalone script: extract/index/search/links/lint/graph |
| `requirements.txt` | `pypdf>=7.1.1`، `python-docx>=1.2.0`، `openpyxl>=3.1.5`، `python-pptx>=1.0.2` |
| `setup.py` | اسکریپت راه‌اندازی / Bootstrap script: `python3 setup.py --root ~/my-archive` پوشه‌ها را می‌سازد، فایل‌ها را کپی می‌کند، `SCHEMA.md` و `COLLECTION.md`ها را می‌نویسد / creates dirs, copies files, writes `SCHEMA.md` + `COLLECTION.md` files |
| `README.md` | معرفی دوزبانهٔ پروژه با quick-start / Bilingual project overview with quick-start |
| `wiki/*.md` | منابع markdown صفحات GitHub Wiki / Source markdown for GitHub Wiki pages |

## جریان کاربر جدید

New user workflow

```bash
git clone https://github.com/net-packet/Hybrid_SQLite-Karpathy_Wiki.git
cd Hybrid_SQLite-Karpathy_Wiki
python3 setup.py --root ~/my-archive
# Add GROQ_API_KEY to ~/.env
export DOCLIB_ROOT=~/my-archive
python3 ~/my-archive/doclib.py add file.pdf -c office-works
```

## گزینه‌های `setup.py`

`setup.py` options

```bash
python3 setup.py --root ~/my-archive --collections office-works maintenance-learning ai-learning
python3 setup.py --root ~/custom --collections my-collection --skip-install
```

## `setup.py` چه می‌کند

What `setup.py` does

۱. `requirements.txt` را با `pip install --user` نصب می‌کند (مگر `--skip-install`).  
۲. وجود `ffmpeg` را چک می‌کند (هشدار اگر نبود).  
۳. ساختار پوشه‌ها را برای هر مجموعه می‌سازد: `raw/{files,web,audio,images}`، `wiki/{sources,entities,concepts}`.  
۴. `doclib.py` را به ریشهٔ آرشیو کپی می‌کند.  
۵. `Home.md` → `SCHEMA.md`.  
۶. `Collection-<name>.md` → `collections/<name>/COLLECTION.md`.  
۷. `wiki/index.md` و `wiki/log.md` خالی برای هر مجموعه می‌سازد.

1. Installs `requirements.txt` via `pip install --user` (unless `--skip-install`).  
2. Checks `ffmpeg` availability (warns if missing).  
3. Creates the directory structure for each collection: `raw/{files,web,audio,images}`, `wiki/{sources,entities,concepts}`.  
4. Copies `doclib.py` to the archive root.  
5. Copies `Home.md` → `SCHEMA.md`.  
6. Copies `Collection-<name>.md` → `collections/<name>/COLLECTION.md`.  
7. Creates empty `wiki/index.md` and `wiki/log.md` per collection.

## پیش‌نیازها

Requirements

- Python 3.11+
- `ffmpeg` در PATH (برای صداهای بزرگ‌تر از ۲۵MB / for audio >25MB)
- کلید Groq در `~/.env` به شکل `GROQ_API_KEY=...` (فقط برای STT صدا / for audio STT only)
