"""Mini-corpus de test.

Les mots de la sourate 1 reprennent des formes réelles (segmentation et traits de
1:1 et 1:4 telles qu'observées dans le fork mustafa0x du corpus v0.4). Le reste est
SYNTHÉTIQUE et sert à exercer des cas limites (clitiques empilés, composé `يومئذ`
sans racine, pluriel irrégulier, muqatta'at). Aucun test ici ne dit quoi que ce soit
du vrai Coran.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from quran_lab.model import Corpus, Segment, Word
from quran_lab.rules import Config, load_config

ROOT = Path(__file__).resolve().parents[1]


def S(sura, aya, word, seg, form, pos, seg_type, root=None, lemma=None, feats=""):  # noqa: N802
    return Segment(sura, aya, word, seg, form, pos, seg_type, root, lemma, feats)


SEGMENTS = (
    # 1:1  بسم الله الرحمن الرحيم
    S(1, 1, 1, 1, "بِ", "P", "PREF", lemma="ب", feats="P|PREF|LEM:ب"),
    S(1, 1, 1, 2, "سْمِ", "N", "STEM", "سمو", "اسْم", "ROOT:سمو|LEM:اسْم|M|GEN"),
    S(1, 1, 2, 1, "ٱللَّهِ", "N", "STEM", "أله", "اللَّه", "PN|ROOT:أله|LEM:اللَّه|GEN"),
    S(1, 1, 3, 1, "ٱل", "P", "PREF", lemma="ال", feats="DET|PREF|LEM:ال"),
    S(1, 1, 3, 2, "رَّحْمَٰنِ", "N", "STEM", "رحم", "رَحْمٰن", "ROOT:رحم|LEM:رَحْمٰن|MS|GEN|ADJ"),
    S(1, 1, 4, 1, "ٱل", "P", "PREF", lemma="ال", feats="DET|PREF|LEM:ال"),
    S(1, 1, 4, 2, "رَّحِيمِ", "N", "STEM", "رحم", "رَحِيم", "ROOT:رحم|LEM:رَحِيم|MS|GEN|ADJ"),
    # 1:4  مالك يوم الدين
    S(1, 4, 1, 1, "مَٰلِكِ", "N", "STEM", "ملك", "مالِك", "ACT_PCPL|VF:1|ROOT:ملك|LEM:مالِك|M|GEN"),
    S(1, 4, 2, 1, "يَوْمِ", "N", "STEM", "يوم", "يَوْم", "ROOT:يوم|LEM:يَوْم|M|GEN"),
    S(1, 4, 3, 1, "ٱل", "P", "PREF", lemma="ال", feats="DET|PREF|LEM:ال"),
    S(1, 4, 3, 2, "دِّينِ", "N", "STEM", "دين", "دِين", "ROOT:دين|LEM:دِين|M|GEN"),
    # 2:1  الم  (muqatta'at, synthétique : un mot, une lettre-initiale)
    S(2, 1, 1, 1, "الٓمٓ", "INL", "STEM", feats="INL"),
    # 3:1  وَٱلْيَوْمِ  (clitiques empilés : و + ال + يوم)  -- synthétique
    S(3, 1, 1, 1, "وَ", "P", "PREF", lemma="و", feats="CONJ|PREF|LEM:و"),
    S(3, 1, 1, 2, "ٱلْ", "P", "PREF", lemma="ال", feats="DET|PREF|LEM:ال"),
    S(3, 1, 1, 3, "يَوْمِ", "N", "STEM", "يوم", "يَوْم", "ROOT:يوم|LEM:يَوْم|M|GEN"),
    # 3:2  أَيَّامٍ  (pluriel, même lemme que يوم)  -- synthétique
    S(3, 2, 1, 1, "أَيَّامٍ", "N", "STEM", "يوم", "يَوْم", "ROOT:يوم|LEM:يَوْم|MP|GEN"),
    # 3:3  يَوْمَئِذٍ  (composé ; SANS racine, comme le suggère la note du fork) -- synthétique
    S(3, 3, 1, 1, "يَوْمَئِذٍ", "T", "STEM", None, None, "T"),
    # 3:4  يَوْمَيْنِ (duel)  -- synthétique
    S(3, 4, 1, 1, "يَوْمَيْنِ", "N", "STEM", "يوم", "يَوْم", "ROOT:يوم|LEM:يَوْم|MD|ACC"),
    # 3:5  مَلِك (roi) vs 3:6 مَلَك (ange): lemmes distincts, même squelette ملك -- synthétique
    S(3, 5, 1, 1, "مَلِكٌ", "N", "STEM", "ملك", "مَلِك", "ROOT:ملك|LEM:مَلِك|M|NOM"),
    S(3, 6, 1, 1, "مَلَكٌ", "N", "STEM", "ملك", "مَلَك", "ROOT:ملك|LEM:مَلَك|M|NOM"),
)

_PAIRS = (
    (1, 1, 1, "بِسْمِ", "بسم"),
    (1, 1, 2, "ٱللَّهِ", "الله"),
    (1, 1, 3, "ٱلرَّحْمَـٰنِ", "الرحمن"),
    (1, 1, 4, "ٱلرَّحِيمِ", "الرحيم"),
    (1, 4, 1, "مَـٰلِكِ", "مالك"),
    (1, 4, 2, "يَوْمِ", "يوم"),
    (1, 4, 3, "ٱلدِّينِ", "الدين"),
    (3, 1, 1, "وَٱلْيَوْمِ", "واليوم"),
    (3, 2, 1, "أَيَّامٍ", "أيام"),
    (3, 3, 1, "يَوْمَئِذٍ", "يومئذ"),
    (3, 4, 1, "يَوْمَيْنِ", "يومين"),
    (3, 5, 1, "مَلِكٌ", "ملك"),
    (3, 6, 1, "مَلَكٌ", "ملك"),
)
# 3:7 synthétique : « يَـٰٓأَيُّهَا ٱلنَّاسُ » = 2 mots en Uthmani, « يا أيها الناس » = 3 en simple.
# Reproduit le cas réel (363 versets de ce type) : les positions diffèrent selon l'orthographe.
_HEADER = (("بِسْمِ", "بسم"), ("ٱللَّهِ", "الله"), ("ٱلرَّحْمَـٰنِ", "الرحمن"), ("ٱلرَّحِيمِ", "الرحيم"))
# 2:1 tel que Tanzil l'imprime : basmala préfixée (4 mots) PUIS les lettres isolées « الم ».
# (Le corpus morphologique, lui, n'a que « الم » en position 1 : décalage de 4 à aligner.)
WORDS = (
    *(Word(2, 1, i, u, "uthmani", header=True) for i, (u, _) in enumerate(_HEADER, 1)),
    *(Word(2, 1, i, s, "simple", header=True) for i, (_, s) in enumerate(_HEADER, 1)),
    Word(2, 1, 5, "الٓمٓ", "uthmani"),
    Word(2, 1, 5, "الم", "simple"),
    *(Word(s, a, w, u, "uthmani") for s, a, w, u, _ in _PAIRS),
    *(Word(s, a, w, sm, "simple") for s, a, w, _, sm in _PAIRS),
    Word(3, 7, 1, "يَـٰٓأَيُّهَا", "uthmani"),
    Word(3, 7, 2, "ٱلنَّاسُ", "uthmani"),
    Word(3, 7, 1, "يا", "simple"),
    Word(3, 7, 2, "أيها", "simple"),
    Word(3, 7, 3, "الناس", "simple"),
)


@pytest.fixture(scope="session")
def corpus() -> Corpus:
    return Corpus(words=WORDS, segments=SEGMENTS)


@pytest.fixture(scope="session")
def cfg() -> Config:
    return load_config(ROOT / "config" / "counting_rules.yaml")
