# Handing this to an AI agent

The repository is designed so an agent can install and use it from a single
file. This page explains what that file says and why.

## The entry point

`AGENTS.md` in the repository root. 67 lines. An agent that reads only that
file should be able to:

1. clone and install
2. know what `VERIFY: PASS` means
3. find the right page when something breaks
4. know the three rules it must not violate

## What the agent is told

| Section | Purpose |
|---|---|
| Install | three commands, and the exact success line |
| What `--verify` checks | so a failure is interpretable, not mysterious |
| After install | the four commands it will actually use |
| Where to look when something breaks | a symptom → page table |
| Hard rules | the four things that must never happen |
| What this is not | prevents it from adding embeddings "to help" |

## The hard rules, and why each exists

**Never modify `raw/`.** Every citation in the wiki points into it. A modified
file means citations that cannot be checked, and no way to know which ones.

**Never add a file without confirmation.** The agent must propose a collection
and wait. A document in the wrong collection will be found in the wrong context
later, and nobody will remember why it is there.

**Every number needs a citation.** File plus page. This is what makes a wrong
number findable six months later.

**`index.db` is disposable.** If in doubt, delete it and re-add from `raw/`.
This prevents the agent from trying to repair a database by hand.

## The failure mode this prevents

An agent given a document archive and no constraints will, in order:

1. add the file to whichever collection seems closest, without asking
2. write a summary page with numbers and no citations
3. when search returns nothing, delete the database and rebuild it
4. when that does not help, start editing `doclib.py`

Each step is individually reasonable and collectively destroys the archive's
value. `AGENTS.md` blocks step 1 and step 2, and gives step 3 a safe form.

## The test that matters

Give a fresh agent only this:

> Read AGENTS.md and install this archive at ~/test-archive. Report the last
> line of output.

It must end with `VERIFY: PASS` and ask no questions. If it asks something
`AGENTS.md` should have answered, that is a bug in `AGENTS.md`.

This is portability condition 5 in [CONTRACT](https://github.com/net-packet/Hybrid_SQLiteFTS5-Karpathy_Wiki/blob/main/CONTRACT.md),
and it is the one that decays silently — nothing detects a stale `AGENTS.md`.

## What the agent should read second

| Need | File |
|---|---|
| the rules of the archive | `SCHEMA.md` (copied into the archive root) |
| ingest procedure detail | `references/ingest-procedures.md` |
| collection boundaries | `references/collection-scope.md` |
| Persian folding | `references/persian-normalization.md` |
| the wiki page contract | `references/wiki-page-contract.md` |

Nine reference files ship with the archive, so the agent does not need the
repository after install — only the archive.

## Why a file and not a prompt

A prompt lives in one conversation. `AGENTS.md` lives in the repository, is
versioned with the code, and is read by every agent that clones it. When the
install procedure changes, the file changes in the same commit — so the
instructions and the code cannot drift apart.
