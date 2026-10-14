# src/quran_lab/ : carte des modules

Logique pure (sans entrées/sorties) sauf indication.

| Module | Rôle |
|---|---|
| `normalize.py` | squelette consonantique, repliements optionnels, inventaire Unicode |
| `buckwalter.py` | translittération Buckwalter → arabe (format du corpus v0.4) |
| `model.py` | `Word`, `Segment`, `Corpus`, position `Loc` |
| `rules.py` | `Rules`, grille de 60 cellules, lecture de la configuration |
| `count.py` | comptage aux 4 niveaux, `type_counts`, ventilation par nombre |
| `multiverse.py` | un énoncé évalué sous toutes les règles ; axes sans effet ; verdict partiel |
| `load.py` | lecture de Tanzil et de la morphologie (texte → objets) |
| `db.py` | persistance DuckDB (entrées/sorties) |
| `validate.py` | contrôles de cohérence des données |
| `audit.py` | audit des sources, test différentiel (seconde implémentation) |
| `export.py` | tables plates du jeu de données |
| `report.py` | rendu Markdown déterministe des rapports |
| `checks.py` | refus des chiffres orphelins, du pré-enregistrement violé, du registre réécrit |
| `guards.py` | logique des hooks de protection (bibliothèque standard seulement) |
| `provenance.py` | empreintes SHA-256 des données et du code |
| `cli.py` | `python -m quran_lab.cli compte|verifie` |
| `stats/nulls.py` | taux de coïncidence N5 |
| `stats/multiplicity.py` | Bonferroni, Holm, Benjamini-Hochberg, Benjamini-Yekutieli, Westfall-Young |
| `stats/ledger.py` | registre des tests en ajout seul |
| `stats/spec_space.py` | espace de spécifications de H001-v2 |

Détail des méthodes : [`docs/methodology/`](../../docs/methodology/).
