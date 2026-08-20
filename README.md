# Personal Claude Code skills

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
| [grill-me](grill-me/SKILL.md) | user (`/grill-me`) | Entry point: calls `grilling` | mattpocock/skills@0ab1b63, verbatim |
| [grilling](grilling/SKILL.md) | model | Relentless interview over a design tree of decisions, rounds via AskUserQuestion | mattpocock/skills@0ab1b63, adapted |
| [to-questionnaire](to-questionnaire/SKILL.md) | user (`/to-questionnaire`) | Turn a decision you can't answer alone into a questionnaire for the person who can | mattpocock/skills@0ab1b63, adapted (recipient-language rule added) |
| [writing-for-agents](writing-for-agents/SKILL.md) | model | Reference for writing skills, CLAUDE.md, and any doc an agent consumes | mattpocock/skills@0ab1b63, verbatim |
