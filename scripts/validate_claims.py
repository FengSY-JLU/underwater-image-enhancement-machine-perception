#!/usr/bin/env python3
"""Check frozen headline claims using the public aggregate CSV tables only.

This is a *summary consistency* test; it does not regenerate source-level
bootstrap intervals, recover individual predictions, or rerun a model.
Requires only the Python standard library.
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def rows(filename: str) -> list[dict[str, str]]:
    with (DATA / filename).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def check(test: bool, message: str) -> None:
    if not test:
        raise AssertionError(message)
    print("PASS:", message)


def main() -> None:
    e1 = rows("e1_frozen_observer_summary.csv")
    check(len(e1) == 30 and all(float(r["mean_delta_miou_pp"]) < 0 for r in e1),
          "E1: 30/30 mean changes are negative")
    check(sum(float(r["ci_high_pp"]) < 0 for r in e1) == 29,
          "E1: 29/30 nominal bootstrap intervals are wholly negative")

    e2 = rows("e2_train_test_domain_matrix.csv")
    check(len(e2) == 18 and len({r["observer"] for r in e2}) == 2 and
          all(len([r for r in e2 if r["observer"] == obs]) == 9
              for obs in {r["observer"] for r in e2}),
          "E2: 18 train/test cells across two architectures")

    e3 = rows("e3_observer_sign_patterns.csv")
    check(len(e3) == 10 and all(
          sum(int(r[k]) for k in ("all_observers_benefit_count", "mixed_sign_count",
                                  "all_observers_harmed_count")) == 110 for r in e3),
          "E3: ten method groups, 110 sources in each joint-sign table")
    mixed_rates = [float(r["mixed_sign_rate_percent"]) for r in e3]
    check(min(mixed_rates) == 13.6 and max(mixed_rates) == 56.4,
          "E3: mixed-sign rate range 13.6–56.4%")

    e4 = rows("e4_source_level_f1_summary.csv")
    check(len(e4) == 39 and all(float(r["mean_delta_f1_pp"]) < 0 for r in e4),
          "E4: 39/39 mean source-level F1 changes are negative")
    sign = rows("e4_holm39_sign_tests.csv")
    check(len(sign) == 39 and all(
          sum(int(r[k]) for k in ("pos", "neg", "zero")) == 3370 for r in sign),
          "E4: 39 tests each account for 3,370 sources")
    check(sum(float(r["hol_record"]) < 0.05 for r in sign) == 38,
          "E4: 38/39 recorded Holm-adjusted p-values < 0.05")

    e5 = rows("e5_visual_task_correlations.csv")
    pearson_sig = [r for r in e5 if float(r["pearson_bh_q"]) < 0.05]
    spearman_sig = [r for r in e5 if float(r["spearman_bh_q"]) < 0.05]
    check(len(e5) == 60 and len(pearson_sig) == 19 and
          len(spearman_sig) == 13,
          "E5: 120 correlations, 32 BH-significant (19 Pearson, 13 Spearman)")
    e5_sig = pearson_sig + spearman_sig
    check(sum(r["metric"] == "UCIQE" for r in e5_sig) == 9 and
          sum(r["metric"] == "UIQM" for r in e5_sig) == 23,
          "E5: 9 UCIQE and 23 UIQM significant associations")
    check(sum(r["pearson_q_ci_crosses_zero"].lower() == "true" for r in e5) == 2,
          "E5: two flagged Pearson q-significant/CI-crossing entries")

    e6 = rows("e6_joint_observer_harm.csv")
    check(len(e6) == 10 and all(
          sum(int(r[k]) for k in ("all_three_harm_count", "all_three_benefit_count",
                                  "mixed_sign_count")) == 110 for r in e6),
          "E6: ten methods, 110 source-level three-observer signs each")
    harm_rates = [float(r["any_observer_harm_percent"]) for r in e6]
    check(min(harm_rates) == 92.7 and max(harm_rates) == 100.0,
          "E6: any-observer-harm range 92.7–100.0%")
    print("All aggregate headline consistency checks passed.")


if __name__ == "__main__":
    main()
