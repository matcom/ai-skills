---
name: design-thinking
description: |
  Entry point for the 5-phase design thinking process. Assesses current state
  and routes to the appropriate phase skill. Each phase runs in an isolated
  agent session and produces a concrete artifact. Phases: understand → define →
  ideate → prototype → test. Invoke when starting any non-trivial problem or
  creative task.
---

# Design Thinking — Entry Point

Using design-thinking to orient the current problem and route to the correct phase.

## The 5 Phases

| Phase | Skill | Input | Output |
|---|---|---|---|
| 1. Understand | `/understand` | Problem description, any available context | `docs/dt/context-brief.md` |
| 2. Define | `/define` | `context-brief.md` | `docs/dt/spec.md` |
| 3. Ideate | `/ideate` | `spec.md` | `docs/dt/plan.md` |
| 4. Prototype | `/prototype` | `plan.md` + `spec.md` | Working artifact (code, doc, etc.) |
| 5. Test | `/test` | `spec.md` + implementation | `docs/dt/audit.md` |

## Artifact Directory

- For repos: `docs/dt/` relative to the repo working directory.
- For vault projects: `vault/Efforts/Projects/<name>/dt/`.

## Context Isolation Principle

Each phase runs in a **new agent session**. Only the previous phase's artifact travels forward. This prevents context bleed — the Understand agent does not carry Prototype details, and the Test agent does not carry the Understand agent's raw notes.

The artifact file is the handoff token. When starting a phase, read the artifact from the prior phase before doing anything else.

## Entry Procedure

Check `docs/dt/` to determine the starting phase:

1. No `dt/` directory, or empty — start at **Understand**.
2. `context-brief.md` exists, no `spec.md` — start at **Define**.
3. `spec.md` exists, no `plan.md` — start at **Ideate**.
4. `plan.md` exists, implementation incomplete — start at **Prototype**.
5. Implementation complete, no `audit.md` — start at **Test**.
6. `audit.md` exists — cycle is complete; review and decide on next action (release, new cycle, or `/design-doc`).

## Non-Linear Navigation

The process is iterative. Legitimate back-transitions:

- Define reveals problem was not understood → back to **Understand**.
- Ideate reveals the spec has fundamental gaps → back to **Define**.
- Prototype reveals a fundamental design issue → back to **Ideate** (or **Define** if the spec was wrong).
- Test reveals the implementation is fundamentally broken → back to **Prototype**.
- Test reveals the spec was wrong → back to **Define**.

Do not back-transition without updating the relevant artifact with what changed and why.

## Commit Convention

```
docs(dt): complete <phase> phase — <brief description>
```

Example: `docs(dt): complete understand phase — mapped auth service problem space`

## Note on Variants

This is the generic version of the design thinking process. Domain-specific variants (code, writing, creative) are a second iteration and are not included here. The generic process applies to all problem types.

---

Proceed: check `docs/dt/` for existing artifacts and invoke the appropriate phase skill.
