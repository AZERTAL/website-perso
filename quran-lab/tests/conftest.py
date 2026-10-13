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

WORDS = (
    Word(1, 1, 1, "بِسْمِ", "بسم"),
    Word(1, 1, 2, "ٱللَّهِ", "الله"),
    Word(1, 1, 3, "ٱلرَّحْمَٰنِ", "الرحمن"),
    Word(1, 1, 4, "ٱلرَّحِيمِ", "الرحيم"),
    Word(1, 4, 1, "مَٰلِكِ", "مالك"),
    Word(1, 4, 2, "يَوْمِ", "يوم"),
    Word(1, 4, 3, "ٱلدِّينِ", "الدين"),
    Word(2, 1, 1, "الٓمٓ", "الم"),
    Word(3, 1, 1, "وَٱلْيَوْمِ", "واليوم"),
    Word(3, 2, 1, "أَيَّامٍ", "أيام"),
    Word(3, 3, 1, "يَوْمَئِذٍ", "يومئذ"),
    Word(3, 4, 1, "يَوْمَيْنِ", "يومين"),
    Word(3, 5, 1, "مَلِكٌ", "ملك"),
    Word(3, 6, 1, "مَلَكٌ", "ملك"),
)


@pytest.fixture(scope="session")
def corpus() -> Corpus:
    return Corpus(words=WORDS, segments=SEGMENTS)


@pytest.fixture(scope="session")
def cfg() -> Config:
    return load_config(ROOT / "config" / "counting_rules.yaml")
