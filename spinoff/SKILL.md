---
name: spinoff
description: Fork a spinoff topic into a new, independent Herdr tab running its own Claude Code session, sized with only the context that topic needs. Use when a conversation clearly branches into an unrelated sub-question worth its own thread, or the user says "spin this off" / "fork this".
---

# Spinoff

A conversation on topic A produces a genuine spinoff, topic B: worth its own thread, not just a quick aside. Fork B into an independent session so A keeps moving and B gets undivided attention.

## 1. Assess what B needs

Judge how self-contained B is against three sizes:

- **Prompt only.** B is a fully-specified, bounded ask ("check whether the join fans out on seller_id"). A short prompt is the whole payload.
- **Prompt + throwaway handoff doc.** B needs background A has but isn't fully bounded yet — call the Skill tool with "handoff" to produce the doc, then the prompt to B references it.
- **Full handoff.** B is substantial enough that the same `/handoff` doc is the primary artifact, not a side reference.

State your recommended size and a one-line gist of what B will actually be told.

## 2. One preview gate

A single AskUserQuestion call: the recommended size first, the gist of B's payload, and the alternative sizes as other options. Approving fires step 3 immediately with no further prompts. This is the only interruption in the whole flow.

## 3. Fire

Check `HERDR_ENV`:

- **`HERDR_ENV=1`**: call the Skill tool with "herdr" for the CLI mechanics, then:
  1. Query the parent pane's **live** cwd fresh (never a value cached earlier in the conversation — the parent may have `cd`ed since).
  2. `herdr tab create --cwd <that cwd>` (add `--label` with a short placeholder phrase if one comes easily; don't labor over it — the existing `herdr-rename-tab.sh` hook renames the tab to the new session's own title automatically once it has one, so nothing further is needed here).
  3. `herdr agent start <name> --kind claude --pane <new pane>`.
  4. `herdr agent prompt <name> "<the sized payload from step 1>"` — no `--wait`. Fire-and-forget.
- **Not in Herdr**: fall back to the Agent tool, `subagent_type: "fork"`, with the same payload. It runs in-process and reports back here instead of opening a tab.

## 4. Report and continue

Tell the user B is running (tab/agent name if Herdr, "forked" if not), then immediately continue working on A. Never poll or wait on B afterward — B is independent from here; the user checks on it directly (switching tabs, or asking A to peek via the `herdr` skill if they explicitly request it).
