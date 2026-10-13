"""Ligne de commande : `python -m quran_lab.cli {compte,verifie} ...` (depuis quran-lab/)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from quran_lab.db import read_corpus
from quran_lab.multiverse import run
from quran_lab.provenance import code_sha, raw_manifest_hash
from quran_lab.report import (
    render_distribution,
    render_grid_table,
    render_variants,
    render_verification_report,
)
from quran_lab.rules import grid, load_config
from quran_lab.stats.nulls import coincidence_rate

LAB = Path(__file__).resolve().parents[2]


def _load(db: Path):
    if not db.exists():
        print(
            f"Base absente : {db}\nLes sources ne sont pas téléchargées ; aucun chiffre n'est "
            "produit. Voir SOURCES.md et scripts/fetch_sources.py.",
            file=sys.stderr,
        )
        raise SystemExit(3)
    return read_corpus(db), load_config(LAB / "config" / "counting_rules.yaml")


# « basmala du texte » (H001) = telle qu'imprimée par la source : Tanzil préfixe 113 basmalas,
# le corpus morphologique n'a que la basmala numérotée 1:1.
_BASMALA_AS_PRINTED = {
    "form": "all_113",
    "stem": "numbered_only",
    "lemma": "numbered_only",
    "root": "numbered_only",
}


def _coincidence_rules(level: str):
    """Cellule de référence du taux N5 : texte simple, composés séparés, basmala du texte."""
    return next(
        r
        for r in grid()
        if r.level == level
        and (r.basmala, r.muqattaat, r.compounds)
        == (_BASMALA_AS_PRINTED[level], "include", "separate")
        and r.text in (None, "simple")
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="quran_lab.cli")
    ap.add_argument("--db", type=Path, default=LAB / "data" / "quran.duckdb")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compte")
    c.add_argument("query")
    c.add_argument("--target", type=int)
    v = sub.add_parser("verifie")
    v.add_argument("query")
    v.add_argument("--target", type=int, required=True)
    v.add_argument("--claim", required=True)
    v.add_argument("--hypothesis", required=True)
    v.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)

    corpus, cfg = _load(a.db)
    m = run(a.query, corpus, cfg, target=a.target)
    if a.cmd == "compte":
        print(render_grid_table(m), render_distribution(m), render_variants(m), sep="\n\n")
        print("\n" + m.reproduction_verdict())
        return 0

    co = {
        level: coincidence_rate(corpus, cfg, _coincidence_rules(level), a.target)
        for level in (("form", "stem", "lemma", "root") if corpus.has_morphology else ("form",))
    }
    cmd = (
        f"cd quran-lab && uv run python -m quran_lab.cli verifie {a.query!r} "
        f"--target {a.target} --claim {a.claim!r} --hypothesis {a.hypothesis} --out {a.out}"
    )
    text = render_verification_report(
        claim=a.claim,
        query=a.query,
        hypothesis=a.hypothesis,
        command=cmd,
        raw_hash=raw_manifest_hash(LAB / "data" / "raw"),
        code=code_sha(LAB.parent),
        m=m,
        coincidences=co,
    )
    a.out.write_text(text, encoding="utf-8")
    print(f"écrit : {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
