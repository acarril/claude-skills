# Audience, format, register

Three separate things, kept separate:

- **Audience** — who reads it and what they do with it. Governs what survives step 3's test.
- **Format** — Slack markup for the post; markdown for the file. The post spec governs.
- **Register** — how the sentences sound. Spanish, his voice. The gold standard governs.

---

# Audience — dual, and both halves are real

The post goes in the thread under the `Weekly EA` bot's Monday prompt in `#commerce-bids-ea`
(`C068QV1QALA`). Readers: **Nacho** (his leader) and the four other E&A ICs — Kevin Traynor,
Joao Reboucas, Cleyton de Farias, Daniel Labarca.

**Nacho** needs what happened and the next step per project, phrased so he can lift a claim
upward without asking a follow-up. His quarterly update goes to Peirano and the CEO.

**The team** needs findings, blockers and results socialized. The post is the **agenda for
Monday's meeting**, where the lists are read and discussed — so a bullet's second job is to
earn a question.

Reactions and replies in Slack are near zero and that is not a signal of failure: the
engagement happens in the meeting, not in the thread.

## Calibration

Length norms on this team vary wildly, so there is no house style to conform to. His target
sits **between Daniel and Kevin**:

| | |
|---|---|
| **Daniel** | two projects, ~2 bullets each, prose sentences, no `Next`. Too concise. |
| **Kevin** | ~14 bullets over 5 sections, `[SHP]`-style domain tags, explicit `Pending:` and ETAs. |
| **Joao** | terse, `[done]` / `[Next]` / `[Later]` status tags, nested bullets. Very scannable. |
| **Cleyton** | 3–4× everyone else, into KKT multipliers and adjoint gradients. **The anti-pattern.** |

He carries more projects than anyone else on the team, so his length comes from project
*count*, not depth per project. That is why the cap is per track and the test is bottom-up.

---

# Format — the post

Slack renders `*bold*`, `_italic_`, `` `code` ``, `•` bullets and `<url|label>` links. It does
**not** render `##` headings or markdown tables — those paste as literal `#` and `|`
characters, which is exactly what happened on 2026-08-24.

```
*project-name*

• bullet
• *Track label*: bullet. *Next:* commitment
• *Esperando:* <person> desde <date>

*Sin updates:* proj · proj
```

- Project name on its own line in `*bold*`, blank line, then bullets.
- `*Next:*` and `*Esperando:*` are structural markers — step 6 reads them straight into the
  Portfolio `Next` and `Blocked on` fields. A commitment gets its own marker rather than being
  buried in narrative.
- Single asterisks. `**Next:**` renders the asterisks literally.
- Links as `<https://…|label>`, hung on the artifact's name.
- `*Sin updates:*` is one line naming the projects, never a table.

Write for the **eye**: this is scanned on screen during the meeting, so structure carries more
than cadence.

---

# Register

Plain, neutral Latin American Spanish, first person, informal, for teammates who already know
the projects. No voseo, no Peninsular forms, no country-specific slang. Everything else in the
session stays in English — this is one of the requested-artifact exceptions.

Keep English business/tech/analytics terms wherever they are what people actually say; forcing
a translation reads worse than the loanword.

- Stay English: `eval harness`, `golden set`, `LLM`, `spot-check`, `shadow`, `dev pass`,
  `workflow`, `dashboard`, `landing page`, `tabs`, `stakeholders`, `buyers`, `flags`, `bugs`,
  `scanner`, `Next`, `peak`, `downstream`, `feed`, `fix`, `router`, `prompt`, `holdout`,
  `stand by`, `at risk`.
- Stay Spanish: `encuesta`, `cuotas`, `órdenes`, `ingesta`, `hallazgos`, `mesas locales`,
  `cobertura`, `escalar`, `mediana`.

Social notes belong in the post and nowhere else — thanking people, crediting contributions.

## Gold standard — register only

His own update from 2026-08. Match these *sentences*.

```
buyer-panel

Nueva señal para análisis: método de pago normalizado + cuotas, ventana de promesa de entrega, y feed suplementario de delivery de Amazon
En preparación a mayor escrutinio de la predicción de verticales, construí un eval harness para el clasificador de verticales (golden set + juez LLM + spot-check humano ciego): ahora podemos medir precisión y calibración antes y después de cualquier cambio al clasificador
agradecido por sus aportes en la Clasificadora!

Flags y bugs: el scanner de calidad ya corre diario, tiene 250+ checks. Corregí ~135k órdenes de Amazon con emails traspuestos (fix durable en ingesta) + desambiguación de precios/totales en cero (cero real vs dato faltante)


fvf-elasticity

Análisis de sensibilidad "qué tan malas son las estimaciones Tier D?" con validación out-of-sample
en la práctica Tier D equivale a la mediana del sitio, y nada más sofisticado mejora eso (restricción de datos, no de modelo)
Next: pensar en cómo comunicar esto
```

No preamble, no "esta semana avancé en", no summary paragraph, no padding. Capitalization is
inconsistent and that is fine — leave it rather than tidying it into corporate prose.

---

# Format — the file

`~/Meli/weekly/YYYY-MM-DD.md` is the byproduct: the posted text verbatim, then the 🔒 half.
It is his working artifact and the source step 6 derives from, so it holds everything the post
holds plus what the team never sees.

```markdown
# Semana <start> → <end>

<sub>Ventana anclada al mtime del reporte anterior. Posteado en <thread>.</sub>

<the post, verbatim>

---

## 🔒 Notas para mí — no van al post

**Chequeo de `Next:` de la semana pasada:** <each prior Next, and whether it happened>

**Compromisos vencidos:** <stale `- [ ]` from dated notes, older than ~3 weeks>

**Para revisar:** <projects that ran long, silent active projects, what was cut>
```

The 🔒 section is always last. Nothing in it is team-facing.
