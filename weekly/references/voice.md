# Audience, format, register

> **Language contract.** Everything below the "Register" heading describes Spanish *that goes
> into the post*. Nothing here licenses Spanish anywhere else. You talk to Alvaro in English —
> including every picker stem, every rationale, and the whole 🔒 half of the `.md`. This file is
> the densest Spanish in the skill and therefore the likeliest place to drift; re-read
> `SKILL.md`'s language contract if you feel the pull.

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

Length norms on this team vary, but the target is now measured, not felt. On 2026-09-07 Nacho
said his post was too verbose; measured against the two posts beside it that morning:

| | bullets | words | median words/bullet | longest | numbers/bullet |
|---|---|---|---|---|---|
| **his post** | 14 | 626 | 38 | 118 | 3.7 |
| **Daniel** | 14 | 288 | 17 | 53 | 0.1 |
| **Kevin** | 13 | 287 | 23 | 43 | 0.7 |

**Target: Kevin's shape.** ~300 words, 12–15 bullets, median ~20 words per bullet, hard cap 40,
at most one number per bullet. He carries more projects than anyone else on the team, so his
length comes from project *count*; per-bullet depth is what has to give.

How the others read, for register:

| | |
|---|---|
| **Daniel** | headline per initiative, one or two lines of status under it, `(igual a semana pasada)` where nothing moved. Prose fragments, no numbers. |
| **Kevin** | `[SHP]`-style domain tags, one or two sentences per bullet, `Sin avances última semana`, `Pending:`, `ETA IT Miércoles 9`. One number when there is one. |
| **Joao** | terse, `[done]` / `[Next]` / `[Later]` status tags, nested bullets. Very scannable. |
| **Cleyton** | 3–4× everyone else, into KKT multipliers and adjoint gradients. **The anti-pattern** — and the one the long-bullet draft drifts toward. |

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
- `*Next:*` and `*Esperando:*` are structural markers — step 8 reads them straight into the
  Portfolio `Next` and `Blocked on` fields. A commitment gets its own marker rather than being
  buried in narrative.
- Single asterisks. `**Next:**` renders the asterisks literally.
- Links as `<https://…|label>`, hung on the artifact's name.
- Backticks on every identifier: column and table names (`VERTICAL_EST`, `PP_CHANNEL`), task
  and image names (`publish`), paths (`.github/workflows`), skills (`/bids:repo`), flags and
  parameters. Slack renders them as code; an unmarked identifier reads as a typo. Job ids and
  issue numbers stay plain (`job 483878`, `#56`). Project headers stay `*bold*`, never code —
  there is no underline in Slack markup, so bold is the whole heading style.
- `*Sin updates:*` is one line naming the projects, never a table.
- Status tags are part of the format: `Sin avances`, `igual a semana pasada`, `Pending: …`,
  `ETA …`. A track that did not move keeps its label and gets a tag, not a sentence.

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

## Worked example — the 2026-09-07 post, re-cut to the target

What he posted that morning ran 626 words over 14 bullets (median 38 words, longest 118), and
Nacho said it was too verbose. The same content at the target, 15 bullets, ~330 words, median
22, longest 37. Every number and mechanism that came out of a bullet moved to the 🔒 talking
points; nothing was lost, only relocated. **Match this shape.**

```
*buyer-panel*

• *Falla de dependencias FDA*: una dependencia con CVE sunset mató todo el pipeline en silencio; arreglado el mismo día. Ya tenemos cómo verlas venir (vista de BQ, FYI al equipo).
• Quedó la maquinaria para versionar generaciones de `VERTICAL_EST` (registry, lineage, cutover y rollback). Nada publicado cambió todavía.
• *v3 del clasificador*: estudio pre-registrado en curso; lidera la cascada k-NN → sonnet (84,6% vs 77% k-NN solo). Decisión ~19/09.
• AmazonNow entra como retailer propio; feed que pedimos nosotros, volumen mínimo.
• *Next:* decidir el labeler de v3 (~19/09)

*price-perception*

• *Panel piloto*: vale la pena. El CSAT previo de la misma persona predice bien y sigue sirviendo seis meses; un panel de 50k baja el MDE a la mitad sin quemar usuarios.
• *Cupones A/B*: wave 3 encuestada el 01/09; le mandé a Giovanna el número de la ronda 1 (+2,3pp, underpowered). *Next:* lectura ~08/09.
• *Cupones relámpago*: cerré la wave 5 para Camila Paiva: n.s., no replica la wave 4. Cinco waves de ruido; cierra el caso de la discontinuación.
• *Astro*: Search respondió el diseño (A/A′/B/B′, sticky por usuario, sin fecha de scale-up). Lectura retrospectiva −1,5pp, n.s., signo contra la historia de ASP. La audiencia se diseña después de leer la wave 3.

*pads-incrementality*

• El refresh mensual bajó los scores ~28%. No es un bug, es el anchor de entrenamiento; republicamos como está y pasamos a anchors pooled antes del 01/10.
• Benchmark zero-shot de TimesFM-3 sobre el forecast de dominios de Ads (#56): la mitad del error del fallback plano y mejor que el modelo actual. Sirve como vara, no para prod (licencia).
• Tratamiento binario (tener/no tener PAds): exploré un diseño con dosis e instrumentos de presupuesto. Solo diseño.

*ivy-pix-pricing*

• Brasil quiere separar el uplift de Ivy del descuento Pix para la inversión 2027. Con la data en mano, el DiD no se sostiene: el control está tratado (Pix y un tercer programa, Aurora). Hay que rediseñar.

*pricing-combopremium*

• Nano empezó una iniciativa (con Dani) para llevar las elasticidades PSJ/PCJ a un reporting diario de pricing.

*fury_bids (repo del equipo)*

• Melisource bloqueó los cambios a `.github/workflows`; las Actions custom (crear/cerrar/revivir proyecto) se reemplazan por un skill `/bids:repo` (PR #87).

*Sin updates:* fvf-elasticity · melimas-inc · ghost-ads
```

---

# Format — the file

`~/Meli/weekly/YYYY-MM-DD.md` is the byproduct: the posted text verbatim, then the 🔒 half.
It is his working artifact and the source step 8 derives from, so it holds everything the post
holds plus what the team never sees.

```markdown
# Week <start> → <end>

<sub>Window anchored to the previous report's mtime, not its filename date. Posted in <thread>.</sub>

<the post, verbatim — the only Spanish in this file>

---

## 🔒 Private notes — not for the post

**Last cycle's `Next:` check:** <each prior Next, and whether it happened>

**Overdue commitments:** <stale `- [ ]` from dated notes, older than ~3 weeks>

**Unverified ops:** <anything a downed tool or MCP server left unchecked>

**Cut this cycle:** <one line per bullet he cut, with the reason — a record, not a re-offer>

**Worth a look:** <projects that ran long, silent active projects>
```

The scaffolding — title, `<sub>` line, 🔒 headings — is **English**. Only the pasted post is
Spanish, plus any Spanish quoted inside an English note (`his `Next:` said "pasarle a Leo mis
notas"`).

The 🔒 section is always last. Nothing in it is team-facing.
