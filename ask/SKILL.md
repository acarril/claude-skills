---
name: ask
description: Re-ask the last message's dangling decisions as multiple-choice pickers.
disable-model-invocation: true
---

# ask

Your last message left decisions hanging in prose. Convert them into `AskUserQuestion`
pickers and ask them properly.

The user fires this because the message failed, not because they want something new.
**Ask only what that message already implied.** Do not invent questions it didn't raise,
and do not re-open decisions it already settled.

## 1. Re-read your last message

Go through it and mark every point where you handed the user a decision without a picker.
The failure modes, in rough order of how often they show up:

| Tell | Example |
|---|---|
| **Parked state** | "Feature X is waiting on your approval." |
| **Conditional offer** | "Once you've tested Y, say the word and I'll open the PR." |
| **Soft offer** | "Let me know if you want me to also handle Z." |
| **Implied action** | "This CSV should probably be gitignored." |
| **Hedged completion** | "Done, though you may want to revisit the threshold." |
| **Buried alternative** | An option you named but didn't pursue, with no ask attached. |
| **Prose question** | A literal question mark outside a picker. |

If nothing is marked, say so in one line and stop. Don't manufacture a question to
justify the invocation.

## 2. Ask them, one picker call at a time

Order by dependency: the decision that unblocks the others goes first. Then, per decision:

- **Recommended option FIRST**, labeled `(Recommended)`. You already have an opinion —
  the prose version leaked it. State it.
- 2-4 options that are **genuinely distinct branches**, not shades of one answer.
  If you can only think of one real branch, it wasn't a decision — act on it instead.
- No "Other" option; the picker supplies it, and it carries any free text.
- A decision with no proposable candidates at all (naming something from scratch) is the
  one case for prose — and even then, offer a default.

Nothing that was a decision in the original message may survive as prose. Facts, results,
and context stay as prose; that part of the message was fine.

## 3. Act on the answers

Once answered, do the work. Don't summarize the answers back first.
