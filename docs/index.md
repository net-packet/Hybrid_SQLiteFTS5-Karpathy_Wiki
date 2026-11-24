---
layout: home

hero:
  name: Hybrid Archive
  text: SQLite FTS5 + a wiki that cites
  tagline: Files you never modify, an index you can rebuild, and a wiki where every number has a page reference.
  actions:
    - theme: brand
      text: Install
      link: /guide/install
    - theme: alt
      text: Why hybrid?
      link: /reference/layer1/Why-Hybrid

features:
  - title: Three layers, kept apart
    details: raw/ is immutable evidence. index.db is a rebuildable cache. wiki/ is interpretation that must cite. Corrupt the database and nothing is lost.
  - title: Persian search that works
    details: تأخیر and تاخیر are the same word. So are کتاب and كتاب, and ۴۸۰ and 480. Folding happens before the index, not after the query.
  - title: Every number has a source
    details: A citation is file plus page. Lint fails a page with no citation. Six months later you can still check it.
  - title: An agent can install it
    details: AGENTS.md is 67 lines. Clone, run setup.py, expect VERIFY PASS. No questions needed.
---
