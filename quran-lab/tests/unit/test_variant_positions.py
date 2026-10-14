from dataclasses import replace

from quran_lab.count import count
from quran_lab.multiverse import run
from quran_lab.rules import Rules


def test_same_word_has_different_positions_in_each_orthography(corpus, cfg):
    # 3:7 synthétique : « الناس » est le mot 2 en Uthmani et le mot 3 en simple. Aucun n'est perdu.
    u = count("الناس", Rules("form", text="uthmani"), corpus, cfg)
    s = count("الناس", Rules("form", text="simple"), corpus, cfg)
    assert u.occurrences == ((3, 7, 2),)
    assert s.occurrences == ((3, 7, 3),)


def test_no_morphology_means_levels_not_evaluated_never_zero(corpus, cfg):
    words_only = replace(corpus, segments=())
    m = run("يوم", words_only, cfg, target=1)
    assert {c.rules.level for c in m.cells} == {"form"}
    assert len(m.cells) == 24
    assert m.not_evaluated == ("stem", "lemma", "root")
    assert (
        "PARTIEL" in m.reproduction_verdict() and "faute de morphologie" in m.reproduction_verdict()
    )
