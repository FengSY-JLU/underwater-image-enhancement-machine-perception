#!/usr/bin/env python3
"""Recompute the 39 two-sided exact sign tests and Holm correction.

Input: ../data/e4_holm39_sign_tests.csv
Requires: scipy
This validates the published aggregate count table; it does not rerun model inference.
"""
from __future__ import annotations
import csv
import math
from pathlib import Path
from scipy.stats import binomtest

CSV_PATH = Path(__file__).resolve().parents[1] / "data" / "e4_holm39_sign_tests.csv"
ALPHA = 0.05
N_EXPECTED = 3370
M_EXPECTED = 39


def holm_adjust(p_values):
    m = len(p_values)
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        value = min(1.0, (m - rank) * p_values[idx])
        running = max(running, value)
        adjusted[idx] = running
    return adjusted


def close(a, b):
    return math.isclose(float(a), float(b), rel_tol=2e-6, abs_tol=1e-14)


def main():
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == M_EXPECTED, f"Expected {M_EXPECTED} rows, got {len(rows)}"
    p_values=[]
    for row in rows:
        pos, neg, zero = int(row["pos"]), int(row["neg"]), int(row["zero"])
        assert pos + neg + zero == N_EXPECTED, (row["domain"], row["endpoint"])
        # Ties are excluded from the exact two-sided sign test.
        p = binomtest(pos, n=pos+neg, p=0.5, alternative="two-sided").pvalue
        p_values.append(p)
    adjusted = holm_adjust(p_values)
    for row, p, hp in zip(rows, p_values, adjusted):
        for col, actual in (("p_record",p),("p_recheck",p)):
            assert close(row[col], actual), f"{col} mismatch: {row['domain']} / {row['endpoint']}"
        for col, actual in (("hol_record",hp),("holm_recheck",hp)):
            assert close(row[col], actual), f"{col} mismatch: {row['domain']} / {row['endpoint']}"
    sig = sum(x < ALPHA for x in adjusted)
    assert sig == 38, f"Expected 38/39 Holm-significant comparisons, got {sig}"
    print(f"PASS: {len(rows)} sign tests; each row sums to {N_EXPECTED}; Holm significant={sig}/{len(rows)}")

if __name__ == "__main__":
    main()
