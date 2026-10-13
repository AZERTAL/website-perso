"""Les valeurs attendues sont calculées À LA MAIN sur le mini-corpus de conftest.py,
avant exécution. Voir les commentaires pour le détail du raisonnement."""

import pytest

from quran_lab.count import count, number_of
from quran_lab.rules import Rules


def n(query, corpus, cfg, **kw):
    return count(query, Rules(**kw), corpus, cfg)


# --- يوم aux quatre niveaux -------------------------------------------------
# Mots portant le radical/lemme/racine يوم : 1:4:2 (يَوْمِ), 3:1:1 (وَٱلْيَوْمِ), 3:2:1 (أَيَّامٍ),
# 3:4:1 (يَوْمَيْنِ). 3:3:1 (يَوْمَئِذٍ) est un composé SANS racine ni lemme.


def test_form_level_is_exact_skeleton_only(corpus, cfg):
    # seul 1:4:2 a le squelette « يوم » ; واليوم, أيام, يومين sont d'autres chaînes
    r = n("يوم", corpus, cfg, level="form", text="uthmani", compounds="separate")
    assert r.occurrences == ((1, 4, 2),)


def test_stem_level_removes_clitics(corpus, cfg):
    # وَٱلْيَوْمِ perd و + ال : son radical est يوم -> 1:4:2 et 3:1:1
    r = n("يوم", corpus, cfg, level="stem", compounds="separate")
    assert r.occurrences == ((1, 4, 2), (3, 1, 1))


def test_lemma_level_merges_inflections(corpus, cfg):
    r = n("يوم", corpus, cfg, level="lemma", compounds="separate")
    assert set(r.occurrences) == {(1, 4, 2), (3, 1, 1), (3, 2, 1), (3, 4, 1)}
    assert r.variants == {"يَوْم": 4}


def test_root_level(corpus, cfg):
    r = n("يوم", corpus, cfg, level="root", compounds="separate")
    assert r.n == 4


def test_root_query_accepts_spaced_letters(corpus, cfg):
    assert n("ي و م", corpus, cfg, level="root", compounds="separate").n == 4


# --- composés ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("level", "text", "separate_n"),
    [("form", "uthmani", 1), ("stem", None, 2), ("lemma", None, 4), ("root", None, 4)],
)
def test_compound_rule_adds_exactly_the_compound(corpus, cfg, level, text, separate_n):
    sep = n("يوم", corpus, cfg, level=level, text=text, compounds="separate")
    base = n("يوم", corpus, cfg, level=level, text=text, compounds="with_base")
    assert sep.n == separate_n
    assert base.n == separate_n + 1
    assert (3, 3, 1) in base.occurrences and (3, 3, 1) not in sep.occurrences
    assert any("[composé]" in v for v in base.variants)


def test_compound_queried_directly_is_unaffected(corpus, cfg):
    r = n("يومئذ", corpus, cfg, level="form", text="uthmani", compounds="separate")
    assert r.occurrences == ((3, 3, 1),)


# --- axe texte : Uthmani vs simple ------------------------------------------


def test_text_axis_changes_the_count(corpus, cfg):
    # Uthmani : مَٰلِكِ perd son alif dagger -> « ملك » (comme مَلِكٌ et مَلَكٌ) -> 3
    # simple  : « مالك » garde son alif -> seulement les 2 autres -> 2
    assert n("ملك", corpus, cfg, level="form", text="uthmani").n == 3
    assert n("ملك", corpus, cfg, level="form", text="simple").n == 2


# --- homographes : lemme vocalisé vs squelette ------------------------------


def test_lemma_skeleton_query_merges_homographs_and_says_so(corpus, cfg):
    r = n("ملك", corpus, cfg, level="lemma")
    assert r.n == 2
    assert r.variants == {"مَلِك": 1, "مَلَك": 1}  # la fusion est VISIBLE


def test_lemma_vocalised_query_is_exact(corpus, cfg):
    assert n("مَلَك", corpus, cfg, level="lemma").occurrences == ((3, 6, 1),)
    assert n("مَلِك", corpus, cfg, level="lemma").occurrences == ((3, 5, 1),)


def test_vocalised_query_rejected_below_lemma_level(corpus, cfg):
    with pytest.raises(ValueError, match="vocalisée"):
        n("مَلَك", corpus, cfg, level="stem")


def test_root_groups_all_three_homographs(corpus, cfg):
    # racine ملك : مالِك (1:4:1), مَلِك, مَلَك
    assert n("ملك", corpus, cfg, level="root").n == 3


# --- muqatta'at -------------------------------------------------------------


def test_muqattaat_include_exclude(corpus, cfg):
    assert n("الم", corpus, cfg, level="form", text="uthmani", muqattaat="include").n == 1
    assert n("الم", corpus, cfg, level="form", text="uthmani", muqattaat="exclude").n == 0


# --- basmala ----------------------------------------------------------------


def test_basmala_three_states(corpus, cfg):
    # الله figure une fois en 1:1. as_text -> 1 ; none -> 0 ;
    # all -> 1 + 112 en-têtes (sourates 2..114 sauf 9)
    kw = {"level": "form", "text": "uthmani"}
    assert n("الله", corpus, cfg, basmala="as_text", **kw).n == 1
    assert n("الله", corpus, cfg, basmala="none", **kw).n == 0
    assert n("الله", corpus, cfg, basmala="all", **kw).n == 113


def test_basmala_all_counts_every_basmala_word(corpus, cfg):
    # racine رحم : 2 mots en 1:1 -> 2 + 2*112
    assert n("رحم", corpus, cfg, level="root", basmala="all").n == 226


def test_header_suras_are_112(corpus):
    assert len(corpus.basmala_header_suras) == 112
    assert 1 not in corpus.basmala_header_suras and 9 not in corpus.basmala_header_suras


# --- ventilation par nombre -------------------------------------------------


def test_number_breakdown(corpus, cfg):
    r = n("يوم", corpus, cfg, level="lemma", compounds="with_base")
    # 1:4:2 M->S ; 3:1:1 M->S ; 3:2:1 MP->P ; 3:4:1 MD->D ; composé 3:3:1 : non marqué
    assert r.by_number == {"S": 2, "P": 1, "D": 1, "?": 1}


@pytest.mark.parametrize(
    ("feats", "expected"),
    [
        ("ROOT:يوم|M|GEN", "S"),
        ("MP|GEN", "P"),
        ("FD|NOM", "D"),
        ("2MS", "S"),
        ("1P|IMPF", "P"),
        ("PN|GEN", "?"),
        ("T", "?"),
    ],
)
def test_number_of(feats, expected):
    assert number_of(feats) == expected
