"""Analyse multivers : un même énoncé évalué sous toutes les règles applicables."""

from __future__ import annotations

from dataclasses import dataclass

from quran_lab.count import CountResult, count
from quran_lab.model import Corpus
from quran_lab.rules import Config, Rules, grid


@dataclass(frozen=True)
class Cell:
    rules: Rules
    result: CountResult
    hit: bool | None  # None si aucune cible n'a été donnée


@dataclass(frozen=True)
class Multiverse:
    query: str
    target: int | None
    cells: tuple[Cell, ...]

    @property
    def counts(self) -> list[int]:
        return [c.result.n for c in self.cells]

    @property
    def n_hits(self) -> int:
        return sum(1 for c in self.cells if c.hit)

    def reproduction_verdict(self) -> str:
        """Verdict PROVISOIRE de reproduction, avant tout modèle nul.

        Ne vaut jamais ROBUSTE : ce statut exige en plus les modèles nuls et la
        correction des comparaisons multiples (voir docs/plans, §5.6).
        """
        if self.target is None:
            return "pas de cible"
        if self.n_hits == 0:
            return "NON REPRODUCTIBLE (aucune cellule ne donne la cible)"
        if self.n_hits == len(self.cells):
            return "reproduit dans toutes les cellules (nuls non encore évalués)"
        return f"DÉPEND DE LA RÈGLE ({self.n_hits}/{len(self.cells)} cellules)"


def run(
    query: str,
    corpus: Corpus,
    cfg: Config,
    *,
    target: int | None = None,
    rules_list: list[Rules] | None = None,
) -> Multiverse:
    cells = []
    for r in rules_list if rules_list is not None else grid():
        res = count(query, r, corpus, cfg)
        cells.append(Cell(r, res, None if target is None else res.n == target))
    return Multiverse(query=query, target=target, cells=tuple(cells))
