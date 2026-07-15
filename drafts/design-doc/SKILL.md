---
name: design-doc
description: |
  Create or update the authoritative design document for a repo, umbrella
  project, or vault area. Idempotent — creates from scratch if missing,
  updates and improves if it exists. Invoke after a release or major
  implementation cycle, or when onboarding needs a current architectural view.
  Trigger phrases: "update the design doc", "sync the design doc", "design-doc",
  "update architecture doc", "compile the design".
---

# design-doc

Compile the authoritative design document for the current scope. The design
doc is the living truth of what the system IS — not what was planned, not
what was once intended, but what exists and must be true today.

## Core principle

Specs and plans are inputs to development. The design doc is the output.
It is updated AFTER implementation is stable (post code-review, at
release/version boundary), never before. This keeps it accurate rather
than aspirational.

## What belongs in a design doc

- **Overview**: what this system is and what it does. One paragraph.
- **Architecture**: components, their responsibilities, how they communicate.
  Layered diagrams when useful. No library names — describe structure, not stack.
- **Invariants**: what must be true for the system to work as described.
  "Every X must have a Y" — architectural contracts, not implementation details.
- **Component interfaces**: public contracts between components. Conceptual
  (what passes between them, the semantic contract), not syntactic.
- **Data model**: key entities and their relationships, semantic meaning.
- **Design decisions**: explicit choices that shaped the architecture, and why.
  Not "we used X library" — "we chose stateless handlers because Y."
- **Out of scope**: what this system explicitly does NOT do or handle.

## What does NOT belong

- Library names and versions (unless the library IS the architecture)
- Build/deploy configuration
- Implementation details (how the code achieves something internally)
- Historical decisions later reversed
- Future roadmap items
- Spec/plan artifacts — those live in docs/superpowers/

## Scope detection

**Repo scope** — working inside repos/<name>/:
- Design doc at docs/design.md within the repo
- Also check design.md at root and docs/architecture.md; consolidate if multiple exist

**Umbrella project scope** — explicitly requested or repo is part of named project:
- Design doc at vault/Efforts/Projects/<name>/design.md
- Gather context from all member repos

**Area/vault scope** — requested for a vault area:
- Design doc at vault/Efforts/Areas/<area>/design.md

When ambiguous, ask Alex before proceeding.

## Procedure

### 1. Determine scope and locate existing doc

```bash
find docs -name "design.md" -o -name "architecture.md" 2>/dev/null
ls design.md 2>/dev/null
git log --oneline -- docs/design.md 2>/dev/null | head -5
```

### 2. Gather context (read yourself, distill into brief)

1. Existing design doc (full, if present)
2. AGENTS.md — repo orientation and structure
3. know-how/*.md — operational knowledge
4. Key structural source files (infer from AGENTS.md)
5. Last 3–5 specs/plans from docs/superpowers/ — for recent deltas, not to copy

```bash
git log --oneline -30
```

### 3. Dispatch synthesis subagent

Spawn a fresh writing subagent with the context brief and this prompt:

---
You are updating (or creating) the design document for <SCOPE_NAME>.

<CURRENT_DESIGN_DOC>
[existing doc content, or "(none — creating from scratch)"]
</CURRENT_DESIGN_DOC>

<CONTEXT_BRIEF>
[your synthesized summary of AGENTS.md, know-how, recent changes, architecture]
</CONTEXT_BRIEF>

Write the design document to <OUTPUT_PATH>.

Rules:
- Describe what EXISTS and is true now. Not planned, not intended.
- Update outdated sections, preserve accurate ones, fill gaps.
- Do NOT include: library names/versions, build config, implementation details,
  reversed decisions, roadmap items.
- Use ASCII diagrams for architecture when helpful.
- Frontmatter: date_updated, scope, generated_by: design-doc skill
- Sections: Overview, Architecture, Invariants, Component Interfaces,
  Data Model, Design Decisions, Out of Scope. Omit if genuinely empty.
- End with: "Written: <word count> words, <N> sections."
---

### 4. Review and commit

Skim for scope violations (library names in architecture, future tense, planning language).

```bash
git add docs/design.md
git commit -m "docs(design): update design doc — <brief reason>"
```

Report to Alex: scope, file path, created or updated, word count.

## Invocation from design-thinking

When invoked from the design-thinking test phase (post code-review, at release
boundary), run automatically. Focus context brief on the delta from the cycle
just completed.

## Idempotency guarantee

Running this skill twice produces a better or equivalent doc, never worse. The
subagent sees the existing doc as input and brings it to current state. If the
existing doc is already accurate, the output should be nearly identical.
