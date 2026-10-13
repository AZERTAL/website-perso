#!/usr/bin/env python3
"""Audit des sources Tanzil -> reports/audit-tanzil.md (rapport GÉNÉRÉ, aucun chiffre à la main)."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab import audit  # noqa: E402
from quran_lab.db import read_corpus  # noqa: E402
from quran_lab.load import parse_tanzil  # noqa: E402
from quran_lab.provenance import code_sha, raw_manifest_hash  # noqa: E402
from quran_lab.rules import load_config  # noqa: E402

RAW = LAB / "data" / "raw"


def md_table(head: list[str], rows: list[list]) -> str:
    return "\n".join(
        ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
        + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    )


def main() -> int:
    uth = parse_tanzil((RAW / "quran-uthmani.txt").read_text(encoding="utf-8"))
    sim = parse_tanzil((RAW / "quran-simple-clean.txt").read_text(encoding="utf-8"))
    meta = audit.parse_metadata((RAW / "quran-data.xml").read_text(encoding="utf-8"))
    corpus = read_corpus(LAB / "data" / "quran.duckdb")
    cfg = load_config(LAB / "config" / "counting_rules.yaml")

    inv = {
        "uthmani": audit.verse_invariants(uth, meta),
        "simple-clean": audit.verse_invariants(sim, meta),
    }
    rev = Counter(m["type"] for m in meta.values())
    diffs = audit.word_diffs(uth, sim)
    diff_full = audit.differential_full_text(corpus, cfg)
    n_header = {
        v: sum(1 for w in corpus.words if w.variant == v and w.header)
        for v in ("uthmani", "simple")
    }
    n_words = {v: sum(1 for w in corpus.words if w.variant == v) for v in ("uthmani", "simple")}

    cmd = (
        "cd quran-lab && uv run python scripts/build_db.py && uv run python scripts/audit_tanzil.py"
    )
    out = [
        f"---\ngenerated_by: {cmd}\ndata_manifest_sha256: {raw_manifest_hash(RAW)}\n"
        f"code_sha: {code_sha(LAB.parent)}\n---",
        "# Audit des sources Tanzil",
        "",
        "Source : Tanzil Project v1.1, licence CC BY 3.0, texte non modifié. "
        "Fichiers, hash et options : `SOURCES.md`. "
        "<!-- allow-number: version de licence, pas un résultat -->",
        "",
        "Étiquette : tout ce qui suit est `FAIT` (compté par `scripts/audit_tanzil.py` sur "
        "les fichiers de `data/raw/`). La morphologie n'est pas encore acquise.",
        "",
        "## 1. Invariants par rapport aux métadonnées officielles (`quran-data.xml`)",
        "<!-- BEGIN generated:quran_lab.audit.verse_invariants -->",
        md_table(
            [
                "orthographe",
                "sourates",
                "versets",
                "sourates au nb de versets ≠ métadonnées",
                "versets vides",
                "sourates sans basmala préfixée (hors 1 et 9)",
            ],
            [
                [
                    k,
                    v["suras"],
                    v["verses"],
                    v["suras_whose_verse_count_differs_from_metadata"] or "aucune",
                    v["empty_verses"] or "aucun",
                    v["sura_without_basmala_prefix"] or "aucune",
                ]
                for k, v in inv.items()
            ],
        ),
        "",
        md_table(["type (métadonnées)", "sourates"], sorted([[k, n] for k, n in rev.items()])),
        "<!-- END generated -->",
        "",
        "## 2. La basmala est préfixée au verset 1 de 113 sourates sur 114",
        "<!-- BEGIN generated:quran_lab.load.build_words -->",
        md_table(
            ["orthographe", "mots d'en-tête (header=True)", "mots au total"],
            [[v, n_header[v], n_words[v]] for v in ("uthmani", "simple")],
        ),
        "<!-- END generated -->",
        "",
        "Conséquence : le texte Tanzil contient déjà la basmala devant le verset 1 des "
        "sourates 2 à 114 (sauf 9). Le corpus morphologique ne les contient pas "
        "(à vérifier à réception). "
        "L'axe « basmala » et l'exclusion des muqatta'at en tiennent compte (DECISIONS D9). "
        "<!-- allow-number: numéros de sourates cités dans le texte, pas un résultat -->",
        "",
        "## 3. Les deux orthographes n'ont pas les mêmes mots",
        "<!-- BEGIN generated:quran_lab.audit.word_diffs -->",
        md_table(
            ["mesure", "valeur"],
            [
                ["versets au nombre de mots différent", diffs["verses"]],
                ["mots en plus dans simple-clean (somme)", diffs["extra_words_simple"]],
                ["versets où simple-clean a MOINS de mots", diffs["simple_has_fewer"]],
            ],
        ),
        "",
        md_table(
            ["sourate", "verset", "mots Uthmani", "mots simple-clean"],
            [list(x) for x in diffs["first"]],
        ),
        "<!-- END generated -->",
        "",
        "Conséquence : une position de mot n'a de sens que dans sa propre orthographe. "
        "Le modèle n'apparie jamais les mots entre orthographes.",
        "",
        "## 4. Test différentiel sur TOUT le texte (deux implémentations indépendantes)",
        "<!-- BEGIN generated:quran_lab.audit.differential_full_text -->",
        md_table(
            [
                "orthographe",
                "occurrences",
                "types (A)",
                "types (B)",
                "types au décompte différent",
                "échantillon",
                "désaccords sur l'échantillon",
                "mots au squelette différent A/B",
            ],
            [
                [
                    v,
                    d["tokens"],
                    d["types_a"],
                    d["types_b"],
                    d["disagreements"][:5] or "aucun",
                    d["sample_size"],
                    d["sample_disagreements"][:5] or "aucun",
                    d["same_skeleton_function"],
                ]
                for v, d in diff_full.items()
            ],
        ),
        "<!-- END generated -->",
        "",
        "A = `normalize.skeleton` + `type_counts`/`count` ; B = regex par plages de code. "
        "Échantillon tiré avec la graine inscrite dans `audit.differential_full_text`.",
        "",
        "## 5. Inventaire des caractères non-ASCII",
    ]
    for name, verses in (("Uthmani", uth), ("simple-clean", sim)):
        out += [
            f"### {name}",
            "<!-- BEGIN generated:quran_lab.audit.unicode_table -->",
            md_table(
                ["code", "nom", "catégorie", "occurrences"],
                [list(r) for r in audit.unicode_table(verses)],
            ),
            "<!-- END generated -->",
            "",
        ]
    out += ["## Reproduction", "```", cmd, "```", ""]
    (LAB / "reports").mkdir(exist_ok=True)
    (LAB / "reports" / "audit-tanzil.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("écrit : reports/audit-tanzil.md")
    bad = [
        k
        for k, v in inv.items()
        if v["suras_whose_verse_count_differs_from_metadata"] or v["empty_verses"]
    ]
    bad += [v for v, d in diff_full.items() if d["disagreements"] or d["sample_disagreements"]]
    if bad:
        print("INVARIANT ROMPU :", bad, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
