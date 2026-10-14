"""Registre des tests : fichier CSV en ajout seul (append-only).

Pourquoi : le piège des comparaisons multiples, c'est de ne pas savoir combien de tests on a
faits. Chaque test réalisé dans le projet est une ligne de `reports/tests_ledger.csv`. Le total
des comparaisons est alors une mesure, pas un souvenir.

« Ajout seul » est garanti par git : `checks.check_ledger` refuse un fichier de travail qui ne
commence pas par le contenu déjà commité.
"""

from __future__ import annotations

import csv
from dataclasses import astuple, dataclass, fields
from pathlib import Path

HEADER = (
    "test_id",
    "date",
    "hypothesis",
    "family",
    "n_comparisons",
    "statistic",
    "p_raw",
    "p_adjusted",
    "status",
)


@dataclass(frozen=True)
class Entry:
    test_id: str
    date: str  # AAAA-MM-JJ
    hypothesis: str
    family: str
    n_comparisons: int  # tailles de la famille au moment du test
    statistic: str
    p_raw: str  # "n/a" quand le test n'a pas de p-value (ex. reproduction pure)
    p_adjusted: str
    status: str  # ROBUSTE | DÉPEND DE LA RÈGLE | NON SIGNIFICATIF | NON REPRODUCTIBLE | PARTIEL


assert tuple(f.name for f in fields(Entry)) == HEADER


def read(path: Path) -> list[Entry]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return [Entry(**{**r, "n_comparisons": int(r["n_comparisons"])}) for r in rows]


def append(path: Path, entry: Entry) -> None:
    """Ajoute une ligne. Refuse un identifiant déjà utilisé : on n'écrase jamais un test."""
    existing = read(path)
    if any(e.test_id == entry.test_id for e in existing):
        raise ValueError(f"test_id déjà présent : {entry.test_id} (ouvrir une nouvelle version)")
    new_file = not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if new_file:
            w.writerow(HEADER)
        w.writerow(astuple(entry))


def total_comparisons(path: Path) -> int:
    """Nombre total de comparaisons déclarées dans tout le projet."""
    return sum(e.n_comparisons for e in read(path))
