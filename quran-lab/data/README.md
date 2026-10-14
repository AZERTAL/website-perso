# data/

| Chemin | Contenu | Versionné ? |
|---|---|---|
| `raw/` | sources brutes **verbatim** (Tanzil Uthmani, simple-clean, métadonnées) | oui (CC BY 3.0 autorise la copie verbatim) |
| `sources_manifest.json` | URL, date, SHA-256 de chaque source | oui |
| `quran.duckdb` | base construite par `make db` | non (reconstruite) |
| `processed/` | jeu de données exporté (`make dataset`) : CSV, Parquet, `NOTICE.md` | non (reconstruit) |

## Règles

- `raw/` est en **lecture seule** (droits `a-w` et hook). Seul `scripts/fetch_sources.py` y écrit.
- Ne jamais éditer un fichier de `raw/` : une transformation produit un fichier ailleurs, par un script.
- Chaque fichier a son empreinte dans `SOURCES.md` ; `make verify-sources` la vérifie.
- Avis de copyright Tanzil : dans les fichiers eux-mêmes ; à reproduire dans tout fichier dérivé.

Documentation : [`docs/data/`](../docs/data/).
