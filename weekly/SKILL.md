---
name: weekly
description: Weekly ritual. Drafts Alvaro's team update in Spanish as a paste-ready Slack post, from repo activity, notes and sessions; grills him bullet by bullet before writing anything; tops it up before he posts; then derives the Notion Portfolio and Impact ledger writes from what he actually posted. Use when taking stock of the week, writing or drafting the weekly update for the team, catching up the portfolio, or when the user types /weekly.
---

# Weekly ritual

One scan, one post. **The paste-ready Slack post is the deliverable**; the markdown file and
the Notion writes are byproducts of it. That ordering is the whole point: the database
survives because it falls out of something Alvaro already has to write.

Two rules, both about who decides:

- **Never write to Notion before he has posted.** What he posts is the source of truth for what
  happened; a scan is only a proposal.
- **Never cut a bullet silently.** You propose and you argue; he selects. Step 4 is the centre
  of this ritual, not a formality at the end of it.

## Language contract

**You talk to Alvaro in English. Spanish exists only inside the post.**

| Surface | Language |
|---|---|
| `weekly/YYYY-MM-DD.slack.txt` | Spanish |
| the verbatim copy of that text inside the `.md` | Spanish |
| a bullet quoted inside a picker option | Spanish — it is the artifact he is judging |
| everything else | **English** |

"Everything else" means every message you write, every picker question stem and every
rationale, every summary, and the whole 🔒 half of the `.md` — that half is a private note to
him, not a team-facing artifact.

This holds *hardest* when it feels wrong. By step 4 you have read tens of thousands of tokens
of Spanish notes, commits and prior posts, and English will feel like a context switch. That
feeling is the failure mode, not a signal. **Drifting into Spanish is the most common defect of
this skill.**

Spanish quoted inside an English sentence stays Spanish: write ``his `Next:` said "pasarle a
Leo mis notas"``, never a translation of it.

## Step 1 — Which run is this, and over what window

*(English, per the language contract.)*

There are two runs per cycle. **Decide which one from the state of `~/Meli/weekly/`, never from
the day of the week** — the nominal Friday draft has in practice been written on a Thursday, a
Sunday and a Monday.

```bash
ls -t ~/Meli/weekly/????-??-??.slack.txt 2>/dev/null | head -1
```

- **No file for the current cycle → FULL RUN.** Steps 2 to 6.
- **A `slack.txt` for this cycle exists and he has not posted → TOP-UP RUN.** Step 7.

That glob is deliberate. Files carrying an extra dot-segment — `2026-08-27.agus.slack.txt` — are
ad-hoc reports to other audiences on their own windows. They are not this ritual's output:
never anchor to them, never treat one as an unposted draft.

### The window

Default: since the most recent ritual file in `~/Meli/weekly/`. If none exists, since last
Monday. If `$ARGUMENTS` names a date or range, use that instead.

**Anchor the start to when the previous report was *written*, not to its filename date.** The
file is named for a Friday but is routinely drafted a day early, so anything landing between
the drafting and the nominal date falls into a gap and is reported by neither run:

```bash
ls -t ~/Meli/weekly/????-??-??.md | head -1 | xargs stat -f '%Sm' -t '%Y-%m-%d %H:%M'
```

Overlap rather than gap: last cycle's file is right there to dedupe against, so a repeated
bullet is cheap where a dropped one is invisible.

State the window out loud before scanning, including the anchor timestamp you used.

## Step 2 — Scan

Read `references/topology.md` for *where* to look and `references/signals.md` for *what counts
as a signal*. Both matter, and the second one matters more.

**Commits are the weakest of the four sources.** A commit-only scan is blind to advisory work,
analysis and meetings — the exact category O3 is about. Scan all four for every project,
including the ones that look quiet:

1. commits, scoped per the topology rules
2. the working tree — `git status --short`, `git diff --stat`, new untracked directories
3. untracked notes, **not** filtered by their filename date
4. agent sessions via `memex` — Claude Code **and** Codex, user messages only, filtered by
   entry timestamp

Also read last cycle's `~/Meli/weekly/*.md`, specifically its `Next:` lines.

A project is quiet only when all four sources are quiet.

## Step 3 — Draft, in Spanish, over-inclusive and scored

Read `references/voice.md` first: it carries who reads this, the register they read it in, and
the exact Slack formatting. Write Spanish, in his voice. **This is the only place Spanish
belongs** — the reasons, marks and everything you say about the draft stay English.

The draft is **wider than the post will be, and every bullet in it is short.** Every candidate
that plausibly passes the test gets written as a real, finished bullet, including the ones a
stricter reading would drop. He cuts; you do not. A bullet he never saw is a decision you made
for him. Over-inclusive means bullet *count*; it never means bullet *length*.

### Length

The prune round controls how many bullets survive, not how long each one is — and the test
below rewards numbers, which inflates bullets. The team's measured norm is in
`references/voice.md` → Calibration. Apply these to every candidate **as it is drafted**, not
after the cuts:

- **~20 words per bullet, hard cap 40.** One sentence of state; optionally one of consequence
  or `Next:`. A bullet over 40 words is two bullets or one bullet plus a talking point.
- **At most one number per bullet.** Pick the one that changes what the reader does. The rest
  go to the talking points in the 🔒 half (step 5).
- **No mechanism in the post.** No "porque", no "no es un bug:", no parenthetical method, no
  candidate lists. What is now true, and what happens next. The mechanism is what he says in
  the meeting when the bullet earns its question.
- **Status tags instead of sentences** for the nothing-happened cases: `Sin avances`,
  `igual a semana pasada`, `Pending: …`, `ETA …` — Kevin's vocabulary, already the team's.

Before and after, the same bullet:

> `• *v3 del clasificador*: pre-registré la selección del labeler (NMV-weighted accuracy contra un test set juzgado por LLM; candidatos cerrados: k-NN, sonnet en batch, catálogo Meli, cascadas; techo de 10 días para el backfill de 5,85M títulos). El diccionario de categorizador-d2 es idéntico al nuestro (361/361 pares), así que la fuga a CPG es un problema de precisión y no de mapeo, y lo decide el test set. Resultado provisorio (falta un candidato): lidera la cascada k-NN → sonnet en batch sobre la cola de baja confianza (84,6% NMV-weighted corregido por el sesgo del juez, vs 77% k-NN solo y 76% sonnet solo), con la mitad de los títulos yendo al LLM y backfill de 1,6 días. Decisión ~19/09.` — 118 words, 9 numbers.
>
> `• *v3 del clasificador*: estudio pre-registrado en curso; lidera la cascada k-NN → sonnet (84,6% vs 77% k-NN solo). Decisión ~19/09.` — 20 words, 2 numbers.

Everything the long version knew still exists: in the prereg, in the notes, and in the
talking points. The post is not where it lives.

### The test: a bullet earns its place when it is a result AND it is consequential

- **Result, not activity.** State what is now true, never what he spent time on.
- **Consequential.** Nacho would act differently, or a teammate would ask about it, or someone
  is worse off not knowing. "What happened?" is the prompt; consequential is the gate.

Both conditions, every bullet. A true, well-written result that changes nothing scores low.

What the test decides in the cases that recur:

| Material | Ruling |
|---|---|
| **Numbers** | **One per bullet**, the one that moved a decision: `106k discrepancias (19%)` is one number, `50k sin CUPED le gana a 20k` is one comparison. The second and third numbers go to the talking points. Precision that only decorates goes — `0.0000000000pp`, `558.741` where `558k` reads the same. |
| **Mechanism, method** | **Never in the bullet.** It goes to the talking points, or the link carries it. The bullet states the result the mechanism produced; if the mechanism itself was the decision this cycle ("no es un bug, es el anchor"), the bullet says the decision, not the argument. |
| **Internal workings, bug fixes** | Report the impact on the result, not the repair: "los ítems que se caían del scoring vuelven a entrar" over "saqué `pre_seller_latest_cartera` del feature set". A fix with no effect on a result scores low. |
| **Politics, deferrals, skepticism** | **High.** A deprioritisation, a stalled dependency, a leader's doubt — this is what Nacho most needs and what he will not learn elsewhere. |

**Links are the compression lever.** A bullet whose artifact exists — Grid doc, dashboard,
deck, published table — carries the link and then states only the outcome. Depth becomes
optional rather than absent, and the bullet stops at the result. This is the single biggest
lever on length.

### Scoring: merit first, then the budget demotes

Mark every bullet `IN` or `BORDERLINE`, with **one English line** under it saying why.

1. **Score on the test alone.** Clears both conditions cleanly → `IN`. Clears one, or clears
   both weakly → `BORDERLINE`.
2. **Then apply the ~3-bullets-per-track expectation.** A track carrying four `IN` bullets
   demotes its weakest and says exactly that: `weakest of 4, budget is 3`. A project carrying
   4+ tracks squeezes tighter.

Length pressure becomes his decision instead of your silent one. That is the whole reason for
two marks rather than a filter.

### Shape

- **Most-moved first.** The top of the list gets the Monday discussion; the tail may not be
  reached.
- **Track sub-labels** where a project runs parallel pipelines (`*Cupones*`, `*Panel piloto*`).
- **Every project that moved carries a `Next:`.** Where it is stalled, `Esperando:` names the
  person and the date it has been waiting since. A `Next:` names something already committed.
- **A project where nothing scored** gets one line under `*Sin updates:*` and no `Next:`.
- **A track that moved last cycle and not this one** keeps its label with a status tag and
  nothing else: `• *Cupones*: igual a semana pasada` / `Sin avances`. That is how Kevin and
  Daniel say it and it reads as continuity, not silence.

## Step 4 — The prune round

*(English stems, English rationales, Spanish bullets. See the language contract.)*

Print the assembled draft first: full Spanish bullets, numbered per project, each with its mark
and its one-line English reason. He reads the whole thing once, in the form it would paste.

Then grill him, project by project.

### One multi-select picker per project

Batch four projects per `AskUserQuestion` call, so a six-project cycle costs two calls.

- **Stem, English:** `[<project>] Which bullets do you cut?`
- **One option per bullet.** Label: `<n> · <short Spanish handle> (IN|BORDERLINE)`. Description:
  **the bullet exactly as it would paste into Slack**, then ` — ` and the English rationale.
  Never a gloss or a truncation. He frequently wants to nitpick *how* a thing is written, and
  that judgment is only possible against the real sentence.
- **The proposed `Next:` is an option too.** It is a commitment he gets audited on next cycle
  and the line step 8 writes into Portfolio; a `Next:` he never consented to is how the field
  rots into aspiration. Where it repeats an unmet commitment, say so in the label:
  `Next: pasarle a Leo mis notas — 2nd cycle unmet`.
- **A `nothing — keep all N` option**, so keeping everything costs one click.

`Other` carries wording instructions alongside the cuts, in the same answer: *"keep 2, corta la
última frase; en 4 decí 'brecha' no 'gap'"*. Apply them, re-render the affected bullets in
Spanish, and show **only the changed lines** — not the project again.

### One consolidated pushback round, then it is settled

Collect every disagreement across all projects into a single multi-select picker: cuts you
would restore, keeps you would drop. One option each, the argument in the description, plus a
`neither — my cuts stand` option.

Argue properly. Name what is lost, never that the test says so:

> `restore · ghost-ads #1 (Conversion Lift apagado)` — the only bullet Nacho will otherwise
> hear about from Gera first.

Whatever he answers is final. **One exchange.** Never re-litigate a bullet he has ruled on
twice.

### Then assemble

- Order most-moved-first, except where he asked for a different order in `Other` — his order
  wins.
- A project whose bullets were all cut drops to the `*Sin updates:*` line and loses its `Next:`.

## Step 5 — Write the two files

Only now. `~/Meli/weekly/` must never hold an unpruned draft: a file on disk reads as decided,
and Monday morning is the wrong moment to discover that it was not.

- `~/Meli/weekly/YYYY-MM-DD.slack.txt` — the paste-ready post. **The deliverable.**
- `~/Meli/weekly/YYYY-MM-DD.md` — that text verbatim, plus the 🔒 half.

### The 🔒 half — English, always last, never team-facing

- **Last cycle's `Next:` check** — each prior `Next:` and whether it happened, as "he said X,
  Y happened". Unchecked `Next:` lines are how the field rots into aspiration.
- **Overdue commitments** — stale `- [ ]` from dated notes, per `references/signals.md`.
- **Unverified ops** — anything you could not check because a tool or MCP server was down.
- **Cut this cycle** — one line per bullet he cut, with the reason. **Not a re-offer**: he saw
  and judged every candidate in step 4. It exists so next cycle can tell a one-off cut from
  something he has now buried three cycles running.
- **Talking points** — per posted bullet, the mechanism and the numbers the length rule kept
  out: two to four lines each, English, in post order. This is what he reads before the
  meeting so the short bullet can earn and answer its question. It is where "why it is not a
  bug", the candidate list, the CI and the second number live.

Then print the shape line and check it against the target before showing him anything:

```bash
wc -w ~/Meli/weekly/YYYY-MM-DD.slack.txt      # target ~300; over 400 is the 2026-09-07 failure
```

Also print bullets, median words per bullet and the longest bullet. If the median is above
25 or any bullet is above 40, fix the draft before he sees it; do not ship the number and
call it out.

Show him the post and stop.

## Step 6 — He edits

His judgment, not yours. He cuts, rewords, and adds what no repo records — conversations,
impressions, what a meeting actually decided. Wait for the edited version; re-read the files if
he edited them directly.

## Step 7 — The top-up run, then he posts

The full run cannot see what lands after it, which is exactly where the 2026-08-23 run lost a
day's work.

1. **Re-scan** (step 2) from the `slack.txt` mtime to now. Small window, one pass.
2. **Draft, score and prune the new candidates the same way** — finished Spanish bullets,
   `IN` / `BORDERLINE`, one picker. Usually one to three candidates, so it is one question.
   Nothing enters the post unjudged, here least of all: he is about to paste it.
3. **Fold the survivors in and rewrite both files.** Tell him, in English, what you added.
4. **Confirm which thread is canonical.** The `Weekly EA` bot posts the prompt in
   `#commerce-bids-ea` (`C068QV1QALA`) Mondays at 08:00, but a teammate sometimes opens a
   duplicate minutes earlier — on 2026-08-24 Kevin did, and the update landed in his thread
   instead of the bot's. Read the channel and pick the one the team is replying to.

He posts it himself. The Slack connector can send, draft and schedule, but **cannot edit a
message once posted** — so a mistake costs a visible re-post, and the paste is worth getting
right the first time.

**Posting early buys airtime.** The team reads each other's lists in Monday's meeting and
whoever posts first speaks first, with more time.

## Step 8 — Derive the Notion writes

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

## Step 9 — Flag impact candidates

Expect zero most cycles. One or two a month is the real rate.

A bullet is a candidate only if it would still matter in two years: a decision that went
differently because of him, a method correction another team adopted, a shipped result with a
number. Shipping code is not impact; changing what someone decided is.

Propose it as a one-sentence `Claim` plus a guess at `Attribution`, and ask yes or no. Write to
the Impact ledger only on an explicit yes.

## Cadence — what is NOT part of this ritual

Keep the weekly small or it dies. Touch these only when he asks:

- **People** — monthly pass, or after meeting someone new; read `references/people.md`
- **Goals** — quarterly
- **Impact ledger** — event-driven, per step 9, not a weekly sweep
