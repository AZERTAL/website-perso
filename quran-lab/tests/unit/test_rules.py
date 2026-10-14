import pytest

from quran_lab.rules import Rules, grid


def test_grid_size_is_60():
    # form : 3 basmala x 2 muq x 2 texte x 2 composés = 24 ; stem/lemma/root : 3x2x1x2 = 12 chacun
    assert len(grid()) == 24 + 3 * 12 == 60


def test_grid_cells_are_unique():
    labels = [r.label() for r in grid()]
    assert len(set(labels)) == len(labels)


def test_text_axis_is_na_below_form_level():
    assert all(r.text is None for r in grid() if r.level != "form")
    assert all(r.text is not None for r in grid() if r.level == "form")


def test_inapplicable_cells_cannot_be_built():
    with pytest.raises(ValueError, match="n/a"):
        Rules("lemma", text="uthmani")
    with pytest.raises(ValueError, match="obligatoire"):
        Rules("form")
