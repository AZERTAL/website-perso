"""Moteur de comptage à 4 niveaux. Logique pure : aucune I/O.

Un décompte est un MULTIENSEMBLE DE POSITIONS, pas un entier. Le nombre en dérive,
donc chaque chiffre est traçable à ses versets.

Niveaux :
- form  : mot Tanzil, squelette consonantique égal au squelette de la requête
- stem  : radical du corpus (préfixes et suffixes retirés) égal à la requête
- lemma : tag LEM du corpus (comparaison exacte si la requête est vocalisée, sinon squelette)
- root  : tag ROOT du corpus
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass

from quran_lab.model import Corpus, Loc, Segment
from quran_lab.normalize import skeleton
from quran_lab.rules import Config, Rules

_NUMBER_RE = re.compile(r"[123]?[MF]?([SDP])")


def number_of(feats: str) -> str:
    """Nombre grammatical d'un segment : S, D, P, ou '?' (non marqué ou sans objet).

    Ventilation de RAPPORT uniquement. Heuristique à valider sur le corpus réel :
    un trait 'M' ou 'F' seul est lu comme singulier.
    """
    tokens = feats.split("|")
    for t in tokens:
        m = _NUMBER_RE.fullmatch(t)
        if m:
            return m.group(1)
    if any(t in ("M", "F") for t in tokens):
        return "S"
    return "?"


@dataclass(frozen=True)
class CountResult:
    query: str
    rules: Rules
    occurrences: tuple[Loc, ...]
    variants: dict[str, int]  # variantes distinctes rencontrées (formes, lemmes, racines)
    by_number: dict[str, int]

    @property
    def n(self) -> int:
        return len(self.occurrences)


def _stems(segs: tuple[Segment, ...]) -> tuple[Segment, ...]:
    return tuple(s for s in segs if s.seg_type == "STEM")


def _word_skeleton(segs: tuple[Segment, ...]) -> str:
    return skeleton("".join(s.form for s in segs))


def _is_exact_query(query: str) -> bool:
    """Une requête vocalisée (contient des marques) est comparée exactement."""
    return skeleton(query) != query


def _keys_for_word(loc: Loc, corpus: Corpus, rules: Rules) -> list[tuple[str, str]]:
    """Clés (type, variante) sous lesquelles un mot est indexé au niveau demandé.

    `type` est la valeur comparée à la requête ; `variante` est ce qu'on affiche.
    """
    if rules.level == "form":
        w = corpus.word_by_loc.get(loc)
        if w is None:
            return []
        raw = w.uthmani if rules.text == "uthmani" else w.simple
        return [(skeleton(raw), raw)]
    segs = corpus.segments_by_word.get(loc, ())
    stems = _stems(segs)
    if rules.level == "stem":
        if not stems:
            return []
        raw = "".join(s.form for s in stems)
        return [(skeleton(raw), raw)]
    if rules.level == "lemma":
        return [(s.lemma, s.lemma) for s in stems if s.lemma]
    if rules.level == "root":
        return [(s.root, s.root) for s in stems if s.root]
    raise ValueError(rules.level)


def _all_locs(corpus: Corpus, rules: Rules) -> list[Loc]:
    if rules.level == "form":
        return [w.loc for w in corpus.words]
    return list(corpus.segments_by_word.keys())


def _excluded_by_rules(loc: Loc, rules: Rules, cfg: Config) -> bool:
    s, a, _ = loc
    if rules.muqattaat == "exclude" and (s, a) in cfg.muqattaat_verses:
        return True
    return rules.basmala == "none" and (s, a) == (1, 1)


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def _matches(key_type: str, query: str) -> bool:
    if _is_exact_query(query):
        return _nfc(key_type) == _nfc(query)
    return skeleton(key_type) == query


def _number_for(loc: Loc, corpus: Corpus) -> str:
    stems = _stems(corpus.segments_by_word.get(loc, ()))
    for s in stems:
        n = number_of(s.feats)
        if n != "?":
            return n
    return "?"


def count(query: str, rules: Rules, corpus: Corpus, cfg: Config) -> CountResult:
    """Compte les occurrences de `query` sous `rules`."""
    if rules.level == "root":
        query = query.replace(" ", "")
    if _is_exact_query(query) and rules.level != "lemma":
        raise ValueError(
            f"requête vocalisée {query!r} : n'a de sens qu'au niveau 'lemma' "
            f"(niveau demandé : {rules.level!r}). Donner le squelette sans diacritiques."
        )
    q = query if _is_exact_query(query) else skeleton(query)
    q_skel = skeleton(query)
    compounds_of_base = {c for c, base in cfg.compounds.items() if base == q_skel}

    occ: list[Loc] = []
    variants: Counter[str] = Counter()
    for loc in _all_locs(corpus, rules):
        if _excluded_by_rules(loc, rules, cfg):
            continue
        keys = _keys_for_word(loc, corpus, rules)
        hit = [(t, v) for t, v in keys if _matches(t, q)]
        is_compound = bool(compounds_of_base) and _is_compound_word(loc, corpus, compounds_of_base)
        if rules.compounds == "separate" and is_compound:
            continue
        if hit:
            occ.append(loc)
            variants[hit[0][1]] += 1
        elif rules.compounds == "with_base" and is_compound:
            occ.append(loc)
            variants[f"[composé] {_compound_label(loc, corpus)}"] += 1

    if rules.basmala == "all":
        base_occ = [o for o in occ if o[:2] == (1, 1)]
        for s in sorted(corpus.basmala_header_suras):
            for _, _, w in base_occ:
                occ.append((s, 0, w))
                variants["[en-tête basmala]"] += 1

    by_number: Counter[str] = Counter(_number_for(loc, corpus) for loc in occ if loc[1] != 0)
    return CountResult(
        query=query,
        rules=rules,
        occurrences=tuple(occ),
        variants=dict(variants),
        by_number=dict(by_number),
    )


def _is_compound_word(loc: Loc, corpus: Corpus, compounds: set[str]) -> bool:
    segs = corpus.segments_by_word.get(loc)
    if segs is not None and _word_skeleton(segs) in compounds:
        return True
    w = corpus.word_by_loc.get(loc)
    return w is not None and skeleton(w.uthmani) in compounds


def _compound_label(loc: Loc, corpus: Corpus) -> str:
    w = corpus.word_by_loc.get(loc)
    if w is not None:
        return w.uthmani
    return "".join(s.form for s in corpus.segments_by_word[loc])


def type_counts(rules: Rules, corpus: Corpus, cfg: Config) -> Counter[str]:
    """Effectif de chaque type (squelette de forme/radical, lemme exact, racine) en UNE passe.

    Chemin de code indépendant de `count` : sert de contrôle croisé et au taux de base N5.
    Ignore les axes `compounds` et `basmala=all` (qui dépendent de la requête).
    """
    c: Counter[str] = Counter()
    for loc in _all_locs(corpus, rules):
        if _excluded_by_rules(loc, rules, cfg):
            continue
        for t, _ in _keys_for_word(loc, corpus, rules):
            c[t] += 1
    return c
