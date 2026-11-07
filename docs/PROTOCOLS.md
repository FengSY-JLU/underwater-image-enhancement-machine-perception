# Protocol and estimand map (review stage)

This document is an index to the **already reported** evidence. It is not a specification of a new experiment, and the provided CSV files are derived aggregate tables rather than a source-level dataset.

| Analysis | Sources and scope | Primary observer(s) and endpoint(s) | Interpretation of shared tables |
|---|---|---|---|
| E1 — immediate utility | SUIM, 110 sources; 10 evaluated configurations x 3 frozen observers | UNet-VGG16, SegFormer-B2, HRNet-W18; GT-present-class source-level mIoU change | 30 means and source-bootstrap intervals, conditional on frozen checkpoints |
| E2 — train/test domains | SUIM; two architectures x 3 training domains x 3 test domains | UNet-VGG16, SegFormer-B2; dataset-global mIoU, plus reported paired contrasts | 18 train/test cells and 12 separately recorded source-paired contrasts; these are not identical estimands |
| E3 — observer dependence | SUIM, 110 sources per configuration; 10 configurations | Three frozen segmentation observers | Counts of sources with all-benefit, all-harm, or mixed response under the historical E3 RAW-reference path |
| E4 — aligned perception endpoints | USIS16K, 3,370 test sources; 13 domains (11 UIE variants, 2 controls) | Faster R-CNN box; Mask R-CNN box and mask | 39 mean source-level fixed-threshold F1 contrasts; separate exact sign tests; endpoints are dependent, with 2 trained models |
| E5 — visual/task associations | SUIM, 10 configurations; 110 sources or 109 for TACL inferential rows | UCIQE and pinned UIQM variant vs 3 frozen segmentation observers | 60 combined Pearson/Spearman rows = 120 tests; BH correction across all 120, plus sign quadrants |
| E6 — reliability | SUIM, 110 sources; 10 configurations x 3 frozen observers | Source-level signed GT-present-class mIoU responses | 30 observer risk profiles and 10 joint sign/harm summaries; fixed checkpoints only |

## Distinctions that must not be erased

1. **Immediate vs matched-domain utility.** E1 holds the task observer frozen, whereas E2 includes separately trained domain-specific task models. A gain against a mismatched enhanced-input baseline is not automatically an advantage over the complete RAW-domain system.
2. **Image geometry.** Original-RAW, geometry-matched RAW, fixed-resolution inference, resource-bounded processing and historical reprojection are not interchangeable controls. E5 additionally reports a one-source TACL width exception (109 inferential pairs in those rows).
3. **E3 vs E6 references.** E3 preserves a historical original-RAW evaluation path, while E6 uses geometry-matched references for some fixed-256 methods. Their sign counts must not be silently pooled.
4. **Source vs dataset aggregation.** A source-averaged segmentation change is not dataset-global mIoU. The E4 per-source fixed-threshold F1 is not COCO dataset-level AP.
5. **Dependencies.** E4's Mask R-CNN box and mask endpoints come from one shared model; they do not constitute two independent trained observers.
6. **Inference limitations.** E1/E5/E6 bootstrap intervals are conditional on the recorded checkpoints and source resampling; source-cluster inference or training-seed uncertainty is not supplied by these tables.
7. **No retrospective optimization.** Review-stage scripts check recorded data. They do not select methods, checkpoints or output variants using held-out labels.

## E4 statistical contract

The final E4 family includes 13 domains x 3 endpoints = 39 tests, with 3,370 original sources per test. Zero source-level F1 changes are excluded from each sign test; positive and negative nonzero changes enter a two-sided exact binomial test against probability 0.5. Holm's step-down familywise correction is applied jointly across all 39 comparisons. The result is 38/39 Holm-adjusted p-values below 0.05. This count concerns sign imbalance, not a claim of independent endpoints, causal effects, or per-image AP.
