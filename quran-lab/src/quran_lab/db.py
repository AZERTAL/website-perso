"""Persistance DuckDB : une ligne par segment morphologique, plus les mots Tanzil."""

from __future__ import annotations

from pathlib import Path

import duckdb

from quran_lab.model import Corpus, Segment, Word

_SEG_COLS = "sura, aya, word, seg, form, pos, seg_type, root, lemma, feats"


def write_corpus(corpus: Corpus, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    con = duckdb.connect(str(path))
    try:
        con.execute(
            "CREATE TABLE segments (sura INT, aya INT, word INT, seg INT, form VARCHAR, "
            "pos VARCHAR, seg_type VARCHAR, root VARCHAR, lemma VARCHAR, feats VARCHAR)"
        )
        con.execute(
            "CREATE TABLE words (sura INT, aya INT, word INT, uthmani VARCHAR, simple VARCHAR)"
        )
        con.executemany(
            "INSERT INTO segments VALUES (?,?,?,?,?,?,?,?,?,?)",
            [
                (s.sura, s.aya, s.word, s.seg, s.form, s.pos, s.seg_type, s.root, s.lemma, s.feats)
                for s in corpus.segments
            ],
        )
        con.executemany(
            "INSERT INTO words VALUES (?,?,?,?,?)",
            [(w.sura, w.aya, w.word, w.uthmani, w.simple) for w in corpus.words],
        )
    finally:
        con.close()


def read_corpus(path: Path) -> Corpus:
    con = duckdb.connect(str(path), read_only=True)
    try:
        segs = con.execute(
            f"SELECT {_SEG_COLS} FROM segments ORDER BY sura, aya, word, seg"
        ).fetchall()
        words = con.execute(
            "SELECT sura, aya, word, uthmani, simple FROM words ORDER BY sura, aya, word"
        ).fetchall()
    finally:
        con.close()
    return Corpus(
        words=tuple(Word(*r) for r in words),
        segments=tuple(Segment(*r) for r in segs),
    )
