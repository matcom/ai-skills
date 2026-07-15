---
name: design-doc
description: |
  Use when a repo, project, or area has accumulated several design/spec/plan
  docs and needs ONE coherent, top-down design document that synthesizes them
  and routes a reader to the right spec for depth. Create or update after a
  release or major implementation cycle, when onboarding needs a current
  architectural view, or when it is unclear which spec is current versus
  superseded. Trigger phrases: "update the design doc", "sync the design doc",
  "design-doc", "compile the design", "give me a top-down view of the design".
---

# design-doc

Compile ONE coherent, top-down design document for the current scope. It is the
single view a reader consults to understand the *complete design as it stands
today* — modules, the general design decisions, how the pieces interact, the
data model, the invariants — and to find *where* each part is specified in
depth.

## Core principle

**The design doc is a coherent top-down synthesis, not a history.** The record
of how the system got here — each feature, each point-in-time decision, in
chronological order — lives in the individual spec/plan docs. The design doc is
the opposite: a timeless, coherent whole that **supersedes and reorganizes**
those specs into one design, and **cites the specific spec** at each point where
a reader needs the depth behind that piece of the design.

Reading order is **design coherence, never chronology.** You organize by how the
design fits together (system → modules → interactions → decisions → data →
invariants), and citations appear at the point of relevance in *that* order — not
in the order the specs were written.

Specs are inputs; the design doc is the output. Update it after implementation is
stable (post code-review, at a release/version boundary), so it describes what
IS, not what is merely intended.

## Design doc vs. the specs it indexes

| The specs/plans | This design doc |
|---|---|
| Per-feature, point-in-time | Whole-system, current |
| Chronological (dated slices) | Coherent (top-down) |
| Some are superseded / partial | Cites only the authoritative one |
| The depth | The map that routes to the depth |

## What belongs

- **Overview** — what the system is and does. One or two paragraphs.
- **Architecture** — the modules/components, their responsibilities, and **how
  they interact**. Layered/ASCII diagrams when useful. Describe structure, not stack.
- **Design decisions** — the general choices that shaped the design, and why
  ("stateless handlers because Y"), stated as settled facts about the current
  design — not as a story of what changed.
- **Component interfaces** — the semantic contracts between components (what
  passes, what is promised), conceptual not syntactic.
- **Data model** — key entities, relationships, and their meaning.
- **Invariants** — what must be true for the design to hold ("every X has a Y").
- **Design → Spec index** — a routing table from each area of the design to its
  authoritative spec(s). In design order, NOT chronological. See below.
- **Out of scope** — what the system explicitly does not do.

**Inline spec citations are a required element, not a nicety.** Every subsection
whose depth is backed by a spec cites it *at the point of relevance* — see
Citation convention.

## What does NOT belong

- **Chronological narrative or changelog.** No "originally X, later changed to
  Y", no "in v1 we…", no dated sequence. That history is the specs' job.
- **Per-spec summaries in spec order.** You synthesize across specs; you do not
  walk them one by one.
- **Superseded decisions presented as current.** Resolve supersession first (below).
- Library names/versions (unless the library IS the architecture).
- Build/deploy config; internal implementation detail; roadmap/future items.

## Resolve the spec corpus and its supersession (before writing)

Design specs pile up and overlap: a later spec often supersedes or partially
revises an earlier one. **You must resolve this before writing**, for one
purpose only: so each subsection cites the **authoritative** spec for that area
and never routes a reader to a stale one. Supersession is a dedup filter on
citations — it is NOT a section, and the doc never narrates it as history.

For each spec, classify: **current** (authoritative for its area), **partial**
(current for part, superseded for the rest), **superseded-by-X**, or
**historical** (context only, never cited as current). When a later spec
consolidates earlier ones, cite the later one; you may note "(consolidates X, Y)"
once, in the index — not as a timeline.

## Scope detection

- **Repo** (inside `repos/<name>/`): doc at `docs/design.md`. Check also root
  `design.md` and `docs/architecture.md`; consolidate if multiple exist.
- **Sub-system inside a repo** (a large app under `apps/<name>/` with its own
  spec pile): its own `apps/<name>/docs/design.md`.
- **Umbrella project**: `vault/Efforts/Projects/<name>/design.md`, context from
  member repos.
- **Area**: `vault/Efforts/Areas/<area>/design.md`.

### Multi-system split

If the scope is really **N systems with distinct lifecycles, dependencies, and
invariants** sharing one repo (e.g. an offline toolkit + a live web app), do not
force one flat doc. Give the repo-level doc a thin "what each part is + index"
role and point to a dedicated `docs/design.md` per sub-system. Detect this during
discovery (below) and decide before dispatching the writer. When genuinely
ambiguous, ask.

## Procedure

### 1. Locate existing doc + inventory the spec corpus

```bash
find . -name "design.md" -o -name "architecture.md" 2>/dev/null
ls docs/ apps/*/docs/ 2>/dev/null          # where do the spec piles live?
git log --oneline -- docs/design.md 2>/dev/null | head -5
```

List every spec/plan under the scope (their dates are only a supersession hint,
not the doc's order).

### 2. Deep architecture discovery (subagent — fan out for large systems)

Dispatch a read-only discovery subagent (Explore or general-purpose). For a large
or multi-system scope, **fan out one subagent per subsystem** and merge. Do NOT
skim yourself and skip this — the discovery is what makes the doc coherent rather
than a spec-by-spec paraphrase.

Give each discovery subagent this contract — it returns a structured brief, it
does NOT write the doc:

> Explore <SCOPE/subsystem> and return a structured brief:
> 1. **Module map** — the real components from the code, each one's
>    responsibility, and **how they interact** (call/data flow). Anchor every
>    claim in a file you read.
> 2. **General design decisions** — the settled choices visible in the code and
>    specs, each with its rationale. Present tense, as facts about the design.
> 3. **Data model & invariants** — key entities/relationships; what must hold.
> 4. **Spec → design-area map** — for each spec/plan doc, which area of the design
>    it specifies, and its supersession status (current / partial / superseded-by
>    / historical), judged against what the code actually does now.
> 5. **Multi-system signal** — is this one coherent system, or N systems sharing a
>    repo? Say which, with the evidence.
> Read the code and the specs; distill, do not transcribe. Return the brief only.

### 3. Decide scope shape

From the discovery brief, confirm single-doc vs. multi-system split and the
output path(s).

### 4. Dispatch the writing subagent

Spawn a fresh writer with the merged discovery brief and this contract:

> You are writing (or updating) the design doc for <SCOPE_NAME> at <OUTPUT_PATH>.
>
> <CURRENT_DESIGN_DOC> … or "(none — creating from scratch)" </CURRENT_DESIGN_DOC>
> <DISCOVERY_BRIEF> … module map, decisions, data/invariants, spec map … </DISCOVERY_BRIEF>
>
> Write a coherent, **top-down** design doc. Organize by how the design fits
> together (system → modules → interactions → decisions → data → invariants),
> NOT by chronology and NOT spec-by-spec.
>
> **Required structure:**
> - Frontmatter: `date_updated`, `scope`, `generated_by: design-doc skill`.
> - Sections: Overview, Architecture, Design Decisions, Component Interfaces,
>   Data Model, Invariants, Design → Spec index, Out of Scope. Omit one only if
>   genuinely empty.
> - **Inline spec citation is REQUIRED**: in every subsection whose depth is
>   backed by a spec, cite the authoritative spec at the point of relevance, as
>   `(detail: [<spec-name>](<relative-path>))`. Cite the current spec only; never
>   a superseded one.
> - **Design → Spec index**: a table mapping each area of the design to its
>   authoritative spec(s), in the SAME top-down order as the doc. A routing table,
>   not a timeline. You may note "(consolidates X)" once here.
>
> **Forbidden:** chronological narrative, changelog, "originally/later/v1"
> phrasing, walking specs one by one, citing a superseded spec as current, library
> names in the architecture (unless the library IS the architecture), roadmap.
>
> Use ASCII diagrams for architecture/interactions when they help. Describe what
> IS, present tense. End with: "Written: <word count> words, <N> sections."

### 5. Review and commit

Skim for: chronological/historical phrasing, spec-by-spec ordering, superseded
specs cited as current, missing inline citations, scope violations (library
names, future tense). Then:

```bash
git add <output paths>
git commit -m "docs(design): <compile|update> design doc — <brief reason>"
```

Report: scope, path(s), created or updated, word count, and any multi-system
split you made.

## Citation convention

- **Inline, at the point of relevance:** `(detail: [solver-por-bloque](../docs/2026-07-13-solver-por-bloque-design.md))`.
- Cite the **authoritative** spec only. If an area's spec was superseded, cite the
  superseding one.
- Order follows the **design**, never the specs' dates.
- The **Design → Spec index** collects the routing in one place, in design order.

## Red flags — STOP

- Writing "originally", "was later changed", "in v1", or any dated sequence → that
  is history; it belongs in the specs, not here.
- Ordering sections or citations by when specs were written.
- Summarizing each spec in turn instead of synthesizing across them.
- Citing a spec you know is superseded as if it were current.
- Skipping the discovery subagent and paraphrasing the specs directly.

## Invocation from design-thinking

When invoked from the design-thinking test phase (post code-review, at a release
boundary), run automatically; focus discovery on the delta from the cycle just
completed, but still produce a coherent whole (not a delta log).

## Idempotency

Running this twice produces a better or equivalent doc, never worse. The writer
sees the existing doc as input and brings it to current state; if it is already
coherent and accurate, the output is nearly identical.
