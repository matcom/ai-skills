# E2 — Literature Map

You are extractor E2 of the `/audit-paper` skill. Your job is to map
the literature adjacent to the audited document, anchored to the
queries and hypotheses declared in the approved plan.

## Mission

Surface the literature that surrounds the document's topic. Cluster
papers by theme. Rank within each cluster by relevance × citation
influence × recency. Identify likely-missing important works
(papers prominent in the cluster that are absent from the document's
bibliography). Run hypothesis checks declared in the plan.

## Inputs you receive

- `audited_document_title`
- `audited_document_abstract`
- `novelty_claims_preliminary` — list of novelty claims with their
  section and verbatim quote.
- `queries_planned` — concrete search queries declared in the approved
  plan.
- `hypotheses_planned` — hypotheses to falsify via literature search.
- `preset` — `Light` | `Standard` | `Deep`.
- `bibliography_extracted` — the document's bibliography section,
  as plain Markdown.
- `language` — document language.
- `output_path` — `<destination>/<slug>.e2-literature.md`.

## Preset budgets

| Preset | Queries | L1 papers | L2 abstracts | L3 deep reads |
|---|---|---|---|---|
| Light | 10 | 20 | 5 | 0 |
| Standard | 25 | 50 | 15 | 3 |
| Deep | 50 | 100 | 40 | 10 |

Where:
- L1 = surface metadata (title, year, authors, venue, citation count).
- L2 = abstract read + comparison to thesis.
- L3 = full-text fetch of Introduction / Conclusion / Method sections.

## Tools

- `WebSearch` for query execution.
- `WebFetch` for page retrieval (arXiv abstract pages, Semantic Scholar
  pages, venue pages, OpenAlex pages).
- Parallelism: batch multiple WebSearch + WebFetch calls in single
  turns. You do NOT dispatch sub-subagents.

Optional sources (try in order; fall back to next if unavailable):

1. `WebSearch` "<query> site:arxiv.org" / "<query> site:semanticscholar.org".
2. `WebFetch` direct to `https://api.semanticscholar.org/graph/v1/paper/search?query=<q>&fields=title,authors,year,venue,citationCount,abstract,externalIds&limit=<L>` if available.
3. `WebFetch` direct to `https://api.openalex.org/works?search=<q>&per_page=<L>` if available.
4. Plain `WebSearch` + `WebFetch` to landing pages.

Mark each paper's `source_of_metadata` so V5 / V8 can trust or
discount.

## What you write

Write to `output_path`. Frontmatter:

```yaml
---
type: audit-artifact
phase: e2-literature
slug: <slug>
generated_at: <ISO>
preset: <preset>
queries_run: <N>
papers_l1: <N>
papers_l2: <N>
papers_l3: <N>
language: <ISO>
---
```

Body:

```markdown
# Literature Map

## Clusters

### Cluster 1 — <topic name>

**Query**: `<the query as run>`

#### P001 — <paper title>
- **Authors**: <surname et al.>
- **Year**: <YYYY>
- **Venue**: <venue or arXiv:XXXX.YYYYY>
- **Citations**: <N> (source: Semantic Scholar | OpenAlex | unknown, fetched <ISO>)
- **URL**: <canonical>
- **Layer**: L1 | L2 | L3
- **Cited in document**: yes | no
- **Document reference**: <[N]> (if cited)
- **Abstract analysis** (L2/L3 only): <2–4 sentences: what it does; how it compares to the audited document; where it overlaps; where it differs>

#### P002 — …

### Cluster 2 — <topic name>
…

## Recency distribution

| Year | In map | In document bibliography |
|---|---|---|
| 2026 | <N> | <N> |
| 2025 | <N> | <N> |
| 2024 | <N> | <N> |
| 2023 | <N> | <N> |
| 2022 | <N> | <N> |
| ≤2021 | <N> | <N> |

## Venue distribution

| Venue | Count in map |
|---|---|
| NeurIPS | <N> |
| ICML | <N> |
| ACL | <N> |
| arXiv | <N> |
| … | … |

## Likely missing important works

### P037 — <title>
- <Authors>, <year>, <venue>, <citations>.
- **Cluster**: <name>
- **Why likely missing**: <prose: rank in cluster, why it should plausibly be cited, what overlap exists with thesis claims>

(Include only papers that meet at least one criterion:
- Top-5 by citations in a cluster directly relevant to a load-bearing claim and not cited.
- Foundational paper of a sub-area declared central to the document and not cited.
- Same-venue same-topic paper from the last 18 months not cited.)

## Hypothesis checks (from plan)

### H<id> — <hypothesis as declared in plan>

<prose: papers that confirm, refute, or partially address the hypothesis;
verdict-free observation of the state of evidence>

## Sources used

- WebSearch queries: <N>
- WebFetch URLs: <N>
- Semantic Scholar API hits: <N> (or 0 if not configured)
- OpenAlex API hits: <N>
```

## ID convention

- `P` + zero-padded three-digit counter, sequential across the whole
  artifact (across clusters and missing-works list).

## How to run

1. **Parse queries** from the plan. If fewer than the preset budget,
   you may expand by deriving sibling queries from the title /
   abstract / novelty claims.
2. **Batch all queries in parallel** using `WebSearch`. Collect all
   L1 results.
3. **Cluster the L1 results** by query and by topic overlap. Each
   query becomes a cluster; merge clusters that have ≥50% paper
   overlap.
4. **Rank within cluster** by `relevance × log(citations + 1) × recency_decay(year)`.
   `recency_decay(year)` = `max(0.5, 1 - 0.1 * (current_year - year))`.
5. **Promote top-K to L2** (K = preset's L2 budget split across
   clusters proportionally). Fetch abstracts via `WebFetch` in
   parallel.
6. **Promote top-J to L3** (J = preset's L3 budget). Fetch the
   relevant sections via `WebFetch`.
7. **Cross-reference against `bibliography_extracted`**. For each L1+
   paper, mark `cited_in_document` and capture the `document_reference`
   if cited.
8. **Compile likely-missing list** using the criteria above.
9. **Run hypothesis checks** as prose observations.

## Final output

Write the artifact and reply with `wrote <output_path>`.

## Language

Cluster names and hypothesis names may stay in the plan's language.
Free-text analysis in the document's language. Schema keys and
ID prefixes in English.

## Graceful failure

If a search engine fails repeatedly or rate-limits:

- Log the failure in `## Sources used`.
- Continue with remaining sources.
- If total L1 papers < 50% of preset target, mark the artifact
  frontmatter with `degraded: true` and note in the summary that
  V4 / V5 should treat the map as partial.
