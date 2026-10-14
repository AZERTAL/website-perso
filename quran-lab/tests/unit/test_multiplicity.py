import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from quran_lab.stats.multiplicity import (
    benjamini_hochberg,
    benjamini_yekutieli,
    bonferroni,
    holm,
    westfall_young_maxt,
)

# Exemple calculé À LA MAIN, dans l'ordre d'entrée (m = 4) :
P = [0.01, 0.04, 0.03, 0.005]


def test_bonferroni_by_hand():
    assert np.allclose(bonferroni(P), [0.04, 0.16, 0.12, 0.02])


def test_holm_by_hand():
    # triés : 0.005 -> 4x = 0.02 ; 0.01 -> 3x = 0.03 ; 0.03 -> 2x = 0.06 ; 0.04 -> 1x = 0.04
    # maximum cumulé : 0.02, 0.03, 0.06, 0.06
    assert np.allclose(holm(P), [0.03, 0.06, 0.06, 0.02])


def test_benjamini_hochberg_by_hand():
    # p*m/rang : 0.02, 0.02, 0.04, 0.04 ; minimum cumulé depuis la fin : 0.02, 0.02, 0.04, 0.04
    assert np.allclose(benjamini_hochberg(P), [0.02, 0.04, 0.04, 0.02])


def test_benjamini_yekutieli_is_bh_times_harmonic_sum():
    c = 1 + 1 / 2 + 1 / 3 + 1 / 4
    assert np.allclose(benjamini_yekutieli(P), np.array([0.02, 0.04, 0.04, 0.02]) * c)


def test_westfall_young_by_hand():
    null = [[1, 2], [3, 1], [0, 0]]  # maxima par ligne : 2, 3, 0
    p = westfall_young_maxt([2.5, 1.0], null)
    # 2.5 : un seul maximum >= 2.5 -> (1+1)/(3+1) ; 1.0 : deux -> (1+2)/(3+1)
    assert np.allclose(p, [0.5, 0.75])


def test_input_validation():
    with pytest.raises(ValueError):
        holm([0.1, 1.2])
    with pytest.raises(ValueError):
        bonferroni([float("nan")])
    assert len(holm([])) == 0


pvals = st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=1, max_size=40)


@given(pvals)
def test_adjusted_never_below_raw_and_within_unit_interval(p):
    p = np.array(p)
    for f in (bonferroni, holm, benjamini_hochberg, benjamini_yekutieli):
        a = f(p)
        assert (a >= p - 1e-12).all() and (a <= 1.0 + 1e-12).all()


@given(pvals)
def test_procedures_are_ordered_by_conservatism(p):
    p = np.array(p)
    assert (benjamini_hochberg(p) <= holm(p) + 1e-12).all()  # BH rejette au moins autant que Holm
    assert (holm(p) <= bonferroni(p) + 1e-12).all()
    assert (benjamini_hochberg(p) <= benjamini_yekutieli(p) + 1e-12).all()


@given(pvals)
def test_order_preserving(p):
    p = np.array(p)
    for f in (holm, benjamini_hochberg):
        a = f(p)
        idx = np.argsort(p, kind="stable")
        assert (np.diff(a[idx]) >= -1e-12).all()  # p plus petite -> p ajustée plus petite ou égale
