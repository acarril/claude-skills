# People — identity: use Slack, not guesswork

Read for the monthly People pass only; the weekly scan does not use this file.

The MELI Slack connector resolves a name to a **verified** email, username and Slack user ID:
`slack_search_users` with a full name, or `slack_read_user_profile` with a known ID.

`Title` is self-set and **roughly 40% filled** — real when present ("Strategic Planning Senior
Manager", "Insights & Analytics (Meli+)", "Buy box - Structured Data - IT"), blank otherwise.
Blank means unset, never junior.

Rules learned 2026-08-20, after an agent had guessed org weight for 21 of 27 people and those
guesses ended up ordering the board Alvaro was meant to judge from:

- **Never infer seniority or influence from team membership, mention frequency, or tone.** If
  Slack has no title and no note states a rank, say so in the field. Blank is information;
  a guess wearing a confident label is not.
- **There is no `Org weight` field** — dropped 2026-08-20, along with `Seniority`. The schema
  is `Team` (business unit) + `Title` (rank as Slack states it, verbatim). The reason is worth
  keeping: Team and Title are **re-derivable** — one Slack lookup re-verifies them — whereas a
  judgement like "how much their opinion would carry" is unverifiable once written, and a wrong
  value is indistinguishable from a right one. Do not reintroduce a scored influence field.
  Whether someone's word counts in a committee is a call Alvaro makes at packet-writing time,
  against the org chart as it is then.
- `Relationship` is the **only** judgement field, and it is his alone. It is not re-derivable,
  which is exactly why it belongs in the database rather than being inferred.
- Record where each fact came from, in the field itself ("Slack, verificado <date>" vs "de tus
  notas"). A fact whose provenance is not visible gets treated as verified.
- Names in notes are frequently distorled by Gemini transcription. Three of 27 did not resolve
  in Slack at all; they are flagged in-row rather than silently kept.
- Watch for two people sharing a name — Nicolás Repetto matched two accounts. Flag, do not pick.

### Gmail is the better source, and answers a different question

Check which account is connected first — personal `alvarocarril@gmail.com` or work
`alvaro.carrilrubio@mercadolibre.cl`. One `newer_than:7d` search tells you.

On the work account, Gmail beats Slack twice over:

- **It finds people Slack cannot.** Silvestre Serantes and Pedro Hardoy have no Slack profile
  but real mailboxes. It also caught a misspelling that had defeated every other lookup: the
  notes say "Pedro Ardoy", the person is **Hardoy**.
- **Distribution lists reveal hierarchy, which no title does.** Nacho's quarterly stakeholder
  update (2026-07-30) went to ~41 people including Ariel Szarfsztejn, David Geisen, Karen
  Bruck, Juan Lavista and Silvestre Serantes. Being *on that list* is documented evidence of
  seniority — far stronger than inferring from team membership. Record it as evidence in the
  row's notes; there is no scored seniority field.

### Rank and hierarchy: query `meliorg`, do not reconstruct by hand

```bash
S=~/.claude/skills/meliorg/scripts/meliorg.py
python3 $S find "Ignacio Campos"   # name or LDAP -> full record
python3 $S chain <ldap>            # up the reporting line to the root
python3 $S reports <ldap>          # direct reports
```

The `meliorg` skill owns the full source-precedence rule and the off-VPN staleness handling —
read it rather than restating it here. Off-VPN the command serves cached data and says so;
surface that, never present it as current. Watch the 60-req/min limit: `find` is one request,
`chain` about six.

**Slack titles are wrong often enough to be unusable for rank.** Measured on 2026-08-20:
Peirano read a rung low, Diogo Pena read "Advertising Product Manager" when he is a Product
Advertising *Expert*, and **both** homonyms of Nicolás Repetto had stale titles. Several VPs
have no Slack profile at all.

Names also collide — Repetto and Rodrigo Palma each returned two people. `find` matches on
name or LDAP only, never department or title, so show the candidates and let Alvaro pick.
Carry the **LDAP username** forward; it is the only stable key.

Direct-report **counts** come free with `reports`. Org **size** (Serantes' 123) does not — the
API has no such field and a full crawl is infeasible, so treat any org-size figure as hearsay
unless Alvaro supplies it. The figures currently in the Notion People rows came from org-chart
screenshots he shared, which is a legitimate source; `meliorg` cannot reproduce them.

Consequences worth remembering: **Peirano is the skip-level**, so his requests are not
stakeholder nice-to-haves. Janaína Silveira and Luis Vergari report to Peirano too, making
them peers of Alvaro's boss. Juanpi Sitler reports to Silvestre. Natalia Quigua is a **Sr
Manager with her own team**, not a working-level counterpart. Tharles Conegundes sits under
Tech & Ops (NPS Commerce), not Commerce Planning — a dependency, not a teammate.

So: org chart for rank and hierarchy, Slack for verified email/ID, Gmail for existence,
spelling, and standing. None of them licenses a guess about people who appear in none.

### A name that fails both is a spelling problem, not a missing person

All three unresolved names on 2026-08-20 turned out to be Gemini transcription artifacts, and
Alvaro knew each correct spelling immediately:

| Notes said | Actually |
|---|---|
| Pedro Ardoy | Pedro **H**ardoy |
| Nico Asendorf | Nicolas A**sch**endorf |
| Maru Cristiani | Maria Eugenia Cristiani |

So when a name resolves in neither system: try phonetic variants (silent leading H, sch/s,
double consonants, a nickname standing in for a full first name), then **ask him**. Do not
write a ⚠️ "not found" into the row and move on — that records a defect in the notes as if it
were a fact about the person.
