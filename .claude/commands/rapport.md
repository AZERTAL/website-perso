---
description: État d'avancement du projet Quran Lab
---
Fais l'état du projet, sans rien inventer :
1. `git log --oneline -15` et `git status -sb`.
2. `cd quran-lab && uv run pytest -q && uv run ruff check .` : résultats exacts.
3. Sources : lis `quran-lab/SOURCES.md` ; quelles sources sont téléchargées et hashées, lesquelles manquent.
4. Hypothèses : liste `quran-lab/hypotheses/` avec leur statut ; nombre de tests du registre si la base existe.
5. Rapports de `quran-lab/reports/` et leur verdict.
6. Blocages (réseau, licences) et ce que l'utilisateur doit faire.
Format : résultat d'abord, puis le détail. Séparer FAIT / non vérifié.
