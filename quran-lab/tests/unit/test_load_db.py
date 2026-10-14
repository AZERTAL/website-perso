from pathlib import Path

import pytest

from quran_lab.db import read_corpus, write_corpus
from quran_lab.load import (
    LoadReport,
    build_words,
    header_anomalies,
    parse_morphology,
    parse_tanzil,
    summarize,
    word_count_differences,
)

FIX = Path(__file__).resolve().parents[1] / "fixtures"


def test_fork_sample_parses_with_real_structure():
    rep = LoadReport()
    segs = parse_morphology((FIX / "fork_sample.txt").read_text(encoding="utf-8"), "fork", rep)
    assert rep.skipped_lines == []
    assert summarize(segs) == {"segments": 16, "words": 11, "PREF": 5, "STEM": 11}
    yawm = next(s for s in segs if s.loc == (1, 4, 2))
    assert (yawm.root, yawm.lemma, yawm.seg_type) == ("يوم", "يَوْم", "STEM")
    assert [s.seg_type for s in segs if s.loc == (1, 1, 3)] == ["PREF", "STEM"]


def test_v04_buckwalter_is_converted_and_header_is_reported_not_hidden():
    rep = LoadReport()
    segs = parse_morphology(
        (FIX / "v04_sample_UNVERIFIED.txt").read_text(encoding="utf-8"), "v04", rep
    )
    assert len(segs) == 3
    assert any("LOCATION" in line for line in rep.skipped_lines)  # l'en-tête est consigné
    yawm = segs[2]
    assert (yawm.root, yawm.form) == ("يوم", "يَوْمِ")
    assert yawm.lemma == "يَوْم"


def test_tanzil_parse_and_comments():
    text = "# Tanzil\n1|1|بِسْمِ ٱللَّهِ\n1|2|ٱلْحَمْدُ لِلَّهِ\n"
    assert parse_tanzil(text) == {(1, 1): "بِسْمِ ٱللَّهِ", (1, 2): "ٱلْحَمْدُ لِلَّهِ"}


def test_tanzil_rejects_duplicates_and_garbage():
    with pytest.raises(ValueError, match="double"):
        parse_tanzil("1|1|a\n1|1|b\n")
    with pytest.raises(ValueError, match="illisible"):
        parse_tanzil("n'importe quoi\n")


def test_each_orthography_keeps_its_own_words_and_positions():
    # cas réel : « يَـٰٓأَيُّهَا » = 1 mot en Uthmani, « يا أيها » = 2 en simple
    uth = {(2, 21): "يَـٰٓأَيُّهَا ٱلنَّاسُ"}
    sim = {(2, 21): "يا أيها الناس"}
    wu, ws = build_words(uth, "uthmani"), build_words(sim, "simple")
    assert [w.word for w in wu] == [1, 2] and [w.word for w in ws] == [1, 2, 3]
    assert {w.variant for w in wu} == {"uthmani"}
    assert word_count_differences(uth, sim) == [(2, 21, 2, 3)]  # signalé, jamais supprimé


def test_word_count_differences_rejects_mismatched_verse_sets():
    with pytest.raises(ValueError, match="une seule"):
        word_count_differences({(1, 1): "a"}, {(1, 2): "a"})


def test_duckdb_roundtrip(corpus, tmp_path):
    p = tmp_path / "q.duckdb"
    write_corpus(corpus, p)
    back = read_corpus(p)
    assert sorted(back.segments, key=lambda s: (s.loc, s.seg)) == sorted(
        corpus.segments, key=lambda s: (s.loc, s.seg)
    )
    key = lambda w: (w.variant, w.loc)  # noqa: E731
    assert sorted(back.words, key=key) == sorted(corpus.words, key=key)


def test_basmala_prefix_is_detected_by_comparison_not_by_assumed_length():
    verses = {
        (1, 1): "بسم الله الرحمن الرحيم",
        (2, 1): "بسم الله الرحمن الرحيم الم",
        (9, 1): "براءة من الله",
        (10, 1): "الر",
    }
    words = {w.loc: w for w in build_words(verses, "simple")}
    assert [words[(2, 1, i)].header for i in range(1, 6)] == [True] * 4 + [False]
    assert not words[(1, 1, 1)].header  # 1:1 est la basmala numérotée, pas un en-tête
    assert not words[(9, 1, 1)].header
    assert header_anomalies(verses) == [
        s for s in range(3, 115) if s != 9
    ]  # absentes ici, signalées
    assert 10 in header_anomalies(verses) and 2 not in header_anomalies(verses)
