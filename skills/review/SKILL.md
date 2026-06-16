---
name: review
description: |
  Use when user asks for a deep, source-grounded audit of an
  academic document — diploma, master's thesis, doctoral thesis,
  or paper. Natural triggers: "/review", "audit this paper",
  "deep review of the thesis we just opened", "vamos a revisar la
  tesis de X", "audita este documento". Distinct from /revise
  (blog prose) and /code-review (PR diffs). Produces a narrative
  report (5–18 pages by level) plus a structured forensic assembly
  sibling, plus per-phase artifact files, all in the document's own
  language. Multi-phase pipeline with three parallel extractors, nine
  parallel evaluators, a synthesizer, and a final narrative redactor
  — total 14 subagents, single level of indirection.
---

# /review — deep academic document audit

Forensic audit of an academic document — thesis (diploma/master/PhD)
or paper. Produces two complementary deliverables sharing the same
slug:

- **`<slug>.md`** — narrative report (5–18 pages by level), written
  in formal academic prose for the document's author. This is what
  humans open.
- **`<slug>.forensic.md`** — structured forensic assembly (§0–§10
  with appendices), the substrate the narrative anchors to. Preserved
  alongside for cite-ability and audit-trail.

Both are descriptive and non-prescriptive: never "this is good" or
"this is bad", never "should fix X" — only "this claim is here, the
evidence cited is there, the field looks like this, this gap exists,
this baseline is missing". Severity is integrated in prose in the
narrative; left as forensic IDs in the forensic substrate.

## When to use

- Explicit invocation: `/review` (no arguments — resolves from context).
- Natural triggers (any language): "audit this paper", "let's review
  Raimel's thesis", "deep review of the paper we just opened",
  "audita la tesis que abrimos hace un rato", "vamos a revisar el
  paper de X".
- After a writing-finalisation session where the user wants a deep
  pre-defense, pre-submission, or opposition-prep pass.

## When NOT to use

- Blog prose review → that's `/revise`.
- PR / code review → that's `/code-review`.
- Quick structural sanity check → overkill; read the document yourself.
- Spell-check / proofreading → out of scope.

## Operating principles

1. **Descriptive, never prescriptive.** No "should", "consider",
   "recommend", "advise". Only "this exists, this is missing, this
   conflicts, this is supported". The reader interprets.
2. **Single source of truth per finding.** Each finding lives in one
   phase artifact file. The final report includes those files
   verbatim, never paraphrases.
3. **Multilingual by default.** Skill prompts and SKILL.md are in
   English. Findings, observations, free-text of artifacts and the
   final report are in the document's own language. Schema field
   names (frontmatter, metadata line keys) remain in English.
4. **Single level of indirection.** Subagents do NOT dispatch
   sub-subagents. Subagent parallelism is at the tool level
   (WebSearch / WebFetch / Read / Grep batched within one turn).
5. **Plan-first.** No fan-out before the user approves a contextual
   plan derived from the actual document.
6. **Phase = barrier.** Phase N+1 cannot start until all subagents
   of Phase N have returned (or been recorded as failed).
7. **Graceful degradation.** If a subagent fails, the pipeline
   continues. Evaluators that depended on it receive an empty
   artifact and note the missing input. The final report records
   what was skipped.

## Workflow overview

```
PHASE 0 — Recon + Plan          [main agent itself; no subagents]
  ├── resolve target document from context
  ├── extract text (pdftotext / pandoc / direct)
  ├── full read by main agent
  ├── detect language, level, repo
  ├── clone repo if URL detected
  ├── propose contextual plan
  └── user approves or modifies in natural language

PHASE 1 — Collection            [3 subagents in parallel]
  ├── E1  extractor-1-claims.md          → <slug>.e1-claims.md
  ├── E2  extractor-2-literature.md      → <slug>.e2-literature.md
  └── E3  extractor-3-artifacts.md       → <slug>.e3-artifacts.md

PHASE 2 — Evaluation            [9 subagents in parallel]
  ├── V1  evaluator-1-structure.md                  → <slug>.v1-structure.md
  ├── V2  evaluator-2-methodology.md                → <slug>.v2-methodology.md
  ├── V3  evaluator-3-results-evidence.md           → <slug>.v3-results-evidence.md
  ├── V4  evaluator-4-novelty.md                    → <slug>.v4-novelty.md
  ├── V5  evaluator-5-state-of-the-art.md           → <slug>.v5-state-of-the-art.md
  ├── V6  evaluator-6-reproducibility.md            → <slug>.v6-reproducibility.md
  ├── V7  evaluator-7-writing-ai-tics.md            → <slug>.v7-writing.md
  ├── V8  evaluator-8-bibliographic-integrity.md    → <slug>.v8-bibliography.md
  └── V9  evaluator-9-ethics-declarations.md        → <slug>.v9-ethics.md

PHASE 3 — Synthesis + redaction       [shell + 2 subagents]
  ├── cat v1..v9 → middle.md                            (mechanical, no LLM)
  ├── synthesizer.md reads middle.md once
  │   ├── writes §0 — Document summary
  │   └── writes §10 — Cross-dimension observations
  ├── cat header + §0 + middle.md + §10 + appendices
  │     → <slug>.forensic.md                            (structured forensic, sibling)
  └── redactor.md reads <slug>.forensic.md once
        → writes <slug>.md                              (narrative, the primary deliverable)
```

The `<slug>.md` produced by the redactor is the report the document's
author opens. The `<slug>.forensic.md` is preserved alongside as a
structured forensic substrate the redactor's claims anchor to.

## File layout

```
.claude/skills/review/
├── SKILL.md                                  ← this file (main agent prompt)
├── schema.md                                 ← finding schema reference
├── level-criteria.md                         ← level-calibration tables
├── extractor-1-claims.md
├── extractor-2-literature.md
├── extractor-3-artifacts.md
├── evaluator-1-structure.md
├── evaluator-2-methodology.md
├── evaluator-3-results-evidence.md
├── evaluator-4-novelty.md
├── evaluator-5-state-of-the-art.md
├── evaluator-6-reproducibility.md
├── evaluator-7-writing-ai-tics.md
├── evaluator-8-bibliographic-integrity.md
├── evaluator-9-ethics-declarations.md
├── synthesizer.md
└── redactor.md
```

Main agent (you) reads ONLY SKILL.md and the document. Every
subagent prompt is loaded from disk just-in-time and passed as
prompt to its subagent. They never enter the main agent's context.

## Phase 0 — Recon and Plan

### Step 0.1 — Resolve the target document

In order of precedence:

1. **Explicit path** the user mentioned in the conversation
   (Goal, current message, recent message). Use it.
2. **File the user is currently looking at** (visible in chat or
   recent `Read` calls).
3. **Latest PDF / .md / .qmd / .tex** in a folder the user
   mentioned (e.g., `~/Downloads`, `./papers/`).
4. If ambiguous: ask **one** question naming the candidates.

If no document resolves, exit with a clear message:

> No document resolved from context. Pass a path explicitly or open the document.

### Step 0.2 — Extract text

| Format | Tool |
|---|---|
| `.pdf` | `pdftotext -layout <path> <cache>.txt` |
| `.md` / `.qmd` | direct Read |
| `.tex` | `pandoc -f latex -t markdown <path> -o <cache>.md` |
| `.docx` | `pandoc -f docx -t markdown <path> -o <cache>.md` |

Cache the extracted text at:

```
.playground/audit-cache/<slug>/<slug>.text.md
```

`<slug>` is `<author-lastname>-<YYYY-MM-DD>` if author is detectable from
the document; otherwise `<filename-stem>-<YYYY-MM-DD>`.

If `.playground/` does not exist, create it. The cache is ephemeral
(gitignored); only the destination artifacts persist.

### Step 0.3 — Full read

Read the extracted text yourself. For documents > 60k tokens, read
in chunks but keep the full mental model. This is the budget you pay
for plan-first: it lets you write a plan grounded in real content
rather than placeholders.

### Step 0.4 — Detect metadata

- **Language.** Heuristic: presence of "Resumen", "Abstract",
  "Zusammenfassung", "Résumé", "概要"; characteristic stop words.
  If confidence is low, ask one question.
- **Level.** Cues: "Trabajo de Diploma" → diploma. "Tesis de
  Maestría" / "Master's Thesis" → master. "Tesis Doctoral" /
  "Doctoral Dissertation" / "PhD Thesis" → phd. "Submitted to
  <venue>" / IEEE / ACM templates / arXiv preprint format → paper.
  Page count gives weak signal (≤30 ≈ paper, 30–80 ≈ diploma/master,
  80+ ≈ phd). If ambiguous, ask.
- **Repo.** Search the text for URLs matching
  `(github|gitlab|bitbucket|codeberg)\.com/[\w-]+/[\w-]+`. The
  cover page of theses often carries it (e.g., printed at the bottom
  of the title page). If found, attempt `git clone --depth=20` into
  `.playground/audit-cache/<slug>/repo/`. Record clone status.
- **Author + title.** Extract from cover / first heading.

### Step 0.5 — Preliminary scan

While reading, jot mentally (or in scratch):

- 5–15 candidate load-bearing claims with section + verbatim quote
- 3–5 themes for E2 to investigate
- 1–3 hypotheses to falsify via literature search
- structural anomalies noticed at first pass (broken cross-refs,
  numbering inconsistencies, placeholder frontmatter)

These feed the plan.

### Step 0.6 — Resolve destination

In order of precedence:

1. **User explicitly named a path** in the conversation.
2. **`./reviews/`** if it exists, or create it under the current
   working directory.
3. **Document inside a git repo** → `<repo-root>/reviews/<slug>.md`
   (or `<repo-root>/docs/reviews/<slug>.md` if `docs/` exists).
4. **Isolated document on disk** → alongside the document:
   `<dirname(path)>/<slug>.md`.

Propose the path in the plan; user can change.

### Step 0.7 — Detect prior iteration

In the proposed destination, look for files matching `<slug>*.md`.
If found, read the most recent one's frontmatter. If
`audited_document` matches, this run is an iteration. Plan declares
it explicitly and proposes dimensions to re-run / inherit.

### Step 0.8 — Choose intensity preset

Default by level:

| Level | Default preset |
|---|---|
| diploma | Standard |
| master | Standard |
| phd | Deep |
| paper | Deep |

User can override in the plan.

### Step 0.9 — Generate plan

Write the plan as Markdown directly into chat (NOT to a file yet).
Structure (translate field names to the document's language; this
template is in Spanish — use English for English documents, etc.):

```markdown
# Audit plan — <document title>

## Documento detectado
- Path: <path>
- Idioma: <ISO> (confianza: high|medium|low)
- Nivel: <diploma|master|phd|paper> (confianza)
- Autor / Título: <…>
- Páginas: <N>
- Repo: <url> | none-detected | clone-failed
- Reporte propuesto: <path>

## Profundidad declarada
- Preset general: <Light|Standard|Deep>
- Subo X a Deep porque <razón> (si aplica)
- Subo Y a Light porque <razón> (si aplica)

## Iteración (solo si aplica)
- Basado en reporte previo: <ruta>
- Dimensiones a re-ejecutar: [V<i>, …]
- Dimensiones a heredar: [V<j>, …]

## Fase 1 — Recolección

### E1 — Claim inventory
- Estratificación: load-bearing, supporting, contextual
- 5 load-bearing identificados de la lectura:
  - C1: «<verbatim>» (§<sección>)
  - C2: «<verbatim>» (§<sección>)
  - …
- Esperable: ~<N> supporting, ~<M> contextual

### E2 — Literature map (preset <…>)
- Queries concretas a lanzar:
  - "<query 1>"
  - "<query 2>"
  - …
- Hipótesis a falsear vía búsqueda:
  - H1: <hipótesis específica derivada del documento>
  - H2: <…>

### E3 — Artifact inventory
- Repo: <auditar | skip — no repo>
- Datasets / benchmarks declarados a inventariar
- Tablas/figuras: ~<N> a indexar

## Fase 2 — Evaluación

### V1 — Estructura formal
Observaciones tempranas: <lista derivada de la lectura preliminar>

### V2 — Metodología
Puntos concretos a auditar: <derivados del documento>

### V3 — Resultados ↔ Evidencia
Foco: claims load-bearing C1…C5 contra Tablas <…> y Figuras <…>

### V4 — Novedad
Claims a verificar: <list de novelty claims con §sección>

### V5 — Estado del arte
Foco: <derivado de la bibliografía vista>

### V6 — Reproducibilidad
Foco: <derivado de E3 preliminar>

### V7 — Escritura + patrones de IA
Idioma: <…>; lentes aplicables: Winston, Pinker, Romero §13 (5 de 8 Don'ts en académico)

### V8 — Integridad bibliográfica
~<R> referencias a verificar; sospechas tempranas: <si las hay>

### V9 — Ética y declaraciones
Foco: <derivado de la lectura>

## Fase 3 — Síntesis
- Reporte único en: <ruta>
- Artefactos hermanos: <slug>.{plan,e1,e2,e3,v1,…,v9}.md
- Wall-clock estimado: ~<T> min

## Aprueba, modifica, o aborta.
```

### Step 0.10 — Apply user response

Parse user's response in their own language:

- Approval words ("ok", "sí", "adelante", "go", "yes") → proceed.
- Negation ("abort", "no") → exit cleanly without further action.
- Modification → parse natural language ("skip V4 y V9", "preset
  Deep en E2", "el reporte ponlo en X", "el nivel es master")
  and re-present the updated plan. Iterate until user approves.

### Step 0.11 — Persist plan

Once approved, write the plan to:

```
<destination_dir>/<slug>.plan.md
```

With frontmatter:

```yaml
---
type: audit-artifact
phase: plan
slug: <slug>
generated_at: <ISO>
audited_document: <path>
audited_document_title: <title>
language: <ISO>
level: <level>
preset: <preset>
destination: <destination_path>
previous_iterations: [<paths>]
---
```

## Phase 1 — Collection (parallel)

Dispatch **three subagents in parallel** in a single message
containing three Agent tool invocations.

For each, the prompt is the concatenation of:

1. The full content of the corresponding `extractor-<N>-*.md` file
   loaded from disk via Read.
2. A separator: `\n\n---\n\n## Inputs\n\n`.
3. The inputs the extractor declares it expects (see each file).
4. A final instruction line:
   `The document is in <language>. Write the artifact in <language>. Keep frontmatter keys, metadata line keys, and ID prefixes in English.`

The subagent writes its artifact to its declared output path
(`<destination>/<slug>.e<N>-<name>.md`) using Write. The subagent's
final response should be just `wrote <path>` for trace.

### Inputs to each extractor

- **E1 claims:** `audited_document_text` (the cached extracted
  text), `language`, the preliminary load-bearing claims identified
  in Phase 0 (as a hint, not a constraint).
- **E2 literature:** `audited_document_title`, `audited_document_abstract`,
  `novelty_claims_preliminary` (from Phase 0 scan), `queries_planned`
  (from approved plan), `hypotheses_planned` (from approved plan),
  `preset`, `bibliography_extracted` (refs section of the document
  as plain Markdown).
- **E3 artifacts:** `audited_document_text`, `repo_path` (if
  cloned) or `null`, list of declared datasets / benchmarks from
  the plan.

### Graceful failure

If a subagent returns an error or writes nothing within reasonable
time, log it. Phase 2 proceeds with the missing artifact treated as
empty. The final report's frontmatter records `phase1_failures: [E2]`.

## Phase 2 — Evaluation (parallel)

Dispatch **nine subagents in parallel** in a single message.

Same dispatch pattern as Phase 1.

### Inputs to each evaluator

Every evaluator receives:

- `audited_document_text`
- `language`
- `level`
- the relevant phase artifacts from Phase 1 (read from disk into the
  prompt body — DO NOT include them in your own context; pass paths
  and let the subagent Read them, OR include their content directly
  in the dispatched prompt body; either way the content does not
  enter your context as main agent).

Specifically:

| Evaluator | Reads also |
|---|---|
| V1 — structure | (document only) |
| V2 — methodology | `<slug>.e1-claims.md` (filtered to methodological claims), level-criteria sub-section |
| V3 — results-evidence | `<slug>.e1-claims.md` (full), `<slug>.e3-artifacts.md` (tables, figures) |
| V4 — novelty | `<slug>.e1-claims.md` (novelty claims only), `<slug>.e2-literature.md` (full) |
| V5 — state-of-the-art | `<slug>.e2-literature.md` (full), document bibliography |
| V6 — reproducibility | `<slug>.e3-artifacts.md` (full), level-criteria sub-section |
| V7 — writing + AI tics | (document only) |
| V8 — bibliographic integrity | document bibliography + WebSearch/WebFetch |
| V9 — ethics + declarations | (document only) + a hint about V7's expected output for cross-ref |

Each subagent writes its artifact to its declared output path.

### Graceful failure

Same as Phase 1. The synthesizer is told which evaluators failed and
mentions them in §10 as "did not complete; see logs".

## Phase 3 — Synthesis + redaction (shell + 2 subagents)

Phase 3 produces TWO deliverables sharing the same slug:

- `<destination_dir>/<slug>.forensic.md` — structured forensic
  assembly. The cat-everything: §0, §1–§9, §10, appendices. Sibling
  artifact. Cite-able, audit-trailable, dense.
- `<destination_dir>/<slug>.md` — **narrative report**, written by
  the redactor in formal academic prose, sized 5–18 pages by level.
  This is what humans open. Anchors to the forensic substrate but
  does not reproduce its IDs / severity tags / per-dimension shape.

### Step 3.1 — Assemble the middle (shell, no LLM)

Run a single Bash command that concatenates the V1–V9 artifact files
in order, stripping their YAML frontmatter, into a working file at
`.playground/audit-cache/<slug>/middle.md`.

Order:

1. `<slug>.v1-structure.md`
2. `<slug>.v2-methodology.md`
3. `<slug>.v3-results-evidence.md`
4. `<slug>.v4-novelty.md`
5. `<slug>.v5-state-of-the-art.md`
6. `<slug>.v6-reproducibility.md`
7. `<slug>.v7-writing.md`
8. `<slug>.v8-bibliography.md`
9. `<slug>.v9-ethics.md`

Frontmatter-stripping recipe (awk):

```sh
awk 'BEGIN{f=0} /^---$/{f++; next} f>=2{print}' <file>
```

Wrap each artifact in its `## §<i> — <section title>` header.

This is mechanical. No tokens.

### Step 3.2 — Synthesizer reads once, writes §0 and §10

Dispatch ONE subagent using `synthesizer.md`. Inputs to its prompt:

- the assembled `middle.md` (the only content it reads from the
  audit besides the original document)
- the plan (`<slug>.plan.md`, frontmatter included)
- the original document text (cached)

Synthesizer returns TWO Markdown blocks:

1. `<section-0>...</section-0>` — §0 Resumen del documento
2. `<section-10>...</section-10>` — §10 Observaciones transversales

Synthesizer does NOT write to disk. Returns text only. Main agent
extracts the two blocks.

### Step 3.3 — Assemble the forensic sibling (shell)

A second Bash command concatenates, in order, into
`<destination_dir>/<slug>.forensic.md`:

1. Forensic frontmatter (main agent writes inline, see below).
2. `# Audit forensic — <title>` H1.
3. The §0 block from the synthesizer.
4. `middle.md` (already prepared in Step 3.1).
5. The §10 block from the synthesizer.
6. `## Apéndice A — Plan ejecutado\n\n` + frontmatter-stripped
   `<slug>.plan.md`.
7. `## Apéndice B — Inventario de claims\n\n` + frontmatter-stripped
   `<slug>.e1-claims.md`.
8. `## Apéndice C — Mapa de literatura\n\n` + frontmatter-stripped
   `<slug>.e2-literature.md`.
9. `## Apéndice D — Inventario de artefactos\n\n` + frontmatter-stripped
   `<slug>.e3-artifacts.md`.
10. `## Apéndice E — Criterios por nivel aplicados\n\n` + the
    sub-sections of `level-criteria.md` that the level-calibrated
    evaluators consumed (V2, V4, V5, V6, V9 sections corresponding
    to the audited level).

This is the audit-trail substrate. The redactor reads it as input.

### Step 3.4 — Redactor writes the narrative (subagent)

Dispatch ONE subagent using `redactor.md`. Inputs to its prompt:

- `forensic_assembly_path` — `<destination_dir>/<slug>.forensic.md`
  (the file you just assembled in Step 3.3).
- `plan_path` — `<destination_dir>/<slug>.plan.md`.
- `audited_document_text_path` — cached extracted text of the
  document (for verbatim quote verification).
- `language`, `level` — from the plan frontmatter.
- `destination_path` — `<destination_dir>/<slug>.md`.
- `artifact_manifest` — structured list of every sibling artifact
  with relative paths and one-line descriptions. Build from the
  plan's `phase_artifacts` map plus the forensic file plus the prior
  iteration's report path (if any). The redactor uses this to
  populate the closing Anexo.

The redactor reads the forensic assembly ONCE, writes the narrative
to `<destination_path>` via Write, and returns
`wrote <destination_path> (N palabras)`.

Word-count band (verified by the redactor via `wc -w`):

| Level | Word count |
|---|---|
| `paper` | 1 800 – 3 500 |
| `diploma` | 2 500 – 5 000 |
| `master` | 4 000 – 7 000 |
| `phd` | 5 000 – 10 000 |

Main agent does NOT read the narrative back. The redactor is the
single source of truth for the narrative.

### Final report frontmatter

Prepend this frontmatter to `<slug>.md` (the narrative) after the
redactor writes its body. Same frontmatter goes on
`<slug>.forensic.md` with `type: audit-forensic` instead of
`audit-report`.

```yaml
---
type: audit-report
slug: <slug>
generated_at: <ISO>
audited_document: <path>
audited_document_title: <title>
language: <ISO>
level: <level>
preset: <preset>
phases_executed: [0, 1, 2, 3]
dimensions_run: [V1, …]
dimensions_skipped: []
phase1_failures: []
phase2_failures: []
phase_artifacts:
  plan: <slug>.plan.md
  e1: <slug>.e1-claims.md
  e2: <slug>.e2-literature.md
  e3: <slug>.e3-artifacts.md
  v1: <slug>.v1-structure.md
  v2: <slug>.v2-methodology.md
  v3: <slug>.v3-results-evidence.md
  v4: <slug>.v4-novelty.md
  v5: <slug>.v5-state-of-the-art.md
  v6: <slug>.v6-reproducibility.md
  v7: <slug>.v7-writing.md
  v8: <slug>.v8-bibliography.md
  v9: <slug>.v9-ethics.md
  forensic: <slug>.forensic.md
previous_iterations: []
---
```

### Step 3.5 — Final output line

Print one line summarising the run:

```
Wrote <destination_dir>/<slug>.md (narrative, N palabras).
Sibling forensic: <slug>.forensic.md. Phase artifacts: <N> files.
Phase failures: <list or 'none'>.
```

## Iteration

When Phase 0 detects a prior iteration:

- The plan declares dimensions to re-run vs inherit.
- Phase 1: re-run only the extractors needed by the re-run
  dimensions (E1 if any of V2/V3/V4 re-run; E2 if V4/V5 re-run;
  E3 if V6 re-run).
- Phase 2: only the declared dimensions run.
- Phase 3 assembly: for inherited dimensions, the §<i> in middle.md
  is a one-line stub:

  ```markdown
  ## §<i> — <name> (V<i>)

  *Inherited from previous iteration: `<path-to-prior-slug.v<i>-<name>.md>`*
  ```

  The §0 includes a paragraph from the synthesizer describing what
  changed since the prior iteration. The redactor, reading the
  forensic assembly, surfaces the inherited dimensions transparently
  in the narrative ("the structural observations of the prior
  iteration are preserved at `<prior-path>`") and integrates the
  new dimensions' findings as if they belonged to the same pass.

- The narrative's closing Anexo lists the prior iteration's report
  as the first artifact under "Audit seccional previo" (or
  language-equivalent heading).

- Frontmatter on both `<slug>.md` and `<slug>.forensic.md`:
  `previous_iterations: [<path-to-prior-report>]`.

## Schema and level-criteria

The shared finding schema (heading + prose body + metadata line) is
documented in `schema.md`. Each evaluator prompt embeds the schema by
reference; subagents that need it can Read `schema.md` themselves.

`level-criteria.md` holds the calibration tables consumed by V2, V4,
V5, V6, V9. Each level-calibrated evaluator prompt instructs the
subagent to Read the relevant sub-section and consult it when emitting
findings that anchor to a level-criterion.

## Hard rules summary

- Two deliverables, same slug, same destination: `<slug>.md`
  (narrative — the primary deliverable) and `<slug>.forensic.md`
  (structured forensic substrate). Sibling phase artifacts named
  `<slug>.<phase>.md`.
- Multilingual: skill prompts in English; artifacts, forensic
  assembly, and narrative in document language.
- Subagents NEVER dispatch subagents.
- Phase 0 reads the document. Phase 1–2 subagents may re-read
  cached text as needed via Read on the cache path.
- Synthesizer reads ONE assembled file once. Redactor reads ONE
  assembled file once. Main agent reads NO phase artifacts in
  Phase 3 — it just `cat`s them for the synthesizer and forensic
  assembly, and passes paths to the redactor.
- No prescriptive language in any artifact (forensic or narrative).
  No verdicts in §0. The narrative integrates severity in prose
  ("requires correction before printing" / "advisable improvement"
  / "descriptive observation") and never reproduces emoji tags,
  the words CLEAR/IMPORTANTE/MENOR, or forensic IDs (`F-V<n>-NNN`,
  `C<n>`) in its body.
- Cross-dimension observations are the synthesizer's job (in the
  forensic substrate); individual evaluators stay in their lane.
  The redactor reorganises by editorial section, not by dimension.

## Failure modes summary

| Failure | Response |
|---|---|
| No document resolvable from context | Exit with message; do not start. |
| PDF unreadable (e.g., scanned without OCR) | Exit; suggest OCR may be needed (without prescribing). |
| Repo URL detected but `git clone` fails | Record `clone_status: failed`; V6 will reflect; continue. |
| Phase 1 subagent fails | Phase 2 proceeds with empty input; report records. |
| Phase 2 subagent fails | Phase 3 stub for that §<i>; report records. |
| Synthesizer fails | Main agent assembles forensic file without §0 and §10; opens with `*Synthesis failed. Forensic assembled mechanically.*`. Redactor still runs against the partial assembly. |
| Redactor fails | Main agent leaves the forensic file as the only deliverable, prints `*Narrative redaction failed. Open <slug>.forensic.md directly.*` in the final output line. |
| Redactor produces out-of-band word count | Main agent treats the run as successful but prints a warning in the final output line; user may re-dispatch the redactor against the same forensic file. |
| Destination not writable | Ask user for alternative path. |
