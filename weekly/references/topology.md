# Scan rules

Most directories under `~/Meli` are clones of `melisource/fury_bids`, one per feature
branch. The directory name, the branch name, and the `projects/<name>/` subdirectory are
the same string. Each clone also contains *other* projects inherited from `develop` —
ignore those; only `projects/<name>/` matching the clone's own name is live in that clone.

## Canonical project keys

These must match the `Project` title in the Notion Portfolio database exactly, or the run
creates duplicate rows.

| Key | Directories | Scan |
|---|---|---|
| `buyer-panel` | `buyer-panel`, `buyer-panel-197`, `buyer-panel-deck` | **all three**, whole repo, dedupe by SHA |
| `pads-incrementality` | `pads-incrementality` | whole repo |
| `price-perception` | `price-perception` | `-- projects/price-perception` |
| `fvf-elasticity` | `fvf-elasticity` | `-- projects/fvf-elasticity` |
| `melimas-inc` | `melimas-inc` | `-- projects/melimas-inc` |
| `pricing-combopremium` | `pricing-combopremium` | `-- projects/pricing-combopremium` |
| `ghost-ads` | `ghost-ads` | `-- projects/ghost-ads` |
| `ads-incrementality` | `ads-incrementality` | `-- projects/ads-incrementality` |
| `assortment-gaps` | `assortment-gaps` | `-- projects/assortment-gaps` |
| `measurable-ai` | `measurable-ai` | `-- projects/measurable-ai` |
| `melimas-freetrial` | `melimas-freetrial` | `-- projects/melimas-freetrial` |
| `lvas` | `lvas` | `-- projects/lvas` |

Aliases Alvaro uses in prose that map to a canonical key:
- `melimas-incrementality`, `melimas`, `Meli+` → `melimas-inc`
- `clasificadora`, `clasificador de verticales` → `buyer-panel`

Not projects, never scan: `fury_ads-pads-workspace` (another team's workspace, reference
only), `DML`, `turbo-mla` (local scratch, not git repos), `portfolio` (superseded by
Notion), `weekly` (this ritual's own output).

## The buyer-panel trap

`buyer-panel`, `buyer-panel-197` and `buyer-panel-deck` are three clones of
`melisource/fury_buyer-panel` on different branches:

```
buyer-panel        feature/yipit-two-pipeline
buyer-panel-197    feature/classifier-197-embed-text
buyer-panel-deck   docs/classifier-implicit-prior
```

They share history. Logging each directory separately triple-counts the shared commits and
makes buyer-panel look like three times the work it was. Collect from all three, dedupe on
commit SHA, attribute everything to the single `buyer-panel` row.

## Commands

fury_bids clone:

```
git -C <dir> log --since=<start> --until=<end> --format='%ad %h %s' --date=short -- projects/<name>
```

Standalone repo (`buyer-panel*`, `pads-incrementality`):

```
git -C <dir> log --since=<start> --until=<end> --format='%ad %h %s' --date=short
```

Notes in the window — the better source for anything involving other people:

```
ls <dir>/projects/<name>/notes/*.md          # fury_bids clones
ls buyer-panel*/notes/*.md                   # buyer-panel
```

Notes are named `YYYY-MM-DD_topic.md`; filter on the filename date, then read the ones in
the window.

## Sanity check

If a project shows commits but is `dormant` or `closed` in Notion, or shows none but is
`active`, surface it. That mismatch is the DB being wrong, and it is worth a line in the
diff rather than silent correction.

## Projects span repos

The recurring pattern: a project starts as a directory inside the `fury_bids` monorepo and
later branches out into its own full FDA repo. The monorepo history stays behind.

| Project | Current repo | Earlier life in fury_bids |
|---|---|---|
| `buyer-panel` | `fury_buyer-panel` | `projects/measurable-ai` — legacy, not in use |
| `pads-incrementality` | `fury_pads-incrementality` | `projects/ads-incrementality` — research history |

For the weekly scan this changes nothing: scan the current repo only. It matters when
looking for prior art, when a claim needs its origin, or when someone asks where something
came from — and `measurable-ai` and `ads-incrementality` remain their own Portfolio rows
because they were their own projects, now closed or dormant.
