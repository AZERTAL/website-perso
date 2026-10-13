from dataclasses import replace

from quran_lab.db import read_corpus, write_corpus


def test_words_only_database_roundtrip(corpus, tmp_path):
    words_only = replace(corpus, segments=())
    write_corpus(words_only, tmp_path / "w.duckdb")
    back = read_corpus(tmp_path / "w.duckdb")
    assert back.segments == () and not back.has_morphology
    assert len(back.words) == len(corpus.words)
    assert sum(w.header for w in back.words) == 8  # 4 mots d'en-tête x 2 orthographes
