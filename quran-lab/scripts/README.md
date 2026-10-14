# scripts/

Points d'entrée en ligne de commande. La logique vit dans `src/quran_lab/` ; ces scripts font les entrées/sorties.

| Script | Rôle |
|---|---|
| `fetch_sources.py` | **seul** script autorisé à écrire dans `data/raw/` ; télécharge, calcule SHA-256, met à jour `SOURCES.md` |
| `verify_sources.py` | recalcule les empreintes et compare au manifeste |
| `build_db.py` | `data/raw/` → `data/quran.duckdb` (mode texte seul sans morphologie) |
| `audit_tanzil.py` | audit des données, test différentiel sur tout le texte |
| `run_h001_v2.py` | exécute H001-v2 et inscrit le résultat au registre |
| `ledger_add.py` | ajoute une ligne au registre des tests |
| `export_dataset.py` | CSV et Parquet dans `data/processed/` |
| `build_status_page.py` | génère `site/status.html` à partir des résultats |
| `check_reports.py` | refuse un chiffre hors bloc généré, un test non pré-enregistré, un registre réécrit |
| `export_standalone_repo.sh` | extrait le projet dans un dépôt dédié |
| `hook_*.py` | hooks de Claude Code (protection des sources, qualité, contrôle de commit) |
