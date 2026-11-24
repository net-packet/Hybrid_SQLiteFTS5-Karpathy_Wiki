# Verify checklist — proving the install works

The five checks `setup.py --verify` runs, what each proves, and what it does
not.

```bash
python3 src/setup.py --root ~/archive --skip-install --verify
```

```
  verify:
    PASS  collections  ai-learning ...
    PASS  schema       tables ok=True, user_version=100
    PASS  add          files rows=1
    PASS  search       query 'قرارداد' -> hit
    PASS  lint         ✅ هیچ ایرادی پیدا نشد.

VERIFY: PASS
```

## What each check proves

| # | Check | Proves | Does **not** prove |
|---|---|---|---|
| 1 | `collections` | `DOCLIB_ROOT` resolves and the three collections exist | that they contain anything |
| 2 | `schema` | tables exist, `user_version = 100` | that the schema is correct for the data |
| 3 | `add` | extraction → chunks → `files` row works end to end | that extraction is correct for *your* file types |
| 4 | `search` | fold → FTS → join → output works | that Persian search is complete |
| 5 | `lint` | the wiki is structurally sound | that any number in it is true |

Check 3 uses a real seed file from `demo/seed/`, copied into the collection
first — because `add` requires sources inside `raw/`. It asserts a row in
`files`, not a line of stdout, so a cheerful message with no row still fails.

## The five portability conditions

`CONTRACT.md` in the repo states them. Each is testable:

| # | Condition | Test |
|---|---|---|
| 1 | installs into an empty directory | `--root /tmp/empty` |
| 2 | works with no network | `--skip-install`, then add a local file |
| 3 | self-verifies | `--verify` prints PASS |
| 4 | Persian search works | `search "قرارداد"` hits |
| 5 | a fresh agent can do it | new session, only `AGENTS.md` read |

Conditions 1–4 are covered by the single `--verify` run. Condition 5 is manual
and is the one that decays: `AGENTS.md` can drift from reality, and nothing
detects it.

## Condition 5 — the honest test

Start a new session with no memory of this one. Give it only:

> Read AGENTS.md and install this archive at ~/test-archive. Report the last
> line of output.

If it needs to ask a question that `AGENTS.md` should have answered, that is a
bug in `AGENTS.md`, not in the agent. Fix the file.

Run this whenever `AGENTS.md` or `setup.toml` changes.

## What to run after a change to `doclib.py`

```bash
python3 src/setup.py --root /tmp/verify-$(date +%s) --skip-install --verify
```

A fresh directory each time. Running `--verify` against an existing archive
proves less, because leftover state can mask a broken install.

## What to run after a change to `setup.toml`

Same command, plus confirm the new entries appeared:

```bash
ls ~/archive/collections/
ls ~/archive/references/
```

`setup.toml` is the install map; a typo in it produces a silently missing
directory, and `--verify` only checks the three collections.

## What `--verify` cannot catch

| Gap | Why |
|---|---|
| a broken DOCX | the seed is markdown |
| a scanned PDF | the seed is markdown |
| Groq failures | no network in the verify path |
| a wrong number in the wiki | lint checks citations exist, not that they are right |
| a collection added to `setup.toml` but not created | verify only checks the three defaults |

The seed is deliberately three small Persian markdown files: fast, no
dependencies, and enough to exercise folding. It is a smoke test, not a test
suite.
