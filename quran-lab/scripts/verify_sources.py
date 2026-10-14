#!/usr/bin/env python3
"""Recalcule les SHA-256 des sources brutes et les compare au manifeste (sortie 1 si écart)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.provenance import sha256_file  # noqa: E402

manifest = json.loads((LAB / "data" / "sources_manifest.json").read_text(encoding="utf-8"))
bad = 0
for row in manifest:
    path = LAB / "data" / "raw" / row["dest"]
    got = sha256_file(path) if path.exists() else "ABSENT"
    ok = got == row["sha256"]
    bad += not ok
    print(f"{'OK     ' if ok else 'ÉCART  '} {row['dest']}  {got[:16]}…")
sys.exit(1 if bad else 0)
