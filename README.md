# my claude-code skills

Flat layout: `~/.claude/skills/<name>/SKILL.md` (Claude Code discovers one level deep).
Versioned with git; plugin-ready later by adding `.claude-plugin/plugin.json` if ever needed.

## Conventions

- **Invocation is the organizing axis.** Skills only ever invoked by typing `/<name>` get
  `disable-model-invocation: true` (zero always-loaded context cost). Skills the model
  should reach on its own keep a `description` with trigger conditions.
- **Provenance.** Ported/adapted skills record their upstream repo + commit here, so they
  can be diffed against upstream later.

## Index

| Skill | Invocation | What it does | Provenance |
|---|---|---|---|
| [handoff](handoff/SKILL.md) | user (`/handoff`) | Compact the conversation into a handoff doc for the next session | own |
| [meet-notes](meet-notes/SKILL.md) | model | Distill Google Meet / Gemini notes into a project knowledge doc | own |
| [title-refresh](title-refresh/SKILL.md) | user (`/title-refresh`) | Refresh a stale session title | own |
| [grill-me](grill-me/SKILL.md) | model | Relentless interview over a design tree of decisions, rounds via AskUserQuestion | mattpocock/skills@0ab1b63, adapted (primitive merged in; was `grilling`) |
| [diagnosing-bugs](diagnosing-bugs/SKILL.md) | model | Phase-gated diagnosis for hard bugs and wrong numbers: red-capable feedback loop before any hypothesis | mattpocock/skills@0ab1b63, rewritten (data/pipeline loop menu, SQL regression checks) |
| [domain-modeling](domain-modeling/SKILL.md) | model | Sharpen project terminology into a CONTEXT.md glossary; record hard-to-reverse choices as ADRs | mattpocock/skills@0ab1b63, adapted (causal-inference framing, single-context only) |
| [grill-with-docs](grill-with-docs/SKILL.md) | user (`/grill-with-docs`) | Entry point: `grill-me` + `domain-modeling` (grill with a paper trail) | mattpocock/skills@0ab1b63, verbatim |
| [to-questionnaire](to-questionnaire/SKILL.md) | user (`/to-questionnaire`) | Turn a decision you can't answer alone into a questionnaire for the person who can | mattpocock/skills@0ab1b63, adapted (recipient-language rule added) |
| [writing-for-agents](writing-for-agents/SKILL.md) | model | Reference for writing skills, CLAUDE.md, and any doc an agent consumes | mattpocock/skills@0ab1b63, verbatim |
| [resolving-merge-conflicts](resolving-merge-conflicts/SKILL.md) | model | Work an in-progress merge/rebase conflict hunk by hunk, resolving by intent; never abort | mattpocock/skills@0ab1b63, verbatim |
| [bro](bro/SKILL.md) | user (`/bro`) | Re-pitch the last message in plain English using the repo's CONTEXT.md vocabulary | mattpocock/skills@0ab1b63, adapted; renamed after pstack's `bro` |
| [wrap-up](wrap-up/SKILL.md) | user (`/wrap-up`) | End-of-session ritual: arc summary, then commits/docs/cleanup/handoff via one checklist | own (designed 2026-08-20 via grilling) |
| [unslop](unslop/SKILL.md) | model | Cut AI tells from written deliverables (pattern catalog + plain-speech rules) | cursor/plugins@51a96e0 (pstack), adapted (scoped to deliverables, Spanish note) |
| [blast-radius](blast-radius/SKILL.md) | user (`/blast-radius`) | Prove the one fact a change is safe because of, via real queries; lineage-aware risk sweep | cursor/plugins@51a96e0 (pstack), rewritten for data/pipeline lineage |
