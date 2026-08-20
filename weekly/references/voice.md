# Voice and layout

Two separate things, do not conflate them:

- **Register** — how the sentences sound. Spanish, his voice. The gold standard below governs.
- **Layout** — how the file is structured. Markdown, spec below. The gold standard does *not*
  govern this; it was pasted as plain text and is not a layout reference.

---

# Layout — `~/Meli/weekly/YYYY-MM-DD.md`

This file is Alvaro's working artifact. It must be scannable in ten seconds. Use real
markdown; never emit a wall of unmarked lines.

```markdown
# Semana <start> → <end>

**Se movió:** `proj` · `proj`
**Quieto:** `proj` · `proj`

---

## <canonical-project-key>

**<Bloque temático>**            ← only when a project has 2+ distinct threads
- bullet
- bullet
- **Next:** <commitment>
- **Esperando:** <person/team> — <what and why it blocks>

---

## Sin updates

| Proyecto | |
|---|---|
| `proj` | <one-line reason, or "Sin updates"> |

---

## 🔒 Notas para mí — no van al post

**Chequeo de `Next:` de la semana pasada:** <each prior Next, and whether it happened>

**Para revisar:**
- <anything worth his attention: silent active projects, drifting objectives, overlong sections>
```

Rules:

- `## <project>` per project that moved, canonical key, backticks off in the heading.
- Bold thematic sub-labels only when a project genuinely has several threads. A project with
  three bullets does not need them.
- **`Next:` and `Esperando:` are structural markers, not prose.** Step 5 reads them directly
  to derive the Portfolio `Next` and `Blocked on` fields. Never bury a commitment inside a
  narrative bullet — if it is a commitment, it gets its own `**Next:**` bullet.
- Quiet projects go in the `Sin updates` table, never as empty `##` sections.
- The 🔒 section is always last and always separated by `---`. Nothing in it is team-facing.

## Posting to Slack

Slack does not render `##` headings or tables — they paste as literal characters. The file is
for him; the post is a separate render. When he asks to post, emit a plain-text version:
project name on its own line, blank line, bullets as bare lines, no markdown syntax. That is
what the gold standard below looks like, and that is why it looks like that.

---

# Register

Plain, neutral Latin American Spanish, first person, informal, for teammates who already know
the projects. No voseo, no Peninsular forms, no country-specific slang. Everything else in the
session stays in English — this is one of the requested-artifact exceptions.

Keep English business/tech/analytics terms wherever they are what people actually say —
forcing a translation reads worse than the loanword.

- Stay English: `eval harness`, `golden set`, `LLM`, `spot-check`, `shadow`, `dev pass`,
  `workflow`, `dashboard`, `landing page`, `tabs`, `stakeholders`, `buyers`, `flags`, `bugs`,
  `scanner`, `Next`, `peak`, `downstream`, `feed`, `fix`, `router`, `prompt`, `holdout`.
- Stay Spanish: `encuesta`, `cuotas`, `órdenes`, `ingesta`, `hallazgos`, `mesas locales`,
  `cobertura`, `escalar`, `mediana`.

## Outcome over activity

Write what is now true, not what you spent time on.

- Yes: "en la práctica Tier D equivale a la mediana del sitio, y nada más sofisticado mejora
  eso (restricción de datos, no de modelo)"
- No: "trabajé en el análisis de sensibilidad de Tier D"

Numbers earn their place: `~135k órdenes`, `250+ checks`, `200k buyers`, `wave 4`.

Social notes belong in the update and nowhere else — thanking people, crediting contributions.

## Gold standard — register only

Alvaro's own update from 2026-08. Match these *sentences*. Ignore its flat layout.

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


ghost-ads
Sin updates, aparte de ser utilizado como input en v2 de pads-incrementality.
```

What it does *not* do: no preamble, no "esta semana avancé en", no summary paragraph, no
padding to fill a section. Capitalization is inconsistent and that is fine — do not tidy it
into corporate prose.
