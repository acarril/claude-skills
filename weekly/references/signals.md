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
