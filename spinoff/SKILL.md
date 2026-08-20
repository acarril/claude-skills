---
name: spinoff
description: Fork a branching topic into its own independent Herdr tab and Claude Code session, carrying only the context that topic needs. Use when a conversation branches into a sub-question worth its own thread, or the user asks to spin one off.
---

# Spinoff

A conversation on topic A produces a genuine spinoff, topic B: worth its own thread, not just a quick aside. Fork B into an independent session so A keeps moving and B gets undivided attention.

## 1. Size the payload

The **payload** is everything B is told at launch. Size it to how self-contained B is:

- **Prompt only.** B is a fully-specified, bounded ask ("check whether the join fans out on seller_id"). A short prompt is the whole payload.
- **Prompt + throwaway handoff doc.** B needs background A holds but isn't fully bounded yet. Call the Skill tool with "handoff" for the doc, then reference it from the prompt.
- **Full handoff.** B is substantial enough that the `/handoff` doc is the payload's primary artifact, not a side reference.

State your recommended size and a one-line gist of the payload.

## 2. One preview gate

A single AskUserQuestion call: the recommended size first, the payload's gist, and the other sizes as options. Approving fires step 3 immediately. This is the only interruption in the flow.

## 3. Fire

Check `HERDR_ENV`:

- **`HERDR_ENV=1`**: call the Skill tool with "herdr" for the CLI mechanics, then:
  1. Query the parent pane's cwd fresh, at fire time (the parent may have `cd`ed mid-conversation).
  2. `herdr tab create --cwd <that cwd>`. `--label` takes a rough placeholder; the tab renames itself once B has a title.
  3. `herdr agent start <name> --kind claude --pane <new pane>`.
  4. `herdr agent prompt <name> "<the payload>"`, without `--wait`.
- **Not in Herdr**: fall back to the Agent tool, `subagent_type: "fork"`, with the same payload. It runs in-process rather than in a tab.

## 4. Report and continue

Name where B is running (its tab and agent, or "forked" for the fallback), then continue working on A.

The two branches then diverge, and the report says which applies:

- **Herdr tab**: B is independent from here. The user checks on it directly by switching tabs, or asks A to read it via the `herdr` skill.
- **Agent-tool fallback**: B's result lands in this session when it finishes, since an in-process fork reports back to its parent.
