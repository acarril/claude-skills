---
name: title-refresh
description: Refresh a stale or early-auto-generated session title to match the conversation.
disable-model-invocation: true
---

# title-refresh

## Overview

Refresh the **current** Claude Code session's displayed title, by appending a fresh
`ai-title` record to the session's `.jsonl` log.

**Your job is to dispatch, not to compose.** Spawn one background subagent and report that
you did. Do not locate the file, read the log, or think about the title yourself.

Why: composing six words is the cheapest work in the session, and doing it inline spends
the session's model on it, blocks the user's turn, and dumps session-log greps into your
context. A `haiku` subagent does it for a fraction of the cost while the user keeps working.

It reads the conversation off disk rather than inheriting it. That is deliberate — a
`fork` would inherit your context but is pinned to *your* model, which defeats the point.
Filtering the log to text-only turns yields ~2.6% of the file (about 9KB on a medium
session), which is the whole conversation minus the tool noise a title shouldn't reflect.

## Dispatch

One `Agent` call: `subagent_type: "general-purpose"`, `model: "haiku"`. Pass the block below
verbatim as the prompt, appending the user's `$ARGUMENTS` as a steer if they gave any.

Then tell the user it's dispatched and stop. The result arrives as a task notification;
relay the `old -> new` line when it does.

````
Refresh the title of the live Claude Code session you are running inside, by appending an
`ai-title` record to its `.jsonl` log. Work only in the session's project directory; do not
touch anything else. Report the old and new titles as `old -> new`, or the reason you stopped.

Non-obvious mechanics. Get these wrong and it fails silently:

- A session's title is not a field on a message. It is a standalone record appended to the
  session log: `{"type":"ai-title","aiTitle":"...","sessionId":"..."}` (`custom-title` /
  `customTitle` is the `/rename` equivalent).
- The effective title is the LAST record of its type. Claude Code ingests the latest one
  into memory and re-emits it on its next flush.
- APPEND a new record. Never edit an existing line: Claude Code keeps re-emitting its
  in-memory copy, so an in-place edit to an old line is not the latest record and is ignored.
- `custom-title` outranks `ai-title` in display precedence.

1. Locate the live session file. Derive the directory from `$PWD` rather than guessing;
   the newest `.jsonl` is this session (subagents like you do not create one, so `ls -t`
   is safe here). Print the file and its current title:

   ```bash
   proj=~/.claude/projects/$(echo "$PWD" | sed 's/[/.]/-/g')
   file=$(ls -t "$proj"/*.jsonl | head -1)
   echo "$file"
   grep '"type":"ai-title"\|"type":"custom-title"' "$file" | tail -1
   ```

2. Mask check. If the file has any `custom-title` record, STOP and report that an
   `ai-title` write would be invisible and the user should use `/rename` instead:

   ```bash
   grep -q '"type":"custom-title"' "$file" && echo "HAS custom-title - stop"
   ```

3. Get the sessionId:

   ```bash
   sid=$(grep -o '"sessionId":"[^"]*"' "$file" | head -1 | cut -d'"' -f4)
   ```

4. Read the conversation. Take text-only turns from both speakers, drop slash-command
   records, and keep the last 40KB so a marathon session cannot blow your context:

   ```bash
   jq -r 'select(.type=="user" or .type=="assistant")
          | (if .type=="user" then "USER: " else "ASST: " end) as $p
          | .message.content
          | if type=="array" then (.[]|select(.type=="text")|.text) else . end
          | $p + .' "$file" 2>/dev/null \
   | grep -vE '^(USER|ASST): *$|local-command-(caveat|stdout)|<command-(name|message|args)>' \
   | tail -c 40000
   ```

   The USER turns say what was asked; the ASST turns say what the work turned out to be.
   Weight both, and weight the end of the conversation over the start.

5. Compose the title: concise, sentence-case, about 4-8 words, matching Claude Code's
   house style. Name the work, not the session ("Skill invocation modes and /ask", not
   "Discussion about skills"). If the caller passed a steer, follow it.

6. Append one well-formed record. Use `python3` so the title is JSON-escaped correctly;
   never hand-build the JSON, or a title containing a quote or colon produces a broken line:

   ```bash
   python3 - "$file" "$sid" "Your composed title here" <<'PY'
   import json, sys
   path, sid, title = sys.argv[1], sys.argv[2], sys.argv[3]
   rec = {"type": "ai-title", "aiTitle": title, "sessionId": sid}
   with open(path, "a") as f:
       f.write(json.dumps(rec, separators=(",", ":")) + "\n")
   PY
   ```

   Compact separators match Claude Code's own format and the no-space greps above.

7. Report `old -> new`. The change lands on Claude Code's next flush, a turn or two later,
   not instantly.
````

## Common mistakes

- **Composing the title yourself** instead of dispatching. The subagent is the skill.
- **Editing the existing title line** instead of appending -> ignored by Claude Code.
- **Finding the dir with `ls`/guessing** instead of deriving it from `$PWD` -> wrong session
  when many project dirs exist.
- **Writing `ai-title` while a `custom-title` exists** -> invisible. Do the mask check.
- **Hand-building the JSON** with a title containing quotes/colons -> malformed line.
