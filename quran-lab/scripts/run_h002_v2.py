#!/usr/bin/env python3
"""Exécute H002-v2 (candidats élargis) -> reports/H002-v2-aql-candidats-elargis.md. Définition : hypotheses/H002-v2.md."""

from __future__ import annotations

import json
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

CANDIDATE = re.compile(r"ع.{0,2}ق.{0,2}ل")  # fixé dans H002-v2
CLASSES = {
    "verbal": re.compile(r"[وف]?[يتن]عقل(ون|وا|ها|ه|ان|ن)?|[وف]?عقل(وه|وها|وا)"),
    "nominal": re.compile(
        r"[وف]?[بلك]?(ال)?م?(عقل|عقول|عاقل|عاقلة|عاقلون|معقول)(ا|ي|ك|هم|ه|ان|ين|ون)?"
    ),
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
        res[v] = classify(toks, lambda t: bool(CANDIDATE.search(t)), CLASSES)
    n = {
        v: {c: sum(f.values()) for c, f in r[0].items()} | {"autre": sum(r[1].values())}
        for v, r in res.items()
    }
    nominal = max(n[v]["nominal"] for v in n)
    other_n = max(n[v]["autre"] for v in n)
    verdict = (
        "NON REPRODUCTIBLE"
        if nominal > 0
        else "PARTIEL (formes « autre » à classer à la main dans ce rapport)"
        if other_n > 0
        else "REPRODUIT sur ce périmètre"
    )
    cmd = "cd quran-lab && uv run python scripts/run_h002_v2.py"
    out = [
        f"---\ngenerated_by: {cmd}\n"
        f"data_manifest_sha256: {raw_manifest_hash(LAB / 'data' / 'raw')}\n"
        f"code_sha: {code_sha(LAB.parent)}\nhypothesis: H002-v2\n---",
        "# H002-v2 : formes de la racine `عقل`, candidats élargis",
        "",
        "Étiquette : `AFFIRMATION POPULAIRE` au départ ; décomptes `FAIT` (texte Tanzil). Essai de "
        "réfutation de H002 : le filtre de candidats accepte les lettres intercalées (`عاقل`, `عقول`).",
        "",
        "## Verdict (lecture pré-enregistrée)",
        "<!-- BEGIN generated:scripts.run_h002_v2.verdict -->",
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
        "- Les faux positifs (mots d'une autre racine) sont listés dans la classe « autre ».",
        "- Lecture Hafs ʿan ʿĀṣim, texte Tanzil uniquement.",
        "",
        "## Reproduction",
        "```",
        cmd,
        "```",
        "",
    ]
    (LAB / "reports" / "H002-v2-aql-candidats-elargis.md").write_text(
        "\n".join(out), encoding="utf-8"
    )
    (LAB / "reports" / "H002-v2.json").write_text(
        json.dumps(
            {
                "verdict": verdict,
                "counts": n,
                "forms": [[f, k] for f, k in res["simple"][0]["verbal"].most_common()],
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    print("écrit : reports/H002-v2-aql-candidats-elargis.md |", verdict)
    ledger = LAB / "reports" / "tests_ledger.csv"
    if not any(e.test_id == "H002-v2" for e in read(ledger)):
        status = (
            "NON REPRODUCTIBLE"
            if nominal > 0
            else "PARTIEL"
            if other_n > 0
            else "DÉPEND DE LA RÈGLE"
        )
        append(
            ledger,
            Entry(
                "H002-v2",
                date.today().isoformat(),
                "H002-v2",
                "F-existence",
                1,
                f"formes nominales : {nominal} ; non classées : {other_n}",
                "n/a",
                "n/a",
                status,
            ),
        )
        print("registre : H002-v2 ajouté")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
