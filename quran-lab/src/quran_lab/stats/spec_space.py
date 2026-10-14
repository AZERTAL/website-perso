"""Espace de spécifications de H001-v2 (voir hypotheses/H001-v2.md : le texte fait foi).

Question : « 365 est-il plus facile à atteindre que ses voisins, quand on balaie toutes les
façons raisonnables de décider quelles formes du mot jour comptent ? »

Analyse morphologique APPROXIMATIVE par expressions régulières sur le squelette : elle ne
remplace pas le corpus morphologique. Aucun mot n'est ignoré en silence : les mots contenant la
séquence mais non reconnus sont listés.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from itertools import product

TOGGLES = ("T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8")
TOGGLE_LABELS = {
    "T1": "conjonction (و, ف)",
    "T2": "préposition (ب, ل, ك)",
    "T3": "article (ال)",
    "T4": "accusatif indéfini (ـا)",
    "T5": "duel (ـين, ـان)",
    "T6": "pronom suffixé",
    "T7": "composé (يومئذ)",
    "T8": "pluriel (أيام)",
}

# Fixées dans hypotheses/H001-v2.md avant tout calcul.
_SINGULAR = re.compile(r"^([وف]?)([بلك]?)(ال)?يوم(ا|ين|ان|كم|هم|ها|نا|ي|ك|ه)?$")
_COMPOUND = re.compile(r"^([وف]?)يومئذ$")
_PLURAL = re.compile(r"^([وف]?)([بلك]?)(ال)?أيام(كم|هم|ها|نا|ه)?$")
_SEQUENCE = "يوم"


def parse_form(skel: str) -> frozenset[str] | None:
    """Classes d'une forme (ensemble d'interrupteurs requis), ou None si ce n'est pas le mot jour.
    La forme de base `يوم` relève de l'ensemble vide (toujours comptée)."""
    m = _COMPOUND.match(skel)
    if m:
        return frozenset({"T7"} | ({"T1"} if m.group(1) else set()))
    m = _SINGULAR.match(skel)
    if m:
        conj, prep, art, suf = m.groups()
        f = set()
        if conj:
            f.add("T1")
        if prep:
            f.add("T2")
        if art:
            f.add("T3")
        if suf == "ا":
            f.add("T4")
        elif suf in ("ين", "ان"):
            f.add("T5")
        elif suf:
            f.add("T6")
        return frozenset(f)
    m = _PLURAL.match(skel)
    if m:
        conj, prep, art, suf = m.groups()
        f = {"T8"}
        if conj:
            f.add("T1")
        if prep:
            f.add("T2")
        if art:
            f.add("T3")
        if suf:
            f.add("T6")
        return frozenset(f)
    return None


@dataclass(frozen=True)
class SpecSpaceResult:
    totals: dict[tuple[str, tuple[bool, ...]], int]  # (texte, masque) -> décompte
    unmatched: dict[str, int]  # mots contenant la séquence mais non reconnus
    by_class: dict[frozenset[str], int]  # classes -> occurrences (texte donné en premier)

    def n_of(self, t: int) -> int:
        """N(T) : nombre de spécifications dont le décompte vaut exactement T."""
        return sum(1 for v in self.totals.values() if v == t)

    @property
    def distinct_totals(self) -> int:
        return len(set(self.totals.values()))


def analyze(tokens_by_text: dict[str, Counter[str]]) -> SpecSpaceResult:
    """tokens_by_text : {"simple": Counter(squelette -> effectif), "uthmani": ...}."""
    totals: dict[tuple[str, tuple[bool, ...]], int] = {}
    unmatched: Counter[str] = Counter()
    by_class: dict[frozenset[str], int] = {}
    for text, tokens in tokens_by_text.items():
        classes: Counter[frozenset[str]] = Counter()
        for skel, n in tokens.items():
            f = parse_form(skel)
            if f is not None:
                classes[f] += n
            elif _SEQUENCE in skel:
                unmatched[skel] += n
        if not by_class:
            by_class = dict(classes)
        for mask in product((False, True), repeat=len(TOGGLES)):
            on = {t for t, v in zip(TOGGLES, mask, strict=True) if v}
            totals[(text, mask)] = sum(n for f, n in classes.items() if f <= on)
    return SpecSpaceResult(totals=totals, unmatched=dict(unmatched), by_class=by_class)


def inert_toggles(res: SpecSpaceResult) -> list[str]:
    """Interrupteurs dont la modification ne change AUCUN décompte, tout le reste étant fixé."""
    inert = []
    for i, t in enumerate(TOGGLES):
        changes = False
        for (text, mask), v in res.totals.items():
            if not mask[i]:
                other = (text, mask[:i] + (True,) + mask[i + 1 :])
                if res.totals[other] != v:
                    changes = True
                    break
        if not changes:
            inert.append(t)
    return inert


def verdict(res: SpecSpaceResult, target: int = 365, lo: int = 360, hi: int = 370) -> str:
    """Lecture pré-enregistrée dans H001-v2. Jamais plus fort que DÉPEND DE LA RÈGLE."""
    n_t = res.n_of(target)
    neighbours = [res.n_of(t) for t in range(lo, hi + 1) if t != target]
    if n_t == 0:
        return "NON REPRODUCTIBLE sur cet espace de règles"
    if n_t <= max(neighbours):
        return "DÉPEND DE LA RÈGLE : atteint, mais pas plus que ses voisins (non remarquable)"
    return "DÉPEND DE LA RÈGLE : atteint plus que ses voisins ; à confirmer (morphologie réelle)"
