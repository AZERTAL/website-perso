import subprocess
from pathlib import Path

from quran_lab.checks import check_preregistration, check_report_text

HEAD = "---\ngenerated_by: cmd\ndata_manifest_sha256: abc1234\ncode_sha: def5678\n---\n"


def test_orphan_number_is_flagged():
    probs = check_report_text(HEAD + "Le mot apparaît 365 fois.\n")
    assert len(probs) == 1 and "365" in probs[0].msg


def test_numbers_inside_generated_block_and_code_are_ok():
    body = (
        "<!-- BEGIN generated:count -->\n| a | 365 |\n<!-- END generated -->\n"
        "```\nuv run x --target 365\n```\n"
    )
    assert check_report_text(HEAD + body) == []


def test_verse_refs_dates_ids_hashes_are_ok():
    body = "Voir 2:255 et 36:1:2, le 2026-10-13, H001-v2, commit 78d71c9.\n"
    assert check_report_text(HEAD + body) == []


def test_decimal_and_allow_marker():
    assert check_report_text(HEAD + "p = 0.03\n")
    assert check_report_text(HEAD + "p = 0.03 <!-- allow-number: seuil fixé en H001 -->\n") == []


def test_missing_fields_and_unclosed_block():
    probs = check_report_text("Rien.\n")
    assert {p.msg.split(" : ")[-1] for p in probs} >= set(("generated_by", "code_sha"))
    assert any("refermé" in p.msg for p in check_report_text(HEAD + "<!-- BEGIN generated:x -->\n"))


def _git(repo, *a, env=None):
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
            **(env or {}),
        },
    )


def test_preregistration_order(tmp_path: Path):
    repo = tmp_path
    _git(repo, "init", "-q")
    hyp, rep = repo / "hypotheses" / "H009.md", repo / "reports" / "r.md"
    hyp.parent.mkdir()
    rep.parent.mkdir()
    # rapport citant une hypothèse absente
    rep.write_text(HEAD.replace("---\n", "---\nhypothesis: H009\n", 1) + "x\n")
    assert "non pré-enregistrée" in check_preregistration(rep, hyp.parent, repo)[0].msg
    # hypothèse écrite mais pas commitée
    hyp.write_text("test")
    assert "pas encore commité" in check_preregistration(rep, hyp.parent, repo)[0].msg
    # ordre correct : hypothèse commitée en premier
    _git(repo, "add", str(hyp))
    _git(repo, "commit", "-qm", "h", env={"GIT_COMMITTER_DATE": "2026-01-01T00:00:00"})
    _git(repo, "add", str(rep))
    _git(repo, "commit", "-qm", "r", env={"GIT_COMMITTER_DATE": "2026-01-02T00:00:00"})
    assert check_preregistration(rep, hyp.parent, repo) == []
    # hypothèse modifiée après le rapport : refusé
    hyp.write_text("test changé après coup")
    _git(repo, "add", str(hyp))
    _git(repo, "commit", "-qm", "h2", env={"GIT_COMMITTER_DATE": "2026-01-03T00:00:00"})
    assert "APRÈS" in check_preregistration(rep, hyp.parent, repo)[0].msg
