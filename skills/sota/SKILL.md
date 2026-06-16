---
name: sota
description: |
  Use when the user wants a structured state-of-the-art review of a
  topic, built from a corpus of already-pulled sources and/or wiki
  pages. Natural triggers: "/sota", "haz un estado del arte sobre X",
  "build a SOTA on X from my sources", "do a SOTA review on X", "tengo
  N papers sobre X, organízame el estado del arte". Distinct from
  /audit-paper (audits an existing document) and /ingest (compiles
  sources into wiki). The output is a single Markdown report
  organised BY DIMENSIONS (paradigms, techniques, domains, evaluation
  methods, etc.) — never chronological. Plan-first: the agent
  proposes dimensions from the corpus and the user approves before
  fan-out. Multi-phase pipeline with one dimension per synthesizer
  subagent (4–7 in parallel) plus a final assembler.
---

# /sota — structured state-of-the-art review

Produces a single Markdown report that synthesises a topic across a
corpus of sources by organising them along **user-relevant
dimensions** (paradigms, techniques, evaluation methods, domains,
theoretical frameworks…) — never as a chronological list of papers.

The skill is the natural complement to `/ingest` (which compiles
sources into a wiki) and to `/audit-paper` (which audits a written
document). `/sota` sits between: it takes the wiki + sources and
produces the SOTA chapter / section that the author can then drop
into their thesis, paper, or design document.

## When to use

- Explicit invocation: `/sota <topic>` or `/sota` (resolves from
  context).
- Natural triggers (any language): "haz un estado del arte sobre
  razonamiento neurosimbólico", "build a SOTA on retrieval-augmented
  generation from my pulled papers", "organize a state-of-the-art
  review of LLM-driven AutoML using everything in my wiki", "tengo
  treinta papers sobre meta-learning, organízame el estado del arte".

## When NOT to use

- The user wants to compile sources into a wiki → that's `/ingest`.
- The user wants to audit a thesis or paper → that's `/audit-paper`.
- The user wants atomic claims extracted from a source → that's
  `/distill`.
- The user wants a chronological "history of the field" — the
  output of `/sota` is explicitly dimensional, not chronological;
  if they want chronological, say so and stop.
- The corpus is empty or fewer than 3 sources — refuse; ask the
  user to `/pull-source` more first.

## Operating principles

1. **Plan-first.** Never fan out before the user approves the
   dimensions. The dimensions are the spine of the report; getting
   them wrong wastes the rest of the pipeline.
2. **By dimensions, never chronological.** The output organises
   approaches along axes of variation the user cares about, not by
   publication date.
3. **Inline citations are mandatory.** Every factual claim is
   anchored to a specific source by `[Author Year]` (or numbered
   `[N]`). The closing References section deduplicates and lists in
   full.
4. **Descriptive, never prescriptive.** No "this approach is the
   best", no "we recommend". Only "approach X proposes …", "approach
   Y differs in …", "the dimension splits the field into …".
5. **Single level of indirection.** Subagents do not dispatch
   sub-subagents. Synthesizer parallelism is at the dimension level.
6. **Phase = barrier.** Phase 2 cannot start until all synthesizers
   have returned.
7. **Graceful degradation.** If a synthesizer fails, the assembler
   inserts a stub for that dimension and the final report records
   the failure in its frontmatter.

## Workflow overview

```
PHASE 0 — Recon + Plan          [main agent itself; no subagents]
  ├── resolve topic from args / context
  ├── resolve corpus directory (defaults ./wiki/ + ./sources/)
  ├── grep + filter corpus by topic
  ├── read frontmatter + first paragraphs of filtered pages
  ├── identify 4–7 candidate dimensions
  ├── propose contextual plan (dimensions + contributing sources)
  └── user approves or modifies in natural language

PHASE 1 — Synthesis             [4–7 subagents in parallel]
  └── one synthesizer.md per dimension
        → .sota-cache/<topic-slug>/dimension-<i>-<slug>.md

PHASE 2 — Assembly              [1 subagent]
  └── assembler.md reads all dimension sections + plan
        ├── writes intro framing topic + dimensions
        ├── writes cross-cutting matrix (approaches × dimensions)
        └── writes deduplicated bibliography
            → returns text blocks; main agent assembles final file

FINAL — Main agent concatenates header + intro + dimensions + matrix
        + bibliography → <output-dir>/sota-<topic-slug>-<date>.md
```

## File layout

```
.claude/skills/sota/
├── SKILL.md                       ← this file (main agent prompt)
├── synthesizer.md                 ← per-dimension synthesizer subagent
├── assembler.md                   ← intro + matrix + bibliography + citation_map
└── tools/
    └── convert-citations.py       ← Phase 3 mechanical substitution
```

Main agent reads ONLY SKILL.md and the corpus. Subagent prompts are
loaded from disk just-in-time and passed as prompt. The vendored
script runs via Bash; main agent never reads its body.

## Phase 0 — Recon and Plan

### Step 0.1 — Resolve the topic

In order of precedence:

1. **Explicit topic** the user passed as `$ARGUMENTS` or in the
   invoking message.
2. **Topic the user just discussed** in recent turns.
3. If ambiguous, ask one question naming candidates.

If no topic resolves, exit with:

> No topic resolved. Pass one explicitly: `/sota <topic>`.

### Step 0.2 — Resolve the corpus directory

Defaults, in order:

1. **User-specified path** in args or recent message ("everything
   in `papers/`", "use the wiki at `./wiki/`").
2. **`./wiki/` + `./sources/`** if both exist relative to cwd.
3. **`./wiki/`** alone if it exists.
4. **`./sources/`** alone if it exists.
5. **`./`** as the corpus root (recursive scan), if nothing more
   structured is present.

### Step 0.3 — Filter corpus by topic

Grep within the resolved directory for the topic terms (and obvious
variants — singular/plural, English/Spanish, hyphenated/spaced
forms). For broader topics, also scan frontmatter `tags:` and
`title:` fields.

Read the frontmatter + first ~30 lines of every filtered page.
This is the budget you pay for plan-first: it lets you propose
dimensions grounded in real content.

If filtered corpus < 3 sources, STOP and report:

> Only N sources found on `<topic>`. SOTA requires at least 3.
> Suggestion: `/pull-source` more material on `<topic>` first.

If filtered corpus > 50 sources, ask the user to narrow.

### Step 0.4 — Identify candidate dimensions

The dimensions are **the spine of the report**. Look for recurring
axes of variation in the filtered content. Typical dimensions for
academic SOTA:

| Dimension class | Example |
|---|---|
| **Paradigm / approach family** | "neural-then-symbolic vs. symbolic-with-neural-modules vs. jointly trained" |
| **Technique / mechanism** | "retrieval-augmented vs. fine-tuned vs. in-context" |
| **Domain of application** | "theorem proving vs. AutoML vs. code generation" |
| **Component structure** | "deterministic validator vs. probabilistic grammar vs. learned critic" |
| **Learning regime** | "RL/self-play vs. evolutionary vs. supervised distillation" |
| **Evaluation method** | "formal verification vs. benchmark accuracy vs. expert comparison" |
| **Theoretical framework** | "grounding vs. compositionality vs. hybrid representation" |
| **Scale of integration** | "tightly coupled vs. loosely coupled vs. agentic pipeline" |

Aim for 4 to 7 dimensions. Fewer than 4 collapses the report into
a glorified summary; more than 7 fragments it. Each dimension must
have at least 2 contributing sources from the corpus (otherwise it
is too narrow to organise around).

### Step 0.5 — Propose the plan

Write the plan as Markdown directly in chat (NOT to a file yet).
Structure in the document's language (or the user's interaction
language if the corpus is bilingual):

```markdown
# Plan SOTA — <topic>

## Corpus detectado
- N páginas filtradas en `<corpus-dir>`:
  - `path/to/page1.md` — `<frontmatter title or H1>`
  - `path/to/page2.md` — …
  …

## Dimensiones propuestas

### D1 — <Dimension name>
**Eje**: <one-line definition of the axis of variation>
**Fuentes contributivas**: `[[page1]]`, `[[page2]]`, `[[page3]]`
**Por qué esta dimensión**: <one-line justification grounded in
the corpus content you read>

### D2 — <Dimension name>
…

## Estructura del reporte
- Introducción (~250 palabras): framing del topic + dimensiones elegidas + alcance del corpus
- Una §sección por dimensión (~400–700 palabras cada una)
- Matriz comparativa final (enfoques × dimensiones)
- Bibliografía con todas las fuentes citadas

## Destino del reporte
`<output-dir>/sota-<topic-slug>-<YYYY-MM-DD>.md`

## Aprueba, modifica, o aborta.
```

The user's modifications can be in natural language: "agrega
dimensión sobre eficiencia computacional", "quita D4, esa es una
sub-dimensión de D2", "cambia el destino a X", "dime las
contributing sources de D3 antes de aprobar".

### Step 0.6 — Output destination

Resolution order:

1. **User-specified path** in the conversation.
2. **`./sota/`** if it exists, or create it under the current
   working directory.
3. **Fallback**: alongside the corpus dir: `<corpus-parent>/sota/`.

Slug: `<topic-kebab>-<YYYY-MM-DD>`.

### Step 0.7 — Persist the plan

After approval, write to:

```
<output-dir>/sota-<topic-slug>-<date>.plan.md
```

With frontmatter:

```yaml
---
type: sota-artifact
phase: plan
slug: <slug>
generated_at: <ISO>
topic: <topic>
language: <ISO>
corpus_dir: <dir>
corpus_pages: [<paths>]
dimensions:
  - id: D1
    name: <name>
    axis: <definition>
    sources: [<paths>]
  - id: D2
    …
output_destination: <path>
---
```

## Phase 1 — Synthesis (parallel)

Dispatch **one subagent per approved dimension** in a single message
containing K Agent tool invocations (K = number of dimensions).

For each, the prompt is the concatenation of:

1. The full content of `synthesizer.md` loaded from disk via Read.
2. A separator: `\n\n---\n\n## Inputs\n\n`.
3. The dimension's `id`, `name`, `axis`, and contributing source
   paths.
4. The topic + language + word target per section (~400–700 words).
5. The citation style: `[Author Year]` with paths normalised so the
   assembler can deduplicate.

The synthesizer writes its output to:

```
.sota-cache/<slug>/dimension-D<i>-<slug>.md
```

The subagent's final response: `wrote <path>`.

### Graceful failure

If a synthesizer fails or returns nothing, log it. Phase 2 proceeds
with the missing section. The final report's frontmatter records
`phase1_failures: [D3]`.

## Phase 2 — Assembly

Dispatch ONE subagent using `assembler.md`. Inputs:

- the assembled dimension files (paths)
- the approved plan (`<slug>.plan.md`)
- the language and topic

The assembler returns FOUR Markdown blocks:

1. `<intro>...</intro>` — introductory section (~250 words).
2. `<matrix>...</matrix>` — cross-cutting matrix table.
3. `<references>...</references>` — deduplicated bibliography with
   `### N {#ref-N}` anchors (Pandoc/Quarto format), sorted
   alphabetically by first author. Each entry includes URL/DOI as
   a Markdown link where available.
4. `<citation_map>...</citation_map>` — a tab-separated table that
   maps each plain-text `[Author Year]` form used by the
   synthesizers to its reference number. Used by the main agent
   for the citation-conversion step.

The assembler does NOT write to disk. Main agent extracts the four
blocks and proceeds to the citation conversion step.

### Graceful failure

If the assembler fails, main agent assembles the report without
intro / matrix / references and inserts a placeholder line:
*Assembly step failed; intro, matrix and references not generated.*

## Phase 3 — Citation conversion (shell, no LLM)

The synthesizers wrote plain `[Author Year]` inline; the assembler
returned the canonical numbered bibliography plus a `citation_map`
block. The main agent now does a mechanical pass using the
vendored script `tools/convert-citations.py`.

### Step 3.1 — Persist the citation map as a TSV

Write the content of the assembler's `<citation_map>` block to:

```
.sota-cache/<slug>/citation-map.tsv
```

The block content is already in tab-separated form (see
`assembler.md`). No transformation required beyond extracting it
from the assembler's response.

### Step 3.2 — Run the conversion script

```bash
python3 .claude/skills/sota/tools/convert-citations.py \
    --cache-dir .sota-cache/<slug>/ \
    --citation-map .sota-cache/<slug>/citation-map.tsv
```

The script:

- Loads the citation map.
- Walks every `dimension-D*.md` file in the cache dir.
- Replaces every `[Author Year]` (single or composite `[A; B; C]`)
  with `^[N](#ref-N)^` Pandoc superscript-link form, joining
  composites with `, `.
- Leaves Markdown links of the form `[text](url)` untouched.
- Reports unmapped citations to stderr; exit code is non-zero
  when any remain.

Add `--dry-run` to preview without writing.

### Step 3.3 — Handle unmapped citations

If the script reports unmapped forms (`[Foo 2099]` etc.), choose:

- **Append to the citation map and re-run**: extend
  `citation-map.tsv` with the missing form pointing to an existing
  or new reference number, append the new reference entry to the
  references block, re-run the script.
- **Accept as plain text**: leave the unmapped `[Author Year]` in
  the final report. The reader can still parse it; only the
  superscript link is missing.

After this step, every dimension file contains Pandoc-renderable
citations and the references section has `{#ref-N}` anchors. The
final report becomes self-contained and Quarto-renderable.

## Phase 4 — Final assembly (shell)

Main agent concatenates, in order, into
`<output-dir>/sota-<topic-slug>-<date>.md`:

1. Final frontmatter (see below).
2. `# Estado del arte — <topic>` H1 (or language-appropriate).
3. `## Introducción` + intro block from the assembler.
4. For each dimension, in plan order:
   - `## <i>. <Dimension name>` H2 (numbered)
   - body of `dimension-D<i>-<slug>.md` (frontmatter-stripped,
     post-citation-conversion). The dimension file already
     contains its `### <Pole>` and `### Resumen` H3 subheadings.
5. `## Matriz comparativa` + matrix block from the assembler.
6. `## Notas y Referencias` + references block from the assembler
   (each entry already carries its `### N {#ref-N}` anchor).

### Final report frontmatter

```yaml
---
type: sota-report
slug: <slug>
generated_at: <ISO>
topic: <topic>
language: <ISO>
corpus_dir: <dir>
corpus_pages_n: <N>
dimensions:
  - D1: <name>
  - D2: <name>
  …
phases_executed: [0, 1, 2]
phase1_failures: []
phase2_failures: false
output_destination: <path>
---
```

### Final output line

Print one line summarising the run:

```
Wrote <output-dir>/sota-<topic-slug>-<date>.md (N palabras).
Dimensions: D1=<name>, D2=<name>, … (K total).
Phase failures: <list or 'none'>.
```

## Hard rules summary

- Plan-first. No fan-out before user approves dimensions.
- By dimensions, never chronological.
- Inline citations mandatory in every dimension section.
- Sub-agents NEVER dispatch sub-sub-agents.
- No prescriptive language. No "this is the best".
- Phase 1 = barrier before Phase 2 starts.
- One report. Sibling artifacts: `<slug>.plan.md` and the
  `.sota-cache/<slug>/` directory (which can be deleted after the
  report is written if disk pressure matters).

## Failure modes

| Failure | Response |
|---|---|
| No topic resolved | Exit with message; do not start. |
| Corpus has < 3 sources on topic | Exit; suggest `/pull-source` first. |
| Corpus has > 50 sources | Ask the user to narrow scope. |
| User refuses to approve a plan after 3 modifications | Stop; report the disagreement. |
| Synthesizer fails for a dimension | Report missing; Phase 2 inserts stub. |
| Assembler fails | Main agent assembles without intro/matrix/references; final line records the failure. |
| Output destination not writable | Ask user for alternative path. |
