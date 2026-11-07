# Anonymous review artifact — protocol-aware UIE benchmark

This repository provides **derived aggregate results** and **small independent verification tools** for a double-anonymous review of underwater image enhancement (UIE) and downstream machine perception. It complements the accompanying manuscript and Supplementary Material; it does not replace the original datasets or the entire experimental pipeline.

## What can be checked now?

| Evidence | Material | What it supports |
|---|---|---|
| E1 | `data/e1_frozen_observer_summary.csv` | Mean frozen-observer segmentation response and reported source-bootstrap intervals |
| E2 | `data/e2_*.csv` | Dataset-global train/test matrix and separately recorded source-paired contrasts |
| E3 | `data/e3_observer_sign_patterns.csv` | Three-observer benefit/harm/mixed-sign counts |
| E4 | `data/e4_*.csv` | Fixed-threshold F1 summaries and 39 exact two-sided sign tests with Holm correction |
| E5 | `data/e5_*.csv` | Protocol map, Pearson/Spearman associations, and visual/task sign quadrants |
| E6 | `data/e6_*.csv` | Fixed-observer harm rates, risk summaries, and joint three-observer outcomes |

For exact units, the evaluation set, geometry, and caveats of each result, see `docs/PROTOCOLS.md` and `docs/DATA_DICTIONARY.md`. `DATA_PROVENANCE.md` records how the summary tables were prepared.

## Quick start: aggregate-data verification

Use Python 3.10 or later at the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/validate_release_tables.py
python scripts/validate_claims.py
python scripts/validate_e4_holm39.py
python scripts/validate_protocol_contracts.py
python scripts/check_repository_hashes.py  # cross-platform, prints CRLF normalization if used
```

These commands validate table shape, selected reported aggregate claims, exact E4 sign-test p-values and Holm adjustments, and the listed file checksums. The E4 test excludes ties and adjusts a single family of 39 hypotheses. **None of these checks reruns image enhancement, neural-network inference, training, or bootstrap sampling.**

To run all available offline checks in one command, use `python scripts/run_review_checks.py`.

To generate **new descriptive plots** of the released aggregate tables (not the original manuscript figures), use `python scripts/plot_aggregate_summaries.py`; see `docs/REVIEWER_REPRODUCIBILITY.md`.

The conceptual research-question evolution schematic can be regenerated separately:

```bash
python scripts/generate_research_question_evolution_figure.py
```

This writes image/PDF/SVG outputs under the script directory; they are not task-result reproduction.

## Data access, limitations, and updates

- Original SUIM/USIS16K images and annotations, third-party checkpoints, and third-party source code are **not redistributed**. Obtain them from their respective providers subject to applicable terms.
- The current artifact does **not** contain complete source-level per-image utility records or the full enhancement/perception training and inference pipelines. Aggregate rows cannot independently reproduce bootstrap intervals or recover the underlying source-level task scores.
- E1/E3/E5/E6 are related analyses of SUIM sources but their geometry/reference contracts are not interchangeable. E4 contains three dependent endpoints from **two** trained models, not three independent models.
- The fixed checkpoints and source-level resampling do not estimate training-seed uncertainty. Further limitations are specified in the accompanying manuscript.
- `RELEASE_NOTES.md` documents additions made after the original review-stage upload. A documentation or script update must not silently revise frozen experimental results.

No names, affiliations, personal email addresses, private filesystem paths, or non-anonymous author files are intended to be included. The review artifact has no explicit open-source reuse license at present; readers should not infer reuse or redistribution rights from public visibility. Please use the journal's editorial correspondence channel if questions require author contact, rather than following potentially identifying external repository links.

## Further review guidance

- `docs/REVIEWER_REPRODUCIBILITY.md`: exact checks supported now and a five-minute review workflow.
- `docs/SOURCE_LEVEL_RELEASE_REQUIREMENTS.md`: conditions for any future release of archived source-level derived records; none are currently included.
- `docs/RELEASE_SCOPE_AND_LICENSE.md`: licenses, anonymity, and archival boundaries.

The original source-level experimental records reside outside this release; documentation of a possible future release must not be understood as their availability.
