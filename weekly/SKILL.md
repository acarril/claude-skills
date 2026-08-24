---
name: weekly
description: Weekly ritual. Drafts Alvaro's team update in Spanish as a paste-ready Slack post, from repo activity, notes and sessions; tops it up Monday before he posts; then derives the Notion Portfolio and Impact ledger writes from what he actually posted. Use when taking stock of the week, writing or drafting the weekly update for the team, catching up the portfolio, or when the user types /weekly.
---

# Weekly ritual

One scan, one post. **The paste-ready Slack post is the deliverable**; the markdown file and
the Notion writes are byproducts of it. That ordering is the whole point: the database
survives because it falls out of something Alvaro already has to write.

**Never write to Notion before he has posted.** What he posts is the source of truth for what
happened; a scan is only a proposal.

## Step 1 — Determine the window

Default window: since the most recent file in `~/Meli/weekly/`. If none exists, since last
Monday. If `$ARGUMENTS` names a date or range, use that instead.

**Anchor the start to when the previous report was *written*, not to its filename date.**
The file is named for a Friday but is routinely drafted a day early, so anything landing
between the drafting and the nominal date falls into a gap and is reported by neither run:

```bash
ls -t ~/Meli/weekly/*.md | head -1 | xargs stat -f '%Sm' -t '%Y-%m-%d %H:%M'
```

Measured 2026-08-23: the previous report was written Thursday 10:17 and named `2026-08-21.md`.
Twenty-eight commits across four projects landed in the gap — the whole CSAT–IHT panel, three
`pricing-combopremium` blockers with O1 at risk, an `fvf-elasticity` dead end — and the run
reported two projects quiet that were not. Overlap rather than gap: last week's file is right
there to dedupe against, so a repeated bullet is cheap where a dropped one is invisible.

State the window out loud before scanning, including the anchor timestamp you used.

## Step 2 — Scan

Read `references/topology.md` for *where* to look and `references/signals.md` for *what
counts as a signal*. Both matter, and the second one matters more.

**Commits are the weakest of the four sources.** A commit-only scan is blind to advisory work,
analysis and meetings — the exact category O3 is about. Scan all four for every project,
including the ones that look quiet:

1. commits, scoped per the topology rules
2. the working tree — `git status --short`, `git diff --stat`, new untracked directories
3. untracked notes, **not** filtered by their filename date
4. Claude Code sessions in `~/.claude/projects/`, user messages only, filtered by entry
   timestamp

Also read last week's `~/Meli/weekly/*.md`, specifically its `Next:` lines.

A project is quiet only when all four sources are quiet.

## Step 3 — Draft the post

Read `references/voice.md` first: it carries who reads this, the register they read it in, and
the exact Slack formatting. Write Spanish, in his voice.

The post is built **bottom-up**. There is no length budget — each candidate faces one test, and
the post is whatever survives it.

### A bullet earns its place when it is a result AND it is consequential

- **Result, not activity.** State what is now true, never what he spent time on.
- **Consequential.** Nacho would act differently, or a teammate would ask about it, or someone
  is worse off not knowing. "What happened?" is the prompt; consequential is the gate.

Both conditions, every bullet. A true, well-written result that changes nothing stays out.

What the test decides in the cases that recur:

| Material | Ruling |
|---|---|
| **Numbers** | Every number in a bullet moved a decision: `106k discrepancias (19%)`, `50k sin CUPED le gana a 20k`, `~135k órdenes`. Precision that only decorates goes — `0.0000000000pp`, `558.741` where `558k` reads the same. |
| **Mechanism, method** | Survives when it changed the result, or when it was the centre of a discussion this week — checkable against a meeting note or a decision that turned on it. Otherwise the link carries it. |
| **Internal workings, bug fixes** | Report the impact on the result, not the repair: "los ítems que se caían del scoring vuelven a entrar" over "saqué `pre_seller_latest_cartera` del feature set". A fix with no effect on a result stays out. |
| **Politics, deferrals, skepticism** | **In.** A deprioritisation, a stalled dependency, a leader's doubt — this is what Nacho most needs and what he will not learn elsewhere. |

**Links are the compression lever.** A bullet whose artifact exists — Grid doc, dashboard,
deck, published table — carries the link and then states only the outcome. Depth becomes
optional rather than absent, and the bullet stops at the result. This is the single biggest
lever on length; his own 2026-08-17 post used it and the ritual had lost it.

### Shape

- **Most-moved first.** The top of the list gets the Monday discussion; the tail may not be
  reached.
- **~3 bullets per track**, an expected shape rather than a rule. A 4th that genuinely passes
  goes in — and the 🔒 section notes that the project ran long, so he can audit whether the
  test was applied honestly. A project carrying 4+ tracks squeezes below 3 each.
- **Track sub-labels** where a project runs parallel pipelines (`*Cupones*`, `*Panel piloto*`).
- **Every project that moved carries a `Next:`.** Where it is stalled, `Esperando:` names the
  person and the date it has been waiting since. A `Next:` names something already committed.
- **A project where nothing passed** gets one line under `*Sin updates:*` and no `Next:`.

### The 🔒 half

Check last week's `Next:` lines against what happened and record it as "dijiste X, pasó Y" —
a note to Alvaro, never a bullet for the team. Unchecked `Next:` lines are how the field rots
into aspiration. Add stale commitments per `references/signals.md`, anything cut that he might
want back, and any project that ran long.

### Write two files

- `~/Meli/weekly/YYYY-MM-DD.slack.txt` — the paste-ready post. **The deliverable.**
- `~/Meli/weekly/YYYY-MM-DD.md` — that text verbatim, plus the 🔒 half.

Show him the post and stop.

## Step 4 — He edits

His judgment, not yours. He cuts, rewords, and adds what no repo records — conversations,
impressions, what a meeting actually decided. Wait for the edited version; re-read the files
if he edited them directly.

## Step 5 — Monday: top up, then he posts

The Friday scan cannot see Friday afternoon or the weekend, which is exactly where the
2026-08-23 run lost a day's work.

1. **Re-run step 2** from the Friday draft's mtime to now. Small window, one pass.
2. **Fold anything that passes step 3's test** into the post, and tell him what you added.
3. **Confirm which thread is canonical.** The `Weekly EA` bot posts the prompt in
   `#commerce-bids-ea` (`C068QV1QALA`) Mondays at 08:00, but a teammate sometimes opens a
   duplicate minutes earlier — on 2026-08-24 Kevin did, and the update landed in his thread
   instead of the bot's. Read the channel and pick the one the team is replying to.
4. **Put it on his clipboard:** `pbcopy < ~/Meli/weekly/YYYY-MM-DD.slack.txt`

He posts it himself. The Slack connector can send, draft and schedule, but **cannot edit a
message once posted** — so a mistake costs a visible re-post, and the paste is worth getting
right the first time.

**Posting early buys airtime.** The team reads each other's lists in Monday's meeting and
whoever posts first speaks first, with more time.

## Step 6 — Derive the Notion writes

Read `references/notion.md` for IDs, exact property names, and the derivation rules.

Derive from **what he posted**, not from your draft — the posted text is the most-edited
version and its wording is his. Propose per-project changes to Portfolio and show the diff
before writing anything:

| Field | Comes from |
|---|---|
| `Next` | his `Next:` lines, verbatim where they read as a sentence |
| `Blocked on` | his `Esperando:` lines — name the person |
| `Status` | a project that visibly woke up, or went quiet for several weeks |
| `Updated` | the window's end date, on every project that had activity |

Only propose what the post supports. A quiet project gets its `Updated` stamped and nothing
else.

## Step 7 — Flag impact candidates

Expect zero most weeks. One or two a month is the real rate.

A bullet is a candidate only if it would still matter in two years: a decision that went
differently because of him, a method correction another team adopted, a shipped result with a
number. Shipping code is not impact; changing what someone decided is.

Propose it as a one-sentence `Claim` plus a guess at `Attribution`, and ask yes or no. Write to
the Impact ledger only on an explicit yes.

## Cadence — what is NOT part of this ritual

Keep the weekly small or it dies. Touch these only when he asks:

- **People** — monthly pass, or after meeting someone new
- **Goals** — quarterly
- **Impact ledger** — event-driven, per step 7, not a weekly sweep
