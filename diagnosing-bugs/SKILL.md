---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs, wrong numbers, and performance regressions. Use when the user says "diagnose"/"debug this", reports something broken/failing/slow, or when a metric, count, or estimate doesn't match what it should be.
---

# Diagnosing Bugs

A discipline for hard bugs. In this line of work the most dangerous bug is not a crash but a **silently wrong number**: a join that fans out, a cohort whose N shifts between runs, a metric that won't reconcile with the dashboard. Skip phases only when explicitly justified.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get the project's definitions of treatment, cohorts, and outcomes, and check ADRs in the area you're touching: what looks like a bug is sometimes a recorded decision.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars and ADC, so credentials stay in the environment rather than in what you show.

## Phase 1: Build a feedback loop

**This is the skill.** Everything else is mechanical. If you have a **tight** pass/fail signal for the bug (one that goes red on _this_ bug), you will find the cause; bisection, hypothesis-testing, and instrumentation all just consume it. If you don't have one, no amount of staring at code or SQL will save you.

Spend disproportionate effort here. **Be aggressive. Be creative. Refuse to give up.**

### Ways to construct one, in roughly this order

1. **Failing test** at whatever seam reaches the bug (pytest for Python estimation or pipeline code).
2. **Pinned assertion query**: a saved SQL query against a frozen snapshot or fixture partition that returns the bad number (or a boolean check), rerunnable via `bq` in seconds.
3. **Seeded repro script**: a minimal script with pinned seed and pinned inputs that reproduces the wrong estimate or output, diffed against known-good values.
4. **Stage diff**: row counts, key cardinality, and schema compared between two pipeline stages (or before/after a suspect join), to localize *where* the numbers go wrong. A fan-out shows up as a cardinality jump.
5. **Reconciliation query**: recompute the metric independently from the source-of-truth table, diff against the pipeline's output. The diff (which rows, which segments) is the signal.
6. **Fixture-date rerun**: rerun the DataFlow/FDA step on one pinned partition date into a sandbox table, assert on the result.
7. **Differential run**: same input through old vs new code (two commits, two configs), diff outputs. Also works across environments (desa vs prod) when that's where the divergence lives.
8. **Bisection harness**: if the bug appeared between two known states (commit, snapshot date, config), automate "check state X" so you can `git bisect run` it, or bisect over partition dates the same way.
9. **Property / seed loop.** If the output is "sometimes wrong", run it across many seeds, dates, or samples and count failures.
10. **Replay a captured artifact.** Save the actual bad extract, payload, or log to disk; replay it through the code path in isolation.

Build the right feedback loop, and the bug is 90% fixed.

### Tighten the loop

Treat the loop as a product. Once you have _a_ loop, **tighten** it:

- **Faster**: sample down. One partition, one cohort, one seller decile. Materialize a frozen fixture table in the sandbox once, then iterate against it, rather than re-scanning the full table every run. Dry-run first to see bytes scanned.
- **Sharper**: assert on the specific symptom (the count, the coefficient, the reconciliation diff), not "query ran without error".
- **More deterministic**: pin seeds, pin snapshot/partition dates (never `CURRENT_DATE` in a repro), fix sort order before any sampling or `LIMIT`.

A 5-minute full-scan loop is barely better than no loop; a 5-second fixture-table loop is tight, a debugging superpower.

### Non-deterministic bugs

The goal is not a clean repro but a **higher reproduction rate**. Loop over many seeds, dates, or samples; narrow to the segment where failures concentrate. A 50%-flake bug is debuggable; 1% is not, so keep raising the rate until it's debuggable.

### When you genuinely cannot build a loop

Stop and say so explicitly. List what you tried. Ask the user for: (a) access to whatever environment reproduces it, (b) a redacted captured artifact (the bad extract, job logs, the dashboard number and its exact definition), or (c) a pinned snapshot to test against. Do **not** proceed to hypothesise without a loop.

### Completion criterion: a tight loop that goes red

Phase 1 is done when the loop is **tight** and **red-capable**: you can name **one command** (a script path, a test invocation, a `bq query` on a saved file) that you have **already run at least once** (show the invocation and its output, redacted), and that is:

- [ ] **Red-capable**: it drives the actual bug code path and asserts the **user's exact symptom**, so it can go red on this bug and green once fixed. Not "runs without erroring"; it must be able to _catch this specific bug_.
- [ ] **Deterministic**: same verdict every run (flaky bugs: a pinned, high reproduction rate, per above).
- [ ] **Fast**: seconds, not minutes.
- [ ] **Agent-runnable**: you can run it unattended.

If you catch yourself reading code to build a theory before this command exists, **stop: jumping straight to a hypothesis is the exact failure this skill prevents.** No red-capable command, no Phase 2.

## Phase 2: Reproduce + minimise

Run the loop. Watch it go red as the bug appears.

Confirm:

- [ ] The loop produces the failure mode the **user** described, not a different failure that happens to be nearby. Wrong bug = wrong fix.
- [ ] The failure is reproducible across multiple runs (or at a high enough rate to debug against).
- [ ] You have captured the exact symptom (the wrong count, the wrong coefficient, the error) so later phases can verify the fix actually addresses it.

### Minimise

Once it's red, shrink the repro to the **smallest scenario that still goes red**. Cut CTEs, joins, filters, columns, covariates, and date ranges **one at a time**, re-running the loop after each cut, and keep only what's load-bearing for the failure. For a wrong-number bug this usually converges on the one join or filter that owns it.

Done when **every remaining element is load-bearing**: removing any one of them makes the loop go green.

Do not proceed until you have reproduced **and** minimised.

## Phase 3: Hypothesise

Generate **3-5 ranked hypotheses** before testing any of them. Single-hypothesis generation anchors on the first plausible idea.

Each hypothesis must be **falsifiable**: state the prediction it makes.

> Format: "If <X> is the cause, then <changing Y> will make the bug disappear / <checking Z> will show the anomaly."

If you cannot state the prediction, the hypothesis is a vibe: discard or sharpen it.

**Show the ranked list to the user before testing.** They often have domain knowledge that re-ranks instantly ("that table's schema changed last week", "we already ruled out #3"). Cheap checkpoint, big time saver. Don't block on it; proceed with your ranking if the user is AFK.

## Phase 4: Instrument

Each probe must map to a specific prediction from Phase 3. **Change one variable at a time.**

Tool preference:

1. **Interactive inspection** where the environment supports it: a REPL or notebook cell over the suspect dataframe, a standalone `SELECT` over the suspect CTE. One inspected intermediate beats ten logs.
2. **Targeted probes** at the boundaries that distinguish hypotheses: a row-count or cardinality check between two specific stages, a print of the one intermediate value.
3. Never "log everything and grep".

**Tag every debug probe** with a unique prefix, e.g. `[DEBUG-a4f2]`, in print statements, log lines, and scratch-query filenames. Cleanup at the end becomes a single grep. Untagged probes survive; tagged probes die.

**Perf branch.** For a slow query or job, probes are usually wrong. Instead: establish a baseline measurement first (dry-run bytes scanned, query plan stages, wall-clock timing on the fixture), then bisect the query CTE by CTE or the job step by step. Measure first, fix second.

## Phase 5: Fix + regression check

Write the regression check **before the fix**, but only if there is a **correct seam** for it.

- For Python code, that's a test at the seam that exercises the real bug pattern: turn the minimised repro into a failing test.
- For SQL/pipeline logic, it's an assertion query checked into the repo (a `checks/` file the pipeline or you can rerun): row counts within bounds, key uniqueness before a join, reconciliation within tolerance.

If the only available seam is too shallow to replicate the bug pattern, a check there gives false confidence. **If no correct seam exists, that itself is the finding.** Note it and flag it.

If a correct seam exists:

1. Turn the minimised repro into a failing test/check at that seam.
2. Watch it fail.
3. Apply the fix.
4. Watch it pass.
5. Re-run the Phase 1 loop against the original (un-minimised) scenario.

## Phase 6: Cleanup

Required before declaring done:

- [ ] Original repro no longer reproduces (re-run the Phase 1 loop)
- [ ] Regression test/check passes (or absence of seam is documented)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` the prefix)
- [ ] Scratch sandbox tables and fixture tables dropped, or clearly named as fixtures worth keeping
- [ ] The hypothesis that turned out correct is stated in the commit / PR message, so the next debugger learns
