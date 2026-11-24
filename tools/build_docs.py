#!/usr/bin/env python3
"""Copy wiki/*.md into docs/reference/ and fix links for VitePress.

The wiki uses relative links that work in a plain directory tree. VitePress
serves from docs/, so every link needs to stay relative — which it does,
because the tree shape is preserved. The only change is the .md extension,
which VitePress strips via cleanUrls.

Run from the repo root:  python3 tools/build_docs.py
"""
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "wiki"
DST = REPO / "docs" / "reference"


def main() -> int:
    if not SRC.is_dir():
        print(f"missing {SRC}")
        return 1
    if DST.exists():
        shutil.rmtree(DST)
    DST.mkdir(parents=True)

    n = 0
    skipped = []
    for f in sorted(SRC.rglob("*.md")):
        rel = f.relative_to(SRC)
        # _Sidebar.md / _Footer.md are GitHub-wiki chrome, not site pages.
        if rel.name.startswith("_"):
            skipped.append(str(rel))
            continue
        out = DST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        n += 1

    print(f"copied {n} pages -> {DST.relative_to(REPO)}")
    if skipped:
        print(f"skipped (wiki-only): {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
