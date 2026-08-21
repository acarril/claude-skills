---
name: meliorg
description: MercadoLibre reporting lines - a person's leader, the chain above them, their direct reports, or their peers. Use when a question turns on who reports to whom or on rank at MELI (skip-level, team membership, seniority). The org chart is authoritative; Slack titles are not. Requires corporate VPN.
argument-hint: "[chain|reports|peers|find|tree] <name-or-ldap>"
allowed-tools: [Bash]
---

# meliorg

Reporting lines from MELI's directory, via the Grid API. Everything runs through
one script; you should not need to write curl.

```bash
S=~/.claude/skills/meliorg/scripts/meliorg.py

python3 $S whoami                  # you, incl. manager_username
python3 $S chain [ldap]            # up the reporting line to the root
python3 $S reports <ldap>          # direct reports, 1 level
python3 $S peers [ldap]            # same direct manager
python3 $S find "Ignacio Campos"   # name or LDAP -> full record
python3 $S tree <ldap> --depth 2   # bounded subtree, see "Cost" below
```

Add `--json` for `{"stale_as_of": null|iso, "data": ...}`, `--refresh` to bypass the
cache. Both flags work on either side of the subcommand.

## Source precedence -- this is the point of the skill

**org chart > Slack > notes > nothing. Never infer.**

The org chart is authoritative and Slack is not. Observed: Peirano's Slack title read
"Strategic Planning Senior Manager" while the chart said **Planning Commerce Sr
Director**, a rung higher. People with no Slack profile at all can be Vice Presidents.

So: never derive a reporting line from Slack titles, email traffic, or meeting
attendance. If this tool cannot answer, say the hierarchy is unknown -- do not guess
from communication patterns. Someone who emails Alvaro constantly may be a peer, a
stakeholder, or from another org entirely.

Use Slack for verified email/ID, Gmail for whether a person exists at all, and this
skill for rank and hierarchy.

## Disambiguation

`find` matches on **name or LDAP only** -- department and title are not searchable, so
"who runs Shipping" has no direct answer. A name query often returns several people
("Ignacio Campos" returns 3). Always show the candidates with title and department and
let the user pick; never silently take the first hit. Use `username` (LDAP) for every
downstream call.

## Cost, and why `tree` is capped

Every node costs one request (two with `--enrich`) against a **60/min per-user** limit.
`chain` is ~6 requests; `tree --depth 2` over a 5-person org was 22 requests in ~9s.
`MAX_DEPTH` is 4 and the script refuses to go deeper. This cannot enumerate MELI, and
attempting it will rate-limit you out. There is no bulk source -- `meli-bi-data` has no
HR dataset, and `LK_USER_*` tables are marketplace customers, not employees.

Answers cache for 7 days at `~/.cache/meliorg.json`.

## Off-VPN

Every endpoint is unreachable without the corporate VPN. The script then serves the
cache and marks it: a banner on **stderr** and `stale_as_of` in the `--json` envelope.
**Surface that staleness to the user** -- an org chart from three weeks ago is exactly
the kind of thing that looks live and is not. With no cached value for that query, it
fails outright rather than guessing.

## How it works underneath

No auth headers; Grid resolves identity at the edge from your network.

| Call | Gives |
|---|---|
| `GET /api/v1/me` | your record + `manager_username` |
| `GET /api/v1/people/search?q=` | any person + `manager_username` (upward) |
| `POST /api/v1/engine/run/json` with `{"share_with":["reportes de X"]}` | direct reports (downward) |

The third is a **dry-run**: `share_with` with no `file`, `doc_id`, or `slack_to` resolves
recipients and grants nothing. Do **not** send `skill_version` -- omitting it skips the
version check entirely, and `skip_version_check: true` does not rescue a stale value.

Related: `grid-sharing` covers turning a name into an email so you can share a file.
That is a different question from where someone sits.
