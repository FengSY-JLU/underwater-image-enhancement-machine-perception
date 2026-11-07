# Aggregate table data dictionary

All files in `data/` are comma-separated text with one header row. Values are **reported derived summaries**, not individual images, labels, predictions, or weights. Percentages and percentage-point (`_pp`) differences have different meanings: a percentage-point change is the arithmetic difference between two percentage scores, not a relative percentage change.

| File | Rows | Main columns | Meaning |
|---|---:|---|---|
| `e1_frozen_observer_summary.csv` | 30 | `method`, `observer`, `mean_delta_miou_pp`, `ci_low_pp`, `ci_high_pp` | Mean paired frozen segmentation changes and recorded 95% source-bootstrap bounds |
| `e2_train_test_domain_matrix.csv` | 18 | `observer`, `train_domain`, `test_domain`, `miou_percent` | Dataset-global mIoU in RAW / HSRUIE / DTI-UIE train/test cells |
| `e2_domain_contrasts.csv` | 12 | `observer_domain`, `contrast`, `mean_delta_pp`, `ci_low_pp`, `ci_high_pp` | Separately recorded RR/RE/EE differences and bootstrap intervals |
| `e3_observer_sign_patterns.csv` | 10 | `method`, `all_observers_benefit_count`, `mixed_sign_count`, `all_observers_harmed_count`, `mixed_sign_rate_percent`, `ci_low_percent`, `ci_high_percent`, `worst_observer_mean_pp` | Source counts and observer-agreement summaries for E3 |
| `e4_source_level_f1_summary.csv` | 39 | `domain`, `endpoint`, `mean_delta_f1_pp`, `ci_low_pp`, `ci_high_pp` | Source-level fixed-threshold F1 comparisons and 95% intervals |
| `e4_holm39_sign_tests.csv` | 39 | `domain`, `endpoint`, `pos`, `neg`, `zero`, `p_record`, `hol_record`, `p_recheck`, `holm_recheck` | Sign counts, recorded and independently rechecked two-sided exact p-values and Holm-adjusted values |
| `e5_method_protocol_map.csv` | 10 | `method`, `task_gain_reference`, `visual_geometry`, `n_sources`, `qualification` | Task-reference provenance, visual geometry, source count, exceptions |
| `e5_visual_task_correlations.csv` | 60 | `method`, `metric`, `observer`, `n_sources`, `pearson_r`, `pearson_bh_q`, `spearman_rho`, `spearman_bh_q`, `pearson_q_ci_crosses_zero` | Two correlation tests per row and BH-adjusted q-values |
| `e5_visual_task_sign_quadrants.csv` | 60 | `method`, `metric`, `observer`, `n_sources`, `visual_positive_task_positive`, `visual_positive_task_negative`, `visual_negative_task_positive`, `visual_negative_task_negative` | Joint signs of visual descriptor and task utility changes |
| `e6_observer_risk_profiles.csv` | 30 | `method`, `observer`, `mean_gain_pp`, `ci_low_pp`, `ci_high_pp`, `harm_rate_percent`, `worst_decile_mean_pp` | Observer-wise mean response, source-bootstrap bounds, rate and lower-tail summary |
| `e6_joint_observer_harm.csv` | 10 | `method`, `all_three_harm_count`, `all_three_benefit_count`, `mixed_sign_count`, `any_observer_harm_count`, `any_observer_harm_percent`, `severe_harm_ge_10pp_count`, `mean_three_observer_pp` | Three-observer joint sign and harm statistics |

## Column conventions

- `method` / `domain`: a **specific evaluated implementation variant**, not necessarily a canonical, native-resolution implementation. Some rows explicitly denote resource-bounded or locally modified variants.
- `observer`: the downstream model under the specified training/freeze state.
- `endpoint`: a task metric readout (a shared neural network may supply multiple endpoints).
- `mean_delta_*_pp` / `mean_gain_pp`: signed change in percentage points versus the respective documented RAW reference; negative values represent harm.
- `ci_low_pp`, `ci_high_pp`, `ci_low_percent`, `ci_high_percent`: recorded 95% bootstrap bounds (not recomputable from aggregates alone).
- `pos`, `neg`, `zero`: counts of positive, negative and tied source changes for one E4 domain–endpoint comparison; each row sums to 3,370.
- `p_record`, `hol_record`: historical statistical outputs; `p_recheck`, `holm_recheck`: independently rechecked outputs. The independent script recomputes the tests from counts.
- `*_bh_q`: Benjamini–Hochberg adjusted p-values across the E5 family of 120 tests. Values exported as `0.0000` are rounded for display, not proof of exact zero.
- `pearson_q_ci_crosses_zero`: marks a Pearson q-significant association whose recorded bootstrap interval crosses zero (two flagged HSRUIE/UIQM cases).
- `n_sources`: source denominator of the corresponding analysis; E5 TACL inferential rows use 109 rather than 110 due to a recorded width exception.
- `worst_decile_mean_pp`: descriptive mean of the most harmful decile; it is not a universal definition of conditional value-at-risk.

These tables should be interpreted with the accompanying manuscript and Supplementary Material, which define metric preprocessing, geometry, test-set roles and statistical caveats. They do **not** contain the inputs necessary to rerun model inference or re-estimate the bootstrap distributions.
