#!/usr/bin/env python3
"""Build docs/ from scratch. docs/ is generated — never edit it, never commit it.

Source of truth:
    wiki/*.md            -> docs/reference/*.md   (all pages, _* excluded)
    wiki/_Sidebar.md     -> the sidebar in docs/.vitepress/config.mts
    wiki/Home.md         -> body of docs/index.md (behind the landing hero)
    tools/site/landing.md  -> frontmatter of docs/index.md
    tools/site/config.mts.tmpl -> docs/.vitepress/config.mts
    tools/site/package.json    -> docs/package.json

docs/ is deleted first, every time. If the build fails halfway, docs/ is
incomplete — run it again rather than patching the output.

Run from the repo root:  python3 tools/build_docs.py
"""
import json
import re
import shutil
import sys
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parent.parent
WIKI = REPO / "wiki"
SITE = REPO / "tools" / "site"
DOCS = REPO / "docs"
BASE = "/Hybrid_SQLiteFTS5-Karpathy_Wiki/"


def fail(msg: str) -> int:
    print(f"ERROR: {msg}")
    return 1


def rewrite_links(text: str, page: Path | None = None) -> str:
    """Point every relative wiki link at its /reference/ URL.

    Links are resolved **relative to the page they appear in**, exactly as a
    file tree would resolve them: from wiki/layer2/DB-FTS.md, `Persian-Normalize`
    means wiki/layer2/Persian-Normalize, i.e. /reference/layer2/Persian-Normalize.
    Flattening to /reference/Persian-Normalize would be a 404.

    Extensionless links (`layer3/X`) and `.md` links are both pages. A link with
    any other extension — ../../raw/files/x.pdf, a .png — is an illustrative
    path into an archive, not a site page, and is left exactly as written.
    """
    here = page.parent if page is not None else Path(".")

    def sub(m: re.Match) -> str:
        target = m.group(1)
        if target.startswith(("http://", "https://", "/", "#", "mailto:")):
            return m.group(0)
        path_part, _, frag = target.partition("#")
        last = path_part.rsplit("/", 1)[-1]
        if last.endswith(".md"):
            path_part = path_part[:-3]
        elif "." in last or not path_part:
            return m.group(0)
        try:
            resolved = (here / path_part).as_posix()
            parts = [p for p in PurePosixPath(resolved).parts if p not in ("", ".")]
            # collapse any remaining .. that escaped the wiki root
            out: list[str] = []
            for part in parts:
                if part == "..":
                    if out:
                        out.pop()
                    continue
                out.append(part)
        except Exception:
            return m.group(0)
        if not out:
            return m.group(0)
        link = "/reference/" + "/".join(out)
        return f"]({link}{'#' + frag if frag else ''})"

    return re.sub(r"\]\(([^)\s]+)\)", sub, text)


def build_sidebar() -> str:
    """Turn wiki/_Sidebar.md into a VitePress sidebar array."""
    src = WIKI / "_Sidebar.md"
    if not src.exists():
        return "[]"
    groups: list[dict] = []
    current: dict | None = None
    for raw in src.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("**") and line.endswith("**"):
            name = line.strip("*").strip()
            current = {"text": name, "collapsed": False, "items": []}
            groups.append(current)
            continue
        m = re.match(r"^-\s*\[([^\]]+)\]\(([^)]+)\)", line)
        if not m:
            continue
        label, target = m.group(1), re.sub(r"\.md$", "", m.group(2))
        if current is None:
            current = {"text": "Pages", "collapsed": False, "items": []}
            groups.append(current)
        current["items"].append({"text": label, "link": f"/reference/{target}"})
    # a group with no items would render as an empty heading
    groups = [g for g in groups if g["items"]]
    return json.dumps(groups, ensure_ascii=False, indent=2)


def main() -> int:
    for need in (WIKI, SITE):
        if not need.is_dir():
            return fail(f"missing {need}")

    # 1. wipe — docs/ is generated, so nothing here is worth keeping.
    # node_modules is the one exception: it is a local install, not content,
    # and deleting it would force a full `npm ci` on every rebuild.
    if DOCS.exists():
        for child in DOCS.iterdir():
            if child.name == "node_modules":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    DOCS.mkdir(parents=True, exist_ok=True)

    # 2. site shell
    for name in ("package.json", "package-lock.json"):
        src = SITE / name
        if src.exists():
            shutil.copy2(src, DOCS / name)
    tpl = (SITE / "config.mts.tmpl").read_text(encoding="utf-8")
    (DOCS / ".vitepress").mkdir()
    (DOCS / ".vitepress" / "config.mts").write_text(
        tpl.replace("{{SIDEBAR}}", build_sidebar()), encoding="utf-8"
    )

    # 3. every wiki page -> docs/reference/, links rewritten
    n = 0
    skipped = []
    for f in sorted(WIKI.rglob("*.md")):
        rel = f.relative_to(WIKI)
        if rel.name.startswith("_"):
            skipped.append(str(rel))
            continue
        out = DOCS / "reference" / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rewrite_links(f.read_text(encoding="utf-8"), rel), encoding="utf-8")
        n += 1

    # 4. landing page: hero frontmatter + the body of wiki/Home.md
    landing = (SITE / "landing.md").read_text(encoding="utf-8").rstrip()
    if not landing.startswith("---"):
        return fail("tools/site/landing.md must start with YAML frontmatter")
    home = WIKI / "Home.md"
    body = home.read_text(encoding="utf-8") if home.exists() else ""
    body = re.sub(r"^#\s+.*?\n", "", body, count=1)  # drop the H1, the hero has it
    (DOCS / "index.md").write_text(
        landing + "\n\n" + rewrite_links(body, Path("Home.md")).lstrip(), encoding="utf-8"
    )

    print(f"built docs/ — {n} pages -> docs/reference")
    if skipped:
        print(f"skipped (wiki-only): {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
