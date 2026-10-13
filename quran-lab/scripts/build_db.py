#!/usr/bin/env python3
"""data/raw/ -> data/quran.duckdb. NON TESTÉ sur les vraies sources (téléchargement bloqué).

Écrit un compte rendu de chargement (lignes ignorées, versets au nombre de mots divergent).
Rien n'est corrigé en silence : tout écart doit être documenté dans docs/divergences.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import write_corpus  # noqa: E402
from quran_lab.load import LoadReport, build_words, parse_morphology, parse_tanzil, summarize  # noqa: E402
from quran_lab.model import Corpus  # noqa: E402

RAW = LAB / "data" / "raw"


def main() -> int:
    needed = ["quran-uthmani.txt", "quran-simple-clean.txt", "quranic-corpus-morphology-0.4.txt"]
    missing = [n for n in needed if not (RAW / n).exists()]
    if missing:
        print(f"Sources manquantes dans data/raw/ : {missing}", file=sys.stderr)
        return 3
    rep = LoadReport()
    uth = parse_tanzil((RAW / needed[0]).read_text(encoding="utf-8"))
    sim = parse_tanzil((RAW / needed[1]).read_text(encoding="utf-8"))
    words = build_words(uth, sim, rep)
    segs = parse_morphology((RAW / needed[2]).read_text(encoding="utf-8"), "v04", rep)
    write_corpus(Corpus(words=words, segments=segs), LAB / "data" / "quran.duckdb")
    print("segments:", summarize(segs))
    print("mots Tanzil appariés:", len(words))
    print(
        "lignes ignorées:",
        len(rep.skipped_lines),
        "| versets à nombre de mots divergent:",
        len(rep.word_count_mismatches),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
