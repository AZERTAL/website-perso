from collections import Counter

import pytest

from quran_lab.stats.spec_space import (
    TOGGLES,
    analyze,
    inert_toggles,
    parse_form,
    verdict,
)


@pytest.mark.parametrize(
    ("skel", "expected"),
    [
        ("يوم", set()),
        ("واليوم", {"T1", "T3"}),
        ("باليوم", {"T2", "T3"}),
        ("يوما", {"T4"}),
        ("يومين", {"T5"}),
        ("يومكم", {"T6"}),
        ("يومئذ", {"T7"}),
        ("فيومئذ", {"T1", "T7"}),
        ("أيام", {"T8"}),
        ("بأيامهم".replace("هم", "ه"), {"T2", "T6", "T8"}),
        ("الأيام", {"T3", "T8"}),
    ],
)
def test_parse_form(skel, expected):
    assert parse_form(skel) == frozenset(expected)


def test_non_day_words_are_not_matched():
    # « al-Qayyum » contient la séquence mais n'est pas le mot jour
    assert parse_form("القيوم") is None
    assert parse_form("يومئذا") is None


def test_totals_hand_computed():
    # base 10, article 3, accusatif indéfini 2, composé 4
    tokens = {"simple": Counter({"يوم": 10, "اليوم": 3, "يوما": 2, "يومئذ": 4, "القيوم": 7})}
    res = analyze(tokens)
    off = (False,) * len(TOGGLES)

    def mask(*on):
        return tuple(t in on for t in TOGGLES)

    assert res.totals[("simple", off)] == 10  # la base seule
    assert res.totals[("simple", mask("T3"))] == 13
    assert res.totals[("simple", mask("T4"))] == 12
    assert res.totals[("simple", mask("T3", "T4"))] == 15
    assert res.totals[("simple", mask("T7"))] == 14
    assert res.unmatched == {"القيوم": 7}  # listé, jamais ignoré en silence
    assert len(res.totals) == 256  # 2^8 interrupteurs pour un texte


def test_n_of_counts_specs_with_exact_total():
    tokens = {"simple": Counter({"يوم": 10, "اليوم": 3})}
    res = analyze(tokens)
    # 7 interrupteurs sans effet ; T3 éteint -> 10, allumé -> 13 : la moitié des 256 chacun
    assert res.n_of(10) == 128 and res.n_of(13) == 128 and res.n_of(11) == 0


def test_inert_toggles_detected():
    tokens = {"simple": Counter({"يوم": 10, "اليوم": 3})}
    res = analyze(tokens)
    assert set(inert_toggles(res)) == set(TOGGLES) - {"T3"}


def test_totals_are_monotone_in_the_toggles():
    tokens = {"simple": Counter({"يوم": 5, "واليوم": 2, "يوما": 1, "يومين": 1, "أيام": 4})}
    res = analyze(tokens)
    for (text, mask), v in res.totals.items():
        for i in range(len(TOGGLES)):
            if not mask[i]:
                assert res.totals[(text, mask[:i] + (True,) + mask[i + 1 :])] >= v


def test_verdict_follows_the_preregistered_reading():
    assert "NON REPRODUCTIBLE" in verdict(analyze({"simple": Counter({"يوم": 10})}))
    # 365 atteint par 128 spécifications, exactement comme un voisin : non remarquable
    tokens = {"simple": Counter({"يوم": 360, "اليوم": 5, "يوما": 5})}
    res = analyze(tokens)
    assert res.n_of(365) > 0
    assert "pas plus que ses voisins" in verdict(res) or "plus que ses voisins" in verdict(res)
    assert "ROBUSTE" not in verdict(res)  # interdit par la prereg
