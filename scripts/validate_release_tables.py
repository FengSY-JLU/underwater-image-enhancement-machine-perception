#!/usr/bin/env python3
"""Check row counts and basic internal consistency of shared aggregate tables."""
import csv
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "e1_frozen_observer_summary.csv": 30,
    "e2_train_test_domain_matrix.csv": 18,
    "e2_domain_contrasts.csv": 12,
    "e3_observer_sign_patterns.csv": 10,
    "e4_source_level_f1_summary.csv": 39,
    "e4_holm39_sign_tests.csv": 39,
    "e5_method_protocol_map.csv": 10,
    "e5_visual_task_correlations.csv": 60,
    "e5_visual_task_sign_quadrants.csv": 60,
    "e6_observer_risk_profiles.csv": 30,
    "e6_joint_observer_harm.csv": 10,
}
def read(name):
    with (ROOT / "data" / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
def main():
    for name, count in EXPECTED.items():
        rows = read(name)
        assert len(rows) == count, f"{name}: expected {count}, got {len(rows)}"
    for row in read("e3_observer_sign_patterns.csv"):
        assert int(row["all_observers_benefit_count"]) + int(row["mixed_sign_count"]) + int(row["all_observers_harmed_count"]) == 110
    for row in read("e5_visual_task_sign_quadrants.csv"):
        total = sum(int(row[k]) for k in ("visual_positive_task_positive", "visual_positive_task_negative", "visual_negative_task_positive", "visual_negative_task_negative"))
        assert total == int(row["n_sources"])
    for row in read("e6_joint_observer_harm.csv"):
        assert int(row["all_three_harm_count"]) + int(row["all_three_benefit_count"]) + int(row["mixed_sign_count"]) == 110
        assert int(row["any_observer_harm_count"]) == int(row["all_three_harm_count"]) + int(row["mixed_sign_count"])
    print(f"PASS: {len(EXPECTED)} aggregate tables; row counts and sign-count identities verified")
if __name__ == "__main__":
    main()
