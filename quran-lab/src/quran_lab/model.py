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
    """Un mot d'UNE orthographe Tanzil (découpage par espaces).

    Les deux orthographes n'ont PAS les mêmes mots ni les mêmes positions : sur le texte
    réel, 363 versets n'ont pas le même nombre de mots en Uthmani et en simple-clean
    (ex. 2:21). Une position `word` n'a de sens que dans sa propre `variant`.
    """

    sura: int
    aya: int
    word: int
    text: str
    variant: str  # "uthmani" | "simple"
    # Vrai pour les 4 mots de la basmala que Tanzil PRÉFIXE au verset 1 des sourates 2 à 114
    # (sauf 9). La morphologie du corpus coranique, elle, ne contient pas ces en-têtes.
    header: bool = False

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

    @property
    def has_morphology(self) -> bool:
        return bool(self.segments)

    @cached_property
    def segments_by_word(self) -> dict[Loc, tuple[Segment, ...]]:
        d: dict[Loc, list[Segment]] = defaultdict(list)
        for s in self.segments:
            d[s.loc].append(s)
        return {k: tuple(sorted(v, key=lambda s: s.seg)) for k, v in d.items()}

    @cached_property
    def word_by_loc(self) -> dict[tuple[str, Loc], Word]:
        return {(w.variant, w.loc): w for w in self.words}

    @cached_property
    def locs_by_variant(self) -> dict[str, list[Loc]]:
        d: dict[str, list[Loc]] = defaultdict(list)
        for w in self.words:
            d[w.variant].append(w.loc)
        return dict(d)
