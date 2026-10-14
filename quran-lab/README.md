# Quran Lab

Recherche computationnelle, rigoureuse et reproductible, sur le texte coranique.

> **Règle absolue.** Aucun chiffre sans script. Chaque affirmation cite ses versets (`sourate:verset`) et porte une étiquette : `FAIT`, `INTERPRÉTATION` ou `AFFIRMATION POPULAIRE`. Les résultats négatifs sont publiés. Le projet ne tire aucune conclusion religieuse des chiffres.

## Pourquoi ce projet existe

Un même mot donne plusieurs chiffres selon la façon de compter (forme exacte, sans préfixes, lemme, racine ; avec ou sans basmala ; etc.). Beaucoup d'affirmations numériques qui circulent ne précisent pas leur règle, et personne ne dit combien de mots « tombent juste » par pur hasard. Quran Lab fait trois choses :

1. **Mesurer** : compter sous toutes les règles applicables et garder les positions (versets), pas seulement un entier.
2. **Tester** : comparer chaque affirmation à un modèle nul, corriger les comparaisons multiples, pré-enregistrer le test avant de voir le résultat.
3. **Documenter** : tout est reproductible (`make`), toute décision est datée (`docs/DECISIONS.md`).

## État du projet

| Brique | État |
|---|---|
| Sources Tanzil (Uthmani, simple-clean, métadonnées) | acquises, empreintes SHA-256 dans [`SOURCES.md`](SOURCES.md) |
| Morphologie (Quranic Arabic Corpus v0.4) | **non acquise** (la page de téléchargement exige une adresse e-mail de contact) |
| Moteur de comptage à 4 niveaux, grille de 60 règles | implémenté et testé ; seul le niveau « forme » est évaluable sans morphologie |
| Audit du texte réel | fait : [`reports/audit-tanzil.md`](reports/audit-tanzil.md) |
| Hypothèse H001 (« jour = 365 ») | niveau forme mesuré, **verdict partiel** : [`reports/H001-yawm-365.md`](reports/H001-yawm-365.md) |
| Recherche de passages (temps, espace, business, apprentissage, intelligence) | faite ; H002 (formes de `عقل`) : voir [`docs/research-program.md`](docs/research-program.md) |
| Modèles nuls N0 à N4, correction multiple, registre des tests | voir [`docs/roadmap.md`](docs/roadmap.md) |
| Embeddings, thèmes, réseau, cycles | planifiés (Phases 4 à 6), non implémentés |
| Tafsir | aucune source acquise |

Détail et traçabilité de chaque exigence du cahier des charges : [`docs/roadmap.md`](docs/roadmap.md).

## Démarrage rapide

Prérequis : [`uv`](https://docs.astral.sh/uv/) et Python 3.12.

```bash
cd quran-lab
uv sync                              # installe les dépendances figées (uv.lock)
make test                            # tests unitaires, de propriétés, différentiels
make lint                            # ruff
uv run python scripts/build_db.py    # data/raw -> data/quran.duckdb
uv run python scripts/audit_tanzil.py            # rapport d'audit des données
uv run python -m quran_lab.cli compte "يوم" --target 365   # grille multivers d'un mot
```

Sans morphologie, `build_db.py` construit une base « texte seul » et le moteur déclare les niveaux radical, lemme et racine **non évalués** (jamais zéro).

## Structure

```
quran-lab/
├── README.md              ce fichier
├── CONTRIBUTING.md        comment travailler dans le projet (pré-enregistrer, tester, commiter)
├── SOURCES.md             provenance, hash et licences des sources
├── Makefile               commandes courantes (test, lint, db, ...)
├── pyproject.toml         dépendances et configuration (uv, pytest, ruff)
├── config/                règles et lexiques en YAML (données de configuration, pas des résultats)
│   ├── queries/               requêtes par domaine (commitées avant exécution)
│   ├── counting_rules.yaml    versets de muqatta'at, mots composés
│   ├── sources.yaml           URL et options de téléchargement
│   └── themes.yaml            lexiques de concepts (BROUILLON non validé)
├── data/
│   ├── raw/               sources brutes, en lecture seule, jamais modifiées
│   ├── processed/         tables dérivées (générées, non versionnées)
│   └── sources_manifest.json  empreintes des fichiers téléchargés
├── src/quran_lab/         le code (logique pure séparée des entrées/sorties)
│   ├── stats/             modèles nuls, correction multiple, registre
│   └── README.md          carte des modules
├── scripts/               points d'entrée en ligne de commande et hooks
├── tests/                 unit/, property/, differential/, golden/, fixtures/
├── hypotheses/            hypothèses pré-enregistrées (H001, ...)
├── reports/               rapports générés par script (jamais écrits à la main)
├── site/                  page de suivi (gabarit + page générée)
└── docs/                  documentation : méthodes, outils, données, décisions
```

Chaque dossier important a son propre `README.md`.

## Documentation

Point d'entrée : [`docs/README.md`](docs/README.md).

- **Méthodes** : comptage, normalisation du texte, modèle de données, statistiques, couche IA, validité, éthique.
- **Outils** : pile technique et pourquoi chaque outil, et le dispositif Claude Code (agents, skills, commandes, hooks).
- **Données** : sources, licences, dictionnaire de données.
- **Reproductibilité** : comment regénérer chaque résultat et le vérifier.
- **Décisions** : journal daté de chaque choix et de chaque erreur corrigée.
- **Glossaire** : chaque notion technique, avec un exemple.

## Licences

- Texte coranique : Tanzil Project, [CC BY 3.0](https://tanzil.net/docs/Text_License), copie verbatim, attribution à tanzil.net.
- Morphologie : Quranic Arabic Corpus, GNU GPL, corpus.quran.com (non encore intégrée).
- Code de Quran Lab : **licence à choisir** par l'auteur (aucune licence n'est encore déclarée ; tant qu'aucune n'est ajoutée, tous droits réservés par défaut).
