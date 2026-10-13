"""Vérification des rapports : chiffres orphelins et pré-enregistrement. Stdlib uniquement.

Règle 1 (chiffres) : hors blocs générés, hors blocs de code, hors titres, tout entier >= 10 ou
tout décimal est refusé, sauf références de versets (s:a), dates, identifiants Hnnn, hash, ou
ligne marquée `<!-- allow-number: raison -->`. Les chiffres vivent dans les blocs générés.

Règle 2 (pré-enregistrement) : un rapport qui cite `hypothesis: Hxxx` exige que
hypotheses/Hxxx.md existe et n'ait pas été modifié après le premier commit du rapport.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

REQUIRED_FIELDS = ("generated_by", "data_manifest_sha256", "code_sha")
_ALLOWED = re.compile(
    r"\d+:\d+(?::\d+)?"  # référence de verset
    r"|\d{4}-\d{2}-\d{2}"  # date
    r"|\bH\d+(?:-v\d+)?\b"  # identifiant d'hypothèse
    r"|\b[0-9a-f]{7,64}\b"  # hash
    r"|\bN[0-5]\b|\bF-\w+"  # nuls et familles
)
_NUMBER = re.compile(r"(?<![\w.])\d+[.,]\d+|(?<![\w.:])\d{2,}(?![\w:])")
_GEN_BEGIN = re.compile(r"<!--\s*BEGIN generated:(\S+)\s*-->")
_GEN_END = re.compile(r"<!--\s*END generated\s*-->")


@dataclass(frozen=True)
class Problem:
    path: str
    line: int
    msg: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.msg}"


def parse_front_matter(text: str) -> tuple[dict[str, str], int]:
    """Renvoie (champs, numéro de la première ligne du corps)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, 1
    fields: dict[str, str] = {}
    for i, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return fields, i + 1
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return {}, 1


def check_report_text(text: str, path: str = "<rapport>") -> list[Problem]:
    problems: list[Problem] = []
    fields, body_start = parse_front_matter(text)
    for f in REQUIRED_FIELDS:
        if not fields.get(f):
            problems.append(Problem(path, 1, f"champ obligatoire manquant : {f}"))
    in_code = in_gen = False
    for n, line in enumerate(text.splitlines(), start=1):
        if n < body_start:
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if _GEN_BEGIN.search(line):
            in_gen = True
            continue
        if _GEN_END.search(line):
            in_gen = False
            continue
        if in_code or in_gen or line.lstrip().startswith("#") or "allow-number" in line:
            continue
        stripped = _ALLOWED.sub(" ", re.sub(r"<!--.*?-->", " ", line))
        m = _NUMBER.search(stripped)
        if m:
            problems.append(
                Problem(
                    path,
                    n,
                    f"chiffre « {m.group()} » hors bloc généré (ajouter un bloc "
                    "<!-- BEGIN generated:script --> ou <!-- allow-number: raison -->)",
                )
            )
    if in_gen:
        problems.append(Problem(path, 1, "bloc généré jamais refermé"))
    return problems


def _git(args: list[str], cwd: Path) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def check_preregistration(report: Path, hyp_dir: Path, repo: Path) -> list[Problem]:
    fields, _ = parse_front_matter(report.read_text(encoding="utf-8"))
    hid = fields.get("hypothesis")
    if not hid:
        return []
    hyp = hyp_dir / f"{hid}.md"
    if not hyp.exists():
        return [Problem(str(report), 1, f"hypothèse {hid} non pré-enregistrée ({hyp} absent)")]
    first_report = _git(["log", "--diff-filter=A", "--format=%ct", "--", str(report)], repo)
    last_hyp = _git(["log", "-1", "--format=%ct", "--", str(hyp)], repo)
    if not last_hyp:
        return [
            Problem(
                str(report),
                1,
                f"{hyp.name} n'est pas encore commité : pré-enregistrer "
                "(commit) AVANT les résultats",
            )
        ]
    if first_report and int(last_hyp) > int(first_report.splitlines()[-1]):
        return [
            Problem(
                str(report),
                1,
                f"{hyp.name} modifié APRÈS le premier commit du rapport : "
                f"ouvrir {hid}-v2 au lieu de modifier le test",
            )
        ]
    return []


def check_all(lab: Path, repo: Path) -> list[Problem]:
    problems: list[Problem] = []
    for rep in sorted((lab / "reports").glob("*.md")):
        problems += check_report_text(rep.read_text(encoding="utf-8"), str(rep.relative_to(repo)))
        problems += check_preregistration(rep, lab / "hypotheses", repo)
    return problems
