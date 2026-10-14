# Pile technique : chaque outil et pourquoi

| Outil | Rôle | Pourquoi celui-là | Où |
|---|---|---|---|
| **Python 3.12** | langage | écosystème scientifique et NLP ; 3.12 épinglé car la compatibilité de `camel-tools` (Phase 5) avec 3.13 est inconnue | `.python-version` |
| **uv** | gestion de l'environnement et des dépendances | installation rapide, fichier de verrouillage `uv.lock` : mêmes versions partout, donc résultats reproductibles | `pyproject.toml`, `uv.lock` |
| **DuckDB** | base de données locale | base analytique embarquée, sans serveur, un seul fichier ; requêtes SQL sur 150 000 mots en millisecondes | `src/quran_lab/db.py` |
| **polars + pyarrow** | tables et insertion en bloc | insertion de 156 000 lignes en moins d'une seconde (l'insertion ligne par ligne prenait plusieurs minutes) | `db.py`, `scripts/export_dataset.py` |
| **numpy** | calcul numérique | corrections des comparaisons multiples | `stats/multiplicity.py` |
| **scipy** | statistiques | déclaré pour la Phase 3, **pas encore utilisé** | `pyproject.toml` |
| **PyYAML** | configuration | règles et lexiques lisibles et versionnés, séparés du code | `config/*.yaml` |
| **pytest** | tests | exécution de 139 tests unitaires, de propriétés et différentiels | `tests/` |
| **hypothesis** | tests de propriétés | génère des centaines d'entrées pour vérifier des lois (idempotence, ordre, monotonie) plutôt que quelques cas écrits à la main | `tests/property/`, `tests/unit/test_multiplicity.py` |
| **ruff** | lint et formatage | un seul outil rapide pour le style et les erreurs courantes | `pyproject.toml` |
| **git** | historique | sert aussi de preuve : le pré-enregistrement et le registre des tests sont vérifiés via les dates et le contenu des commits | `checks.py` |
| **GitHub Actions** | intégration continue | refait lint, tests et vérification des rapports à chaque push | `.github/workflows/quran-lab-ci.yml` |
| **Chromium sans interface** | rendu de la page de suivi | contrôle visuel clair/sombre et téléphone | usage ponctuel |
| **Claude Code** | agent de développement | agents spécialisés, skills, commandes et hooks qui imposent les règles du projet | [`claude-code.md`](claude-code.md) |

## Choix volontairement écartés

- **Carnets Jupyter** : un script versionné et relançable est reproductible ; un carnet exécuté dans le désordre ne l'est pas.
- **Entraîner des embeddings sur le seul Coran** : environ 78 000 mots, trop peu pour une représentation fiable (seulement comme contrôle).
- **Compter sur des traductions** : interdit par le cahier des charges ; elles ne servent qu'à l'affichage.

## Prévu, pas encore installé

`camel-tools` et modèles pré-entraînés (Phase 5), `networkx` (réseau de concepts), `statsmodels` et `PyMC` (modèles de répartition), `matplotlib`/`plotly` (figures), site public Next.js sur Vercel (Phase 7).

## Reproduire l'environnement

```bash
cd quran-lab
uv sync          # installe exactement les versions de uv.lock
make test        # 139 tests
```
