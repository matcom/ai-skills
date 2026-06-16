# Level criteria — calibration tables

Tables consumed by V2, V4, V5, V6, and V9 to calibrate their findings
by academic level (diploma / master / phd / paper). When an evaluator
emits a finding that anchors to a level-criterion, it cites the path
(e.g., `V2.statistical_tests.diploma`) in the finding's metadata
line. The final report reproduces the consulted sub-sections in
Appendix E.

Levels:

- `diploma` — undergraduate final-year thesis (Trabajo de Diploma, BSc thesis).
- `master` — Master's thesis (MSc/MA).
- `phd` — Doctoral dissertation (PhD).
- `paper` — submitted/published research paper at a peer-reviewed venue.

Criteria are descriptive standards drawn from community norms.
Evaluators report observations against them; they never instruct the
document to meet them.

---

## V2 — Methodology

### V2.baselines

| Level | Criterion |
|---|---|
| diploma | ≥1 baseline; may be trivial (random / mean predictor / simplest model). |
| master | ≥2 baselines, one of which corresponds to a SOTA-adjacent approach in the field. |
| phd | ≥3 baselines, at least one of which is the explicit SOTA at submission time. |
| paper | ≥3 baselines including explicit SOTA; venue-typical ablations expected (component-by-component). |

### V2.ablations

| Level | Criterion |
|---|---|
| diploma | Implicit ablations acceptable (e.g., comparing two configurations of own system). |
| master | Explicit ablation of at least one component. |
| phd | Ablation of each major component declared as a contribution. |
| paper | Ablation per component + sensitivity analysis of key hyperparameters. |

### V2.statistical_tests

| Level | Criterion |
|---|---|
| diploma | Recommended for paired comparisons; not required. Reporting std-dev across trials suffices. |
| master | Expected for paired comparisons (Wilcoxon signed-rank, sign test, t-test on differences, bootstrap CI). |
| phd | Required for all comparative claims. Correction for multiple comparisons when applicable. |
| paper | Required + correction for multiple comparisons + effect-size reporting (Cohen's d, Cliff's delta, etc.). |

### V2.sample_size

| Level | Criterion |
|---|---|
| diploma | ≥10 independent trials per configuration; ≥5 datasets/instances. |
| master | ≥20 trials; ≥10 datasets/instances. |
| phd | ≥30 trials + power analysis for primary claims; ≥20 datasets/instances when applicable. |
| paper | ≥30 trials + power + seeds reported; dataset count justified against venue norms. |

### V2.threats_to_validity

| Level | Criterion |
|---|---|
| diploma | Implicit threats acknowledged in discussion. |
| master | Brief dedicated subsection on threats / limitations. |
| phd | Dedicated section addressing internal, external, construct, and statistical conclusion validity. |
| paper | Dedicated section + explicit mitigations + replicability statement. |

### V2.reproducibility_protocol

| Level | Criterion |
|---|---|
| diploma | Protocol describable (datasets, splits, metrics named). |
| master | Protocol fully described + seeds mentioned + code referenced. |
| phd | Protocol + seeds + environment + dataset versions + code DOI/commit pinned. |
| paper | All of phd + reproducibility checklist (NeurIPS-style or venue-specific). |

---

## V4 — Novelty

### V4.differentiation_from_prior_art

| Level | Criterion |
|---|---|
| diploma | Differentiator named at least once in the document, even informally. |
| master | Differentiator articulated with at least one explicit comparison paragraph to one closest prior work. |
| phd | Differentiator articulated against ≥3 closest prior works; conceptual contribution distinct from incremental engineering. |
| paper | Differentiator articulated + venue-aligned (matches the kind of contribution the venue rewards: theory / system / empirical study). |

### V4.scope_of_novelty_claim

| Level | Criterion |
|---|---|
| diploma | Local novelty acceptable ("first integration of X+Y in this context", "first application to Z"). |
| master | Component novelty + integration novelty: one of the two should be substantive. |
| phd | Genuine novelty on at least one axis: problem formulation, method, or experimental insight. |
| paper | Novelty must clear the bar of the venue's typical contribution profile. |

### V4.prior_art_engagement

| Level | Criterion |
|---|---|
| diploma | Closest prior works cited and briefly contrasted. |
| master | Closest prior works cited, contrasted, and discussed in their own subsection. |
| phd | All closest prior works engaged with substantively (methods, results, limitations of each). |
| paper | Full engagement + venue-appropriate related-work survey. |

---

## V5 — State of the Art

### V5.coverage_breadth

| Level | Criterion |
|---|---|
| diploma | The main cluster of work surrounding the thesis topic is covered (10–25 papers). |
| master | Main + adjacent clusters covered (25–60 papers). |
| phd | Main + adjacent + boundary clusters covered (60–150+ papers). |
| paper | Venue-aligned: NeurIPS/ICML/ACL-class survey of the directly-relevant literature; orthogonal areas referenced. |

### V5.recency

| Level | Criterion |
|---|---|
| diploma | At least 30% of citations from the last 5 years. |
| master | At least 40% from the last 5 years; foundational classics balanced. |
| phd | At least 50% from the last 5 years; tracking of last 12-18 months of arXiv preprints expected. |
| paper | At least 60% from the last 3 years; explicit engagement with venue-recent prior work (last 1–2 cycles). |

### V5.citation_weight

| Level | Criterion |
|---|---|
| diploma | Load-bearing claims must cite at least one source per claim. |
| master | Load-bearing claims cite source + author named in body at first mention. |
| phd | Citation weight calibrated: foundational classics in introduction, recent works in related-work, peer SOTA in experimental comparison. |
| paper | All cited works' role in the argument must be clear (foundational vs comparison vs replicated vs disputed). |

### V5.missing_important_work

| Level | Criterion |
|---|---|
| diploma | Tolerable to miss minor recent works; the top-3 most-cited of the cluster expected. |
| master | Top-5 most-cited of each adjacent cluster expected. |
| phd | Top-10 most-cited of each cluster + last 12-month preprints expected. |
| paper | No top-tier cluster-paper should be absent; gap-spot checks against Semantic Scholar / OpenAlex expected. |

---

## V6 — Reproducibility

### V6.documentation

| Level | Criterion |
|---|---|
| diploma | README naming the project + how to run the main experiment. |
| master | README + dependencies list + brief usage examples. |
| phd | README + dependencies pinned + script-to-table mapping + environment description. |
| paper | All of phd + reproducibility statement aligned with venue norms. |

### V6.environment

| Level | Criterion |
|---|---|
| diploma | Dependencies file present (requirements.txt / pyproject.toml / environment.yml) even if loosely versioned. |
| master | Dependencies pinned to minor versions. |
| phd | Dependencies fully pinned + lockfile + Python/R version declared. |
| paper | Dependencies pinned + lockfile + Dockerfile or equivalent environment freeze. |

### V6.determinism

| Level | Criterion |
|---|---|
| diploma | Seeds mentioned in document; presence in code optional. |
| master | Seeds declared in code and in document, consistent. |
| phd | Seeds + deterministic execution flag (where framework supports) + GPU-determinism note when applicable. |
| paper | All of phd + verified bit-reproducibility of at least one headline result. |

### V6.entry_points

| Level | Criterion |
|---|---|
| diploma | At least one entry-point script identifiable from documentation or filename. |
| master | Entry points documented with arguments. |
| phd | Entry points + one-command reproduction (Makefile / justfile / shell script). |
| paper | All of phd + a single command produces all reported tables and figures. |

### V6.tests

| Level | Criterion |
|---|---|
| diploma | Tests not required. |
| master | At least smoke tests of the central component. |
| phd | Unit tests + at least one integration test of the experimental pipeline. |
| paper | Tests + CI configured if repo is public. |

### V6.data_availability

| Level | Criterion |
|---|---|
| diploma | Datasets named with source. |
| master | Datasets named + access path documented (URL / DOI / "available on request"). |
| phd | Datasets named + access path + version pinned + license documented. |
| paper | All of phd + venue-specific data statement. |

---

## V9 — Ethics and Declarations

### V9.ai_use_declaration

| Level | Criterion |
|---|---|
| diploma | Declaration of generative-AI use in research and writing recommended if any AI tools were used. |
| master | Declaration expected; should name tools, phases (research, drafting, code generation, translation), and supervision protocol. |
| phd | Declaration expected and complete; sections of the document where AI assistance was significant identified. |
| paper | Declaration expected and aligned with venue policy (NeurIPS, ICML, ACL, Nature, etc. have specific requirements). |

### V9.data_ethics

| Level | Criterion |
|---|---|
| diploma | When human subjects involved, consent statement mentioned. |
| master | Consent + IRB/ethics-committee approval named when applicable. |
| phd | Full statement on human subjects, consent, anonymisation, data governance, IRB approval where applicable. |
| paper | All of phd + venue-specific data ethics review (e.g., NeurIPS broader-impact). |

### V9.coi_statement

| Level | Criterion |
|---|---|
| diploma | Not required. |
| master | Not required; tutor/advisor relationship implicit. |
| phd | Tutors/advisors + sponsors declared. |
| paper | Full COI statement aligned with venue policy. |

### V9.dual_use

| Level | Criterion |
|---|---|
| diploma | Not required unless topic is clearly dual-use sensitive (LLMs, surveillance ML, biosec, autonomous weapons). |
| master | Discussion encouraged for dual-use-relevant topics. |
| phd | Dual-use / societal-impact discussion expected for relevant topics. |
| paper | Venue-aligned: NeurIPS broader-impact statement; ACL ethics statement; etc. |

### V9.data_availability_statement

| Level | Criterion |
|---|---|
| diploma | Not required as a formal statement; data sources mentioned in methodology. |
| master | Brief statement: where the data lives, how to obtain. |
| phd | Formal "Data availability" statement: location, version, license, access conditions. |
| paper | Formal statement aligned with venue requirements. |

### V9.code_availability_statement

| Level | Criterion |
|---|---|
| diploma | Repo URL printed somewhere in the document if code exists. |
| master | "Code available at" statement with URL and brief description. |
| phd | Formal "Code availability" statement: repo URL + commit/tag/DOI pinned to the version that produced the reported results. |
| paper | Formal statement + Zenodo DOI or equivalent permanent identifier when venue requires. |
