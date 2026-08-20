---
name: wrap-up
description: End-of-session ritual. Assess the session's leavings, then offer commits, docs, cleanup, and a handoff through one checklist.
disable-model-invocation: true
---

# Wrap-up

The user believes this thread's work is over. Close it out: assess, summarise, then propose every closing action through **one gate**.

## 1. Assess (no interaction)

- `git status` and diffs. Separate **session-touched** files (the files this conversation created or edited, cross-checked against git) from **pre-existing dirt** (unstaged changes the session didn't make).
- Current branch. Note if it's `develop`, `main`, or `master`.
- **Scratch artifacts** the session created: temp scripts, debug outputs, dead exploration files.
- **Undocumented residue**: terms sharpened or hard-to-reverse decisions made this session with no `CONTEXT.md`/ADR entry yet (call the Skill tool with "domain-modeling" for the formats), and durable operational learnings (quirks, commands, pitfalls) worth recording in the repo's `CLAUDE.md` or gotchas file.
- Whether work clearly **continues** (unfinished items, a stated next session).

Not a git repo: skip everything git; the rest of the ritual still runs.

Done when you can name every candidate action with its exact contents.

## 2. Arc summary (terminal only)

3-5 short bullets: what we set out to do, what happened, what's left. Nothing persisted. Super short and sweet.

## 3. One checklist

A single AskUserQuestion call (multi-select) listing only the items that apply:

- **Commits**: propose 1..N logical commits of the session's changes; the exact grouping and messages go in the option previews, so approving the item approves the commits verbatim. Pre-existing dirt is always its own separate item, never silently mixed in.
- **Branch**: when on `develop`/`main`/`master`, offer to create a `feature/*` branch to hold the commits; committing in place stays possible but must be the explicit choice.
- **Docs**: the pending `CONTEXT.md`/ADR entries and `CLAUDE.md`/gotchas learnings, each named with a one-line gist of what would be written.
- **Cleanup**: the scratch files proposed for deletion, listed by path.
- **Handoff**: only when work clearly continues; on approval, call the Skill tool with "handoff".
- **Learnings**: when the session taught a durable lesson about how to work (a dead end, a correction from the user, a recipe worth keeping), name the specific edit to the skill, CLAUDE.md, or gotchas file that would encode it; approving the item applies that edit. One-offs are not learnings.

Nothing on this list executes without being selected. If no item applies, say so after the summary and stop.

## 4. Execute and close

Run the approved items. Commit messages match the repo's existing log style (check `git log`), plain imperative otherwise. Then, if commits landed and a remote exists, one final question: push? Default no.

Report in a few lines: commits made (with hashes), files written, files deleted, handoff path if any.
