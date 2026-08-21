# Signals — where a week's work actually shows up

**Commits are the weakest of the four sources, not the strongest.** A commit-only scan is
systematically blind to advisory work, analysis, and meetings — which is precisely the
category O3 is about. Scan all four every run.

| Source | Catches | Reliability |
|---|---|---|
| Commits | shipped code, docs | high, but narrow |
| Working tree | in-flight work, uncommitted analysis | high |
| Untracked notes | meetings, decisions, distilled transcripts | high |
| Claude sessions | exploration, advisory, what he asked and concluded | rich but needs care |

## 1. Commits

Per `topology.md`. Straightforward.

## 2. Working tree — uncommitted work is still work

```
git -C <dir> status --short -- projects/<name>
git -C <dir> diff --stat -- projects/<name>
```

A `+1391/−77` diff on a dashboard is a week of work that no commit records. New untracked
directories (`oneoffs/<something>/`) are usually a whole new workstream — open the README
inside before describing it.

Also worth a look when git shows nothing:

```
find projects/<name> -type f -newermt <start> -not -path '*/.git/*' -not -path '*/__pycache__/*'
```

## 3. Untracked notes — do not filter these by filename date

Committed notes can be filtered by their `YYYY-MM-DD_` filename. Untracked ones cannot:
he distils meeting transcripts in batches, so a note *written* this week routinely carries
last month's meeting date.

**Rule: an untracked note has never appeared in any weekly, regardless of its filename
date.** Surface it. If the meeting is old, say when it happened — "distilé las notas de las
reuniones de PP del 05 al 14/08" is the honest line, and it is real work.

## 4. Claude Code sessions — the advisory record

Transcripts live in `~/.claude/projects/<mangled>/`, where `<mangled>` is the absolute path
with every `/` replaced by `-`. A project usually has **two** directories — one rooted at the
repo, one at `projects/<name>` — and both must be checked:

```
-Users-acarril-Meli-price-perception
-Users-acarril-Meli-price-perception-projects-price-perception
```

Extract **user messages only**, filtered by entry timestamp (not file mtime — a session can
span weeks). His own messages are short, carry the intent, and are cheap to read; the
assistant side is enormous and mostly redundant.

```python
import json, glob
START = '<window start>'
SKIP = ('<local-command', '<command-name', '<command-message', '[Request interrupted',
        'Base directory', '<system-reminder', '<task-notification')
for p in glob.glob(f'{mangled_dir}/*.jsonl'):
    for line in open(p, errors='ignore'):
        try: j = json.loads(line)
        except: continue
        if j.get('type') != 'user': continue
        ts = (j.get('timestamp') or '')[:16]
        if ts[:10] < START: continue
        c = (j.get('message') or {}).get('content')
        txt = c if isinstance(c, str) else ' '.join(
            x.get('text','') for x in c if isinstance(x, dict) and x.get('type') == 'text')
        txt = txt.strip()
        if not txt or txt.startswith(SKIP) or len(txt) < 25: continue
        print(ts, txt[:260].replace('\n', ' '))
```

When a specific claim needs the answer and not just the question, grep the same files for the
keyword and pull the adjacent assistant message. Do this sparingly — the files reach 10MB+.

### Care required

Sessions record **what he explored**, not **what is true or shipped**. Two failure modes:

- Never report an explored idea as a delivered thing. "Exploramos CUPED" is honest;
  "implementamos CUPED" is false.
- A conclusion reached in a session is real and reportable — including negative results.
  "CUPED no sirve acá: ρ² ≈ 0.03–0.07" is one of the more valuable lines a week can produce.

Cross-check anything load-bearing against an artifact in the working tree.

## Why this matters for the Notion side

His O3 objective is "define what advisory value looks like, then evidence it", and its stated
failure mode is that advisory work disappears because nothing records it. Advisory work
leaves **no commits** — it lives in sessions and untracked meeting notes. A commit-only scan
would let O3 fail silently, exactly as the objective predicts.

## 5. `notes/TODO.md` — the living backlog

Where candidate work lives: undated, edited in place, deleted when done or when it stops
mattering. The format is Alvaro's, established in `fvf-elasticity`: one item per bullet with
what, why, how to test, a prior on whether it will work, a **trigger** for when it becomes
relevant, and a link to the note that motivated it. A `## Parked (not planned)` section holds
things deliberately declined.

Read it every run. It is the source for the Portfolio `Next` field: `Next` should be the item
you are actually about to do, quoted from here or from his edited update — not invented.

**Do not move backlogs into Notion.** Four task mechanisms already exist and each does
something the others cannot:

| Where | Holds | Lifecycle |
|---|---|---|
| dated `notes/*.md` `- [ ]` | commitments made to people in a meeting | append-only, never edited |
| `notes/TODO.md` | candidate work, might never happen | edited in place |
| `docs/superpowers/plans/*.md` | committed work, decomposed for agents | created on commitment, done at merge |
| Notion `Next` | the single next step | overwritten weekly |

The progression is TODO item → track → Impact claim. Notion holds the last two.

### Stale commitments

Unchecked `- [ ]` in **dated** notes are promises made to people, and nothing chases them —
there are 50+ open across the repos, some from May. When one is older than ~3 weeks and its
project is active, surface it in the 🔒 section. Do not tick or edit a dated note: they are
append-only logs.

## Identity: use Slack, not guesswork

The MELI Slack connector resolves a name to a **verified** email, username and Slack user ID:
`slack_search_users` with a full name, or `slack_read_user_profile` with a known ID.

`Title` is self-set and **roughly 40% filled** — real when present ("Strategic Planning Senior
Manager", "Insights & Analytics (Meli+)", "Buy box - Structured Data - IT"), blank otherwise.
Blank means unset, never junior.

Rules learned 2026-08-20, after an agent had guessed org weight for 21 of 27 people and those
guesses ended up ordering the board Alvaro was meant to judge from:

- **Never infer seniority or influence from team membership, mention frequency, or tone.** If
  Slack has no title and no note states a rank, say so in the field. Blank is information;
  a guess wearing a confident label is not.
- **There is no `Org weight` field** — dropped 2026-08-20, along with `Seniority`. The schema
  is `Team` (business unit) + `Title` (rank as Slack states it, verbatim). The reason is worth
  keeping: Team and Title are **re-derivable** — one Slack lookup re-verifies them — whereas a
  judgement like "how much their opinion would carry" is unverifiable once written, and a wrong
  value is indistinguishable from a right one. Do not reintroduce a scored influence field.
  Whether someone's word counts in a committee is a call Alvaro makes at packet-writing time,
  against the org chart as it is then.
- `Relationship` is the **only** judgement field, and it is his alone. It is not re-derivable,
  which is exactly why it belongs in the database rather than being inferred.
- Record where each fact came from, in the field itself ("Slack, verificado <date>" vs "de tus
  notas"). A fact whose provenance is not visible gets treated as verified.
- Names in notes are frequently distorled by Gemini transcription. Three of 27 did not resolve
  in Slack at all; they are flagged in-row rather than silently kept.
- Watch for two people sharing a name — Nicolás Repetto matched two accounts. Flag, do not pick.

### Gmail is the better source, and answers a different question

Check which account is connected first — it has been the personal `alvarocarril@gmail.com`
rather than `alvaro.carrilrubio@mercadolibre.cl`. One `newer_than:7d` search tells you.

On the work account, Gmail beats Slack twice over:

- **It finds people Slack cannot.** Silvestre Serantes and Pedro Hardoy have no Slack profile
  but real mailboxes. It also caught a misspelling that had defeated every other lookup: the
  notes say "Pedro Ardoy", the person is **Hardoy**.
- **Distribution lists reveal hierarchy, which no title does.** Nacho's quarterly stakeholder
  update (2026-07-30) went to ~41 people including Ariel Szarfsztejn, David Geisen, Karen
  Bruck, Juan Lavista and Silvestre Serantes. Being *on that list* is documented evidence of
  seniority — far stronger than inferring from team membership, and the only defensible basis
  found for a `high` org weight.

### Rank and hierarchy: query `meliorg`, do not reconstruct by hand

```bash
S=~/.claude/skills/meliorg/scripts/meliorg.py
python3 $S find "Ignacio Campos"   # name or LDAP -> full record
python3 $S chain <ldap>            # up the reporting line to the root
python3 $S reports <ldap>          # direct reports
```

The `meliorg` skill owns the full source-precedence rule and the off-VPN staleness handling —
read it rather than restating it here. Off-VPN the command serves cached data and says so;
surface that, never present it as current. Watch the 60-req/min limit: `find` is one request,
`chain` about six.

**Slack titles are wrong often enough to be unusable for rank.** Measured on 2026-08-20:
Peirano read a rung low, Diogo Pena read "Advertising Product Manager" when he is a Product
Advertising *Expert*, and **both** homonyms of Nicolás Repetto had stale titles. Several VPs
have no Slack profile at all.

Names also collide — Repetto and Rodrigo Palma each returned two people. `find` matches on
name or LDAP only, never department or title, so show the candidates and let Alvaro pick.
Carry the **LDAP username** forward; it is the only stable key.

Direct-report **counts** come free with `reports`. Org **size** (Serantes' 123) does not — the
API has no such field and a full crawl is infeasible, so treat any org-size figure as hearsay
unless Alvaro supplies it. The figures currently in the Notion People rows came from org-chart
screenshots he shared, which is a legitimate source; `meliorg` cannot reproduce them.

Consequences worth remembering: **Peirano is the skip-level**, so his requests are not
stakeholder nice-to-haves. Janaína Silveira and Luis Vergari report to Peirano too, making
them peers of Alvaro's boss. Juanpi Sitler reports to Silvestre. Natalia Quigua is a **Sr
Manager with her own team**, not a working-level counterpart. Tharles Conegundes sits under
Tech & Ops (NPS Commerce), not Commerce Planning — a dependency, not a teammate.

So: org chart for rank and hierarchy, Slack for verified email/ID, Gmail for existence,
spelling, and standing. None of them licenses a guess about people who appear in none.

### A name that fails both is a spelling problem, not a missing person

All three unresolved names on 2026-08-20 turned out to be Gemini transcription artifacts, and
Alvaro knew each correct spelling immediately:

| Notes said | Actually |
|---|---|
| Pedro Ardoy | Pedro **H**ardoy |
| Nico Asendorf | Nicolas A**sch**endorf |
| Maru Cristiani | Maria Eugenia Cristiani |

So when a name resolves in neither system: try phonetic variants (silent leading H, sch/s,
double consonants, a nickname standing in for a full first name), then **ask him**. Do not
write a ⚠️ "not found" into the row and move on — that records a defect in the notes as if it
were a fact about the person.
