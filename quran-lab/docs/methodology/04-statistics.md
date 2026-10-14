# 04 · Statistiques : séparer le signal du hasard

Le cerveau humain voit des motifs partout. Cette page explique les garde-fous qui empêchent de prendre un hasard pour une découverte.

Code : [`src/quran_lab/stats/`](../../src/quran_lab/stats/), [`checks.py`](../../src/quran_lab/checks.py). Protocole : [`hypotheses/`](../../hypotheses/).

## Ce qui est implémenté, ce qui ne l'est pas

| Brique | État | Où |
|---|---|---|
| Pré-enregistrement des hypothèses, vérifié par git | **implémenté** | `hypotheses/`, `checks.check_preregistration` |
| Registre des tests en ajout seul | **implémenté** | `stats/ledger.py`, `reports/tests_ledger.csv` |
| Corrections des comparaisons multiples (Bonferroni, Holm, BH, BY, Westfall-Young) | **implémenté, testé** (pas encore appliqué à un jeu de tests réel) | `stats/multiplicity.py` |
| Taux de coïncidence N5 | **implémenté** (faible pouvoir discriminant, voir plus bas) | `stats/nulls.py` |
| Espace de spécifications (voisins) | **implémenté** pour H001-v2 | `stats/spec_space.py` |
| Modèles nuls N0 à N4 (Poisson/binomiale négative, permutations, Markov) | **planifié** | Phase 3 |
| Bootstrap par grappes de sourates, régression binomiale négative, bayésien hiérarchique | **planifié** | Phase 3 |
| Détection de ruptures chronologiques | **planifié**, exploratoire seulement | Phase 3 |

## 1. Pré-enregistrer : écrire le test avant de voir le résultat

**Pourquoi.** Si je regarde les données, puis je choisis le test qui « marche », la p-value ne vaut rien. Exemple : tester 500 règles de comptage et ne montrer que celle qui donne 365.

**Comment.** `hypotheses/Hxxx.md` fixe la requête, la cellule de règles principale, la statistique, le modèle nul, le seuil et la famille de tests. Il est commité **avant** les résultats. `checks.check_preregistration` compare les dates git : un rapport dont l'hypothèse a été modifiée après lui est refusé au commit. Pour changer un test, on ouvre `Hxxx-v2` ; l'original reste visible.

**Cas réel dans ce dépôt.** H001 (« jour = 365 ») a été commitée avant tout comptage. Son premier résultat a été relu par un relecteur indépendant, qui a trouvé qu'une combinaison de formes donne exactement 365. Cette combinaison a été trouvée *en regardant le résultat* : l'extension a donc été déclarée comme `H001-v2`, **post hoc**, avec la divulgation de ce que l'auteur savait déjà (voir [`hypotheses/H001-v2.md`](../../hypotheses/H001-v2.md) et [DECISIONS D15](../DECISIONS.md)).

## 2. Le registre des tests

Chaque test réalisé est une ligne de `reports/tests_ledger.csv` (identifiant, famille, taille de la famille, statistique, p brute, p ajustée, statut). Le fichier est en **ajout seul** : `checks.check_ledger` refuse un fichier de travail qui ne commence pas par le contenu déjà commité. Le total des comparaisons du projet est affiché dans les rapports.

## 3. Comparaisons multiples

Si l'on teste 100 000 paires de mots, environ 5 000 « tomberont juste » à 5 % par pur hasard. On ajuste donc les p-values.

| Méthode | Contrôle | Quand |
|---|---|---|
| Bonferroni | au moins une fausse découverte (FWER), très conservateur | petite famille |
| Holm | FWER, toujours au moins aussi puissant que Bonferroni | petite famille |
| Benjamini-Hochberg | proportion de fausses découvertes (FDR) | grande famille, tests indépendants ou positivement dépendants |
| Benjamini-Yekutieli | FDR sous dépendance quelconque | grande famille corrélée |
| Westfall-Young max-T | FWER par permutation, tient compte des corrélations | paires de mots d'un même texte |

**Exemple chiffré (calculé à la main, repris dans les tests)** : pour les p-values `[0.01, 0.04, 0.03, 0.005]`, Holm donne `[0.03, 0.06, 0.06, 0.02]` et Benjamini-Hochberg `[0.02, 0.04, 0.04, 0.02]`. Trois propriétés sont vérifiées sur des entrées générées automatiquement (bibliothèque `hypothesis`) : p ajustée ≥ p brute, ordre préservé, BH ≤ Holm ≤ Bonferroni.

## 4. Modèles nuls : « quel monde sans effet ? »

Un modèle nul simule un monde où le phénomène étudié n'existe pas. On compare le résultat réel à ce que ce monde produit.

| Nul | Conserve | Casse | Teste |
|---|---|---|---|
| N0 Poisson / binomiale négative avec décalage de longueur | fréquence globale | tout ordre | écart à l'attendu d'un mot |
| N1 permutation des mots dans chaque sourate | contenu de chaque sourate | ordre interne | répartition fine |
| N2 permutation des versets entre sourates | contenu des versets | structure des sourates | thèmes par sourate |
| N3 permutation des mots du texte entier | fréquences globales | tout | co-occurrences |
| N4 chaîne de Markov sur n-grammes de racines | statistique locale | cohérence globale | structures séquentielles |
| N5 « taux de base » : combien de types tombent sur la cible | — | — | coïncidences numériques |

Seul **N5** est implémenté. Les nuls N0 à N4 sont planifiés (Phase 3).

**Burstiness.** Un mot rare est souvent groupé (une histoire le répète), donc sa variance dépasse celle de Poisson. Avant de parler de « surprenant », on teste la dispersion.

## 5. Ce que mesure H001-v2 (et pourquoi N5 ne suffit pas)

N5 compte combien de types lexicaux ont exactement le décompte cible. Pour 365 il en trouve zéro, avec zéro attendu : il ne discrimine rien. La question pertinente est autre : **« 365 est-il plus facile à atteindre que ses voisins quand on balaie les règles ? »**.

`spec_space.py` définit 512 spécifications (8 interrupteurs de classes de formes × 2 orthographes). Pour chaque total `T`, `N(T)` est le nombre de spécifications qui donnent exactement `T`. Résultat (rapport [`reports/H001-v2-espace-de-regles.md`](../../reports/H001-v2-espace-de-regles.md)) : `N(365) = 5` ; le maximum de `N(T')` pour `T'` de 360 à 370 est 8 (en `T' = 364`) ; les 512 spécifications ne donnent que 171 totaux distincts. 365 est donc atteint, mais **pas plus que ses voisins**. La lecture était fixée avant le calcul.

## 6. Statuts d'un résultat

| Statut | Définition |
|---|---|
| `ROBUSTE` | tient sous toutes les règles (≥ 95 % de la grille) ET passe N0 à N3 ET survit à la correction multiple |
| `DÉPEND DE LA RÈGLE` | vrai seulement sous certaines règles, qui sont listées |
| `NON SIGNIFICATIF` | ne dépasse pas le modèle nul |
| `NON REPRODUCTIBLE` | le chiffre annoncé n'apparaît dans aucune cellule évaluée, ou dépend d'un texte modifié |
| `PARTIEL` | des niveaux n'ont pas pu être évalués : verdict non définitif |

`ROBUSTE` est **interdit** tant que N0 à N3 ne sont pas implémentés. Aucun résultat du projet n'a ce statut.

## Limites

- Les mots d'une même sourate ne sont pas indépendants : tout test inférentiel devra utiliser un bootstrap par sourates ou des nuls qui préservent la structure.
- Compter beaucoup de règles ne multiplie pas l'information : un axe sans effet (`multiverse.inert_axes`) ne produit pas de mesure indépendante.
- Une p-value seule ne suffit jamais : tailles d'effet et intervalles seront toujours rapportés (planifié).
