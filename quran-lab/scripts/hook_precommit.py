#!/usr/bin/env python3
"""PreToolUse (Bash) : avant un `git commit`, valide les rapports et le pré-enregistrement."""

import json
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.guards import is_commit  # noqa: E402

if is_commit(json.load(sys.stdin)):
    r = subprocess.run(
        [sys.executable, str(LAB / "scripts" / "check_reports.py")], capture_output=True, text=True
    )
    if r.returncode != 0:
        print("COMMIT REFUSÉ par check_reports.py :\n" + r.stdout + r.stderr, file=sys.stderr)
        sys.exit(2)
