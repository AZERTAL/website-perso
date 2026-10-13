"""Persistance DuckDB : une ligne par segment morphologique, plus les mots Tanzil."""

from __future__ import annotations

from pathlib import Path

import duckdb
import polars as pl

from quran_lab.model import Corpus, Segment, Word

_SEG_FIELDS = ("sura", "aya", "word", "seg", "form", "pos", "seg_type", "root", "lemma", "feats")
_SEG_COLS = ", ".join(_SEG_FIELDS)
_WORD_FIELDS = ("variant", "sura", "aya", "word", "text", "header")


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
            "CREATE TABLE words (variant VARCHAR, sura INT, aya INT, word INT, "
            "text VARCHAR, header BOOLEAN)"
        )
        # Insertion en bloc (executemany insère ligne par ligne : minutes pour 150 000 mots).
        if corpus.segments:
            segs = pl.DataFrame(
                {c: [getattr(s, c) for s in corpus.segments] for c in _SEG_FIELDS},
                schema_overrides={"root": pl.String, "lemma": pl.String},
            )
            con.register("segs_df", segs.to_arrow())
            con.execute(f"INSERT INTO segments SELECT {_SEG_COLS} FROM segs_df")
        words = pl.DataFrame({c: [getattr(w, c) for w in corpus.words] for c in _WORD_FIELDS})
        con.register("words_df", words.to_arrow())
        con.execute(f"INSERT INTO words SELECT {', '.join(_WORD_FIELDS)} FROM words_df")
    finally:
        con.close()


def read_corpus(path: Path) -> Corpus:
    con = duckdb.connect(str(path), read_only=True)
    try:
        segs = con.execute(
            f"SELECT {_SEG_COLS} FROM segments ORDER BY sura, aya, word, seg"
        ).fetchall()
        words = con.execute(
            "SELECT sura, aya, word, text, variant, header FROM words "
            "ORDER BY variant, sura, aya, word"
        ).fetchall()
    finally:
        con.close()
    return Corpus(
        words=tuple(Word(*r) for r in words),
        segments=tuple(Segment(*r) for r in segs),
    )
