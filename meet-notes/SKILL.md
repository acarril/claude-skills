---
name: meet-notes
description: >-
  Distill Google Meet / Gemini meeting notes into a structured knowledge document in
  the current project. Use when the user asks to get, distill, or save notes from a
  meeting, or asks what was discussed in one — even without saying "Meet" or
  "transcript".
---

# Meet Notes

Distill a Google Meet transcript into a structured knowledge document and save it to the current project.

Gemini's own summary loses the epistemic layer — who said what, with what confidence, and whether others agreed — so this skill distills the raw transcript instead.

## Step 1 — Resolve the target date

- Default: **today**
- Honor explicit hints: "yesterday", "last Tuesday", a specific date
- Convert to a full-day time window in the user's local timezone

## Step 2 — Fetch calendar events and show picker

Call `mcp__claude_ai_Google_Calendar__list_events` for the target date. Filter results to only meetings that have a `conferenceUrl` (Google Meet link) — those are the ones that can have Gemini notes.

**Time filtering:**
- If the target date is today: only include meetings whose `end` time is in the past (already happened)
- If yesterday or any other date: include all meetings from that day

**Picker:** Always present the filtered list and ask the user to pick, even if only one meeting matches. Float the most likely match to the top based on any topic hint in the user's message (e.g. if they said "elasticidad", float that meeting first). Show meeting title, time, and organizer for each option.

## Step 3 — Find the Gemini notes doc in Drive

Spawn a subagent to run the search. This avoids polluting the main context with Drive result content snippets — all the main agent needs back is a file ID and title.

Give the subagent:
- The selected meeting title (from Step 2)
- The target date

The subagent should run **two queries in parallel** — a combined `or` query with a limited page size will exhaust results on owned docs and bury shared ones (notes owned by the meeting organizer are only *shared* with you):

1. `title contains 'Notes by Gemini'`
2. `title contains 'Notas de Gemini'`

It should merge the results and collect **every** doc whose title starts with the meeting title. A single meeting often produces several Gemini docs — an English "Notes by Gemini", a language variant, a standalone **Transcript** doc — and the first one found frequently has an **empty** transcript tab while the real transcript lives in a doc it links to. For a recurring meeting, order candidates so the one whose embedded date matches the target date comes first.

> `sharedWithMeTime` is NOT a valid Drive API query field — do not use it.

The subagent returns: a list of candidates `[{file_id, title}, ...]`, date-matched first, or a not-found signal. Step 5 reads them in order and follows their internal links if needed.

**If no doc is found:** tell the user and stop. Transcription is opt-in per meeting and notes may take a few minutes to appear after the call ends.

## Step 4 — Check for an existing output file

Output path: `notes/YYYY-MM-DD_<meeting-title-slug>.md` under the project root

- Slug: lowercase meeting title, spaces replaced with hyphens, special characters stripped
- Example: `notes/2026-05-12_elasticidad-en-pricing-seller-optimizacion.md`

If a file already exists at that path: tell the user and stop. Do not overwrite silently.

If the `notes/` directory doesn't exist: create it and tell the user.

## Step 5 — Distill and write via subagent

Spawn a subagent for everything involving the transcript — reading, checking, distilling, and writing. The main agent never touches the transcript text.

Give the subagent:
- The candidate list (from Step 3)
- The output file path (from Step 4)
- The attendee list (names + emails from the calendar event)
- The meeting title and date

The subagent should:

1. **Read the candidates in order** using `mcp__claude_ai_Google_Drive__read_file_content`, starting with the first. The document has two sections: a Gemini-generated summary ("Resumen" / "Summary") — ignore this — and a verbatim transcript with speaker labels and timestamps — use only this.

   - **If the transcript is empty or only filler** (greetings, "Transcription ended after 00:0X", or a summary saying it couldn't be produced): do NOT give up. The doc has a **"Meeting records"** section linking to a standalone **Transcript** doc and/or language-variant **"Notes by Gemini (…)"** docs. Extract those links, resolve each to a Drive file ID (the ID is the `/document/d/<ID>/` segment of the URL), and read them — plus the remaining candidates from the list — until you find one with a real transcript. Only after exhausting all of them, return a not-found signal to the main agent, which warns the user that the doc exists but has no transcript (transcription may have been disabled) and stops.
   - **If a doc is too large** to return in one call (`read_file_content` errors and saves the content to a local file): read that saved file in sequential chunks until you have 100% of the transcript before distilling.

2. **Distill** the transcript into the output file. What to capture:
   - Deduplicate within the conversation: if something is mentioned three times, write it once
   - Preserve epistemic metadata: who said it, how confidently, and what the room's reaction was
   - Distinguish facts from hypotheses from open questions
   - Capture dissent explicitly: if person A proposed X and person B was skeptical, write it that way
   - Do NOT attempt to diff against prior notes in the project — redundancy is fine and useful
   - Ignore: scheduling logistics, technical difficulties, filler
   - **Correct known mistranscriptions** of team vocabulary (see glossary below) before writing

3. **Write the file** at the output path using the structure in Step 6.

4. **Return** to the main agent: the file path written and a 2-3 sentence summary of the main decisions/outcomes.

### Mistranscription glossary

Gemini reliably mangles Mercado Libre / analytics jargon. Apply these corrections during distillation (match case-insensitively, respect word boundaries so you don't touch substrings like "GMV" inside other tokens):

| Heard as | Correct term |
|---|---|
| `BC` | `VC` (variable contribution) |
| `GNB` | `GMV` (gross merchandise value; sometimes used interchangeably with NMV) |
| `Bayern P` / `Bayern Panel` | `Buyer Panel` |

This list is not exhaustive — if a token is obviously a phonetic garble of a known term from the project context (e.g. sub-combo names, `PSJ`, `PCJ`, `FVF`, `lambda`), fix it and note nothing. When genuinely unsure whether something is a mistranscription, leave it verbatim.

**Language of the output file:** match the language of the transcript (neutral Latin American Spanish for Spanish meetings — no voseo, no lunfardo, no Argentinian register unless directly quoting a participant).

## Step 6 — Write the output file

Use this exact structure:

```markdown
---
meeting: <meeting title>
date: <YYYY-MM-DD>
attendees:
  - name: <display name>
    email: <email>
  - ...
---

# <meeting title> — <date>

## Decisiones

- <Decision>. [<who proposed it> / <level of agreement: unánime, mayoría, con reservas de X>]

## Hipótesis y afirmaciones

- <Claim or hypothesis>. [<who said it>, <confidence: con confianza / con reservas / como hipótesis> / <reaction: X estuvo de acuerdo / Y fue escéptico>]

## Preguntas abiertas

- <Open question> [no resuelta / pendiente para próxima reunión]

## Próximos pasos

- [ ] **<Assignee>**: <action item>

## Contexto y antecedentes

<Freeform narrative of important framing, background, constraints, or evidence established during the call. This is the richest section — capture anything that would help a future agent understand the project state after reading this document.>
```

Omit any section that has no content. The "Contexto y antecedentes" section is the most important — don't shortchange it.

## Step 7 — Confirm to the user

After writing:
1. Print the file path clearly
2. Print a short preview: the Decisiones and Próximos pasos sections only (not the full document)

Nothing else — no offers, no follow-up questions.

## Tools required

- `mcp__claude_ai_Google_Calendar__list_events`
- `mcp__claude_ai_Google_Drive__search_files`
- `mcp__claude_ai_Google_Drive__read_file_content`
