import pytest

from quran_lab.buckwalter import bw_to_ar


def test_matches_real_tokens_seen_in_corpus_fork():
    # formes réelles observées dans quran-morphology.txt (1:1)
    assert bw_to_ar("somi") == "سْمِ"
    assert bw_to_ar("{ll~ahi") == "ٱللَّهِ"
    assert bw_to_ar("yawomi") == "يَوْمِ"


def test_unknown_symbol_raises_instead_of_passing_silently():
    with pytest.raises(ValueError, match="inconnus"):
        bw_to_ar("abé")


def test_shadda_fatha_order_is_canonical():
    # Le corpus réel écrit fatha puis shadda ; Buckwalter l'inverse. NFC doit les unifier.
    assert bw_to_ar("l~a") == "لَّ"
