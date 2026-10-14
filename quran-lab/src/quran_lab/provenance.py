"""Empreintes de provenance : données brutes et version du code."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def raw_manifest_hash(raw_dir: Path) -> str:
    """Empreinte unique de data/raw/ : SHA-256 des couples (nom, sha256), triés. Ignore .gitkeep."""
    h = hashlib.sha256()
    for p in sorted(raw_dir.glob("*")):
        if p.is_file() and p.name != ".gitkeep":
            h.update(f"{p.name}\t{sha256_file(p)}\n".encode())
    return h.hexdigest()


def code_sha(repo: Path) -> str:
    def git(*a: str) -> str:
        r = subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True)
        return r.stdout.strip() if r.returncode == 0 else ""

    sha = git("rev-parse", "--short=12", "HEAD") or "inconnu"
    dirty = git("status", "--porcelain", "--", "quran-lab/src", "quran-lab/config")
    return sha + ("-dirty" if dirty else "")
