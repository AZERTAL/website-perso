#!/usr/bin/env python3
"""Télécharge les sources dans data/raw/, calcule leur SHA-256, met à jour SOURCES.md.

Seul script autorisé à écrire dans data/raw/ (voir hook_guard_raw.py). Les fichiers sont
ensuite en lecture seule (chmod 444). Aucune URL n'est devinée : `url: null` => refus explicite.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

import yaml

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.provenance import sha256_file  # noqa: E402

BEGIN, END = "<!-- BEGIN sources-table -->", "<!-- END sources-table -->"


def sources_table(rows: list[dict]) -> str:
    head = (
        "| id | fichier | URL | téléchargé le | SHA-256 | licence (à confirmer) |\n"
        "|---|---|---|---|---|---|"
    )
    lines = [
        f"| {r['id']} | {r['dest']} | {r['url']} | {r['date']} | `{r['sha256']}` "
        f"| {r['license_note']} |"
        for r in rows
    ]
    return "\n".join([head, *lines])


def merge_rows(old: list[dict], new: list[dict]) -> list[dict]:
    """Fusionne par identifiant : `--only` ne doit jamais effacer les autres lignes."""
    by_id = {r["id"]: r for r in old}
    by_id.update({r["id"]: r for r in new})
    return list(by_id.values())


def upsert_table(md: str, table: str) -> str:
    block = f"{BEGIN}\n{table}\n{END}"
    if BEGIN in md and END in md:
        a, b = md.index(BEGIN), md.index(END) + len(END)
        return md[:a] + block + md[b:]
    return md.rstrip() + "\n\n" + block + "\n"


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "quran-lab/0.1 (research)"})
    with urllib.request.urlopen(req, timeout=60) as r:  # proxy et CA via variables d'environnement
        return r.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="id d'une source")
    a = ap.parse_args()
    cfg = yaml.safe_load((LAB / "config" / "sources.yaml").read_text(encoding="utf-8"))
    raw = LAB / "data" / "raw"
    rows, failures = [], []
    for s in cfg["sources"]:
        if a.only and s["id"] != a.only:
            continue
        if not s.get("url"):
            failures.append(
                f"{s['id']}: url null, à lire sur {s['page']} puis renseigner config/sources.yaml"
            )
            continue
        if a.dry_run:
            print(f"[dry-run] {s['id']} <- {s['url']}")
            continue
        dest = raw / s["dest"]
        try:
            data = download(s["url"])
        except Exception as e:  # réseau bloqué, 403, TLS : on le dit, on n'invente rien
            failures.append(f"{s['id']}: échec du téléchargement ({type(e).__name__}: {e})")
            continue
        if dest.exists():
            os.chmod(dest, 0o644)
        dest.write_bytes(data)
        os.chmod(dest, 0o444)
        rows.append({**s, "date": dt.date.today().isoformat(), "sha256": sha256_file(dest)})
    if rows:
        manifest = LAB / "data" / "sources_manifest.json"
        old = json.loads(manifest.read_text(encoding="utf-8")) if manifest.exists() else []
        merged = merge_rows(old, rows)
        manifest.write_text(
            json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        md_path = LAB / "SOURCES.md"
        md = md_path.read_text(encoding="utf-8")
        md_path.write_text(upsert_table(md, sources_table(merged)), encoding="utf-8")
        print(f"{len(rows)} source(s) enregistrée(s) dans SOURCES.md")
    for f in failures:
        print("ÉCHEC", f, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
