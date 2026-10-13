#!/usr/bin/env python3
"""Refuse un commit : rapport avec chiffre hors bloc généré, ou test non pré-enregistré."""

import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.checks import check_all  # noqa: E402

repo = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=LAB, capture_output=True, text=True, check=True
    ).stdout.strip()
)
problems = check_all(LAB, repo)
for p in problems:
    print(p)
if problems:
    print(f"\n{len(problems)} problème(s). Commit refusé.")
    sys.exit(1)
print("check_reports : OK")
