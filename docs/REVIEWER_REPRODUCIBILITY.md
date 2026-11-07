# Reviewer reproducibility guide (review stage)

## Available evidence levels

**Level A — table integrity and headline consistency:** 11 derived aggregate CSV files; `validate_release_tables.py`, `validate_claims.py`, `validate_protocol_contracts.py`, and cross-platform SHA-256 checks. These recompute structural counts and check reported headline statements against the released aggregate files; the summaries originate from archived manuscript/Supplementary results.

**Level B — independent statistical recalculation from published counts:** `validate_e4_holm39.py` recomputes exact two-sided sign tests and Holm familywise adjustment for E4 from `pos`, `neg`, and `zero` in the released table. Ties are excluded from each sign test; the source denominators remain 3,370.

**Level C — new visualizations from released aggregates:** `plot_aggregate_summaries.py` creates descriptive plots from the summary CSVs. These plots are *new review aids*, not claims to reproduce the original manuscript figures from raw experiment records.

**Unavailable from this repository:** individual source-level mIoU/F1 and visual-quality records, original enhancement outputs, annotations, full checkpoints, inference/retraining pipeline, and bootstrap draw records. As a result, the repository cannot recompute bootstrap confidence bounds, reproduce individual images or tasks, or recreate COCO AP from source predictions.

## Quick start

```bash
python -m pip install -r requirements.txt
python scripts/run_review_checks.py
python scripts/plot_aggregate_summaries.py
```

The plotting script creates files in the local `generated/aggregate_plots/` folder, which is not part of the shared baseline. `python scripts/check_repository_hashes.py --strict` additionally requires exact canonical LF bytes and may fail on Windows checkouts using CRLF; the default mode reports any LF normalization explicitly.

## Scientific distinctions

- E1: signed *source-averaged* frozen-observer GT-present-class segmentation mIoU changes (pp); reported intervals use source resampling conditional on fixed checkpoints.
- E2: 18 *dataset-global* mIoU cells; 12 separately derived source-paired contrasts; do not derive all contrasts by subtracting global cells.
- E3: historical original-RAW observer-response sign classes; E6 is a distinct risk-analysis reference and may use geometry-matched controls. Their categories are not equivalent.
- E4: 3,370 USIS16K sources; 13 variants including controls; 39 fixed-threshold source-level F1 endpoints from two trained models; box/mask Mask R-CNN readouts share weights. The 39 tests use one Holm family and do not establish model independence.
- E5: 60 rows each with Pearson and Spearman results: 120 BH-adjusted tests. TACL pairs have the stated 109-source inferential exception; `0.0000` q-values are rounded, not exact zeros.
- E6: risk profiles summarize a 110-source set under E6 protocol; observer means/quantiles should not be reinterpreted as cross-task guarantees.

For details see `docs/PROTOCOLS.md`, `docs/DATA_DICTIONARY.md`, and `DATA_PROVENANCE.md`.
