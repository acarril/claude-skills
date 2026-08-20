---
name: grill-me
description: Grill the user relentlessly about a plan, decision, analysis design, or idea. Use when the user says "grill me", wants to stress-test their thinking, or asks for a hard interview before committing to a design.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round, then wait for the answers before recomputing.

## Asking a round

Use the AskUserQuestion tool, not prose lists. It takes up to 4 questions per call; if the frontier is larger, issue successive calls until the round is covered. For each question:

- Put your recommended answer FIRST, labeled "(Recommended)".
- Options must be genuinely distinct branches of the tree, not shades of one answer.
- A decision that needs free text the picker can't express (a name, a date, wording the user must author) is asked in prose instead, still with your recommended default stated.

A question whose answer depends on another question still open in this round belongs to a _later_ round, not this one.

Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round.

## Facts vs decisions

Finding _facts_ is your job, never the user's. When a frontier question needs a fact from the environment (filesystem, data, tools, docs), dispatch a sub-agent or look it up yourself; don't ask the user for anything you could find. Don't block on it: a running exploration is an unsettled prerequisite, so only the questions downstream of it wait; ask the rest of the frontier now. The _decisions_ are the user's: put each to them and wait.

## Done

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Do not act on the result until the user confirms you have reached a shared understanding.
