---
name: distill
description: |
  Use when the user wants to extract a Zettelkasten-style atomic
  note from a source. Natural triggers: "/distill", "make this a
  Zettel", "pull the claim out of …", "what's the atomic note
  here?", "atomic-ize this", "extract a Zettel from this". Source
  can be: the current conversation, one or more files the user
  names explicitly, a pulled source, a transcription, or multiple
  drafts converging on a shared idea. Output: one or more draft
  Markdown files in `./notes/atomic/`, ready for the user to
  review and promote into their canonical notes.
---

# distill

Extract Zettel-worthy atomic notes from any source and deposit
them as drafts. Promotion to canonical notes is **always** manual —
the user copy-pastes-and-edits in their own voice.

## Operating principles

1. **Drafts only, never auto-promote.** Every distill output lands
   in `./notes/atomic/`. The user manually promotes to whatever
   their canonical-notes folder is (`./evergreens/`, `./permanent/`,
   their Obsidian vault, their notes app — the skill does not
   need to know).
2. **Source must be explicit.** Before extracting anything, name
   the source and confirm it. Distilling from the wrong material
   wastes the work.
3. **One claim per Zettel.** A Zettel-worthy note is atomic. If
   the body has an "and also", it is two Zettels, not one.
4. **Title is a narrative claim.** Not a noun phrase
   ("Maintenance"), but a specific claim ("Operative knowledge
   must grow sublinearly with work done"). The title is
   defensible as a standalone assertion.

## What is a Zettel-worthy note

A draft Zettel meets ALL of these:

- **Standalone.** Readable without context. Anyone landing on
  this note cold should understand the claim and why it matters.
- **Self-contained.** No "as discussed above" or "see the audio".
  The claim's substance is in this note.
- **Short.** 2–4 paragraphs of body. If longer, the claim is
  probably not yet atomic — split it.
- **Memorable.** The reader can restate the claim in one sentence
  after reading.
- **Title is a claim.** Sentence form, asserts something
  specific.
- **Linked.** When relevant adjacent notes exist (in
  `./notes/atomic/` or elsewhere), `## Related` includes
  wikilinks to them.

If a candidate fails any of these, either reshape it until it
passes or abandon it. A weak Zettel pollutes the candidate pool.

## When to use

- The user explicitly invokes distill (see triggers above).
- The user just produced a load-bearing claim in conversation
  they want captured.

## When NOT to use

- Summarisation requests — that's a summary, not a Zettel.
- Briefing generation — different artifact, different home.
- Long-form essays or design docs — distill is for atomic notes,
  not for prose.

## Procedure

### 1. Identify the source — tiered discovery

In order, until source is determined:

1. **Conversation context.** If the claim is in the current
   conversation (just discussed, just transcribed), use that.
   State explicitly: "Distilling from this conversation,
   specifically `<the relevant message>`."

2. **Explicit files.** If the user named files ("distill from
   these three transcriptions"), use exactly those. Confirm by
   listing them back.

3. **Vague gesture — search.** If the user said "I think I've
   written about this before" or "go find what I've said about X":
   - Grep across the project for keyword overlap:
     ```bash
     grep -rln '<keyword>' --include='*.md' .
     ```
   - List matches as candidates. Confirm BEFORE extracting:
     "I found these N notes that look relevant: [...]. Distill
     from these, or refine the search?"

4. **Multiple drafts converging.** If asked to merge several
   existing drafts (in `./notes/atomic/` or elsewhere) into a
   higher-level concept, list the drafts being merged and confirm
   before extraction.

### 2. Extract candidate claims

Read the source(s) carefully. Identify the **load-bearing
claims** — the sentences that, if removed, would change the
meaning of the surrounding material. Filler, examples, asides,
and "thinking out loud" passages are not load-bearing; they are
scaffolding that helped the author arrive at the claim.

Common patterns that signal a load-bearing claim:

- An assertion stated multiple times in different words.
- A "the principle is …" / "the key idea is …" / "what matters
  is …".
- A definition the author coins or reaches for.
- A negation that closes off a wrong path ("the only reason to
  do this is X, and X is a bad reason").

If the source has multiple distinct load-bearing claims, produce
multiple Zettels — one per claim. Don't pack them into one note.

### 3. Draft each Zettel

File location: `./notes/atomic/<YYYY-MM-DD>-<slug>.md` where
`<slug>` is a hyphenated lowercase short-form of the title (3–6
words).

Frontmatter:

```yaml
---
date: <YYYY-MM-DD>
type: zettel_candidate
source: "<raw path to source file>"
status: draft — awaiting manual promotion
---
```

The `source:` field is a **raw path string**, not a `[[wikilink]]`.
This keeps provenance metadata intact without creating a graph
edge that may not be wanted in the destination notes system.

Body structure:

```markdown
# <Title — narrative claim, sentence-form>

<Paragraph 1 — state the claim plainly. What is being asserted.>

<Paragraph 2 — why the claim holds. The reasoning, the evidence,
or the mechanism. Should make the claim defensible, not just
stated.>

<Optional paragraph 3 — implications, scope, or boundary
conditions. When does this hold? When does it not? What follows
from it?>

<Optional paragraph 4 — one concrete example or counterexample.>

## Related

- [[<adjacent note slug>]] — one-line description of the link.
- [[<another note>]] — another link.
```

Keep paragraphs tight. If you cannot say what the claim is in
the first sentence of paragraph 1, the claim is not yet atomic.

If no adjacent notes exist yet, leave the `## Related` section
empty rather than inventing links.

### 4. Surface the drafts

After writing, tell the user:

- Which source(s) you distilled from.
- How many candidates you produced and their titles.
- Where each landed.
- Any candidates you rejected and why (helps calibrate).

Do not say "promoted to canonical" — you never do that. Say
"drafted in `./notes/atomic/`, ready for your review."

## Output location

Defaults, in this order:

1. **User-specified path** in the conversation.
2. **`./notes/atomic/`** if it exists, or create it under the
   current working directory.
3. **`./distilled/`** or **`./zettels/`** if either already exists.

## What this skill explicitly does NOT do

- **Never auto-promote a draft** into the user's canonical-notes
  folder. Promotion is manual, by the user, in their own voice.
- **Never modify the source.** Distillation reads; it does not
  edit the material it draws from.
- **Never produce a Zettel without an identified source.** "I
  just thought of this" is not a valid source — that's the
  user's job, not the skill's.
- **Never combine unrelated claims into one note** to reduce
  note count. Atomicity beats tidiness.
