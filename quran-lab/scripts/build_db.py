#!/usr/bin/env python3
"""data/raw/ -> data/quran.duckdb.

Texte Tanzil obligatoire. Morphologie (Quranic Arabic Corpus v0.4) facultative : sans elle la base
ne contient que les mots, et seuls les décomptes au niveau « forme » sont possibles (les autres
niveaux sont déclarés non évalués, jamais mis à 0).
Aucun écart n'est corrigé en silence : tout est affiché, et doit être documenté dans
docs/divergences.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import write_corpus  # noqa: E402
from quran_lab.load import (  # noqa: E402
    LoadReport,
    build_words,
    parse_morphology,
    parse_tanzil,
    summarize,
    word_count_differences,
)
from quran_lab.model import Corpus  # noqa: E402

RAW = LAB / "data" / "raw"
UTH, SIM = "quran-uthmani.txt", "quran-simple-clean.txt"
MORPH = "quranic-corpus-morphology-0.4.txt"


def main() -> int:
    missing = [n for n in (UTH, SIM) if not (RAW / n).exists()]
    if missing:
        print(f"Sources Tanzil manquantes dans data/raw/ : {missing}", file=sys.stderr)
        return 3
    rep = LoadReport()
    uth = parse_tanzil((RAW / UTH).read_text(encoding="utf-8"))
    sim = parse_tanzil((RAW / SIM).read_text(encoding="utf-8"))
    words = build_words(uth, "uthmani") + build_words(sim, "simple")
    diffs = word_count_differences(uth, sim)
    segs = ()
    if (RAW / MORPH).exists():
        segs = parse_morphology((RAW / MORPH).read_text(encoding="utf-8"), "v04", rep)
        print("segments:", summarize(segs))
    else:
        print("MORPHOLOGIE ABSENTE : niveaux stem/lemma/root non évaluables.")
    write_corpus(Corpus(words=words, segments=segs), LAB / "data" / "quran.duckdb")
    n_u = sum(1 for w in words if w.variant == "uthmani")
    print(f"mots Uthmani : {n_u} | mots simple-clean : {len(words) - n_u}")
    print(f"versets au nombre de mots différent entre orthographes : {len(diffs)}")
    print(f"lignes de morphologie ignorées : {len(rep.skipped_lines)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
