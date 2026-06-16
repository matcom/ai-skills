---
name: pull
description: |
  Use when the user wants to pull, fetch, download, crawl, or save a
  webpage, paper, news article, blog post, PDF, DOCX, or any other
  external document into the local `./sources/` folder as Markdown
  with provenance frontmatter. Natural triggers: "/pull",
  "pull this", "download this article", "save this paper", "get the
  X homepage", "fetch this PDF". Distinct from `WebFetch` which is
  for one-shot reads — `pull` archives a citable copy.
---

# pull

Capture external documents into a local `./sources/` folder as
Markdown with provenance frontmatter. The iron rule: a Sources
file's body is **never hand-written**. Every byte comes from a
conversion tool run over a fetched artifact. The agent's only
editorial acts are (1) choosing the URL, (2) choosing
title / slug / type, (3) verifying the output is clean, (4)
flagging failures.

## When to use

- The user asks to pull, fetch, download, save, or crawl any
  external document.
- A knowledge-work task needs an authoritative citation and the
  artifact is not already in `./sources/`.
- The user wants a durable, citable copy (not a transient `WebFetch`).

## When NOT to use

- The user asks a quick question that does not need citation or
  archival — just answer via `WebFetch` or `WebSearch`.
- The content is an internal artifact (design doc, note,
  journal). Those belong elsewhere in the project.
- The content is transient (a commit URL, a PR link). Link to it
  in the conversation; don't archive.

## How it works

The skill shells out to **`markitdown`** (Microsoft's MarkItDown
tool), which converts HTML / PDF / DOCX / PPTX / XLSX / CSV / TXT /
RTF / and many more formats to Markdown.

Install once:

```bash
pipx install markitdown[all]
# or
uv tool install 'markitdown[all]'
```

The skill runs:

```bash
markitdown <url-or-path> > /tmp/pull-XXXX.md
```

then writes the body plus frontmatter to
`./sources/<YYYY-MM-DD>-<slug>.md`.

## Output location

Defaults, in this order:

1. **User-specified path** in the conversation.
2. **`./sources/`** if it exists, or create it under the current
   working directory.
3. **`./Sources/`** (capitalised) if it exists.

Subdirectories under `sources/` (`papers/`, `news/`, `blogs/`)
are acceptable **only when the flat layout actually hurts** —
never preemptively.

## Filename conventions

- Format: `YYYY-MM-DD-<slug>.md`
- `<slug>` is lowercase alphanumerics and hyphens, max 60 chars
- Collisions on the same date with the same slug: refuse the pull;
  ask the user to pick a different slug or pass `--overwrite`.

## Frontmatter shape

Written by the skill, never by hand:

```yaml
---
type: source
source_type: <webpage|paper|news|blog|email|doc|report|...>
url: <original URL>
title: "<human-readable title>"
fetched_at: <ISO-8601 timestamp with timezone>
fetcher: markitdown
---
```

The agent must determine and pass:
- `--title "<title>"` — when known from context, ALWAYS pass it.
  The title-extraction fallback (first H1 → domain) is imperfect
  on sites with heavy navigation preamble.
- `--type <type>` — common values: `webpage` (default), `paper`,
  `news`, `blog`, `email`, `doc`, `report`.

Optional fields that the agent may add when extractable from the
source:
- `author` — when prominent in the document.
- `published_date` — distinct from `fetched_at`.
- `lang` — when the source is in a language other than the agent's
  current interaction language.

YAGNI for everything else — don't add speculative fields.

## Procedure

### 1. Resolve the URL

The user passes a URL explicitly, or names a document the agent
should fetch ("the Wei et al. 2022 CoT paper" → look up the arXiv
URL via WebSearch first, then proceed).

### 2. Run markitdown

```bash
markitdown "<url>" > /tmp/pull-<random>.md
```

If `markitdown` exits non-zero, surface the error and stop.
Suggest alternative URLs (e.g., the arXiv PDF instead of the
abstract page) or fall back to `WebFetch` to read content directly,
then pipe that into a second invocation:

```bash
echo "<content>" | markitdown - > /tmp/pull-<random>.md
```

### 3. Verify the output

Before writing the final file:

1. **Exit code is zero.**
2. **Inspect the preview** — read the first ~400 chars of the
   converted body. Look for failure signals: paywall / login
   banners; cookie-consent boilerplate as the only content; 403 /
   404 HTML; navigation-only skeletons.
3. **Check the size** — under ~500 bytes of body is suspicious for
   most real pages.
4. **Sample the middle** — for substantive sources, read lines
   50–100 of the file to confirm the conversion did not silently
   truncate or mangle formatting.

If the output is bad: delete the temp file (the one case where a
Sources artifact may be deleted), adjust the approach (better URL,
better `--title`, fall back to `WebFetch`), retry. Do NOT silently
write a broken Source.

### 4. Write the final file

Compose the frontmatter, then concatenate with the markitdown
output. Write to `./sources/<YYYY-MM-DD>-<slug>.md`. Use the
Write tool.

### 5. Report

Tell the user: the destination path, file size, and the first
sentence or two of the body so they can verify it landed
correctly.

## Anti-patterns

- ❌ Manually copy-pasting web content into a Sources file.
  Breaks the provenance guarantee.
- ❌ Editing a Sources file's body to "clean up" formatting. If
  markitdown produces bad output, fix the pipeline or accept the
  imperfection — don't silently edit the source.
- ❌ Writing a Sources file with hand-written prose about the
  source ("this article says..."). That belongs in synthesis
  (`./wiki/`, `./notes/`), with a link to the Source.
- ❌ Pulling without verifying the output. A silently-broken
  Source is worse than no Source.

## Known limits and iteration path

These are places where the pipeline will likely need growth.
Don't pre-build; extend when a real pull bites one of these.

- **JS-heavy / SPA sites** — `markitdown` fetches via `requests`,
  no JS execution. If a pull returns mostly boilerplate, fall back
  to `WebFetch` + pipe.
- **Paywalled content** — `markitdown` has no auth state. The
  user must extract content through their own browser session and
  pipe it in.
- **PDFs behind redirects** — if `markitdown` fails on a
  particular redirect chain, `curl` to a temp file and pass the
  path to `markitdown`.
- **Title extraction from bad HTML** — always pass `--title`
  explicitly when known from context.
- **Large files** — `markitdown` can take a while on big PDFs.
  Default Bash timeout (120 s) may not be enough; raise to 300 s
  on the call.
