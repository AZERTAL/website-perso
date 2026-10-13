#!/usr/bin/env python3
"""PostToolUse : après modification de quran-lab/src ou tests, lancer ruff puis pytest."""

import json
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
payload = json.load(sys.stdin)
fp = (payload.get("tool_input") or {}).get("file_path", "")
if not fp.endswith(".py") or not any(f"/quran-lab/{d}/" in fp for d in ("src", "tests")):
    sys.exit(0)

for cmd in (["uv", "run", "ruff", "check", "."], ["uv", "run", "pytest", "-q", "-x"]):
    r = subprocess.run(cmd, cwd=LAB, capture_output=True, text=True)
    if r.returncode != 0:
        print(
            f"ÉCHEC après modification de {fp}\n$ {' '.join(cmd)}\n"
            f"{r.stdout[-2500:]}{r.stderr[-800:]}",
            file=sys.stderr,
        )
        sys.exit(2)
