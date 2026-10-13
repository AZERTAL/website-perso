from collections import Counter

from quran_lab.checks import check_report_text
from quran_lab.cli import main
from quran_lab.db import write_corpus
from quran_lab.multiverse import run
from quran_lab.provenance import raw_manifest_hash, sha256_file
from quran_lab.report import render_verification_report
from quran_lab.stats.nulls import coincidence_from_counts


def test_coincidence_counts_exact_hits_and_neighbour_baseline():
    # effectifs : deux types à 10, un type à 9, un à 11, aucun à 8/12
    tc = Counter({"a": 10, "b": 10, "c": 9, "d": 11, "e": 3})
    r = coincidence_from_counts(tc, target=10, window=2)
    assert r["observed_types_at_target"] == 2
    assert r["types_at_target"] == ["a", "b"]
    # voisins 8, 9, 11, 12 -> effectifs 0, 1, 1, 0 -> moyenne 0.5
    assert r["expected_types_at_target"] == 0.5


def test_manifest_hash_is_deterministic_and_content_sensitive(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / ".gitkeep").write_text("")
    h1 = raw_manifest_hash(tmp_path)
    assert h1 == raw_manifest_hash(tmp_path)
    (tmp_path / "a.txt").write_text("y")
    assert h1 != raw_manifest_hash(tmp_path)
    assert len(sha256_file(tmp_path / "a.txt")) == 64


def test_generated_report_passes_its_own_checker(corpus, cfg):
    m = run("يوم", corpus, cfg, target=2)
    text = render_verification_report(
        claim="le mot jour apparaît N fois",
        query="يوم",
        hypothesis="H000",
        command="cmd",
        raw_hash="abc1234",
        code="def5678",
        m=m,
        coincidences={"form": coincidence_from_counts(Counter({"x": 2}), 2)},
    )
    assert check_report_text(text) == []
    assert text == render_verification_report(
        claim="le mot jour apparaît N fois",
        query="يوم",
        hypothesis="H000",
        command="cmd",
        raw_hash="abc1234",
        code="def5678",
        m=m,
        coincidences={"form": coincidence_from_counts(Counter({"x": 2}), 2)},
    )  # déterministe


def test_cli_refuses_without_database(tmp_path, capsys):
    import pytest

    with pytest.raises(SystemExit) as e:
        main(["--db", str(tmp_path / "absent.duckdb"), "compte", "يوم"])
    assert e.value.code == 3
    assert "aucun chiffre" in capsys.readouterr().err


def test_cli_compte_end_to_end_on_fixture_db(corpus, tmp_path, capsys):
    db = tmp_path / "q.duckdb"
    write_corpus(corpus, db)
    assert main(["--db", str(db), "compte", "يوم", "--target", "4"]) == 0
    out = capsys.readouterr().out
    assert "| lemma |" in out and "DÉPEND DE LA RÈGLE" in out
