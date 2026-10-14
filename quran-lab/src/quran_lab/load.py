"""Lecture des sources brutes -> objets du modèle. Fonctions pures sur du texte (pas de chemin).

Deux formats de morphologie sont acceptés :
- "v04"  : Quranic Arabic Corpus v0.4 canonique (Buckwalter, `(s:a:w:g)`)  -- NON VALIDÉ sur le
           vrai fichier (domaine bloqué) ; écrit de mémoire, tolérant.
- "fork" : fork mustafa0x (arabe, `s:a:w:g`) -- VALIDÉ sur un extrait réel de 1:1 à 1:5.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Literal

from quran_lab.buckwalter import bw_to_ar
from quran_lab.model import Segment, Word

MorphFormat = Literal["v04", "fork"]
_LOC_RE = re.compile(r"^\(?(\d+):(\d+):(\d+):(\d+)\)?$")


@dataclass
class LoadReport:
    """Tout ce qui n'a pas pu être lu proprement. Rien n'est ignoré en silence."""

    skipped_lines: list[str] = field(default_factory=list)


def parse_tanzil(text: str) -> dict[tuple[int, int], str]:
    """`sourate|verset|texte` -> {(sourate, verset): texte}. Les lignes `#` sont ignorées."""
    verses: dict[tuple[int, int], str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 2)
        if len(parts) != 3 or not (parts[0].isdigit() and parts[1].isdigit()):
            raise ValueError(f"ligne Tanzil illisible : {line[:80]!r}")
        key = (int(parts[0]), int(parts[1]))
        if key in verses:
            raise ValueError(f"verset en double dans la source : {key}")
        verses[key] = parts[2]
    return verses


def _header_len(verses: dict[tuple[int, int], str], sura: int) -> int:
    """Nombre de mots de basmala préfixés au verset 1 de `sura` (0 si absente), par comparaison
    avec les mots du verset 1:1 dans la MÊME orthographe. Aucune longueur n'est supposée."""
    if sura in (1, 9) or (sura, 1) not in verses:
        return 0
    ref = verses[(1, 1)].split()
    return len(ref) if verses[(sura, 1)].split()[: len(ref)] == ref else 0


def header_anomalies(verses: dict[tuple[int, int], str]) -> list[int]:
    """Sourates (hors 1 et 9) dont le verset 1 ne commence PAS par la basmala."""
    return [s for s in range(2, 115) if s != 9 and _header_len(verses, s) == 0]


def build_words(verses: dict[tuple[int, int], str], variant: str) -> tuple[Word, ...]:
    """Mots d'UNE orthographe. Aucun appariement entre orthographes : leurs positions diffèrent."""
    out: list[Word] = []
    for (sura, aya), text in sorted(verses.items()):
        h = _header_len(verses, sura) if aya == 1 else 0
        out.extend(
            Word(sura, aya, i, tok, variant, header=i <= h) for i, tok in enumerate(text.split(), 1)
        )
    return tuple(out)


def word_count_differences(
    uthmani: dict[tuple[int, int], str], simple: dict[tuple[int, int], str]
) -> list[tuple[int, int, int, int]]:
    """Versets au nombre de mots différent : (sourate, verset, n_uthmani, n_simple)."""
    if uthmani.keys() != simple.keys():
        only = sorted(uthmani.keys() ^ simple.keys())[:5]
        raise ValueError(f"versets présents dans une seule orthographe, ex. {only}")
    return [
        (*k, len(uthmani[k].split()), len(simple[k].split()))
        for k in sorted(uthmani)
        if len(uthmani[k].split()) != len(simple[k].split())
    ]


def _features(raw: str) -> tuple[str | None, str | None, str]:
    root = lemma = None
    for tok in raw.split("|"):
        if tok.startswith("ROOT:"):
            root = tok[5:]
        elif tok.startswith("LEM:"):
            lemma = tok[4:]
    if "PREF" in raw.split("|"):
        seg_type = "PREF"
    elif "SUFF" in raw.split("|"):
        seg_type = "SUFF"
    else:
        seg_type = "STEM"
    return root, lemma, seg_type


def parse_morphology(
    text: str, fmt: MorphFormat, report: LoadReport | None = None
) -> tuple[Segment, ...]:
    segs: list[Segment] = []
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        m = _LOC_RE.match(cols[0]) if len(cols) >= 4 else None
        if m is None:
            if report is not None:
                report.skipped_lines.append(line[:120])
            continue
        sura, aya, word, seg = (int(x) for x in m.groups())
        form, pos, feats = cols[1], cols[2], cols[3]
        root, lemma, seg_type = _features(feats)
        if fmt == "v04":
            form = bw_to_ar(form)
            root = bw_to_ar(root) if root else None
            lemma = bw_to_ar(lemma) if lemma else None
        segs.append(Segment(sura, aya, word, seg, form, pos, seg_type, root, lemma, feats))
    return tuple(segs)


def summarize(segments: tuple[Segment, ...]) -> dict[str, int]:
    """Comptes de contrôle, à comparer à des attentes DOCUMENTÉES, jamais à la mémoire."""
    words = {s.loc for s in segments}
    by_type: dict[str, int] = defaultdict(int)
    for s in segments:
        by_type[s.seg_type] += 1
    return {"segments": len(segments), "words": len(words), **dict(by_type)}
