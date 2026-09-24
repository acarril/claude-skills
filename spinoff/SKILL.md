---
name: spinoff
description: Fork a branching topic into its own independent Herdr tab and Claude Code session, carrying only the context that topic needs. Use when a conversation branches into a sub-question worth its own thread, or the user asks to spin one off.
---

# Spinoff

A conversation on topic A produces a genuine spinoff, topic B: worth its own thread, not just a quick aside. Fork B into an independent session so A keeps moving and B gets undivided attention.

## 1. Size the payload

The **payload** is everything B is told at launch. Size it to how self-contained B is:

- **Prompt only.** B is a fully-specified, bounded ask ("fix the null handling in the shipments step and open a PR"). A short prompt is the whole payload. Bounded does not mean read-only — most spinoffs edit code; step 3 decides where.
- **Prompt + throwaway handoff doc.** B needs background A holds but isn't fully bounded yet. Call the Skill tool with "handoff" for the doc, then reference it from the prompt.
- **Full handoff.** B is substantial enough that the `/handoff` doc is the payload's primary artifact, not a side reference.

State your recommended size and a one-line gist of the payload.

## 2. One preview gate

A single AskUserQuestion call: the recommended size first, the payload's gist, and the other sizes as options. Approving fires steps 3 and 4 immediately. This is the only interruption in the flow.

## 3. Decide where B works

Resolve A's cwd first. In Herdr that is `herdr pane get <parent pane>` — the same call returns the `display_agent` step 4 needs, so make it once and keep both values. Otherwise use `pwd`. If `git -C <cwd> rev-parse --show-toplevel` fails, A is not in a repo: hand B A's cwd and skip the rest of this section.

**Default: B shares A's cwd and A's branch.** One directory has one HEAD and one index, so B must never switch branches there, and commits only the paths it changed (`git add <paths>`, never `git add -A` / `git commit -a`, which would sweep in A's uncommitted edits). Put both rules in the payload.

**Worktree when B's work is destructive or conflicting**: B needs its own branch or PR separate from A's, rewrites history, or edits files A is also changing. A new branch in A's directory would move A onto it too, so B gets a worktree instead. Say which mode you chose in step 2's gist.

1. Use the **repo root** from `rev-parse --show-toplevel`, not the raw cwd — A may have `cd`ed into a subdirectory.
2. `git -C <root> worktree add <root>/.worktrees/<slug> -b <slug>`, where `<slug>` is a short kebab-case tag for B's topic. Then make sure `.worktrees/` is in `$(git -C <root> rev-parse --git-common-dir)/info/exclude` (append it if absent): a local-only ignore, so the worktree never shows in A's `git status` and is never committed. This branches from A's current HEAD; B renames or rebases the branch itself if its task needs a different base.
3. Link the untracked files B needs, because a worktree receives only tracked files. Read the real list before you link — it differs per repo, and a guessed name creates a dead symlink:

   ```
   git -C <root> status --porcelain --ignored -uall
   ```

   - Symlink anything A and B must agree on. `.grid-mappings.json` is the one that bites: without it B does a fresh Grid upload instead of a version bump, and the doc's URL changes.
   - Symlink large ignored data directories rather than copy them.
   - Copy interpreter pins such as `.python-version`.
   - Do **not** symlink `.venv`. One shared environment works until B changes a dependency, and then B's `poetry install` mutates A's environment. B runs its own install when it first needs to execute code, not before.
4. Give B the path inside the worktree that mirrors where A was: worktree root plus A's cwd relative to `<root>`, so B lands in the same subdirectory A was working in. Nothing removes the worktree automatically, so report its path and let the user `git worktree remove` it once B's PR merges.

One exception: a worktree hides A's *uncommitted* edits, because it starts from a commit. If B's task depends on work A has not committed, give B A's cwd instead and say so in the report, so the git hazard above is a known risk rather than a surprise.

## 4. Fire

B runs the same model as A, unless the user asked for a different one.

Check `HERDR_ENV`:

- **`HERDR_ENV=1`**: call the Skill tool with "herdr" for the CLI mechanics, then:
  1. Query the parent pane fresh, at fire time — step 3 already made this call, so reuse its result. One `herdr pane get <parent pane>` returns both things you need: its `cwd` (the parent may have `cd`ed mid-conversation) and its `display_agent`, which `~/.config/herdr/herdr-model-label.sh` keeps set to A's live model (`opus-5.5`, `sonnet-5`) and which follows a mid-session `/model` switch.
  2. Derive the model. Take the segment of `display_agent` before the first `-` (`opus-5.5` → `opus`) and use it as the alias if it is `opus`, `sonnet`, `haiku`, or `fable`. Do not try to rebuild a full model id from `display_agent`: the label is lossy for dotted versions (`haiku-4.5` is not `claude-haiku-4-5-20251001`), and the alias already means "latest of that family". Anything else — null on a fresh pane whose first `Stop` has not fired yet, a `gpt-*` label from a codex parent, a stale topic name — falls back to `jq -r '.model // empty' ~/.claude/settings.json`, passed to `--model` **verbatim**: that is a settings token like `opus[1m]`, not a family alias, so do not validate it against the list above. Only if that is empty too, use `claude-opus-5-5`. Never omit `--model`: an org-enforced default can outrank the settings.json preference at startup, and a resumed session re-resolves the same way rather than remembering what it ran on. The flag is the only thing that beats it.
  3. `herdr tab create --cwd <B's cwd from step 3> --env HERDR_LAUNCH_SKIP=1`. **Never pass `--label`.** B names its own tab: Claude Code generates a conversation title, and the `herdr-automatic-rename` plugin copies it over. A placeholder label defeats that permanently — the plugin reads any non-placeholder label on first sight as a hand rename and sets `enabled:false` for that tab forever, so your guess sticks and B's real title never lands. With no `--label` the tab starts as a bare number, which the plugin treats as unowned and adopts. **`--env HERDR_LAUNCH_SKIP=1` is required on this machine**: `terminal.default_shell` is a picker script, and its fzf holds the new pane's foreground, so the next step fails with `agent_pane_busy` without it. If you inherited a pane already sitting on the picker, `herdr pane send-keys <pane> Escape` drops it to a shell.
  4. `herdr agent start <name> --kind claude --pane <new pane> -- --model <the model from step 2>`. Native agent args go after `--`. `<name>` is a **handle** for the commands below, not a display label — keep it short and mechanical, and do not try to make it descriptive.
  5. Mask that handle: `herdr pane report-metadata <new pane> --source local:model-label --display-agent <the parent's display_agent from step 1>`. The sidebar's `agent` token resolves display_agent > name > kind, and `herdr-model-label.sh` only writes on Stop, so without this the handle is what shows until B finishes its first turn. B runs the parent's model, so the parent's label is the correct value, and the hook overwrites it with a freshly-read one later. Skip if step 1 found no `display_agent`.
  6. `herdr agent prompt <name> "<the payload>"`, without `--wait`.
- **Not in Herdr**: fall back to the Agent tool, `subagent_type: "fork"`, with the same payload, plus `isolation: "worktree"` when step 3 chose a worktree. It runs in-process rather than in a tab, and always inherits A's model, so steps 1–2 do not apply. The fork creates and cleans up its own worktree, so step 3's `worktree add` is redundant here — skip it, and put step 3's linking instructions in the payload for B to run against A's cwd.

## 5. Report and continue

Name where B is running (its tab and agent, or "forked" for the fallback) and, when step 3 made one, B's worktree path as a `file://` URL plus the branch it sits on, then continue working on A. Refer to B by its tab id and pane, not by a name you invented — the tab is still a bare number at this point and will name itself shortly.

The two branches then diverge, and the report says which applies:

- **Herdr tab**: B is independent from here. The user checks on it directly by switching tabs, or asks A to read it via the `herdr` skill.
- **Agent-tool fallback**: B's result lands in this session when it finishes, since an in-process fork reports back to its parent.
