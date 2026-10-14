#!/usr/bin/env python3
"""Exécute H002 (formes de la séquence `عقل`) -> reports/H002-aql-formes.md. Définition : hypotheses/H002.md."""

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import read_corpus  # noqa: E402
from quran_lab.normalize import skeleton  # noqa: E402
from quran_lab.provenance import code_sha, raw_manifest_hash  # noqa: E402
from quran_lab.stats.form_classes import classify  # noqa: E402
from quran_lab.stats.ledger import Entry, append, read  # noqa: E402

NEEDLE = "عقل"
# Fixées dans hypotheses/H002.md avant tout calcul. L'ordre compte : verbal d'abord.
CLASSES = {
    "verbal": re.compile(r"[وف]?[يتن]عقل(ون|وا|ها|ه|ان|ن)?|[وف]?عقل(وه|وها|وا)"),
    "nominal": re.compile(r"[وف]?[بلك]?(ال)?(عقل|عقول|عاقل|عاقلة|معقول)(ا|ي|ك|هم|ه|ان|ين|ون)?"),
}


def table(head, rows):
    return "\n".join(
        ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    )


def main() -> int:
    corpus = read_corpus(LAB / "data" / "quran.duckdb")
    res = {}
    for v in ("simple", "uthmani"):
        toks = Counter(skeleton(w.text) for w in corpus.words if w.variant == v)
        res[v] = classify(toks, NEEDLE, CLASSES)
    n = {
        v: {c: sum(f.values()) for c, f in r[0].items()} | {"autre": sum(r[1].values())}
        for v, r in res.items()
    }
    nominal = max(n[v]["nominal"] for v in n)
    other = max(n[v]["autre"] for v in n)
    verdict = (
        "NON REPRODUCTIBLE"
        if nominal > 0
        else "PARTIEL (formes « autre » à classer à la main)"
        if other > 0
        else "REPRODUIT sur ce périmètre"
    )
    cmd = "cd quran-lab && uv run python scripts/run_h002.py"
    out = [
        f"---\ngenerated_by: {cmd}\n"
        f"data_manifest_sha256: {raw_manifest_hash(LAB / 'data' / 'raw')}\n"
        f"code_sha: {code_sha(LAB.parent)}\nhypothesis: H002\n---",
        "# H002 : formes de la séquence `عقل`",
        "",
        "Étiquette : `AFFIRMATION POPULAIRE` au départ ; les décomptes sont des `FAIT` (texte Tanzil). "
        "Classement par expressions régulières fixées dans `hypotheses/H002.md` : approximation de la "
        "morphologie, à confirmer avec le corpus morphologique.",
        "",
        "## Verdict (lecture pré-enregistrée)",
        "<!-- BEGIN generated:scripts.run_h002.verdict -->",
        verdict,
        "<!-- END generated -->",
        "",
        "## Décomptes par classe et par orthographe",
        "<!-- BEGIN generated:quran_lab.stats.form_classes.classify -->",
        table(
            ["orthographe", "verbal", "nominal", "autre"],
            [(v, n[v]["verbal"], n[v]["nominal"], n[v]["autre"]) for v in n],
        ),
        "<!-- END generated -->",
    ]
    for v in res:
        classes, rest = res[v]
        out += [
            "",
            f"## Formes rencontrées ({v})",
            "<!-- BEGIN generated:quran_lab.stats.form_classes.forms -->",
        ]
        rows = [(c, f, k) for c, forms in classes.items() for f, k in forms.most_common()]
        rows += [("autre", f, k) for f, k in rest.most_common()]
        out += [
            table(["classe", "forme (squelette)", "occurrences"], rows) if rows else "aucune forme",
            "<!-- END generated -->",
        ]
    out += [
        "",
        "## Limites",
        "- Approximation par expressions régulières ; le sens n'est pas distingué.",
        "- La forme nue est classée nominale par prudence (elle pourrait être un verbe à l'accompli).",
        "- Lecture Hafs ʿan ʿĀṣim, texte Tanzil uniquement.",
        "",
        "## Reproduction",
        "```",
        cmd,
        "```",
        "",
    ]
    (LAB / "reports" / "H002-aql-formes.md").write_text("\n".join(out), encoding="utf-8")
    print("écrit : reports/H002-aql-formes.md |", verdict)
    ledger = LAB / "reports" / "tests_ledger.csv"
    if not any(e.test_id == "H002" for e in read(ledger)):
        status = (
            "NON REPRODUCTIBLE" if nominal > 0 else "PARTIEL" if other > 0 else "DÉPEND DE LA RÈGLE"
        )
        append(
            ledger,
            Entry(
                "H002",
                date.today().isoformat(),
                "H002",
                "F-existence",
                1,
                f"formes nominales : {nominal} ; non classées : {other}",
                "n/a",
                "n/a",
                status,
            ),
        )
        print("registre : H002 ajouté")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
