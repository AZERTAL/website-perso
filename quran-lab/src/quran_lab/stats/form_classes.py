"""Classement de formes par expressions régulières (approximation de la morphologie).

Utilisé par les hypothèses du type « tous les mots construits sur telle séquence sont verbaux »
(H002). Les expressions régulières sont FIXÉES dans le fichier d'hypothèse, avant le calcul. Tout
candidat non classé est listé : rien n'est ignoré en silence.
"""

from __future__ import annotations

import re
from collections import Counter


def classify(
    tokens: Counter[str], needle: str, classes: dict[str, re.Pattern[str]]
) -> tuple[dict[str, Counter[str]], Counter[str]]:
    """Candidats = tokens contenant `needle`. Renvoie (classes -> formes, autres).
    Un token qui correspond à plusieurs classes est rangé dans la PREMIÈRE, dans l'ordre donné."""
    out: dict[str, Counter[str]] = {name: Counter() for name in classes}
    other: Counter[str] = Counter()
    for tok, n in tokens.items():
        if needle not in tok:
            continue
        for name, pat in classes.items():
            if pat.fullmatch(tok):
                out[name][tok] += n
                break
        else:
            other[tok] += n
    return out, other
