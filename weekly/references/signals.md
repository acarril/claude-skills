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

## 4. Agent sessions — the advisory record

**The source that catches advisory work.** It leaves no commits, so a scan that skips it lets
O3 fail silently. Use `memex`, not a glob over `~/.claude/projects/`: the glob is Claude-only,
and Codex holds more than half of these sessions.

Run `memex index` once at the start of the scan (~5s, incremental). `memex sessions` does
**not** auto-index, so without this the last few days are missing.

### Discovery — one call covers every project

```bash
memex sessions --since <window start> --limit 500 --json-array
```

Each row carries `session_id`, `source`, `source_path`, `cwd`, `git_root`, `started_at`,
`last_at`, `message_count`. **Group by `git_root`** — its basename is the directory key in
`topology.md`; memex resolves both the repo root and `projects/<name>` to the same git root.

Scope to one repo with `--cwd ~/Meli/<dir>`. It matches by path component, so
`--cwd ~/Meli/buyer-panel` does **not** pull in `buyer-panel-197` or `buyer-panel-deck` —
the triple-count trap does not apply here.

Two traps of its own:

- **`--since` means "session active in the window"**, not "has an in-window user message". It
  over-includes: a session whose real work predates the window appears if anything touched it
  since. The per-message date filter below is what actually enforces the window. Never report
  a session as this week's work just because it was listed.
- **Codex forks share one `session_id` across several `rollout-*.jsonl` files.** Always pass
  `--source-path` when fetching, and dedupe on `(session_id, ts, text)`.

### Extraction — user messages only

His own messages are short, carry the intent, and are cheap to read; the assistant side is
enormous and mostly redundant. Filter by entry timestamp, never file mtime — a session can
span weeks.

`memex session` pages at **500 records** and sessions here reach several thousand. Paginate
with `--offset` or you silently truncate the biggest projects: measured on the 2026-08-18
window, skipping pagination lost 102 of 367 Claude messages, all from the longest sessions,
with no error.

```python
import json, subprocess, datetime
START = '<window start>'
SKIP = ('<local-command', '<command-name', '<command-message', '[Request interrupted',
        'Base directory', '<system-reminder', '<task-notification',
        '# AGENTS.md instructions')
PAGE = 500

def day(ms):
    return datetime.datetime.fromtimestamp(ms / 1000, datetime.UTC).strftime('%Y-%m-%d')

def records(session_id, source_path):
    off = 0
    while True:
        out = subprocess.run(
            ['memex', 'session', session_id, '--source-path', source_path,
             '--offset', str(off), '--limit', str(PAGE)],
            capture_output=True, text=True).stdout.splitlines()
        for line in out:
            try: yield json.loads(line)['record']
            except Exception: pass
        if len(out) < PAGE: return
        off += PAGE

rows = json.loads(subprocess.run(
    ['memex', 'sessions', '--since', START, '--limit', '500', '--json-array'],
    capture_output=True, text=True).stdout)

seen = set()
for r in rows:
    root = r.get('git_root') or ''
    if not root.startswith('/Users/acarril/Meli/'): continue
    proj = root.rsplit('/', 1)[-1]
    for rec in records(r['session_id'], r['source_path']):
        if rec.get('role') != 'user': continue
        if day(rec['ts']) < START: continue
        txt = (rec.get('text') or '').strip()
        if not txt or txt.startswith(SKIP) or len(txt) < 25: continue
        key = (r['session_id'], rec['ts'], txt)
        if key in seen: continue
        seen.add(key)
        print(proj, r['source'], day(rec['ts']), txt[:260].replace('\n', ' '))
```

Records nest under a `record` key. `ts` is epoch **milliseconds** for both Claude and Codex.

When a specific claim needs the answer and not just the question, search inside the session
instead of grepping a 10MB file:

```bash
memex search "<exact term>" --session <session_id> --sort ts --limit 50
```

`memex search` requires a non-empty query — there is no sweep mode, which is why discovery
goes through `memex sessions` and not `search`.

### Care required

Sessions record **what he explored**, not **what is true or shipped**. Two failure modes:

- Never report an explored idea as a delivered thing. "Exploramos CUPED" is honest;
  "implementamos CUPED" is false.
- A conclusion reached in a session is real and reportable — including negative results.
  "CUPED no sirve acá: ρ² ≈ 0.03–0.07" is one of the more valuable lines a week can produce.

Cross-check anything load-bearing against an artifact in the working tree.

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
