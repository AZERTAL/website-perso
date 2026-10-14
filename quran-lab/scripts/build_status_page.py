#!/usr/bin/env python3
"""Construit site/status.html à partir des RÉSULTATS (base DuckDB, rapport d'audit JSON, manifeste
des sources, git). Aucun chiffre n'est saisi dans le gabarit : tout vient de ce script.

Les rares éléments qui ne sortent pas d'un script sont marqués « manuel » dans la page.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import read_corpus  # noqa: E402
from quran_lab.multiverse import run  # noqa: E402
from quran_lab.normalize import skeleton  # noqa: E402
from quran_lab.rules import grid, load_config  # noqa: E402
from quran_lab.stats.ledger import total_comparisons  # noqa: E402
from quran_lab.stats.spec_space import TOGGLES, analyze, verdict  # noqa: E402

TARGET = 365
QUERY = "يوم"


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=LAB.parent, capture_output=True, text=True)
    return r.stdout.strip()


def pytest_count() -> int:
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
        cwd=LAB,
        capture_output=True,
        text=True,
    )
    m = re.search(r"(\d+) passed", r.stdout)
    if r.returncode != 0 or not m:
        raise SystemExit("les tests ne passent pas : page non générée\n" + r.stdout[-800:])
    return int(m.group(1))


def main() -> int:
    audit = json.loads((LAB / "reports" / "audit-tanzil.json").read_text(encoding="utf-8"))
    corpus = read_corpus(LAB / "data" / "quran.duckdb")
    cfg = load_config(LAB / "config" / "counting_rules.yaml")
    mv = run(QUERY, corpus, cfg, target=TARGET)
    by_rules = {c.rules: c for c in mv.cells}

    cells = []
    for r in grid():
        c = by_rules.get(r)
        cells.append(
            {
                "level": r.level,
                "basmala": r.basmala,
                "muqattaat": r.muqattaat,
                "text": r.text,
                "compounds": r.compounds,
                "count": None if c is None else c.result.n,
            }
        )
    ev = [c for c in cells if c["count"] is not None]
    sep = {c["count"] for c in ev if c["compounds"] == "separate"}
    wth = {c["count"] for c in ev if c["compounds"] == "with_base"}
    assert len(sep) == 1 and len(wth) == 1, (
        "les autres axes changent le décompte : la page doit le dire"
    )
    h001 = {
        "target": TARGET,
        "sep": sep.pop(),
        "with": wth.pop(),
        "n_sep": sum(c["compounds"] == "separate" for c in ev),
        "n_with": sum(c["compounds"] == "with_base" for c in ev),
        "n_eval": len(ev),
    }

    ref = next(
        c
        for c in mv.cells
        if (c.rules.level, c.rules.basmala, c.rules.muqattaat, c.rules.text, c.rules.compounds)
        == ("form", "all_113", "include", "uthmani", "with_base")
    )
    items = sorted(ref.result.variants.items(), key=lambda kv: (-kv[1], kv[0]))
    top = [
        {"form": k.removeprefix("[composé] "), "n": n, "compound": k.startswith("[composé]")}
        for k, n in items[:8]
    ]
    forms = {
        "total": sum(n for _, n in items),
        "distinct": len(items),
        "top": top,
        "rest": len(items) - len(top),
    }

    tokens = {
        v: Counter(skeleton(w.text) for w in corpus.words if w.variant == v)
        for v in ("simple", "uthmani")
    }
    sp = analyze(tokens)
    reviewer_mask = tuple(t in ("T1", "T2", "T3", "T4") for t in TOGGLES)
    nb = [sp.n_of(t) for t in range(360, 371) if t != TARGET]
    h2 = {
        "range": [350, 380],
        "target": TARGET,
        "n": {t: sp.n_of(t) for t in range(350, 381)},
        "verdict": verdict(sp),
        "specs": len(sp.totals),
        "distinct": sp.distinct_totals,
        "n_target": sp.n_of(TARGET),
        "max_neighbour": max(nb),
        "reviewer_total": sp.totals[("simple", reviewer_mask)],
    }
    domains = []
    for jf in sorted((LAB / "reports" / "passages").glob("*.json")):
        qs = json.loads(jf.read_text(encoding="utf-8"))
        meta = yaml.safe_load(
            (LAB / "config" / "queries" / f"{jf.stem}.yaml").read_text(encoding="utf-8")
        )
        phrases = [q for q in qs if q["kind"] == "phrase" and q["occurrences"]][:5]
        domains.append(
            {
                "id": jf.stem,
                "title": meta["title"],
                "n_queries": len(qs),
                "n_found": sum(1 for q in qs if q["occurrences"]),
                "n_v1_missed": sum(q["occurrences"] - q["occurrences_v1"] for q in qs),
                "items": [
                    {
                        "text": q["text"],
                        "n": q["occurrences"],
                        "n_v1": q["occurrences_v1"],
                        "refs": q["verses"][:6],
                        "more": max(0, len(q["verses"]) - 6),
                    }
                    for q in phrases
                ],
            }
        )
    h002 = json.loads((LAB / "reports" / "H002-v2.json").read_text(encoding="utf-8"))
    ledger_total = total_comparisons(LAB / "reports" / "tests_ledger.csv")

    inv = audit["invariants"]["uthmani"]
    w, hw, wd, df = (
        audit["words"],
        audit["header_words"],
        audit["word_diffs"],
        audit["differential"],
    )
    stats = [
        {"n": inv["suras"], "l": "sourates", "s": "FAIT · égal aux métadonnées Tanzil"},
        {"n": inv["verses"], "l": "versets", "s": "FAIT · même total dans les deux orthographes"},
        {"n": w["uthmani"], "l": "mots, orthographe Uthmani", "s": "FAIT · découpage par espaces"},
        {
            "n": w["simple"],
            "l": "mots, orthographe simple-clean",
            "s": "FAIT · découpage par espaces",
        },
        {
            "n": wd["verses"],
            "l": "versets au nombre de mots différent entre les deux orthographes",
            "s": "FAIT · reports/audit-tanzil.md §3",
        },
        {
            "n": df["uthmani"]["n_disagreements"] + df["simple"]["n_disagreements"],
            "l": "désaccords entre deux implémentations indépendantes du squelette",
            "s": f"FAIT · {df['uthmani']['types_a']:,} + {df['simple']['types_a']:,} types, texte entier".replace(
                ",", " "
            ),
        },
        {
            "n": len(cells),
            "l": "règles de comptage par requête, dont " + str(len(ev)) + " évaluées",
            "s": "FAIT · rules.grid(), cellules n/a exclues",
        },
        {
            "n": ledger_total,
            "l": "comparaisons déclarées au registre des tests",
            "s": "FAIT · reports/tests_ledger.csv, ajout seul",
        },
        {
            "n": h2["specs"],
            "l": "spécifications de formes balayées (H001-v2)",
            "s": f"FAIT · dont {h2['distinct']} décomptes distincts",
        },
        {
            "n": h2["n_target"],
            "l": f"spécifications qui donnent exactement {TARGET}",
            "s": f"FAIT · le voisin le mieux placé en a {h2['max_neighbour']}",
        },
        {
            "n": df["simple"]["types_a"],
            "l": "mots distincts (squelettes) en simple-clean",
            "s": "FAIT · reports/audit-tanzil.json",
        },
        {
            "n": 10,
            "l": "règles cassées volontairement, toutes détectées par les tests",
            "s": "MANUEL · test de mutation, non scripté",
        },
    ]
    finds = [
        {
            "k": "D9",
            "t": "La basmala est déjà dans le texte",
            "p": f"Tanzil préfixe la basmala au verset 1 de <b>113 sourates</b> sur 114 : {hw['uthmani']} mots d'en-tête en Uthmani. "
            "Le modèle de départ supposait le contraire et aurait compté deux fois la basmala. "
            "Exclure les muqatta'at d'un verset ne doit pas non plus la retirer.",
        },
        {
            "k": "D10",
            "t": "Les deux orthographes n'ont pas les mêmes mots",
            "p": f"<b>{wd['verses']} versets</b> n'ont pas le même nombre de mots en Uthmani et en simple-clean "
            f"(ex. 2:21). Apparier les mots par position aurait supprimé ces versets sans un bruit.",
        },
        {
            "k": "D11",
            "t": "Une normalisation qui inventait des lettres",
            "p": "Le signe d'allongement sur un alif était recomposé en lettre <b>آ</b>, et la hamza portée par un tatwil "
            "disparaissait après réordonnancement Unicode. Avant correction : <b>1 077 graphies distinctes</b> "
            "(3 687 occurrences) divergeaient entre les deux implémentations <i>(mesure manuelle, consignée dans D11)</i>.",
        },
        {
            "k": "Preuve",
            "t": "Deux programmes, zéro désaccord",
            "p": "Après correction, la normalisation écrite avec les catégories Unicode et celle écrite avec des plages de code "
            "donnent exactement les mêmes effectifs sur <b>tout le texte</b>, dans les deux orthographes.",
        },
    ]

    finds.insert(
        3,
        {
            "k": "D15",
            "t": "Un relecteur indépendant a rendu le verdict FRAGILE",
            "p": f"Sans connaître notre raisonnement, il a trouvé qu'une combinaison de formes du mot donne exactement <b>{h2['reviewer_total']}</b> "
            "(arithmétique re-vérifiée). Mais cette règle a été trouvée <b>après</b> avoir vu le résultat. Réponse : une nouvelle hypothèse "
            f"pré-enregistrée (H001-v2) balaie {h2['specs']} règles. Résultat : {TARGET} est atteint par <b>{h2['n_target']}</b> d'entre elles, "
            f"mais son voisin le mieux placé l'est par <b>{h2['max_neighbour']}</b> : {TARGET} n'est pas plus facile à atteindre que ses voisins. "
            "Huit faiblesses relevées, traitement point par point dans DECISIONS D15. <i>(verdict de la relecture : manuel, rapport d'agent)</i>",
        },
    )
    manifest = json.loads((LAB / "data" / "sources_manifest.json").read_text(encoding="utf-8"))
    names = {
        "tanzil_uthmani": "Tanzil · Uthmani",
        "tanzil_simple_clean": "Tanzil · simple-clean",
        "tanzil_metadata": "Tanzil · métadonnées",
    }
    sources = [
        {
            "t": names.get(r["id"], r["id"]),
            "d": f"<span class='mono'>{r['sha256'][:12]}…</span> · téléchargé le {r['date']} · CC BY 3.0, texte non modifié",
            "chip": "acquis",
            "cls": "ok",
        }
        for r in manifest
    ]
    sources.append(
        {
            "t": "Quranic Arabic Corpus · morphologie v0.4",
            "d": "GNU GPL · page de téléchargement protégée par un e-mail de contact",
            "chip": "en attente",
            "cls": "warn",
        }
    )
    ph = [
        ("1", "Sources, base, 4 niveaux de comptage, H001", "en cours", "now"),
        ("2", "Moteur multivers complet, 15 à 20 affirmations populaires", "à venir", "pend"),
        (
            "3",
            "Modèles nuls, correction des comparaisons multiples, bootstrap par sourates",
            "à venir",
            "pend",
        ),
        (
            "4",
            "Lexiques de 12 concepts, validation contre l'ontologie du corpus",
            "à venir",
            "pend",
        ),
        ("5", "Embeddings, thèmes, regroupements, contrôles négatifs", "à venir", "pend"),
        ("6", "Réseau de concepts, cycles, rimes et formules", "à venir", "pend"),
        ("7", "Tafsir cité, site public, automatisation nocturne", "à venir", "pend"),
        ("8", "Rapport technique, résultats négatifs inclus", "à venir", "pend"),
    ]
    phases = [{"t": f"Phase {n}", "d": d, "chip": c, "cls": k} for n, d, c, k in ph]

    data = {
        "commit": git("rev-parse", "--short=7", "HEAD"),
        "commit_full": git("rev-parse", "HEAD"),
        "tests": pytest_count(),
        "h001": h001,
        "cells": cells,
        "forms": forms,
        "stats": stats,
        "h2": h2,
        "domains": domains,
        "h002": h002,
        "finds": finds,
        "sources": sources,
        "phases": phases,
    }
    tpl = (LAB / "site" / "status.template.html").read_text(encoding="utf-8")
    out = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
    (LAB / "site" / "status.html").write_text(out, encoding="utf-8")
    print(f"site/status.html écrit ({len(out) // 1024} Ko) · H001 {h001} · tests {data['tests']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
