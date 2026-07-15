# drafts/ — skills under design iteration

Skills here are **not installable** and are **not picked up by `install.sh`**
(which only copies subdirs of `skills/`). They are parked for design review
before being promoted to `skills/`.

Unlike the academic skills in this repo, these are a generic **design-thinking**
process. They remain under active review — several open tensions are being
worked out before they are recommended for install:

- Context isolation between phases is described but not mechanized (no subagent
  dispatch enforces it).
- Artifact-location conventions (`docs/dt/`, in-repo `docs/design.md`) need
  reconciling with existing design-doc homes.
- Ceremony weight (five artifacts + a commit per phase) is heavy for the broad
  "any non-trivial problem" trigger.

Contents:

- `design-thinking/` — router for a 5-phase process.
- `understand/` `define/` `ideate/` `prototype/` `test/` — the five phase skills.
- `design-doc/` — idempotent authoritative-design-doc compiler.

To promote one: resolve its open questions, then `git mv drafts/<name> skills/<name>`
and document it in `AGENTS.md` + `README.md`.
