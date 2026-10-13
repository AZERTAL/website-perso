---
description: Compte un mot ou une racine aux 4 niveaux et sous toutes les règles (grille multivers)
argument-hint: <mot ou racine arabe> [--target N]
---
Compte `$ARGUMENTS` dans le corpus.

1. Vérifie que `quran-lab/data/quran.duckdb` existe. Sinon, dis-le et arrête-toi : la base n'est pas construite (sources absentes), tu n'inventes aucun chiffre.
2. Lance : `cd quran-lab && uv run python -m quran_lab.cli compte $ARGUMENTS`.
3. Rends le tableau tel quel (niveau × règle -> décompte), la distribution des décomptes sur la grille, et la liste des variantes fusionnées.
4. Ajoute 3 versets pris dans les occurrences, avec leurs tokens et la raison du comptage.
5. Étiquette : tout nombre est `FAIT` avec sa règle ; précise les cellules `n/a`.
