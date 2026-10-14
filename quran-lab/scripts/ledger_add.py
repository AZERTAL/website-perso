#!/usr/bin/env python3
"""Ajoute UNE ligne au registre des tests (reports/tests_ledger.csv, en ajout seul)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.stats.ledger import Entry, append  # noqa: E402

ap = argparse.ArgumentParser()
for name in ("test_id", "date", "hypothesis", "family", "statistic", "status"):
    ap.add_argument(f"--{name.replace('_', '-')}", required=True)
ap.add_argument("--n-comparisons", type=int, required=True)
ap.add_argument("--p-raw", default="n/a")
ap.add_argument("--p-adjusted", default="n/a")
a = ap.parse_args()
append(
    LAB / "reports" / "tests_ledger.csv",
    Entry(
        a.test_id,
        a.date,
        a.hypothesis,
        a.family,
        a.n_comparisons,
        a.statistic,
        a.p_raw,
        a.p_adjusted,
        a.status,
    ),
)
print("ajouté :", a.test_id)
