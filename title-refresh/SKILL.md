---
name: title-refresh
description: Use when the current Claude Code session's title is stale or was auto-generated early and no longer reflects the conversation, and you want to refresh/rename/update it to match what's actually been discussed. Triggered by /title-refresh.
---

# title-refresh

## Overview

Refresh the **current** Claude Code session's displayed title to reflect the conversation so far, by appending a fresh `ai-title` record to the session's `.jsonl` log.

Run this from inside the live session whose title you want to change — you (the agent) already hold the full conversation in context, so you compose the title directly. No subagent.

## Key facts (non-obvious — get these wrong and it silently fails)

- A session's title is **not** a field on a message. It's a standalone record appended to the session log: `{"type":"ai-title","aiTitle":"...","sessionId":"..."}` (and `custom-title`/`customTitle` for `/rename`).
- The effective title is the **last** record of its type. Claude Code ingests the latest one from the file into memory and re-emits it on its next flush.
- **APPEND a new record — never edit an existing line.** Claude Code keeps re-emitting its in-memory copy; an in-place edit to an old line is not the latest record and gets ignored.
- Display precedence: **`custom-title` outranks `ai-title`.** If the session has a `custom-title`, a fresh `ai-title` will not show.

## Procedure

1. **Locate the live session file.**
   ```bash
   proj=~/.claude/projects/$(echo "$PWD" | sed 's/[/.]/-/g')
   file=$(ls -t "$proj"/*.jsonl | head -1)   # newest = this live session
   echo "$file"
   ```
   Print the file and its current title so a mis-target is catchable (rare, but possible if two sessions share one cwd):
   ```bash
   grep '"type":"ai-title"\|"type":"custom-title"' "$file" | tail -1
   ```

2. **Mask check.** If the file contains any `custom-title` record, STOP — an `ai-title` write would be invisible. Tell the user to use `/rename` instead, or to confirm they want the title written as a `custom-title`.
   ```bash
   grep -q '"type":"custom-title"' "$file" && echo "HAS custom-title — stop"
   ```

3. **Get the sessionId** from the file:
   ```bash
   sid=$(grep -o '"sessionId":"[^"]*"' "$file" | head -1 | cut -d'"' -f4)
   ```

4. **Compose the title** from the conversation you hold in context: concise, sentence-case, ~4-8 words, matching Claude Code's house style; weight the overall arc and the most recent direction. If the user passed arguments to the skill, use them as a steer.

5. **Append** one well-formed record (use `python3` so the title is correctly JSON-escaped — never hand-build the JSON with quotes in the title):
   ```bash
   python3 - "$file" "$sid" "Your composed title here" <<'PY'
   import json, sys
   path, sid, title = sys.argv[1], sys.argv[2], sys.argv[3]
   rec = {"type": "ai-title", "aiTitle": title, "sessionId": sid}
   with open(path, "a") as f:
       f.write(json.dumps(rec, separators=(",", ":")) + "\n")  # compact: matches CC's format + the no-space greps above
   PY
   ```

6. **Report** `old → new` title. Note it takes effect on Claude Code's next flush (a turn or two), not instantly.

## Common mistakes

- **Editing the existing title line** instead of appending → ignored by Claude Code. Always append.
- **Finding the dir with `ls`/guessing** instead of deriving it from `$PWD` → picks the wrong session when many project dirs exist.
- **Writing `ai-title` while a `custom-title` exists** → invisible (precedence). Do the mask check.
- **Hand-building the JSON** with a title containing quotes/colons → malformed line. Use `python3`/`json.dumps`.
