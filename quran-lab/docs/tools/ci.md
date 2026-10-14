# Intégration continue

Fichier : [`.github/workflows/quran-lab-ci.yml`](../../../.github/workflows/quran-lab-ci.yml). Déclenché à chaque push et chaque pull request qui touche `quran-lab/`.

| Étape | Commande | Ce qu'elle garantit |
|---|---|---|
| Récupération complète de l'historique | `actions/checkout` avec `fetch-depth: 0` | `check_reports.py` lit l'historique git (ordre pré-enregistrement / résultats, registre en ajout seul) |
| Installation | `uv sync` | versions exactes de `uv.lock` |
| Lint | `ruff check .` | pas d'erreur de style ou de code |
| Formatage | `ruff format --check .` | formatage uniforme |
| Tests | `pytest -q` | 139 tests, dont le test différentiel sur tout le texte (les sources sont dans le dépôt) |
| Rapports | `python3 scripts/check_reports.py` | aucun chiffre hors bloc généré, pré-enregistrement respecté, registre des tests intact |

## État

Le fichier de workflow est écrit. **Son résultat n'a pas été consulté dans cette session** (le connecteur GitHub était déconnecté). À vérifier dans l'onglet « Actions » du dépôt.

## Prévu, non écrit

- Pipeline complet nocturne (`make all`) et reconstruction du rapport.
- Redéploiement du site public après chaque exécution réussie.
- Tâche planifiée pour un rapport hebdomadaire.
