#!/usr/bin/env python3
"""Bootstrap a hybrid SQLite-FTS5 + wiki document archive.

Everything this script copies is declared in setup.toml. It holds no
knowledge of the archive layout itself — change the TOML, not this file.

    python3 setup.py --root ~/archive
    python3 setup.py --root ~/archive --verify
    python3 setup.py --root ~/archive --skip-install
"""
from __future__ import annotations

import argparse
import os
import shutil
import sqlite3
import subprocess
import sys
import tomllib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOML = REPO / "setup.toml"


def load_plan() -> dict:
    with open(TOML, "rb") as fh:
        return tomllib.load(fh)


def install_deps(skip: bool) -> None:
    if skip:
        print("  deps: skipped (--skip-install)")
        return
    req = REPO / "src" / "requirements.txt"
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "-q", "-r", str(req)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(f"  deps: FAILED\n{r.stderr[-800:]}")
        print("  hint: run with --skip-install if the packages are already present")
        sys.exit(1)
    print("  deps: installed")


def check_ffmpeg() -> None:
    if shutil.which("ffmpeg"):
        print("  ffmpeg: found")
    else:
        print("  ffmpeg: NOT found — audio files over 25 MB cannot be split")


def build(root: Path, plan: dict) -> None:
    collections = plan["collections"]["default"]

    for coll in collections:
        for d in plan["dir"]:
            (root / "collections" / coll / d["path"]).mkdir(parents=True, exist_ok=True)
        for f in plan["file"]:
            target = root / "collections" / coll / f["path"]
            if not target.exists():
                target.write_text(f["content"], encoding="utf-8")
        coll_md = REPO / "template" / "collections" / coll / "COLLECTION.md"
        if coll_md.exists():
            shutil.copy2(coll_md, root / "collections" / coll / "COLLECTION.md")
        else:
            print(f"  warn: no COLLECTION.md template for {coll}")

    for entry in plan["copy"]:
        src, dst = REPO / entry["from"], root / entry["to"]
        if not src.exists():
            print(f"  warn: missing source {entry['from']}")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    # Create index.db eagerly and stamp its schema version, so --verify has
    # something to check even before the first ingest.
    doclib = root / "doclib.py"
    if doclib.exists():
        env = dict(os.environ, DOCLIB_ROOT=str(root))
        subprocess.run([sys.executable, str(doclib), "stats"],
                       capture_output=True, text=True, env=env)
    db = root / "index.db"
    if db.exists():
        con = sqlite3.connect(db)
        con.execute(f"PRAGMA user_version = {plan['archive']['schema_version']}")
        con.commit()
        con.close()

    print(f"  collections: {len(collections)} ({', '.join(collections)})")


def verify(root: Path, plan: dict) -> bool:
    """Five checks. Any failure means the install did not work."""
    doclib = root / "doclib.py"
    results: list[tuple[str, bool, str]] = []

    def run(*args: str) -> tuple[int, str]:
        env = dict(os.environ, DOCLIB_ROOT=str(root))
        r = subprocess.run([sys.executable, str(doclib), *args],
                           capture_output=True, text=True, env=env)
        return r.returncode, (r.stdout + r.stderr)

    # 1 — collections listed
    code, out = run("collections")
    expected = plan["collections"]["default"]
    ok = code == 0 and all(c in out for c in expected)
    results.append(("collections", ok, out.strip().splitlines()[0] if out.strip() else "no output"))

    # 2 — index.db exists with the right schema version
    db = root / "index.db"
    ok, detail = False, "index.db missing"
    if db.exists():
        con = sqlite3.connect(db)
        tables = {r[0] for r in con.execute(
            "select name from sqlite_master where type in ('table','view')")}
        ver = con.execute("pragma user_version").fetchone()[0]
        con.close()
        need = {"files", "chunks", "chunks_fts"}
        ok = need <= tables and ver == plan["archive"]["schema_version"]
        detail = f"tables ok={need <= tables}, user_version={ver}"
    results.append(("schema", ok, detail))

    # 3 — add a file, then 4 — find it by a Persian query
    seed = REPO / "demo" / "seed"
    probe = next(iter(sorted(seed.glob("*"))), None) if seed.exists() else None
    if probe is None:
        results.append(("add", False, "no demo/seed file to test with"))
        results.append(("search", False, "skipped — add failed"))
    else:
        # doclib requires sources to live inside the collection, so stage the
        # seed file there first (this is what a real ingest does too).
        staged = root / "collections" / expected[0] / "raw" / "files" / probe.name
        staged.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(probe, staged)
        code, out = run("add", str(staged), "-c", expected[0])
        # The CLI prints a Persian summary; the durable proof is a row in `files`.
        rows = 0
        if db.exists():
            con = sqlite3.connect(db)
            rows = con.execute("select count(*) from files").fetchone()[0]
            con.close()
        ok = code == 0 and rows >= 1
        results.append(("add", ok, f"files rows={rows}"))

        word = "قرارداد"
        code, out = run("search", word)
        ok = code == 0 and word in out
        results.append(("search", ok, f"query '{word}' -> {'hit' if ok else 'no hit'}"))

    # 5 — lint clean
    code, out = run("lint", "-c", expected[0])
    ok = code == 0
    results.append(("lint", ok, out.strip().splitlines()[-1] if out.strip() else "no output"))

    print("\n  verify:")
    for name, ok, detail in results:
        print(f"    {'PASS' if ok else 'FAIL'}  {name:<12} {detail}")

    passed = all(r[1] for r in results)
    print(f"\nVERIFY: {'PASS' if passed else 'FAIL'}")
    if not passed:
        print("  next: read wiki/layer4/Debug-Playbook.md in the repo")
    return passed


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap a hybrid document archive.")
    ap.add_argument("--root", default=None, help="archive root (default from setup.toml)")
    ap.add_argument("--collections", nargs="+", default=None, help="override collection list")
    ap.add_argument("--skip-install", action="store_true", help="do not pip install")
    ap.add_argument("--verify", action="store_true", help="run the five acceptance checks")
    args = ap.parse_args()

    plan = load_plan()
    if args.collections:
        plan["collections"]["default"] = args.collections

    root = Path(os.path.expanduser(args.root or plan["archive"]["default_root"])).resolve()

    print(f"archive root: {root}")
    print("installing:")
    install_deps(args.skip_install)
    check_ffmpeg()
    build(root, plan)

    if args.verify:
        return 0 if verify(root, plan) else 1
    print("\nnext: python3 setup.py --root <path> --verify")
    return 0


if __name__ == "__main__":
    sys.exit(main())
