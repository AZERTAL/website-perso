from pathlib import Path

import pytest

from quran_lab.db import read_corpus, write_corpus
from quran_lab.load import LoadReport, build_words, parse_morphology, parse_tanzil, summarize

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


def test_build_words_reports_mismatch_instead_of_guessing():
    rep = LoadReport()
    words = build_words({(1, 1): "a b", (1, 2): "c d e"}, {(1, 1): "a b", (1, 2): "c d"}, rep)
    assert [w.loc for w in words] == [(1, 1, 1), (1, 1, 2)]
    assert rep.word_count_mismatches == [(1, 2, 3, 2)]


def test_duckdb_roundtrip(corpus, tmp_path):
    p = tmp_path / "q.duckdb"
    write_corpus(corpus, p)
    back = read_corpus(p)
    assert sorted(back.segments, key=lambda s: (s.loc, s.seg)) == sorted(
        corpus.segments, key=lambda s: (s.loc, s.seg)
    )
    assert sorted(back.words, key=lambda w: w.loc) == sorted(corpus.words, key=lambda w: w.loc)
