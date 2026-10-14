from collections import Counter

import pytest

from quran_lab.model import Corpus, Word
from quran_lab.passages import Query, load_queries, search, verse_tokens
from quran_lab.stats.form_classes import classify


def corpus_of(verses: dict[tuple[int, int], str], headers=()) -> Corpus:
    words = []
    for (s, a), text in verses.items():
        for i, t in enumerate(text.split(), 1):
            words.append(Word(s, a, i, t, "simple", header=(s, a, i) in headers))
    return Corpus(words=tuple(words), segments=())


VERSES = {
    (2, 1): "لعلكم تعقلون وقال لعلكم تعقلون",
    (3, 4): "أفلا تعقلون",
    (3, 5): "يعقلون والذين يعقلون",
    (4, 1): "بسم الله لعلكم تعقلون",  # 3 premiers mots = basmala préfixée (header)
}


def vt():
    return verse_tokens(corpus_of(VERSES, headers={(4, 1, 1), (4, 1, 2)}))


def q(kind, text):
    return Query("t", kind, text, "")


def test_word_query_counts_occurrences_with_clitics():
    r = search(q("word", "يعقلون"), vt())
    assert r.n_occurrences == 2 and r.verses == ["3:5"]
    # « والذين يعقلون » : le mot est le second ; « ويعقلون » serait accepté (clitique)
    r2 = search(q("word", "تعقلون"), vt())
    assert r2.n_occurrences == 4 and r2.n_suras == 3


def test_phrase_query_requires_consecutive_words_in_one_verse():
    r = search(q("phrase", "لعلكم تعقلون"), vt())
    assert [h.ref for h in r.hits] == ["2:1", "2:1", "4:1"]
    assert search(q("phrase", "تعقلون لعلكم"), vt()).n_occurrences == 0
    # deux mots à cheval sur deux versets ne comptent pas
    assert search(q("phrase", "تعقلون أفلا"), vt()).n_occurrences == 0


def test_first_word_of_a_phrase_may_carry_a_conjunction():
    assert search(q("phrase", "قال لعلكم"), vt()).n_occurrences == 1  # « وقال لعلكم »


def test_header_words_are_excluded_from_verses():
    toks = vt()[(4, 1)]
    assert toks == ["لعلكم", "تعقلون"]
    assert [h.start for h in search(q("phrase", "لعلكم تعقلون"), vt()).hits if h.ref == "4:1"] == [
        1
    ]


def test_absent_expression_is_a_result_not_an_error():
    r = search(q("phrase", "ألف سنة"), vt())
    assert r.n_occurrences == 0 and r.verses == []


def test_query_text_is_normalised_like_the_corpus():
    assert search(q("word", "تَعْقِلُونَ"), vt()).n_occurrences == 4  # diacritiques ignorés


def test_load_queries_rejects_duplicates_and_unknown_kinds(tmp_path):
    p = tmp_path / "x.yaml"
    p.write_text(
        "domain: d\ntitle: t\nqueries:\n  - {id: a, kind: word, text: x, why: w}\n"
        "  - {id: a, kind: word, text: y, why: w}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="double"):
        load_queries(p)
    p.write_text(
        "domain: d\ntitle: t\nqueries:\n  - {id: a, kind: regex, text: x, why: w}\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="kind"):
        load_queries(p)


def test_real_query_files_load_and_have_unique_ids():
    from pathlib import Path

    d = Path(__file__).resolve().parents[2] / "config" / "queries"
    files = sorted(d.glob("*.yaml"))
    assert len(files) >= 5
    ids = []
    for f in files:
        _, _, qs = load_queries(f)
        ids += [x.id for x in qs]
    assert len(ids) == len(set(ids))


import re  # noqa: E402


def test_classify_lists_unclassified_candidates_and_first_class_wins():
    toks = Counter({"يعقلون": 5, "العقل": 2, "عقلوه": 1, "معقلا": 3, "يسمعون": 9})
    classes = {
        "verbal": re.compile(r"[وف]?[يتن]عقل(ون)?|[وف]?عقلوه"),
        "nominal": re.compile(r"(ال)?عقل"),
    }
    out, other = classify(toks, "عقل", classes)
    assert out["verbal"] == Counter({"يعقلون": 5, "عقلوه": 1})
    assert out["nominal"] == Counter({"العقل": 2})
    assert other == Counter({"معقلا": 3})  # listé, jamais ignoré
    assert "يسمعون" not in other  # pas un candidat


def test_classify_accepts_a_candidate_predicate_for_infix_letters():
    import re as _re

    toks = Counter({"عاقل": 2, "تعقلون": 4, "عقول": 1, "علم": 9})
    cand = _re.compile(r"ع.{0,2}ق.{0,2}ل")
    classes = {
        "verbal": _re.compile(r"[يتن]عقل(ون)?"),
        "nominal": _re.compile(r"(عاقل|عقول)"),
    }
    out, other = classify(toks, lambda t: bool(cand.search(t)), classes)
    # le filtre contigu `عقل` aurait manqué « عاقل » et « عقول » : zéro nominal par artefact
    assert out["nominal"] == Counter({"عاقل": 2, "عقول": 1})
    assert out["verbal"] == Counter({"تعقلون": 4}) and not other
    assert sum(classify(toks, "عقل", classes)[0]["nominal"].values()) == 0
