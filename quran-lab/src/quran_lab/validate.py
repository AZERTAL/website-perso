"""Contrôles de cohérence des données (pas des règles de comptage)."""

from __future__ import annotations

from collections import defaultdict

from quran_lab.model import Corpus


def lemma_root_conflicts(corpus: Corpus) -> dict[str, set[str]]:
    """Lemmes (exacts) rattachés à plus d'une racine. Attendu vide ; sinon, à documenter
    dans docs/divergences.md (erreur d'annotation, ou homographe de lemme)."""
    seen: dict[str, set[str]] = defaultdict(set)
    for s in corpus.segments:
        if s.seg_type == "STEM" and s.lemma and s.root:
            seen[s.lemma].add(s.root)
    return {lem: roots for lem, roots in seen.items() if len(roots) > 1}


def words_without_stem(corpus: Corpus) -> list[tuple[int, int, int]]:
    """Mots du corpus morphologique sans segment radical (invariant : aucun)."""
    return [
        loc
        for loc, segs in corpus.segments_by_word.items()
        if not any(s.seg_type == "STEM" for s in segs)
    ]
