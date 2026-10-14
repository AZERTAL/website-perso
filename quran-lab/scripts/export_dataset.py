#!/usr/bin/env python3
"""Exporte le jeu de données dans data/processed/ (CSV et Parquet) avec l'avis de licence Tanzil.

Le texte (`text`) est le texte Tanzil VERBATIM ; `skeleton` est une colonne DÉRIVÉE.
Les fichiers générés ne sont pas versionnés (voir .gitignore) : `make dataset` les reconstruit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import polars as pl

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import read_corpus  # noqa: E402
from quran_lab.export import SURA_COLUMNS, WORD_COLUMNS, sura_rows, word_rows  # noqa: E402

NOTICE = """# Jeu de données Quran Lab

Fichiers : `words.csv` / `words.parquet` (une ligne par mot et par orthographe),
`suras.csv` / `suras.parquet` (métadonnées de sourate).

Dictionnaire de données : quran-lab/docs/data/data-dictionary.md

## Attribution obligatoire

Le texte coranique de ces fichiers provient du Tanzil Project (https://tanzil.net),
version 1.1, sous licence Creative Commons Attribution 3.0.
Termes (https://tanzil.net/docs/Text_License) : copie verbatim autorisée, modification du texte
interdite, source à indiquer avec un lien vers tanzil.net, avis de copyright à reproduire dans
tous les fichiers dérivés.

    Tanzil Quran Text, Copyright (C) 2007-2021 Tanzil Project.
    License: Creative Commons Attribution 3.0

La colonne `text` est le texte Tanzil sans modification. La colonne `skeleton` est calculée par
quran_lab.normalize.skeleton et n'appartient pas au texte de Tanzil.
"""


def main() -> int:
    out = LAB / "data" / "processed"
    out.mkdir(parents=True, exist_ok=True)
    corpus = read_corpus(LAB / "data" / "quran.duckdb")
    words = pl.DataFrame(word_rows(corpus), schema=list(WORD_COLUMNS), orient="row")
    xml = (LAB / "data" / "raw" / "quran-data.xml").read_text(encoding="utf-8")
    suras = pl.DataFrame(sura_rows(xml), schema=list(SURA_COLUMNS), orient="row")
    for name, df in (("words", words), ("suras", suras)):
        df.write_csv(out / f"{name}.csv")
        df.write_parquet(out / f"{name}.parquet")
    (out / "NOTICE.md").write_text(NOTICE, encoding="utf-8")
    print(f"données écrites dans {out} : {words.height} mots, {suras.height} sourates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
