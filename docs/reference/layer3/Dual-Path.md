# Two paths to an answer, and when to use which

Every question about the corpus is answered one of two ways. They are not
interchangeable, and using the wrong one is the most common failure.

## Path A — the index

**Question shape:** "where is this word", "which file mentions X", "find the
clause about penalties".

```bash
python3 doclib.py search "جریمه تاخیر"
```

| Gives you | Does not give you |
|---|---|
| exact chunks, with file and page | synthesis |
| the original text, unmodified | whether two sources agree |
| reproducible results | anything outside the corpus |

Use it when you need **a pointer**, or when you need to **verify** something the
wiki claims.

## Path B — the wiki

**Question shape:** "what do these contracts say about penalties overall",
"is the budget consistent with the contract", "which document is authoritative".

Read `wiki/` — `sources/`, `entities/`, `concepts/` — then verify with Path A.

| Gives you | Does not give you |
|---|---|
| synthesis across sources | completeness — the wiki is written by hand |
| contradictions made explicit | freshness — it does not update itself |
| a place to record judgement | anything not yet ingested |

## The rule

```
Question ──► does it need more than one source?
                │
        no ─────┴───── yes
         │              │
    Path A         Path B, then Path A to verify
```

**Never answer a synthesis question with Path A alone.** Three search hits are
not a synthesis; they are three hits. Saying "the contract says X" from one
chunk, when another chunk two pages later says "except in case Y", is the
failure mode this rule prevents.

**Never answer a factual question with Path B alone.** The wiki is prose written
by a human or an agent; it drifts. If the wiki says ۴۸۰,۰۰۰,۰۰۰ and the PDF says
۴۲۰,۰۰۰,۰۰۰, the PDF wins — and the wiki page is a bug to fix.

## Worked example

Question: *"Does the maintenance contract's penalty clause contradict the
budget's assumption?"*

1. **Path B:** read `sources/contract-1405.md` → penalty is 0.5%/hour, capped at
   10% of contract value. Read `sources/budget-1405.md` → the budget line
   assumes a 5% maximum deduction.
2. **Contradiction found:** 10% cap vs 5% assumption.
3. **Path A to verify:** `search "سقف جریمه"` → confirms `ص ۳` says ۱۰ درصد.
   `search "۵ درصد"` → confirms the budget line.
4. **Record it** in a `concepts/` page, citing both.

Neither path alone reaches step 2. Path B without Path A would leave the numbers
unverified; Path A without Path B would never surface the comparison.

## Where the two paths are documented

- Path A mechanics: [Query-Router](../layer2/Query-Router.md)
- Path B rules: [Wiki-Page-Contract](Wiki-Page-Contract.md)
- The full ingest that feeds both: [Ingest-Workflow](Ingest-Workflow.md)
