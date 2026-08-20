---
name: blast-radius
description: "Find what a change could break somewhere else before it ships, and prove the one fact it's safe because of by running a real query or script instead of writing it up. Use for 'blast radius of X', 'what could this break', or a small diff you don't trust."
disable-model-invocation: true
---

# Blast radius

Find what a change breaks somewhere else, before it ships. The change might be a query edit, a schema change, a pipeline-step modification, or estimation code.

Listing the direct dependents is not the job. The agent can grep those in a second. The job is the breakage grep won't show you.

## Don't trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether or not it's true, and that is the trap. So don't hand back the writeup. Find the one or two facts the whole thing depends on and prove them by running real code or a real query. Words are where you start, not what you ship.

### How sure are you

For each fact the change's safety depends on, get it as far down this list as is cheap, and say where it stopped.

1. You said so. Worthless on its own.
2. You pointed at the line. A real `file:line`, a job dependency listing, a table schema.
3. You showed the bad case can't happen. You walked the failure step by step and it doesn't reach.
4. You ran it. A query or script against real data that fails loud if you're wrong.
5. You reproduced it downstream. The consuming job, dashboard, or estimate actually shows the effect (or its absence).

Any safety fact you can't get to step 4, say so out loud. Don't write it up as settled. Step 4 is usually one small query: a key-uniqueness check before the join, a row-count reconciliation on a pinned partition, a diff of old-vs-new output on the same input.

## Steps

1. **Read the change.** The diff, what it adds, changes, and deletes, and what it now does differently, including the part the diff doesn't spell out (a filter that also drops NULLs, a join that can fan out, a type change that alters aggregation).
2. **Find the one fact it's safe because of.** Most changes that look scary are safe because of a single fact, like "this key is unique in the right-hand table" or "no downstream job reads this column". Find that fact. If it holds, most of the scary cases die at once. Spend your time here, not on a long list of maybes.
3. **Look where grep stops.** Follow the lineage a symbol search misses:
   - Downstream DataFlow/FDA jobs that read the touched table (job dependencies, not just repo grep).
   - Other queries, saved views, and dashboards consuming the table or metric.
   - Schema contracts: WHOWNER/DataMesh consumers, column types, partitioning and backfill semantics (does the change apply to history or only forward?).
   - Dev vs prod divergence: does the change behave the same against sandbox and production tables?
   - For code: callers, config, and anything reading the same output files.
4. **Be honest about each risk.** Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed; list the ones you checked and cleared separately. Cite a real `file:line` or table/job name; a search that finds nothing is still an answer; never invent a consumer.
5. **Prove the one fact.** Write the query or script, run it (dry-run first if the scan is big), and paste what happened. If you can't prove it cheaply, mark it unproven. Don't round up.

## What to hand back

- **What it does.** What changed, including the part that isn't obvious.
- **The one fact it's safe because of.** State it, say which ladder step you got it to, and show the proof. If you couldn't prove it, write unproven.
- **Risks.** Only the real ones. Each names how it breaks, where (`file:line`, table, job), how likely and how bad, and how to check.
- **Cleared.** What you checked and why it's fine.
- **Before you ship.** The cheapest check that catches the real break, including the query or script you wrote.
