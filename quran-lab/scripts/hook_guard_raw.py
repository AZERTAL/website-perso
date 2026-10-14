#!/usr/bin/env python3
"""PreToolUse : interdit toute écriture dans quran-lab/data/raw/ (sauf fetch_sources.py)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from quran_lab.guards import decide  # noqa: E402

msg = decide(json.load(sys.stdin))
if msg:
    print(msg, file=sys.stderr)
    sys.exit(2)
