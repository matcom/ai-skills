# Finding schema — shared reference

Every evaluator (V1–V9) and the synthesizer (for cross-dimension §10
observations) emits findings using this single schema. The schema
itself is in Markdown — no JSON, no fixed enums for categorisation.

## Anatomy of a finding

```markdown
### F-V<N>-<NNN> — <descriptive one-line title>

<one to three paragraphs of prose. cite verbatim from the document
when relevant — wrap quotes in « » or "" depending on document language.
anchor each claim with §section / lines N–M / Table X / Figure Y / paper
reference [N] / repo file `src/foo.py:42`. external evidence (papers,
tables, repo files) is cited inline in the prose, not as a separate
section.>

— polarity: positive|negative|neutral · confidence: high|medium|low · related: [[#C001]], [[#F-V2-003]] · criteria: V2.statistical_tests.diploma
```

## Field-by-field

### Heading

`### F-V<N>-<NNN> — <title>`

- `V<N>`: evaluator number (1–9). Synthesizer's cross-dimension
  findings use `V10`.
- `<NNN>`: zero-padded three-digit counter, per-evaluator. Reset
  to 001 in each evaluator's artifact.
- `<title>`: a sentence (≤90 chars) that names the observation
  descriptively. The title carries the categorisation — there is no
  separate `Category` field. Examples:
  - `F-V1-001 — Numeración de capítulos inconsistente entre TOC, §0.5 y cierre del Cap 1`
  - `F-V3-001 — "B nunca empeora A" — comparación pareada sin test estadístico`
  - `F-V5-007 — Cluster "in-context learning" — 12 papers ≥100 citas en 2024–25, ninguno citado`
  - `F-V6-004 — README presente con 0 líneas`
  - `F-V8-002 — Entrada [42] sin autor; arXiv ID 2511.20333 sospechoso`

### Body — prose

One to three paragraphs. Reads like a forensic note. Standards:

- Quote the document verbatim where helpful. Use «» for Spanish/French/
  Russian-style; "" for English; 「」 for Japanese; conventions of the
  document's language.
- Anchor every claim:
  - In-document: `§<section>`, `lines <N>–<M>`, `Table <X>`, `Figure <Y>`.
  - External (papers): inline as `[<ref-number>]` (as the document
    cites it) plus `(arXiv:XXXX.YYYYY)` or `(DOI: ...)` when the
    finding turns on the external paper's actual content.
  - Repo: `` `<repo-relative-path>:<line>` `` or `` `<file>` `` for
    whole-file references.
- No prescriptive language. Banned verbs / phrases (any language):
  *should, must, ought, consider, recommend, suggest, advise,
  convendría, debería, sugiero, recomiendo, propongo, hace falta,
  conviene, valdría, se podría*. Replace with descriptive
  reformulation: instead of "should add a Wilcoxon test", write
  "no paired statistical test (Wilcoxon, sign test, t-test) is
  reported".
- Positive findings (polarity: positive) describe what the document
  does well, using the same forensic register. Examples:
  - `F-V2-005 — Diseño experimental incremental aísla el efecto de cada componente`
  - `F-V5-012 — Cobertura del cluster "AutoML clásico" — 14 papers fundacionales citados de los 16 más influyentes`
- Cite `criteria-ref` in the prose when it anchors the finding:
  "El criterio `V2.statistical_tests` para `level=diploma` se lee:
  'Recomendable para comparaciones pareadas, no requerido'."

### Metadata line

A single line at the end, fields separated by ` · `, lowercase keys
with `: ` separator. Required keys:

- `polarity`: `positive`, `negative`, or `neutral`.
  - `positive` — the observation recognises something well-executed.
  - `negative` — the observation identifies a gap, omission,
    inconsistency, overclaim, or failure.
  - `neutral` — descriptive observation without valence.
- `confidence`: `high`, `medium`, or `low`. This describes the
  subagent's certainty about its OWN observation, not the urgency
  or importance of the finding. A negative finding with
  `confidence: low` is "the subagent saw a possible gap but could
  not fully verify" — not "minor issue".
- `related`: comma-separated list of cross-references using the
  `[[#<ID>]]` Obsidian-style syntax. IDs can be `C<NNN>` (claim
  from E1), `P<NNN>` (paper from E2), `F-V<N>-<NNN>` (another
  finding). Empty if no cross-refs.
- `criteria`: optional. When the finding applies a level-calibrated
  criterion from `level-criteria.md`, cite the path:
  `V2.statistical_tests.diploma`. Omit the field if no criterion was
  consulted.

## Worked example — V3 finding

```markdown
### F-V3-001 — "B nunca empeora A" — comparación pareada sin test estadístico

El claim «En ningún caso la configuración B empeora los resultados de A» aparece en §4.4.2, líneas 2344–2346. La Tabla 4.5 lo sostiene por comparación puntual: best-B ≥ best-A para los 8 datasets de la muestra reducida. No se reporta un test estadístico pareado (Wilcoxon signed-rank, sign test, t-test sobre diferencias) en el documento ni en el código del repo. El criterio `V2.statistical_tests` para `level=diploma` en `level-criteria.md` se lee: «Recomendable para comparaciones pareadas, no requerido». El claim usa el adverbio "significativamente" en el Resumen (líneas 67–68) sin anclar a un test.

— polarity: neutral · confidence: high · related: [[#C002]], [[#F-V2-003]] · criteria: V2.statistical_tests.diploma
```

## Worked example — V7 finding

```markdown
### F-V7-004 — Densidad alta de patrones consistentes con generación LLM en §1.2

§1.2 (Meta-Learning para AutoML, líneas 816–940) presenta 14 oraciones consecutivas con estructura «<sustantivo metaconcepto>… permite/aporta/proporciona <serie de tres>», sin variación rítmica y sin primera persona. Las triadas tipo «proporciona razonamiento verificable, control estructurado y conocimiento de dominio explícito» (líneas 567–568) caen bajo Romero §13 Don't 3 (cola larga en el tercer ítem). Frases-plantilla en líneas 521, 547, 565, 589 abren con «sin embargo» seguido de un metaconcepto. Comparable a §0.5 (Metodología, líneas 402–489) que el documento declara como "redactado con asistencia de Deepseek" en §0.5 (líneas 492–506); §1.2 no aparece en la declaración.

— polarity: negative · confidence: medium · related: [[#F-V9-002]]
```

## Worked example — V5 positive finding

```markdown
### F-V5-012 — Cobertura del cluster "AutoML clásico" — 14 papers fundacionales citados

El cluster temático "AutoML clásico" (Auto-Sklearn, Auto-WEKA, TPOT, hyperparameter optimization) contiene 16 papers identificados como fundacionales por el literature map (citation count > 500, año < 2020, cited-in-cluster > 8 times). La bibliografía cita 14 de los 16: [6, 7, 8, 33, 47, 48, 50, 53, 57, 58, 59, 60, 61, 65]. Los dos no citados ([P022] Komer 2014 "Hyperopt-Sklearn", 240 citas; [P031] Mendoza 2016 "Towards Auto-Keras", 198 citas) cumplen umbral mínimo de relevancia pero ya quedan representados por entradas vecinas del mismo grupo.

— polarity: positive · confidence: high · related: [[#P022]], [[#P031]]
```

## What MUST NOT appear in a finding

- "should", "must", "ought to", "consider", "recommend", "suggest",
  "advise", "convendría", "debería", "se podría", "valdría",
  "hace falta", "conviene", or any equivalent in any language.
- A verdict ("this thesis is weak", "the methodology is poor").
- An action item ("add a Wilcoxon test", "cite Brown 2020").
- A summary score or grade.

## What MAY appear in a finding

- Verbatim quotes from the document.
- Verbatim quotes from external sources (papers, repos).
- Specific anchors (line ranges, table numbers).
- Comparisons with level-criteria.
- Cross-references to other findings via `[[#<ID>]]`.
- Counts, percentages, distributions ("12 of 16", "5 occurrences in
  §1.2", "0 lines in README").
