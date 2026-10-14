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
    not_evaluated: tuple[str, ...] = ()  # niveaux impossibles faute de morphologie (≠ 0)

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
        partial = ""
        if self.not_evaluated:
            partial = (
                f" PARTIEL : {len(self.cells)} cellules évaluées, niveaux non évalués "
                f"({', '.join(self.not_evaluated)}) faute de morphologie ; verdict non définitif."
            )
        if self.n_hits == 0:
            if self.not_evaluated:
                return f"aucune cellule évaluée ne donne la cible.{partial}"
            return "NON REPRODUCTIBLE (aucune cellule ne donne la cible)"
        if self.n_hits == len(self.cells):
            return f"reproduit dans toutes les cellules évaluées (nuls non évalués).{partial}"
        return f"DÉPEND DE LA RÈGLE ({self.n_hits}/{len(self.cells)} cellules).{partial}"


def inert_axes(m: Multiverse) -> list[str]:
    """Axes de règles qui ne changent AUCUN décompte, tout le reste étant fixé.

    Sert à ne pas confondre « 24 cellules » avec « 24 mesures indépendantes » : pour un mot
    sans basmala ni lettre isolée, l'axe basmala et l'axe muqatta'at sont inertes."""
    names = ("basmala", "muqattaat", "text", "compounds")
    inert = []
    for i, name in enumerate(names):
        groups: dict[tuple, set[int]] = {}
        varies = set()
        for c in m.cells:
            r = c.rules
            vals = (r.basmala, r.muqattaat, r.text, r.compounds)
            varies.add(vals[i])
            groups.setdefault((r.level, *vals[:i], *vals[i + 1 :]), set()).add(c.result.n)
        if len(varies) > 1 and all(len(g) == 1 for g in groups.values()):
            inert.append(name)
    return inert


def run(
    query: str,
    corpus: Corpus,
    cfg: Config,
    *,
    target: int | None = None,
    rules_list: list[Rules] | None = None,
) -> Multiverse:
    skipped: tuple[str, ...] = ()
    if rules_list is None:
        if corpus.has_morphology:
            rules_list = grid()
        else:
            rules_list = grid(("form",))
            skipped = ("stem", "lemma", "root")
    cells = []
    for r in rules_list:
        res = count(query, r, corpus, cfg)
        cells.append(Cell(r, res, None if target is None else res.n == target))
    return Multiverse(query=query, target=target, cells=tuple(cells), not_evaluated=skipped)
