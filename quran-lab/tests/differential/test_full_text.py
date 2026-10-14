"""Test différentiel sur TOUT le texte Tanzil (nécessite data/raw/, versionné dans le dépôt)."""

from collections import Counter
from pathlib import Path

import pytest

from quran_lab.audit import naive_skeleton
from quran_lab.count import type_counts
from quran_lab.load import build_words, parse_tanzil
from quran_lab.model import Corpus
from quran_lab.rules import Rules, load_config

LAB = Path(__file__).resolve().parents[2]
RAW = LAB / "data" / "raw"
FILES = {"uthmani": "quran-uthmani.txt", "simple": "quran-simple-clean.txt"}

pytestmark = pytest.mark.needs_data


@pytest.mark.skipif(not all((RAW / f).exists() for f in FILES.values()), reason="sources absentes")
@pytest.mark.parametrize("variant", ["uthmani", "simple"])
def test_every_type_count_agrees_on_the_whole_text(variant):
    verses = parse_tanzil((RAW / FILES[variant]).read_text(encoding="utf-8"))
    corpus = Corpus(words=build_words(verses, variant), segments=())
    cfg = load_config(LAB / "config" / "counting_rules.yaml")
    a = type_counts(Rules("form", text=variant, compounds="separate"), corpus, cfg)
    b = Counter(naive_skeleton(w.text) for w in corpus.words)
    assert {t for t in set(a) | set(b) if a.get(t, 0) != b.get(t, 0)} == set()
    assert sum(a.values()) == len(corpus.words)


@pytest.mark.skipif(not (RAW / FILES["simple"]).exists(), reason="sources absentes")
def test_known_structure_of_the_raw_files():
    """Invariants tirés du rapport d'audit (reports/audit-tanzil.md), contrôlés ici en continu."""
    uth = parse_tanzil((RAW / FILES["uthmani"]).read_text(encoding="utf-8"))
    sim = parse_tanzil((RAW / FILES["simple"]).read_text(encoding="utf-8"))
    assert uth.keys() == sim.keys()
    assert len({s for s, _ in uth}) == 114
