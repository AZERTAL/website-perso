"""Recherche de passages : où une expression apparaît, avec quelles formes. Logique pure.

Cartographie (`FAIT`), pas interprétation. Ne prouve aucun motif : un motif doit battre un modèle
nul (voir docs/research-program.md). Les requêtes viennent de `config/queries/*.yaml`, commités
AVANT exécution.

Appariement : squelette consonantique (`normalize.skeleton`) sur l'orthographe simple-clean.
- mot : le mot, éventuellement précédé de clitiques (conjonction, préposition, article) ;
- expression : mots consécutifs dans un même verset ; le premier peut porter `و` ou `ف`.
Les mots de la basmala préfixée par Tanzil (`header`) sont exclus : ils ne font pas partie du
verset numéroté.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml

from quran_lab.model import Corpus
from quran_lab.normalize import skeleton

VerseKey = tuple[int, int]


@dataclass(frozen=True)
class Query:
    id: str
    kind: str  # "word" | "phrase"
    text: str
    why: str


@dataclass(frozen=True)
class Hit:
    sura: int
    aya: int
    start: int  # rang (à partir de 1) du premier mot de l'occurrence dans le verset
    forms: tuple[str, ...]  # squelettes réellement rencontrés

    @property
    def ref(self) -> str:
        return f"{self.sura}:{self.aya}"


@dataclass(frozen=True)
class QueryResult:
    query: Query
    hits: tuple[Hit, ...]

    @property
    def n_occurrences(self) -> int:
        return len(self.hits)

    @property
    def verses(self) -> list[str]:
        seen: dict[str, None] = {}
        for h in self.hits:
            seen.setdefault(h.ref, None)
        return list(seen)

    @property
    def n_suras(self) -> int:
        return len({h.sura for h in self.hits})

    @property
    def forms(self) -> Counter[str]:
        return Counter(" ".join(h.forms) for h in self.hits)


def load_queries(path: Path) -> tuple[str, str, list[Query]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    qs = [Query(q["id"], q["kind"], q["text"], q["why"]) for q in raw["queries"]]
    ids = [q.id for q in qs]
    if len(set(ids)) != len(ids):
        raise ValueError(f"identifiants de requête en double dans {path.name}")
    bad = [q.id for q in qs if q.kind not in ("word", "phrase")]
    if bad:
        raise ValueError(f"kind inconnu pour {bad}")
    return raw["domain"], raw["title"], qs


def verse_tokens(corpus: Corpus, variant: str = "simple") -> dict[VerseKey, list[str]]:
    """Squelettes des mots de chaque verset, dans l'ordre, sans la basmala préfixée."""
    d: dict[VerseKey, list[tuple[int, str]]] = defaultdict(list)
    for w in corpus.words:
        if w.variant == variant and not w.header:
            d[(w.sura, w.aya)].append((w.word, skeleton(w.text)))
    return {k: [t for _, t in sorted(v)] for k, v in d.items()}


_CLITICS = "[وف]?[بلك]?(?:ال)?"


def _word_re(word: str) -> re.Pattern[str]:
    return re.compile(f"{_CLITICS}{re.escape(word)}")


def search(query: Query, vt: dict[VerseKey, list[str]], rule: str = "v2") -> QueryResult:
    """rule "v1" : le premier mot d'une expression ne porte que `و` ou `ف` (règle pré-enregistrée).
    rule "v2" : il peut aussi porter `ب`, `ل` ou `ك` (ajoutée après avoir constaté que v1 manque
    `كألف سنة`, voir DECISIONS D16). Les deux sont rapportées côte à côte.
    """
    if rule not in ("v1", "v2"):
        raise ValueError(rule)
    words = skeleton(query.text).split()
    if not words:
        raise ValueError(f"requête vide : {query.id}")
    if query.kind == "word":
        pats = [_word_re(words[0])]
    else:
        first = "[وف]?" if rule == "v1" else "[وف]?[بلك]?"
        pats = [re.compile(f"{first}{re.escape(words[0])}")] + [
            re.compile(re.escape(w)) for w in words[1:]
        ]
    hits: list[Hit] = []
    n = len(pats)
    for (sura, aya), toks in sorted(vt.items()):
        for i in range(len(toks) - n + 1):
            if all(p.fullmatch(toks[i + j]) for j, p in enumerate(pats)):
                hits.append(Hit(sura, aya, i + 1, tuple(toks[i : i + n])))
    return QueryResult(query, tuple(hits))
