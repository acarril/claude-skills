---
name: weekly
description: Friday ritual. Drafts the team weekly update in Spanish from repo activity and notes, then derives the Notion Portfolio and Impact ledger writes from the update Alvaro actually edited. Use when taking stock of the week, writing or drafting the weekly update for the team, catching up the portfolio, or when the user types /weekly.
---

# Weekly ritual

One scan, three outputs. The team update is the primary artifact — the Notion writes are
derived from it, never gathered separately. This ordering is the whole point: the database
survives because it is a byproduct of something Alvaro already has to write.

**Never write to Notion before step 4.** The update he edits is the source of truth for
what actually happened; a scan is only a proposal.

## Step 1 — Determine the window

Default window: since the most recent file in `~/Meli/weekly/`. If none exists, since last
Monday. If `$ARGUMENTS` names a date or range, use that instead.

State the window out loud before scanning.

## Step 2 — Scan

Read `references/topology.md` for *where* to look and `references/signals.md` for *what
counts as a signal*. Both matter, and the second one matters more.

**Commits are the weakest of the four sources.** A commit-only scan is blind to advisory
work, analysis and meetings — the exact category O3 is about. Scan all four for every
project, including the ones that look quiet:

1. commits, scoped per the topology rules
2. the working tree — `git status --short`, `git diff --stat`, new untracked directories
3. untracked notes, **not** filtered by their filename date
4. Claude Code sessions in `~/.claude/projects/`, user messages only, filtered by entry
   timestamp

Also read last week's `~/Meli/weekly/*.md`, if it exists, specifically its `Next:` lines.

Never write "Sin updates" for a project on the strength of an empty git log alone.

## Step 3 — Draft the update

Read `references/voice.md` before writing a single line. Match the register; do not write
translated English.

Structure: one section per project that moved, bullets underneath, `Next:` inline where
there is a genuine commitment. Name projects that did not move and say so plainly rather
than omitting them.

Then check last week's `Next:` lines against what actually happened, and say so in the
draft — "dijiste X, pasó Y" — as a note to Alvaro, not as a bullet for the team. Unchecked
`Next:` lines are how the field rots into aspiration.

Report the outcome, not the activity. "Fay-Herriot post_sd ahora bootstrapea el MSE
completo" beats "trabajé en estimación de elasticidad."

Write the draft to `~/Meli/weekly/YYYY-MM-DD.md` (the Friday's date) and show it to him.

## Step 4 — He edits

Stop. This is his judgment, not yours. He will cut, reword, and add things no repo records —
conversations, impressions, what a meeting actually decided.

Wait for the edited version before continuing. Re-read the file if he edited it directly.

## Step 5 — Derive the Notion writes

Read `references/notion.md` for IDs, exact property names, and the derivation rules.

From the **edited** update, propose per-project changes to the Portfolio database, and show
them as a diff before writing anything:

| Field | Comes from |
|---|---|
| `Next` | his `Next:` lines, verbatim where possible |
| `Blocked on` | anything phrased as waiting on a person or team |
| `Status` | a project that visibly woke up (dormant → active) or went quiet |
| `Updated` | the window's end date |

Only propose what the update supports. A project with no bullets gets its `Updated` stamped
and nothing else — do not invent a `Next` for a quiet project.

## Step 6 — Flag impact candidates

Expect zero most weeks. One or two a month is the real rate.

A bullet is a candidate only if it would still matter in two years: a decision that went
differently because of him, a method correction another team adopted, a shipped result with
a number. Shipping code is not impact; changing what someone decided is.

Propose it as a one-sentence `Claim` plus a guess at `Attribution`, and ask yes or no. Never
write to the Impact ledger without an explicit yes.

## Cadence — what is NOT part of this ritual

Keep the weekly small or it dies. Do not touch these unless he asks:

- **People** — monthly pass, or after meeting someone new
- **Goals** — quarterly
- **Impact ledger** — event-driven, per step 6, not a weekly sweep
