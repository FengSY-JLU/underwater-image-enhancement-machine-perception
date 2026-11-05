# Data provenance and interpretation

## Shared numerical tables

The CSV files in `data/` are aggregate and derived results reported in the manuscript's Supplementary Material. They were transcribed from the final anonymous Supplementary LaTeX tables without rerunning enhancement or perception-model inference. Their estimands and protocols are described in the corresponding table captions in the Supplementary Material.

| File | Contents | Rows |
|---|---|---:|
| `e1_frozen_observer_summary.csv` | E1 source-averaged mIoU changes and source-bootstrap intervals | 30 |
| `e2_train_test_domain_matrix.csv` | E2 dataset-global mIoU across observer/train/test domains | 18 |
| `e2_domain_contrasts.csv` | E2 source-paired domain contrasts and intervals | 12 |
| `e3_observer_sign_patterns.csv` | E3 three-observer sign-pattern counts and mixed-sign intervals | 10 |
| `e4_source_level_f1_summary.csv` | E4 source-level fixed-threshold F1 changes and intervals | 39 |
| `e4_holm39_sign_tests.csv` | E4 positive/negative/tied counts, exact two-sided sign-test p-values, and Holm-adjusted values | 39 |
| `e5_method_protocol_map.csv` | E5 task-reference provenance and visual-geometry protocol | 10 |
| `e5_visual_task_correlations.csv` | E5 Pearson/Spearman coefficients and BH-adjusted q-values | 60 rows / 120 tests |
| `e5_visual_task_sign_quadrants.csv` | E5 visual/task sign-quadrant counts | 60 |
| `e6_observer_risk_profiles.csv` | E6 observer-level mean, interval, harm rate, and lower-tail summary | 30 |
| `e6_joint_observer_harm.csv` | E6 joint three-observer sign and harm summaries | 10 |

## E4 sign-test definition

For each domain–endpoint comparison, zero changes are excluded. The two-sided exact sign test evaluates whether positive and negative nonzero source changes are equally likely under the null. The 39 raw p-values are adjusted jointly using the Holm step-down procedure. The CSV retains the full-precision values recorded in the frozen result table and independent recheck columns. `scripts/validate_e4_holm39.py` recomputes the tests from the counts.

## Important boundaries

- These files are aggregate summaries, not source-level image data.
- Bootstrap intervals are conditional on the evaluated fixed checkpoints and do not quantify training-seed variability.
- The E4 box and mask endpoints have shared model dependencies as described in the Supplementary Material.
- Original SUIM and USIS16K images/annotations are not included or redistributed here. Users must obtain them from their original providers and follow their terms.
- Third-party pretrained weights and third-party source trees are not included.
- The shared scripts do not rerun the full enhancement/recognition benchmark.
