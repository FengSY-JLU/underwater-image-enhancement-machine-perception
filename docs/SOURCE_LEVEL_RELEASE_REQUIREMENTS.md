# Requirements for a future *verified* source-level release

**Status: not included in this public artifact.** The repository does not currently contain the original archived source-level data necessary to independently calculate the paper's bootstrap intervals and correlations. This document defines admissibility checks, not a promise that such files are available.

## Data that would enable re-analysis

| Analysis | Minimum derived data to release after archival verification | Contract to preserve |
|---|---|---|
| E1 | One row per source/configuration/frozen-observer, with the RAW and enhanced source-level GT-present-class mIoU or paired signed delta | Frozen checkpoint ID, geometry, original-RAW baseline, 110-source set, pp unit |
| E2 | Source-paired task scores associated with its RR/RE/ER/EE train-test cells, with training-domain observer IDs | Source-paired contrasts are not the same estimand as dataset-global mIoU |
| E3 | Three observer scores or signed deltas per source/configuration | Historical E3 original-RAW reference; independent from E6 evaluation |
| E4 | One source ID + domain + endpoint + fixed-threshold RAW/enhanced F1 pair or signed F1 delta for each eligible record | 13 domain variants, 3,370 sources, 3 dependent endpoints, two trained models, thresholds and geometry |
| E5 | Source-paired visual metric values/deltas (UCIQE and pinned UIQM) and correctly referenced task deltas | 110 or 109 paired sources; two metrics, three observers, 120-test BH family; geometry/reference provenance |
| E6 | Observer-wise source responses with same-source grouping, harm/quantile decisions and reference contract | 110 sources; preserve geometry-matched controls, separate from historical E3 |

The release must preserve source identifiers consistent across multiple methods *only where this is justified by the source manifest*. Do not publish image pixels, annotations, bounding boxes, raw file paths, internal directories, account identifiers, personal metadata, or third-party checkpoints without explicit rights to do so. Source IDs and checkpoint hashes must be reviewed for identifying information and linkage risks.

## Frozen evidence and interpretation

Before publishing any source-level file, require: (1) provenance traced to the archived scoring/evidence artifact, (2) frozen method and geometry identity, (3) explicit unit and metric denominator, (4) original source coverage and exception rows, (5) source-paired key uniqueness, (6) deterministic reproduction of each *published aggregate* when feasible, with defined numerical tolerances, (7) privacy/ownership review, and (8) a new versioned release note. Where historical bootstrap seeds, estimands, or archived raw draws are unavailable, describe recomputed intervals as an independently specified re-analysis, **not** exact reproduction of frozen paper intervals.

A source-level CSV inferred from summary means or sign counts is not permissible: infinitely many different source-level datasets could yield the same aggregates. Additional source-level records cannot be fabricated or reconstructed from the 11 public tables.
