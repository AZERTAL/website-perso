# website-perso

Ce dépôt contient deux projets indépendants.

| Dossier | Projet | Techno | Démarrer |
|---|---|---|---|
| racine (`src/`, `index.html`, `package.json`) | Site portfolio personnel | Vite, React, TypeScript, Tailwind | `npm install && npm run dev` |
| [`quran-lab/`](quran-lab/README.md) | **Quran Lab** : recherche computationnelle sur le corpus coranique | Python 3.12, DuckDB, `uv` | [`quran-lab/README.md`](quran-lab/README.md) |

Les deux ne partagent aucun code. Le portfolio n'est pas modifié par Quran Lab.

## Où est quoi

```
.
├── src/ index.html package.json ...   portfolio (Vite + React)
├── quran-lab/                         projet de recherche (code, données, docs, rapports)
├── .claude/                           agents, commandes, skills et hooks de Claude Code
├── .github/                           CI, modèles d'issues et de pull requests
├── .githooks/                         hook git de pré-commit (à activer : voir quran-lab/CONTRIBUTING.md)
└── CLAUDE.md                          règles de travail du projet Quran Lab
```

## Quran Lab en une phrase

Compter le texte du Coran sous **toutes** les règles de comptage raisonnables, tester les affirmations numériques populaires contre un modèle nul, et publier les résultats, y compris négatifs. Chaque chiffre sort d'un script versionné.

Lecture conseillée : [`quran-lab/README.md`](quran-lab/README.md), puis [`quran-lab/docs/README.md`](quran-lab/docs/README.md).

## Note sur la structure du dépôt

Un dépôt dédié à Quran Lab serait plus propre à terme (le site public de recherche n'a pas sa place à côté d'un portfolio). Le script [`quran-lab/scripts/export_standalone_repo.sh`](quran-lab/scripts/export_standalone_repo.sh) extrait le projet avec son historique, ses agents et sa CI, prêt à pousser vers un nouveau dépôt.
