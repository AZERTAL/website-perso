"""Modèle de données du corpus : objets immuables, sans I/O."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from functools import cached_property

Loc = tuple[int, int, int]  # (sourate, verset, rang du mot) ; verset 0 = en-tête basmala virtuelle


@dataclass(frozen=True)
class Segment:
    """Un segment morphologique (préfixe, radical ou suffixe) d'un mot du corpus."""

    sura: int
    aya: int
    word: int
    seg: int
    form: str  # arabe avec diacritiques, orthographe du corpus
    pos: str
    seg_type: str  # "PREF" | "STEM" | "SUFF"
    root: str | None  # lettres de la racine sans espaces, ex. "يوم"
    lemma: str | None
    feats: str  # traits bruts, séparés par "|"

    @property
    def loc(self) -> Loc:
        return (self.sura, self.aya, self.word)


@dataclass(frozen=True)
class Word:
    """Un mot du texte Tanzil (découpage par espaces), dans les deux orthographes."""

    sura: int
    aya: int
    word: int
    uthmani: str
    simple: str

    @property
    def loc(self) -> Loc:
        return (self.sura, self.aya, self.word)


@dataclass(frozen=True)
class Corpus:
    """Texte Tanzil + segmentation morphologique, alignés sur la même clé `Loc`."""

    words: tuple[Word, ...]
    segments: tuple[Segment, ...]
    # sourates portant une basmala non numérotée en tête (calculées, pas saisies)
    basmala_header_suras: frozenset[int] = field(
        default_factory=lambda: frozenset(range(2, 115)) - {9}
    )

    @cached_property
    def segments_by_word(self) -> dict[Loc, tuple[Segment, ...]]:
        d: dict[Loc, list[Segment]] = defaultdict(list)
        for s in self.segments:
            d[s.loc].append(s)
        return {k: tuple(sorted(v, key=lambda s: s.seg)) for k, v in d.items()}

    @cached_property
    def word_by_loc(self) -> dict[Loc, Word]:
        return {w.loc: w for w in self.words}
