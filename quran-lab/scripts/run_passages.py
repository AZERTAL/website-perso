#!/usr/bin/env python3
"""Exécute les requêtes de config/queries/*.yaml -> reports/passages/<domaine>.md et .json.

Les fichiers de requêtes sont commités AVANT ce script. Cartographie (FAIT), pas interprétation.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
from quran_lab.db import read_corpus  # noqa: E402
from quran_lab.passages import load_queries, search, verse_tokens  # noqa: E402
from quran_lab.provenance import code_sha, raw_manifest_hash  # noqa: E402

MAX_REFS, MAX_TEXTS = 40, 3


def main() -> int:
    corpus = read_corpus(LAB / "data" / "quran.duckdb")
    vt = verse_tokens(corpus, "simple")
    text_of: dict[tuple[int, int], list[tuple[int, str]]] = defaultdict(list)
    for w in corpus.words:
        if w.variant == "simple" and not w.header:
            text_of[(w.sura, w.aya)].append((w.word, w.text))
    verse_text = {k: " ".join(t for _, t in sorted(v)) for k, v in text_of.items()}

    out_dir = LAB / "reports" / "passages"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = raw_manifest_hash(LAB / "data" / "raw")
    sha = code_sha(LAB.parent)
    cmd = "cd quran-lab && uv run python scripts/run_passages.py"
    for path in sorted((LAB / "config" / "queries").glob("*.yaml")):
        domain, title, queries = load_queries(path)
        results = [search(q, vt) for q in queries]
        md = [
            f"---\ngenerated_by: {cmd}\ndata_manifest_sha256: {raw}\ncode_sha: {sha}\n---",
            f"# Domaine : {title}",
            "",
            "Étiquette : `FAIT` (recherche de passages dans le texte Tanzil simple-clean, squelette "
            "consonantique). Cartographie, pas interprétation : aucune lecture de tafsir n'est "
            "incluse (aucune source acquise). Un motif exige un modèle nul (phase ultérieure).",
            "",
            f"Requêtes : `config/queries/{path.name}`, commitées avant l'exécution. "
            "Une expression absente du texte est un résultat.",
            "",
            "## Vue d'ensemble",
            "<!-- BEGIN generated:quran_lab.passages.search -->",
            "| id | type | expression | occurrences | versets | sourates |",
            "|---|---|---|---:|---:|---:|",
        ]
        for r in results:
            q = r.query
            md.append(
                f"| {q.id} | {q.kind} | {q.text} | {r.n_occurrences} | {len(r.verses)} | {r.n_suras} |"
            )
        md += ["<!-- END generated -->", "", "## Détail par requête"]
        for r in results:
            q = r.query
            md += [f"### {q.id} : {q.text}", f"Pourquoi dans ce domaine : {q.why}.", ""]
            md.append("<!-- BEGIN generated:quran_lab.passages.search -->")
            if not r.hits:
                md.append("aucune occurrence dans le texte")
            else:
                refs = r.verses
                shown = ", ".join(refs[:MAX_REFS]) + (" ..." if len(refs) > MAX_REFS else "")
                forms = "; ".join(f"{f} ({n})" for f, n in r.forms.most_common(8))
                md += [f"versets : {shown}", f"formes rencontrées : {forms}", ""]
                for ref in refs[:MAX_TEXTS]:
                    s, a = (int(x) for x in ref.split(":"))
                    md.append(f"> {ref} : {verse_text[(s, a)]}")
            md += ["<!-- END generated -->", ""]
        md += ["## Reproduction", "```", cmd, "```", ""]
        (out_dir / f"{domain}.md").write_text("\n".join(md), encoding="utf-8")
        (out_dir / f"{domain}.json").write_text(
            json.dumps(
                [
                    {
                        "id": r.query.id,
                        "kind": r.query.kind,
                        "text": r.query.text,
                        "occurrences": r.n_occurrences,
                        "verses": r.verses,
                    }
                    for r in results
                ],
                ensure_ascii=False,
                indent=1,
            ),
            encoding="utf-8",
        )
        found = sum(1 for r in results if r.hits)
        print(f"{domain}: {len(results)} requêtes, {found} avec au moins une occurrence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
