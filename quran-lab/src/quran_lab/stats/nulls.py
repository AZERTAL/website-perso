"""Taux de coïncidence N5 : combien de types lexicaux tombent EXACTEMENT sur un nombre cible ?

Idée : « 365 » est frappant pour un humain, mais parmi ~2000 types lexicaux, plusieurs ont
mécaniquement un effectif égal à n'importe quel entier donné. On compare le nombre de types
tombant exactement sur la cible à celui des entiers voisins (fenêtre ± `window`).
La fenêtre est pré-enregistrée dans l'hypothèse ; ce n'est pas un modèle nul complet
(N0-N4 : Phase 3), seulement une mesure de plausibilité de coïncidence.
"""

from __future__ import annotations

from collections import Counter
from statistics import mean

from quran_lab.count import type_counts
from quran_lab.model import Corpus
from quran_lab.rules import Config, Rules


def coincidence_from_counts(tc: Counter[str], target: int, window: int = 5) -> dict:
    values = Counter(tc.values())  # effectif -> nombre de types ayant cet effectif
    neighbours = [v for v in range(target - window, target + window + 1) if v != target and v > 0]
    expected = mean(values.get(v, 0) for v in neighbours)
    hits = sorted(t for t, c in tc.items() if c == target)
    return {
        "n_types": len(tc),
        "target": target,
        "observed_types_at_target": len(hits),
        "expected_types_at_target": expected,
        "window": window,
        "types_at_target": hits,
    }


def coincidence_rate(
    corpus: Corpus, cfg: Config, rules: Rules, target: int, window: int = 5
) -> dict:
    return coincidence_from_counts(type_counts(rules, corpus, cfg), target, window)
