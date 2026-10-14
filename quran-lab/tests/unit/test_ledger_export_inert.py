import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from quran_lab.checks import check_ledger
from quran_lab.export import WORD_COLUMNS, word_rows
from quran_lab.multiverse import inert_axes, run
from quran_lab.stats import ledger

E = ledger.Entry("H900", "2026-10-14", "H900", "F-test", 1, "stat", "n/a", "n/a", "PARTIEL")


def test_ledger_append_only_and_totals(tmp_path):
    p = tmp_path / "l.csv"
    ledger.append(p, E)
    ledger.append(p, replace(E, test_id="H901", n_comparisons=3))
    assert [e.test_id for e in ledger.read(p)] == ["H900", "H901"]
    assert ledger.total_comparisons(p) == 4
    with pytest.raises(ValueError, match="déjà présent"):
        ledger.append(p, E)  # on n'écrase jamais un test
    assert p.read_text(encoding="utf-8").splitlines()[0].startswith("test_id,date")


def _git(repo, *a):
    subprocess.run(
        ["git", *a],
        cwd=repo,
        check=True,
        capture_output=True,
        env={
            "GIT_AUTHOR_NAME": "t",
            "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t",
            "GIT_COMMITTER_EMAIL": "t@t",
            "PATH": "/usr/bin:/bin",
        },
    )


def test_check_ledger_refuses_rewritten_history(tmp_path: Path):
    lab = tmp_path / "quran-lab"
    path = lab / "reports" / "tests_ledger.csv"
    _git(tmp_path, "init", "-q")
    ledger.append(path, E)
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "l")
    ledger.append(path, replace(E, test_id="H901"))  # ajout : accepté
    assert check_ledger(lab, tmp_path) == []
    path.write_text(
        path.read_text(encoding="utf-8").replace("PARTIEL", "ROBUSTE"), encoding="utf-8"
    )
    assert "ajout de lignes" in check_ledger(lab, tmp_path)[0].msg  # réécriture : refusée


def test_inert_axes_for_a_word_without_basmala_effect(corpus, cfg):
    words_only = replace(corpus, segments=())
    m = run("يوم", words_only, cfg)
    # « يوم » n'apparaît ni dans la basmala ni dans les lettres isolées : ces axes sont inertes,
    # l'orthographe aussi dans la fixture, mais pas les composés
    inert = inert_axes(m)
    assert "basmala" in inert and "muqattaat" in inert
    assert "compounds" not in inert


def test_export_rows_are_verbatim_plus_derived(corpus):
    rows = word_rows(corpus)
    assert len(rows) == len(corpus.words)
    assert len(rows[0]) == len(WORD_COLUMNS)
    r = next(x for x in rows if x[0] == "uthmani" and x[1:4] == (1, 4, 2))
    assert r[4] == "يَوْمِ" and r[5] == "يوم" and r[6] is False  # texte verbatim, squelette dérivé
