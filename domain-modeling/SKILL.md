---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing a repo's terminology (treatment definitions, cohorts, outcomes, metrics), writing or editing a CONTEXT.md, or recording or editing a decision record (ADR).
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallise. (Merely *reading* `CONTEXT.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

```
/
├── CONTEXT.md              <- glossary of the project's language
├── docs/
│   └── adr/                <- decision records (methodological and technical)
│       ├── 0001-synthetic-control-not-did.md
│       └── 0002-winsorize-outcomes-p99.md
└── src/
```

Create files lazily: only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'treated seller' as ≥1 shipped order, but you seem to mean enablement. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'adoption': do you mean enablement or first usage? Those are different events, and one of them is your instrument."

### Discuss concrete scenarios

When definitions are being discussed, stress-test them with specific edge cases. A seller who enables in March, ships one order in April, churns in May: treated? In which cohort? Invent scenarios that force the user to be precise about boundaries.

### Cross-reference with code

When the user states a definition, check whether the code agrees. If you find a contradiction, surface it: "Your glossary says outcome is net of cancellations, but the query on the consolidated table doesn't filter them. Which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up: capture them as they happen. Use the format in [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. It is a glossary and nothing else: not a spec, a scratch pad, or a repository for implementation decisions.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

Methodological decisions qualify exactly like technical ones: identification strategy, donor pool construction, sample restrictions, winsorization, why an obvious alternative estimator was rejected. If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
