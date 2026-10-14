# Documentation de Quran Lab

Index. Chaque page dit ce qui est **implémenté**, ce qui est **planifié**, et ce qui n'est **pas vérifié**.

## Méthodes : comment on compte et comment on conclut

| Page | Contenu |
|---|---|
| [01 · Règles de comptage](methodology/01-counting-rules.md) | les 4 niveaux, les axes de règles, la grille de 60 cellules, `n/a` ≠ 0 |
| [02 · Normalisation du texte arabe](methodology/02-normalization.md) | le « squelette » consonantique, les pièges Unicode trouvés sur le texte réel |
| [03 · Modèle de données et pipeline](methodology/03-data-model-and-pipeline.md) | du fichier brut à la base DuckDB, la basmala, les deux orthographes |
| [04 · Statistiques](methodology/04-statistics.md) | pré-enregistrement, modèles nuls, comparaisons multiples, statuts d'un résultat |
| [05 · Couche IA](methodology/05-ai-methods.md) | embeddings, thèmes, réseau, cycles : méthode prévue et critères de validation (non implémenté) |
| [06 · Validité et limites](methodology/06-validity-and-limits.md) | menaces à la validité et comment chacune est traitée |
| [07 · Éthique et respect du texte](methodology/07-ethics.md) | règles de conduite du projet |

## Outils

| Page | Contenu |
|---|---|
| [Pile technique](tools/stack.md) | chaque outil, à quoi il sert, pourquoi celui-là |
| [Dispositif Claude Code](tools/claude-code.md) | agents, skills, commandes slash, hooks : ce qu'ils imposent |
| [Intégration continue](tools/ci.md) | ce que la CI vérifie |

## Données

| Page | Contenu |
|---|---|
| [Sources et licences](data/sources.md) | Tanzil, Quranic Arabic Corpus, options choisies, conditions d'attribution |
| [Dictionnaire de données](data/data-dictionary.md) | tables DuckDB, fichiers de rapport, jeu de données exporté |
| [Divergences entre sources](divergences.md) | écarts constatés et règle retenue |

## Pilotage

| Page | Contenu |
|---|---|
| [Reproductibilité](reproducibility.md) | comment regénérer chaque résultat et le vérifier |
| [Feuille de route et traçabilité](roadmap.md) | chaque exigence du cahier des charges, son état, où elle vit |
| [Décisions](DECISIONS.md) | journal daté : décision, raison, application |
| [Plans](plans/) | plans de phase |
| [Glossaire](glossary.md) | chaque notion technique, avec un exemple |

## Conventions de lecture

- `FAIT` : compté ou vérifié sur le texte source, règle indiquée.
- `INTERPRÉTATION` : lecture d'un exégète ou d'un chercheur, citée.
- `AFFIRMATION POPULAIRE` : circule en ligne ou dans des livres, à vérifier, jamais présentée comme acquise.
- Statuts d'un pattern : `ROBUSTE`, `DÉPEND DE LA RÈGLE`, `NON SIGNIFICATIF`, `NON REPRODUCTIBLE`.
- « Implémenté » veut dire : du code existe et des tests le couvrent. « Planifié » veut dire : décrit, pas encore écrit.
