# نصب

```bash
git clone https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki.git
cd Hybrid_SQLiteFTS5-Karpathy_Wiki
python3 src/setup.py --root ~/archive --verify
```

آخرین خط خروجی باید این باشد:

```
VERIFY: PASS
```

هر چیز دیگری یعنی نصب نشده. موفقیت را گزارش نکن.

## چه چیزی ساخته می‌شود

```
~/archive/
├── doclib.py            تنها فایل اجرایی
├── SCHEMA.md            قواعد، در یک صفحه
├── index.db             خالی، user_version = 100
├── references/          ۹ فایل مرجع
└── collections/
    ├── office-works/
    │   ├── COLLECTION.md
    │   ├── raw/{files,web,audio,images}/
    │   └── wiki/{index.md,log.md,sources/,entities/,concepts/}
    ├── maintenance-learning/
    └── ai-learning/
```

## پیش‌نیازها

| نیاز | چرا |
|---|---|
| Python 3.11+ | `tomllib` از ۳.۱۱ در کتابخانه استاندارد است |
| `pypdf`، `python-docx`، `openpyxl`، `python-pptx` | `setup.py` نصب می‌کند |
| `ffmpeg` | فقط برای صدای بیش از ۲۵ مگابایت |
| `GROQ_API_KEY` | فقط برای تبدیل صدا به متن |

## پنج بررسی `--verify`

| بررسی | انتظار |
|---|---|
| `collections` | سه مجموعه از `setup.toml` وجود دارند |
| `schema` | `files`، `chunks`، `chunks_fts` هستند؛ `user_version = 100` |
| `add` | یک فایل نمونه ایندکس می‌شود؛ `files` حداقل یک ردیف دارد |
| `search` | `search "قرارداد"` نتیجه می‌دهد |
| `lint` | ایراد ساختاری ندارد |

## تکرارپذیری

اجرای دوبارهٔ `setup.py` بی‌خطر است. `index.md` و `log.md` فقط اگر نباشند
ساخته می‌شوند، و `index.db` هرگز حذف نمی‌شود.

## حذف

```bash
rm -rf ~/archive
```

بدون پکیج سیستمی، بدون سرویس، بدون state گلوبال.
