"""Audit des données Tanzil. Fonctions pures ; l'I/O est dans scripts/audit_tanzil.py."""

from __future__ import annotations

import random
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter

from quran_lab.count import count, type_counts
from quran_lab.load import header_anomalies, word_count_differences
from quran_lab.model import Corpus
from quran_lab.normalize import skeleton
from quran_lab.rules import Config, Rules

_MARKS = re.compile(
    r"[ً-ٰٟۖ-ۜ۟-۪ۨ-ۭـ۝۞۩"
    r"ۥۦ‌-‏]"
)


def naive_skeleton(s: str) -> str:
    """Seconde implémentation, INDÉPENDANTE de normalize.skeleton (plages de code + regex,
    sans catégories Unicode), pour le test différentiel."""
    s = re.sub("ـ[ٕٔ]", "ء", s)
    return _MARKS.sub("", s.replace("ٱ", "ا"))


def parse_metadata(xml_text: str) -> dict[int, dict]:
    root = ET.fromstring(xml_text)
    return {
        int(s.get("index")): {
            "ayas": int(s.get("ayas")),
            "type": s.get("type"),
            "name": s.get("name"),
            "tname": s.get("tname"),
            "order": int(s.get("order")),
        }
        for s in root.find("suras")
    }


def verse_invariants(verses: dict[tuple[int, int], str], meta: dict[int, dict]) -> dict:
    per_sura = Counter(s for s, _ in verses)
    return {
        "suras": len(per_sura),
        "verses": len(verses),
        "suras_whose_verse_count_differs_from_metadata": sorted(
            s for s, m in meta.items() if per_sura.get(s) != m["ayas"]
        ),
        "empty_verses": sorted(k for k, t in verses.items() if not t.strip()),
        "sura_without_basmala_prefix": header_anomalies(verses),
    }


def unicode_table(verses: dict[tuple[int, int], str]) -> list[tuple[str, str, str, int]]:
    c: Counter[str] = Counter(ch for t in verses.values() for ch in t)
    return sorted(
        (f"U+{ord(ch):04X}", unicodedata.name(ch, "?"), unicodedata.category(ch), n)
        for ch, n in c.items()
        if ord(ch) > 127
    )


def differential_full_text(corpus: Corpus, cfg: Config, sample: int = 100, seed: int = 20261013):
    """A (skeleton + type_counts/count) contre B (regex indépendante) sur TOUT le texte,
    par orthographe : types, désaccords d'effectifs, désaccords sur un échantillon."""
    out = {}
    for variant in ("uthmani", "simple"):
        words = [w.text for w in corpus.words if w.variant == variant]
        b = Counter(naive_skeleton(t) for t in words)
        rules = Rules("form", text=variant, compounds="separate")
        a = type_counts(rules, corpus, cfg)
        disagree = sorted(t for t in set(a) | set(b) if a.get(t, 0) != b.get(t, 0))
        rng = random.Random(seed)
        picked = rng.sample(sorted(b), min(sample, len(b)))
        via_count = [t for t in picked if count(t, rules, corpus, cfg).n != b[t]]
        out[variant] = {
            "tokens": len(words),
            "types_a": len(a),
            "types_b": len(b),
            "disagreements": disagree,
            "sample_size": len(picked),
            "sample_disagreements": via_count,
            "same_skeleton_function": sum(
                1 for t in set(words) if skeleton(t) != naive_skeleton(t)
            ),
        }
    return out


def word_diffs(uth, sim):
    d = word_count_differences(uth, sim)
    return {
        "verses": len(d),
        "extra_words_simple": sum(s - u for *_, u, s in d),
        "simple_has_fewer": sum(1 for *_, u, s in d if s < u),
        "first": d[:10],
    }
