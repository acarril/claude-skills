# Notion write rules

Home page "Work": https://app.notion.com/p/3c161f26a848818b8963c671f4c772b9

| Database | Data source ID | Touched by this ritual |
|---|---|---|
| Portfolio | `73e8e500-a85f-460a-ac4e-b4aa8de36542` | yes, weekly |
| Impact ledger | `2c0392d0-e1d5-4978-908c-1f96c269ab26` | only on an explicit yes |
| Goals | `e494f374-52d6-41d2-b075-d9d70771aa10` | no — quarterly |
| People | `99305162-cb2d-4f82-b5eb-55645a720f80` | no — monthly |

## Portfolio properties

Title is `Name` — the row's own name, nothing else. Writable by this ritual: `Next`,
`Blocked on`, `Status`, `Updated`.

Leave alone: `Role`, `Goal`, `Repo`, `Branch`, `Local path`, `Stakeholder`, `Impact`, and
the `Objective` / `People` / `Impact claims` relations. Those change on human decisions, not
on a week of commits.

`Infra` (multi-select: `fda`, `dataflow`, `grid`, `qualtrics`) says **what a row is built
on** — hence where it breaks and who to call. It is descriptive and it is **not** evidence of
production. `comparacion-yipit-mlb` carries `fda` and writes only to `meli-sbox`; every one
of the 15 directories has a `workflows.yml` because they are all clones of the same FDA
template. Tooling is not production.

`Track infra` is a read-only rollup of the tracks' `Infra` onto the project row — the "does
any track use dataflow" visibility, without converting it into a claim.

The `Infra check` view lists rows carrying `dataflow` or `fda` **without** `Prod`. It is a
prompt, not a rule: each row there is either correctly sandbox-only, or a `Prod` someone
forgot. Glance at it during the weekly; do not auto-tick anything.

`Prod` (checkbox) is orthogonal to `Status`: something in the row runs unattended and can
break — a scheduled DataFlow job, an FDA workflow, a WHOWNER table others consume. Set on
`price-perception` (3 DataFlow jobs owning `DM_PRICEPERCEPTION_RESPONSES` and
`DM_PRICEPERCEPTION_SURVEYED_HISTORY`), `buyer-panel`, `pads-incrementality`,
`bp / clasificador-verticales`, `pads / legacy-cutover`.

**`paused` + `Prod` is the alarm**: nobody is watching something that can still break.
`Needs attention` filters on `Blocked on IS NOT EMPTY OR (Prod AND paused)` for exactly this
reason. The combination is empty today; keep it that way, and when the ritual moves a Prod
row to `paused`, say so out loud.

Do not set `Prod` on offline or sandbox work. `bp / comparacion-yipit-mlb` writes only to
`meli-sbox` and its plan states "no FDA/platform mutations" — it is not Prod.

`Status` options: `active`, `paused`, `closed` — and that is deliberately all three.

Status tracks **where his attention is, not where the code is.** `live` and `dormant` were
removed 2026-08-20 as false distinctions: `live` meant "in production", which is a different
variable from "being worked on" (buyer-panel was both, and the select forced it to pick),
and `paused` vs `dormant` was already visible in whether `Blocked on` says anything.

Production state is the `Prod` checkbox, added 2026-08-20 — never a status value.

## Dates are expanded

Date properties do **not** accept a single value. Use the expanded keys or the write fails:

```
"date:Updated:start": "2026-08-21"
```

Same for `date:Date:start` (Impact ledger) and `date:Last interaction:start` (People).

## Derivation rules

From the **edited** update only:

- `Next` ← his `Next:` lines, verbatim where they read as a sentence. If a project has
  several, join them; do not summarize them into something vaguer than what he wrote.
- `Blocked on` ← anything phrased as waiting on a person or team. Name the person. If
  nothing in the update says he is waiting, clear the field rather than leaving a stale one.
- `Status` ← propose a change only on visible evidence: commits and bullets on a `dormant`
  row → `active`; nothing for several consecutive weeks on an `active` row → raise it as a
  question, do not demote silently.
- `Updated` ← the window's end date, on every project that had any activity. A project with
  no activity keeps its old date — that is what makes staleness visible in the views.

Show the full diff and get approval before writing. One `notion-update-page` call per
changed row, `command: "update_properties"`.

## Impact ledger

Only on an explicit yes. Required at minimum: `Claim` (one sentence, committee-ready),
`date:Date:start`, `Attribution`, `Project` relation.

`Scope USD/yr` is the size of the decision surface, not a claimed effect — leave it blank
rather than guessing, and put the sourcing question in `Scope basis`. `What changed because
of me` is the field that carries the claim; a row without it is an artifact, not impact.

`Attribution` options: `owned`, `co-owned`, `advised`, `method-corrected`, `enabled`.

## Known stale rows, as of 2026-08-20

Fix on the first run:

- ~~`fury_ads-incrementality` — repo deleted 2026-08-04.~~ Fixed 2026-08-20: `closed`.
- ~~`pads-incrementality` — marked `dormant`, has real activity.~~ Fixed 2026-08-20: `active`.
- `buyer-panel` — `Branch` says `master`; the live clones are on
  `feature/yipit-two-pipeline`, `feature/classifier-197-embed-text`,
  `docs/classifier-implicit-prior`.
- `pricing-combopremium` — marked `active` and carries O1, but nearly no commits since
  early August. Ask; do not demote silently.

## Tracks

Portfolio holds both projects and tracks in one table, distinguished by the `Part of`
self-relation:

- `Project` empty → the row is a **project**
- `Project` set → the row is a **track** inside that project
- `Tracks` empty → the row is a **leaf**: either a track, or a project with no tracks

Three columns carry the hierarchy: `Name` (own name), `Project` (relation to parent),
`Tracks` (relation to children). `Project` and `Tracks` are the two ends of one
self-relation — renaming or ALTERing either recreates the pair and spawns duplicates, so
touch them only with `RENAME COLUMN`.

A track earns a row only when it has its own goal, blocker, or next step. Otherwise it stays
a bold heading in the weekly and nothing more. `melimas-inc` and `ghost-ads` deliberately
have none.

### Which row gets the write

**Write to the leaf, never to the parent.** A bold track heading in the weekly maps to its
track row; its `Next:` and `Esperando:` lines fill that row's fields. A project that has
tracks should not get its own `Next` — it would compete with its children's and nothing
would know which is current.

Track names are bare (`dashboard`, `comparacion-yipit-mlb`) — the `Project` column supplies
the context that a `pp /` prefix used to. One trade-off: relation pickers in other databases
show only `Name`, so a generic track name like `dashboard` loses its project there. If that
becomes annoying, re-prefix the titles; nothing else depends on the format.

### The hierarchy is a plain relation, not Notion sub-items

`Part of` / `Tracks` is an ordinary self-relation. It does **not** give the expandable
parent rows of Notion's native Sub-items feature, which is a UI toggle that cannot be set
through the API. The `All rows` view groups by `Part of` instead, which achieves the same
readability. If sub-items ever get enabled by hand in the UI, check whether it adopts this
relation or creates its own pair — if the latter, one of them has to go.

### Views and the leaf rule

`By goal` and the home page board filter on `Tracks IS EMPTY` — leaves only. That shows
each track under the objective it actually serves, without double-counting its parent.
`Projects` is the default (leftmost) tab: `Project IS EMPTY`, the 13 top-level rows.
`All Tracks` is `Project IS NOT EMPTY`, grouped by `Project`. `Needs attention` is
deliberately unfiltered: a blocker matters wherever it sits.

View order is what makes a view the default in Notion, and the API cannot reorder tabs —
so a view's *config* gets swapped onto the existing leftmost view rather than creating a
new one and dragging it. There is no delete-view API either; stale tabs have to be removed
by hand.

### One project, two objectives

`pricing-combopremium` carries O1 through `combo / pnl-redesign` and O3 through
`combo / brasil-poc-advisory`. At project grain those collapse into one `Goal` cell and one
of them disappears. That is the case tracks exist for — do not flatten it back.

## The Repo column

`Repo` is **rich text holding markdown links**, not a select. Notion parses
`[label](url)` written into a text property into a real link — the cell shows the label and
clicks through. This is the only way to get a linked, custom-labelled value; select options
cannot carry URLs, and a URL property cannot carry a label.

Label rules:

- Drop the `fury_` prefix — every Meli repo has it, so it carries no information.
- Monorepo rows read `bids/<branch minus its prefix>`: branch `feature/price-perception`
  becomes `bids/price-perception`.
- Standalone repos read `<repo minus fury_>` and add `/<branch>` when one branch is the
  point: `buyer-panel/yipit-two-pipeline`, `pads-incrementality/live`.
- Several repos are separated by ` · `, current first.

URLs are `https://github.com/melisource/<repo>/tree/<full-branch>` — the full branch,
including the `feature/` or `release/` prefix stripped from the label.

Tracks link to their own branch, which is where this earns its keep: `buyer-panel` the
project points at the repo root, while its two tracks point at
`feature/classifier-197-embed-text` and `feature/yipit-two-pipeline`.

## Self-relation rollups bind to the opposite end

Confirmed twice on this database: `ROLLUP('<relation>', ...)` on a **self-relation** binds to
the *other* end of the pair. To roll up over `Tracks` (children), write `ROLLUP('Project',
...)`. To roll up over `Project` (parent), write `ROLLUP('Tracks', ...)`. Always check the
returned `relationPropertyUrl` against the relation you wanted before trusting the column —
rollup *values* come back as opaque `rollupResult://` handles and cannot be verified by query.

Also: statements in one `update_data_source` call are parsed together, so a rollup cannot
reference a column added in the same call. Split them.
