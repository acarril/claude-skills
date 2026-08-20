# CONTEXT.md Format

## Structure

```md
# {Project Name}

{One or two sentence description of what this project is and why it exists.}

## Language

**Treated seller**:
Seller with at least one order shipped via the feature during the exposure window.
_Avoid_: adopter, enabled seller (enablement is a different event)

**Exposure window**:
2026-03-01 to 2026-05-31, fixed calendar window. Not seller-specific.

**Outcome**:
Seller-month NMV, net of cancellations.
_Avoid_: GMV, sales, revenue
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others under `_Avoid_`.
- **Keep definitions tight.** One or two sentences max. Define what it IS, not what it does.
- **Only include terms specific to this project's context.** General programming or statistics concepts (timeouts, standard errors, utility patterns) don't belong even if the project uses them extensively. Before adding a term, ask: is this a concept unique to this project, or a general concept? Only the former belongs.
- **Group terms under subheadings** when natural clusters emerge (e.g. Design, Data, Metrics). If all terms belong to a single cohesive area, a flat list is fine.

One `CONTEXT.md` at the repo root. If neither it nor a term exists yet, create the file lazily when the first term is resolved.
