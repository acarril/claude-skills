# ADR Format

ADRs (decision records, methodological or technical) live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create the `docs/adr/` directory lazily: only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording *that* a decision was made and *why*, not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`): useful when decisions are revisited
- **Considered Options**: only when the rejected alternatives are worth remembering
- **Consequences**: only when non-obvious downstream effects need to be called out

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to offer an ADR

All three of these must be true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will look at the analysis and wonder "why on earth did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If a decision is easy to reverse, skip it: you'll just reverse it. If it's not surprising, nobody will wonder why. If there was no real alternative, there's nothing to record beyond "we did the obvious thing."

### What qualifies

- **Identification strategy.** "Synthetic control, not DiD: pre-trends diverge before 2025-10 due to the fee change. Do not re-suggest DiD without addressing it."
- **Sample and data decisions.** Donor pool construction, eligibility restrictions, winsorization thresholds, why a table or snapshot was chosen over another.
- **Rejected alternatives when the rejection is non-obvious.** If you considered IV and rejected it for a subtle exclusion-restriction concern, record it; otherwise someone (or a future agent session) will suggest it again.
- **Deliberate deviations from the obvious path.** Anything where a reasonable reader (or the econometrics-police reviewer) would assume the opposite. These stop the next person from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use table X because its history only starts 2025-06." "Stakeholder committed to reporting at the seller-month level."
- **Technology choices that carry lock-in.** Pipeline architecture, orchestration choices, schema decisions that would take real effort to unwind.
