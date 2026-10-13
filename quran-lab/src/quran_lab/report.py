"""Rendu Markdown des résultats. Déterministe (aucun horodatage) : régénérer redonne le même octet.

Tout chiffre est placé dans un bloc `<!-- BEGIN generated:... -->` que `checks.py` reconnaît.
"""

from __future__ import annotations

from collections import Counter

from quran_lab.multiverse import Multiverse

LIMITS = (
    "Texte de référence : Tanzil, lecture Hafs ʿan ʿĀṣim, numérotation des versets de cette "
    "tradition. Les décomptes ne se transposent pas aux autres lectures."
)


def render_grid_table(m: Multiverse) -> str:
    head = "| niveau | basmala | muqatta'at | texte | composés | décompte |" + (
        " cible atteinte |" if m.target is not None else ""
    )
    sep = "|---|---|---|---|---|---:|" + ("---|" if m.target is not None else "")
    rows = []
    for c in m.cells:
        r = c.rules
        row = (
            f"| {r.level} | {r.basmala} | {r.muqattaat} | {r.text or 'n/a'} | "
            f"{r.compounds} | {c.result.n} |"
        )
        if m.target is not None:
            row += f" {'oui' if c.hit else 'non'} |"
        rows.append(row)
    return "\n".join([head, sep, *rows])


def render_distribution(m: Multiverse) -> str:
    """Courbe de spécification en texte : valeur du décompte -> nombre de cellules."""
    by_level: dict[str, Counter[int]] = {}
    for c in m.cells:
        by_level.setdefault(c.rules.level, Counter())[c.result.n] += 1
    lines = ["| niveau | décompte | nombre de cellules |", "|---|---:|---:|"]
    for level, cnt in by_level.items():
        for value in sorted(cnt):
            lines.append(f"| {level} | {value} | {cnt[value]} |")
    return "\n".join(lines)


def render_variants(m: Multiverse) -> str:
    """Variantes fusionnées dans la cellule canonique de chaque niveau."""
    lines = ["| niveau | variantes fusionnées (forme: effectif) |", "|---|---|"]
    for c in m.cells:
        r = c.rules
        if (r.basmala, r.muqattaat, r.compounds) == ("as_text", "include", "with_base") and (
            r.text in (None, "uthmani")
        ):
            v = ", ".join(f"{k}: {n}" for k, n in sorted(c.result.variants.items())) or "(aucune)"
            lines.append(f"| {r.level} | {v} |")
    return "\n".join(lines)


def render_coincidence(co: dict) -> str:
    return (
        f"| type lexical | valeur |\n|---|---:|\n"
        f"| types distincts | {co['n_types']} |\n"
        f"| types à exactement {co['target']} | {co['observed_types_at_target']} |\n"
        f"| attendu (moyenne des entiers voisins, ± {co['window']}) | "
        f"{co['expected_types_at_target']:.2f} |\n"
    )


def render_verification_report(
    *,
    claim: str,
    query: str,
    hypothesis: str,
    command: str,
    raw_hash: str,
    code: str,
    m: Multiverse,
    coincidences: dict[str, dict],
) -> str:
    fm = (
        f"---\ngenerated_by: {command}\ndata_manifest_sha256: {raw_hash}\ncode_sha: {code}\n"
        f"hypothesis: {hypothesis}\n---\n"
    )
    body = [
        f"# Vérification : {claim}",
        "",
        "Étiquette de départ : `AFFIRMATION POPULAIRE`. Les décomptes ci-dessous sont des "
        "`FAIT`, chacun relatif à sa règle (colonne par colonne).",
        "",
        f"Limites : {LIMITS}",
        "",
        "## Verdict de reproduction (provisoire, avant modèles nuls)",
        "<!-- BEGIN generated:quran_lab.report.verdict -->",
        m.reproduction_verdict(),
        "<!-- END generated -->",
        "",
        "## Décompte sous chaque règle applicable",
        "<!-- BEGIN generated:quran_lab.report.render_grid_table -->",
        render_grid_table(m),
        "<!-- END generated -->",
        "",
        "## Courbe de spécification (valeur -> nombre de cellules)",
        "<!-- BEGIN generated:quran_lab.report.render_distribution -->",
        render_distribution(m),
        "<!-- END generated -->",
        "",
        "## Variantes fusionnées",
        "<!-- BEGIN generated:quran_lab.report.render_variants -->",
        render_variants(m),
        "<!-- END generated -->",
        "",
        "## Taux de coïncidence N5 (combien de types tombent exactement sur la cible)",
    ]
    for level, co in coincidences.items():
        body += [
            f"### {level}",
            "<!-- BEGIN generated:quran_lab.stats.nulls.coincidence_rate -->",
            render_coincidence(co),
            "<!-- END generated -->",
            "",
        ]
    body += [
        "## Reproduction",
        "```",
        command,
        "```",
        "",
        "Statut final : à assigner après relecture `statisticien-sceptique`. "
        "Sans modèles nuls N0-N4 (Phase 3), `ROBUSTE` n'est pas attribuable.",
    ]
    return fm + "\n".join(body) + "\n"
