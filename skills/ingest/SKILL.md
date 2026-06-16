---
name: ingest
description: |
  Use when the user wants to compile a set of pulled sources into
  a structured, cross-linked wiki. Natural triggers: "/ingest",
  "compile these papers into a wiki", "synthesize my sources",
  "ingest the X papers focusing on Y", "build me a wiki page per
  method from these papers". Distinct from /pull (fetches sources)
  and /sota (produces a state-of-the-art review). Input: a folder of
  Markdown sources (typically `./sources/`). Output: cross-linked
  pages in `./wiki/` with per-source summaries and synthesis pages.
---

# ingest

Read one or more files from `./sources/` and compile them into
structured, cross-linked pages in `./wiki/`, following natural-language
guidance from the user.

## When to use

- The user has accumulated several pulled sources and wants them
  digested into a navigable wiki.
- A research / writing task needs the corpus organized by concept
  / method / debate / entity rather than by raw source.
- The user names a focus or ontology for the synthesis ("one page
  per evaluation benchmark", "focusing on training tricks").

## When NOT to use

- The user wants atomic claims as Zettelkasten notes → that's
  `/distill`.
- The user wants a state-of-the-art chapter draft → that's `/sota`.
- The user wants to audit a written document → that's `/audit-paper`.
- The corpus has fewer than 3 sources — ingest is overkill;
  suggest reading the sources directly.

## Input format

The user passes natural-language guidance. Examples:

- "the paper at `sources/2026-04-20-foo.md`"
- "everything I pulled since 2026-04-15 about transformers"
- "the three mixture-of-experts papers, focusing on training tricks"
- "`sources/papers/foo.md` and `sources/papers/bar.md`, one page per
  evaluation benchmark"

Parse the guidance to determine three things:

1. **Scope** — which source files to read. Resolve explicit paths
   directly. For topic references ("about X"), grep within
   `./sources/` (body text + frontmatter `tags:`, `title:`,
   `topic:` fields). For time windows ("since YYYY-MM-DD" or
   "yesterday"), filter by frontmatter `date:` or filename date
   prefix. If the resolved set has more than 10 files, STOP, list
   candidates, and ask the user to trim before proceeding.

2. **Focus** — the angle to extract. If the guidance includes
   phrases like "focusing on", "just the X", "extract the Y",
   narrow the synthesis to that angle. Absence of narrowing means
   extract broadly.

3. **Ontology** — the shape of output pages. If the guidance
   includes phrases like "one page per X", "by X", "grouped by X",
   constrain output shape. Absence means choose ontology from
   content.

If any of the three is ambiguous beyond reasonable inference,
STOP and ask one clarifying question before proceeding. Do not
invent scope.

## Contract

**Write only inside `./wiki/`.** Read anywhere. Never modify
sources — they are authoritative raw material.

**Two kinds of output pages:**

1. **Per-source summaries** — produced *only* when the source has
   artifact identity (a paper, book, talk, canonical article —
   signals: arxiv ID / DOI / ISBN / author list in frontmatter, or
   the source is clearly a bounded artifact). One file per such
   source at `./wiki/sources/<source-slug>.md`, where
   `<source-slug>` matches the source filename without extension.
   If the file already exists, UPDATE it (do not duplicate); append
   today's timestamp to `ingestion_runs:` and refresh the body as
   needed. Skip the summary entirely if the source is a random
   webpage, pasted markdown, or otherwise non-artifact.

   When focus is narrowed (e.g., "focusing on training tricks"),
   the summary floor is waived — no source-summaries unless they
   are part of the focus.

2. **Synthesis pages** — free-shape, produced as the content
   warrants. Flat in `./wiki/` (no subfolders). Filenames are
   slugs from page titles (lowercase, hyphen-separated). The
   `kind:` frontmatter field distinguishes page types (`entity`,
   `concept`, `method`, `debate`, `timeline`, or any other value
   the material calls for).

**Every page carries this frontmatter, always:**

```yaml
---
kind: <entity|concept|method|debate|timeline|source-summary|...>
sources: ["[[source-slug-1]]", "[[source-slug-2]]"]
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingestion_runs: ["YYYY-MM-DDTHH:MM", ...]
---
```

- `kind` — mandatory. For source-summaries, use `source-summary`.
  For synthesis pages, pick from the canonical set or invent as
  needed.
- `sources` — list of wikilinks to the source files this page
  draws from. For source-summaries, a single source. For synthesis
  pages, every source that contributed.
- `created` — today's date if new; preserve existing value if
  updating.
- `updated` — today's date, always.
- `ingestion_runs` — append today's ISO timestamp
  (`YYYY-MM-DDTHH:MM`) to the existing list; if new page, start
  fresh.

Additional frontmatter fields (`aliases`, `tags`, etc.) are
permitted when useful.

**Cross-link freely.** Wiki pages link to other Wiki pages via
`[[other-page]]`. Source citations live in the `sources:`
frontmatter, NOT in body wikilinks (sources are metadata, not
graph edges). Source-summary pages live at
`./wiki/sources/<slug>.md`; to reference one in prose, use
`[[sources/<slug>]]`.

**Existing pages may be freely re-written.** When new sources
introduce new claims about an existing concept page, merge those
claims in; split pages that have grown too large; merge
overlapping pages. The whole wiki is regenerable. Do not be
conservative about touching existing pages — the compounding
value of the wiki depends on re-synthesis.

## Process

1. **Parse the guidance** — determine scope, focus, ontology. If
   scope resolves to more than 10 files, list candidates and stop.
2. **Read the sources** — full body + frontmatter. Note
   `source_type`, `title`, `date`, any arxiv / DOI identifiers.
3. **Read the existing wiki** — at minimum `ls ./wiki/` to know
   what exists. Read any page about to be touched or
   cross-referenced.
4. **Plan the page deltas** — decide: which source-summaries to
   write (respecting the artifact + focus rules), which synthesis
   pages to create, which existing pages to update. Briefly
   narrate the plan in your response so the user can interrupt if
   the ontology is wrong.
5. **Write the pages** — produce frontmatter + body for each. Be
   concrete and cite sources — every factual claim should trace
   to a source in the `sources:` list.
6. **Report** — tell the user what was parsed (scope / focus /
   ontology) and what was written (page deltas with paths).

## Refusals and stops

- If guidance is empty or unintelligible → ask for guidance, do
  nothing.
- If scope resolves to zero sources → report empty result, do
  nothing.
- If scope resolves to more than 10 sources → list candidates,
  ask to trim.
- If a source file cannot be read → report the failure, ingest
  the rest.
- If about to write a file whose path is NOT under `./wiki/` →
  STOP. That is an error.
- If the user asks to modify sources or write outside `./wiki/`
  → refuse and explain the read-only contract on sources.

## Example invocation

```
/ingest the paper at sources/2026-04-20-new-llm-paper.md
```

Response shape:

1. "Parsed scope: single file `sources/2026-04-20-new-llm-paper.md`.
   No focus narrowing. Ontology: agent-chosen from content."
2. "Reading the source … identified 4 concepts: mixture-of-depths,
   dynamic routing, conditional compute, expert-choice."
3. "Existing wiki pages: `[[mixture-of-experts]]` is relevant and
   will be updated."
4. "Plan: 1 source-summary, 3 new synthesis pages, 1 updated
   synthesis page."
5. Write files.
6. "Done. New: `[[mixture-of-depths]]`, `[[dynamic-routing]]`,
   `[[conditional-compute]]`. Updated: `[[mixture-of-experts]]`.
   Summary: `[[sources/2026-04-20-new-llm-paper]]`."

## Anti-patterns

- ❌ Hand-writing prose in a source-summary that contradicts the
  source. Summaries are extracts, not editorials.
- ❌ Inventing wikilinks to non-existent pages. Either create the
  target page in the same run, or use plain text.
- ❌ Promoting a wiki synthesis page to canonical / evergreen
  status. Synthesis pages are regenerable; canonical knowledge
  lives elsewhere by user convention.
- ❌ Writing the same content to multiple pages. Each claim has
  one canonical home, with cross-links from elsewhere.
