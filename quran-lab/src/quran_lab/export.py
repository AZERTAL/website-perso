"""Export du jeu de données : tables plates, sans I/O (voir scripts/export_dataset.py)."""

from __future__ import annotations

from quran_lab.audit import parse_metadata
from quran_lab.model import Corpus
from quran_lab.normalize import skeleton

WORD_COLUMNS = ("variant", "sura", "aya", "word", "text", "skeleton", "header")
SURA_COLUMNS = ("sura", "name", "tname", "ayas", "type", "order")


def word_rows(corpus: Corpus) -> list[tuple]:
    """Une ligne par mot et par orthographe. `text` est le texte Tanzil VERBATIM ;
    `skeleton` est dérivé (voir docs/methodology/02-normalization.md)."""
    return [
        (w.variant, w.sura, w.aya, w.word, w.text, skeleton(w.text), w.header)
        for w in sorted(corpus.words, key=lambda w: (w.variant, w.sura, w.aya, w.word))
    ]


def sura_rows(xml_text: str) -> list[tuple]:
    """Métadonnées de sourate issues de quran-data.xml (classement mecquois/médinois de Tanzil,
    ordre de révélation de Tanzil : un référentiel parmi d'autres, débattu)."""
    meta = parse_metadata(xml_text)
    return [
        (s, m["name"], m["tname"], m["ayas"], m["type"], m["order"])
        for s, m in sorted(meta.items())
    ]
