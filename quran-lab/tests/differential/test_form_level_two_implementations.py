"""Test différentiel : deux implémentations INDÉPENDANTES du niveau « forme ».

A = quran_lab.count (normalisation par catégories Unicode)
B = ci-dessous (normalisation par plages de code regex, parcours naïf du texte brut)
Elles doivent concorder exactement. Un désaccord est un bug jusqu'à preuve du contraire.
"""

import re

import pytest

from quran_lab.count import count
from quran_lab.rules import Rules

_MARKS = re.compile(
    r"[\u064b-\u065f\u0670\u06d6-\u06dc\u06df-\u06e8\u06ea-\u06ed\u0640\u06dd\u06de\u06e9]"
)


def naive_skeleton(s: str) -> str:
    s = re.sub(r"\u0640[\u0654\u0655]", "\u0621", s)
    s = s.replace("\u0671", "\u0627")
    return _MARKS.sub("", s)


def naive_form_count(query, raw_lines, variant):
    """raw_lines : [(sura, aya, texte)] ; compte les mots dont le squelette == requête."""
    total = 0
    for _s, _a, text in raw_lines:
        total += sum(1 for tok in text.split() if naive_skeleton(tok) == query)
    return total


def raw_lines_from(corpus, variant):
    by_verse: dict[tuple[int, int], list[str]] = {}
    for w in sorted(corpus.words, key=lambda w: w.loc):
        if w.variant == variant:
            by_verse.setdefault((w.sura, w.aya), []).append(w.text)
    return [(s, a, " ".join(ws)) for (s, a), ws in by_verse.items()]


@pytest.mark.parametrize("variant", ["uthmani", "simple"])
@pytest.mark.parametrize("query", ["يوم", "ملك", "الم", "الله", "أيام", "واليوم", "يومئذ", "غائب"])
def test_two_implementations_agree(corpus, cfg, variant, query):
    a = count(query, Rules("form", text=variant, compounds="separate"), corpus, cfg).n
    b = naive_form_count(query, raw_lines_from(corpus, variant), variant)
    assert a == b


@pytest.mark.needs_data
@pytest.mark.skip(reason="exécuter sur le texte Tanzil complet dès réception des sources")
def test_full_tanzil_text_all_types():
    """À activer à l'étape 3 : A et B doivent concorder sur TOUS les types de TOUT le texte."""
