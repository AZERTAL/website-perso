"""Lois qui doivent tenir pour N'IMPORTE QUEL corpus bien formé."""

from quran_lab.count import count, type_counts
from quran_lab.model import Segment
from quran_lab.multiverse import Multiverse, run
from quran_lab.normalize import skeleton
from quran_lab.rules import Rules, grid
from quran_lab.validate import lemma_root_conflicts


def test_every_word_belongs_to_its_own_stem_lemma_and_root_queries(corpus, cfg):
    """Loi correcte : un mot est dans les décomptes de SON radical, SON lemme exact, SA racine.

    (Contre-exemple à la loi naïve « radical ⊆ lemme » : مَلِك et مَلَك partagent un
    squelette mais ont deux lemmes, et أيام n'a pas le squelette de son lemme يوم.)
    """
    sep = {"compounds": "separate"}
    for loc, segs in corpus.segments_by_word.items():
        for st in (s for s in segs if s.seg_type == "STEM" and s.lemma and s.root):
            assert loc in count(skeleton(st.form), Rules("stem", **sep), corpus, cfg).occurrences
            assert loc in count(st.lemma, Rules("lemma", **sep), corpus, cfg).occurrences
            assert loc in count(st.root, Rules("root", **sep), corpus, cfg).occurrences


def test_exact_lemma_is_contained_in_its_root(corpus, cfg):
    """Vrai ssi chaque lemme n'a qu'une racine (voir validate.lemma_root_conflicts)."""
    assert lemma_root_conflicts(corpus) == {}
    sep = {"compounds": "separate"}
    for s in corpus.segments:
        if s.seg_type == "STEM" and s.lemma and s.root:
            lem = count(s.lemma, Rules("lemma", **sep), corpus, cfg)
            root = count(s.root, Rules("root", **sep), corpus, cfg)
            assert set(lem.occurrences) <= set(root.occurrences)


def test_lemma_root_conflict_is_detected(corpus):
    from dataclasses import replace

    bad = replace(
        corpus,
        segments=(*corpus.segments, Segment(9, 9, 9, 1, "x", "N", "STEM", "ملك", "يَوْم", "")),
    )
    assert lemma_root_conflicts(bad) == {"يَوْم": {"يوم", "ملك"}}


def test_two_code_paths_agree(corpus, cfg):
    """`count` (une requête) et `type_counts` (tous les types, une passe) doivent concorder."""
    bases = set(cfg.compounds.values())
    for r in grid():
        if (r.basmala == "all_113" and r.level != "form") or r.compounds != "separate":
            continue
        tc = type_counts(r, corpus, cfg)
        for t, expected in tc.items():
            if skeleton(t) in bases:
                continue  # type_counts ignore la règle des composés (documenté)
            assert count(t, r, corpus, cfg).n == expected, (r.label(), t)


def test_counts_are_order_independent(corpus, cfg):
    from dataclasses import replace

    shuffled = replace(
        corpus,
        words=tuple(reversed(corpus.words)),
        segments=tuple(reversed(corpus.segments)),
    )
    for r in grid():
        a = count("يوم", r, corpus, cfg)
        b = count("يوم", r, shuffled, cfg)
        assert sorted(a.occurrences) == sorted(b.occurrences), r.label()


def test_multiverse_never_confuses_missing_with_zero(corpus, cfg):
    m = run("يوم", corpus, cfg, target=999)
    assert len(m.cells) == 60  # les cellules n/a ne sont pas dans la grille
    assert "NON REPRODUCTIBLE" in m.reproduction_verdict()


def test_verdict_logic():
    from quran_lab.count import CountResult

    def cell(n, hit):
        from quran_lab.multiverse import Cell

        r = Rules("lemma")
        return Cell(r, CountResult("x", r, tuple((1, 1, i) for i in range(n)), {}, {}), hit)

    assert "DÉPEND" in Multiverse("x", 3, (cell(3, True), cell(4, False))).reproduction_verdict()
    assert "toutes" in Multiverse("x", 3, (cell(3, True),)).reproduction_verdict()
    assert Multiverse("x", None, (cell(3, None),)).reproduction_verdict() == "pas de cible"
