"""Règles de comptage : l'espace R et sa configuration (`config/counting_rules.yaml`)."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Literal

import yaml

Level = Literal["form", "stem", "lemma", "root"]
Basmala = Literal["all_113", "numbered_only", "none"]
Muq = Literal["include", "exclude"]
TextVariant = Literal["uthmani", "simple"]
Compounds = Literal["with_base", "separate"]

LEVELS: tuple[Level, ...] = ("form", "stem", "lemma", "root")
BASMALA: tuple[Basmala, ...] = ("all_113", "numbered_only", "none")
MUQ: tuple[Muq, ...] = ("include", "exclude")
TEXTS: tuple[TextVariant, ...] = ("uthmani", "simple")
COMPOUNDS: tuple[Compounds, ...] = ("with_base", "separate")


@dataclass(frozen=True)
class Rules:
    """Un point de l'espace des règles. `text` vaut None quand l'axe est sans objet (n/a)."""

    level: Level
    basmala: Basmala = "all_113"
    muqattaat: Muq = "include"
    text: TextVariant | None = None
    compounds: Compounds = "with_base"

    def __post_init__(self) -> None:
        if self.level == "form" and self.text is None:
            raise ValueError("niveau 'form' : l'axe `text` est obligatoire")
        if self.level != "form" and self.text is not None:
            raise ValueError(f"niveau '{self.level}' : l'axe `text` est n/a (doit valoir None)")

    def label(self) -> str:
        t = self.text or "n/a"
        return f"{self.level}|bsm={self.basmala}|muq={self.muqattaat}|txt={t}|cmp={self.compounds}"


def grid(levels: tuple[Level, ...] = LEVELS) -> list[Rules]:
    """Toutes les cellules APPLICABLES. Les cellules n/a n'existent pas (elles ne valent pas 0)."""
    cells: list[Rules] = []
    for level in levels:
        texts: tuple[TextVariant | None, ...] = TEXTS if level == "form" else (None,)
        for b, m, t, c in product(BASMALA, MUQ, texts, COMPOUNDS):
            cells.append(Rules(level, b, m, t, c))
    return cells


@dataclass(frozen=True)
class Config:
    muqattaat_verses: frozenset[tuple[int, int]]
    compounds: dict[str, str]  # mot composé (squelette) -> mot de base (squelette)


def load_config(path: Path) -> Config:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    verses = frozenset((int(s), int(a)) for s, a in raw["muqattaat_verses"])
    compounds = {str(k): str(v) for k, v in raw["compounds"].items()}
    return Config(muqattaat_verses=verses, compounds=compounds)
