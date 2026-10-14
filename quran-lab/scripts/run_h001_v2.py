#!/usr/bin/env python3
"""Exécute H001-v2 (espace de spécifications) -> reports/H001-v2-espace-de-regles.md.

Le test est défini dans hypotheses/H001-v2.md, commité avant ce script. Le script ne change
aucun paramètre de ce fichier.
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import date
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import read_corpus  # noqa: E402
from quran_lab.normalize import skeleton  # noqa: E402
from quran_lab.provenance import code_sha, raw_manifest_hash  # noqa: E402
from quran_lab.stats.ledger import Entry, append, read  # noqa: E402
from quran_lab.stats.spec_space import (  # noqa: E402
    TOGGLE_LABELS,
    TOGGLES,
    analyze,
    inert_toggles,
    parse_form,
    verdict,
)

TARGET, LO, HI, RANGE = 365, 360, 370, (340, 390)


def table(head, rows):
    return "\n".join(
        ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    )


def main() -> int:
    corpus = read_corpus(LAB / "data" / "quran.duckdb")
    tokens = {
        v: Counter(skeleton(w.text) for w in corpus.words if w.variant == v)
        for v in ("simple", "uthmani")
    }
    res = analyze(tokens)
    n = {t: res.n_of(t) for t in range(RANGE[0], RANGE[1] + 1)}
    neigh = {t: n[t] for t in range(LO, HI + 1) if t != TARGET}
    off = {(v, m) for (v, m) in res.totals}
    del off
    reviewer_mask = tuple(t in ("T1", "T2", "T3", "T4") for t in TOGGLES)
    rows_forms = []
    for skel, c in sorted(tokens["simple"].items(), key=lambda kv: -kv[1]):
        f = parse_form(skel)
        if f is not None:
            rows_forms.append((skel, c, ", ".join(sorted(f)) or "base"))
    cmd = "cd quran-lab && uv run python scripts/run_h001_v2.py"
    out = [
        f"---\ngenerated_by: {cmd}\n"
        f"data_manifest_sha256: {raw_manifest_hash(LAB / 'data' / 'raw')}\n"
        f"code_sha: {code_sha(LAB.parent)}\nhypothesis: H001-v2\n---",
        "# H001-v2 : espace de règles de forme et de clitiques",
        "",
        "Étiquette : `AFFIRMATION POPULAIRE` au départ. Test **post hoc**, déclaré comme tel dans "
        "`hypotheses/H001-v2.md`. Les décomptes sont des `FAIT` (texte Tanzil, analyse par "
        "expressions régulières, approximation de la morphologie).",
        "",
        "## Verdict (lecture pré-enregistrée)",
        "<!-- BEGIN generated:quran_lab.stats.spec_space.verdict -->",
        verdict(res, TARGET, LO, HI),
        "<!-- END generated -->",
        "",
        "Le statut ne peut pas dépasser `DÉPEND DE LA RÈGLE` : la règle atteignant la cible a été "
        "trouvée après lecture du résultat, et les modèles nuls ne sont pas implémentés.",
        "",
        "## N(T) : combien de spécifications donnent exactement T",
        "<!-- BEGIN generated:quran_lab.stats.spec_space.n_of -->",
        table(
            ["T", "N(T)", "rôle"],
            [
                (t, n[t], "cible" if t == TARGET else "voisin" if LO <= t <= HI else "")
                for t in range(RANGE[0], RANGE[1] + 1)
            ],
        ),
        "<!-- END generated -->",
        "",
        "<!-- BEGIN generated:quran_lab.stats.spec_space.summary -->",
        table(
            ["mesure", "valeur"],
            [
                ["spécifications", len(res.totals)],
                ["décomptes distincts", res.distinct_totals],
                ["interrupteurs sans effet", ", ".join(inert_toggles(res)) or "aucun"],
                ["N(cible)", n[TARGET]],
                ["max N(voisins)", max(neigh.values())],
            ],
        ),
        "<!-- END generated -->",
        "",
        "## La spécification citée par le relecteur",
        "<!-- BEGIN generated:quran_lab.stats.spec_space.reviewer_mask -->",
        table(
            ["texte", "interrupteurs actifs", "décompte"],
            [
                ("simple", "T1, T2, T3, T4", res.totals[("simple", reviewer_mask)]),
                ("uthmani", "T1, T2, T3, T4", res.totals[("uthmani", reviewer_mask)]),
            ],
        ),
        "<!-- END generated -->",
        "",
        "Cette spécification n'est qu'une parmi toutes ; elle a été trouvée en regardant le "
        "résultat. Sa valeur ne prouve rien tant qu'on ne sait pas combien de spécifications "
        "atteignent aussi les nombres voisins (tableau N(T) ci-dessus).",
        "",
        "## Interrupteurs",
        table(["code", "classe de formes incluse"], [(t, TOGGLE_LABELS[t]) for t in TOGGLES]),
        "",
        "## Formes reconnues (texte simple)",
        "<!-- BEGIN generated:quran_lab.stats.spec_space.parse_form -->",
        table(["forme", "occurrences", "classes"], rows_forms),
        "<!-- END generated -->",
        "",
        "## Mots contenant la séquence mais non reconnus (listés, jamais ignorés)",
        "<!-- BEGIN generated:quran_lab.stats.spec_space.unmatched -->",
        table(
            ["forme", "occurrences (texte simple, puis uthmani)"],
            [
                (k, f"{tokens['simple'].get(k, 0)} / {tokens['uthmani'].get(k, 0)}")
                for k in sorted(
                    {k for v in tokens.values() for k in v if "يوم" in k and parse_form(k) is None}
                )
            ],
        ),
        "<!-- END generated -->",
        "",
        "## Limites",
        "- Approximation par expressions régulières : ne remplace pas le corpus morphologique ; "
        "le test sera refait sur les vrais radicaux (`H001-v3`).",
        "- Le sens (jour calendaire, Jour du Jugement, période) n'est pas distingué.",
        "- Lecture Hafs ʿan ʿĀṣim, texte Tanzil uniquement.",
        "",
        "## Reproduction",
        "```",
        cmd,
        "```",
        "",
    ]
    (LAB / "reports" / "H001-v2-espace-de-regles.md").write_text("\n".join(out), encoding="utf-8")
    print("écrit : reports/H001-v2-espace-de-regles.md")
    ledger = LAB / "reports" / "tests_ledger.csv"
    if not any(e.test_id == "H001-v2" for e in read(ledger)):
        v = verdict(res, TARGET, LO, HI)
        append(
            ledger,
            Entry(
                "H001-v2",
                date.today().isoformat(),
                "H001-v2",
                "F-nombres",
                1,
                f"N({TARGET})={n[TARGET]} contre max N(voisins {LO}-{HI})={max(neigh.values())} "
                f"sur {len(res.totals)} spécifications",
                "n/a",
                "n/a",
                "NON REPRODUCTIBLE" if v.startswith("NON") else "DÉPEND DE LA RÈGLE",
            ),
        )
        print("registre : H001-v2 ajouté")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
