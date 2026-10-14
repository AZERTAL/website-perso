# 01 · Règles de comptage

Code : [`src/quran_lab/count.py`](../../src/quran_lab/count.py), [`rules.py`](../../src/quran_lab/rules.py), [`multiverse.py`](../../src/quran_lab/multiverse.py). Tests : [`tests/unit/test_count.py`](../../tests/unit/test_count.py), [`tests/property/test_count_props.py`](../../tests/property/test_count_props.py).

## L'idée centrale : un décompte n'est pas un nombre

« Combien de fois le mot *jour* apparaît-il ? » n'a pas **une** réponse. Cela dépend de ce qu'on appelle « le même mot ». Le projet ne choisit pas : il calcule la réponse sous toutes les règles applicables (analyse multivers) et montre la dispersion.

**Exemple concret (mesuré sur le texte Tanzil, niveau forme).** Le mot `يوم` donne 217 occurrences si l'on exclut les composés comme `يومئذ`, et 282 si on les inclut. Même texte, même mot, deux chiffres légitimes pour deux questions différentes. Aucun n'est « le bon ».

Un décompte est donc stocké comme un **ensemble de positions** `(sourate, verset, rang du mot)`. Le nombre en dérive (`len`). Chaque chiffre est traçable à ses versets.

## Les 4 niveaux

| Niveau | On compte | Exemple pour « jour » | Source de l'information |
|---|---|---|---|
| `form` (forme) | les mots dont le squelette consonantique est égal à la requête | `يوم` seul. `واليوم` et `أيام` ne comptent pas | texte Tanzil |
| `stem` (radical) | le radical après retrait des préfixes et suffixes | `واليوم` → `يوم` (و et ال retirés) | morphologie |
| `lemma` (lemme) | toutes les flexions d'un même mot | `يوم`, `يومين`, `أيام` | morphologie |
| `root` (racine) | tous les mots de la racine | ي و م | morphologie |

Les niveaux `stem`, `lemma`, `root` exigent la morphologie du Quranic Arabic Corpus, **non encore acquise** : ils sont déclarés *non évalués*.

## Les axes de règles

| Axe | Valeurs | S'applique à |
|---|---|---|
| Basmala | `all_113`, `numbered_only`, `none` | tous les niveaux |
| Lettres isolées (muqatta'at) | `include`, `exclude` | tous les niveaux |
| Orthographe | `uthmani`, `simple` | **niveau forme seulement** |
| Mots composés (ex. `يومئذ`) | `with_base`, `separate` | tous les niveaux |

Total : forme 3 × 2 × 2 × 2 = 24 cellules ; radical, lemme, racine 3 × 2 × 1 × 2 = 12 chacun ; **60 cellules** (`quran_lab.rules.grid()`).

### `n/a` n'est pas zéro

L'orthographe n'a aucun sens pour le lemme (le corpus morphologique n'existe qu'en une seule orthographe). Cette cellule n'existe pas : elle est « non applicable ». De même, quand la morphologie manque, les cellules radical/lemme/racine sont « non évaluées ». Les traiter comme `0` fabriquerait un résultat. Le code les écarte (`Multiverse.not_evaluated`) et le verdict devient **PARTIEL**.

### La basmala (trois états)

Constat sur le texte réel : Tanzil préfixe la basmala au verset 1 de **113 sourates sur 114** (toutes sauf la 9) ; 1:1 est la basmala elle-même. Donc :

- `all_113` : on compte les 113 basmalas (l'état du texte Tanzil tel quel au niveau forme) ;
- `numbered_only` : seule 1:1 (la basmala qui est un verset numéroté) ;
- `none` : aucune.

Au niveau forme, les 112 en-têtes sont de vrais mots marqués `header=True`. Aux niveaux morphologiques, le corpus n'a pas ces en-têtes ; `all_113` y ajoute des copies *virtuelles* des occurrences de 1:1.

> Exclure les muqatta'at d'un verset ne retire **jamais** sa basmala : l'une relève de l'axe muqatta'at, l'autre de l'axe basmala. Un test le garantit.

### Les mots composés

`يومئذ` = `يوم` + `إذ`. Selon la source d'annotation, il compte ou non pour `يوم`. La règle est donc explicite et ne dépend pas de l'annotation : `config/counting_rules.yaml` liste les composés et leur base ; `with_base` les ajoute, `separate` les retire.

## Requête vocalisée ou non

- Une requête **sans diacritiques** (`يوم`) est comparée au squelette.
- Une requête **avec diacritiques** (`مَلَك`, « ange ») est comparée *exactement*, et n'est acceptée qu'au niveau lemme. Cela permet de séparer les homographes `مَلَك` (ange), `مَلِك` (roi), `مُلْك` (royauté).
- Pour une requête sans diacritiques au niveau lemme, le résultat liste les **variantes fusionnées** : la fusion est visible, jamais silencieuse.

## Ventilation singulier / duel / pluriel

Chaque résultat porte une ventilation `S`, `D`, `P`, `?` (`?` : non marqué ou sans objet). C'est une heuristique de *rapport* (`count.number_of`), pas un axe de la grille. Elle reste à valider sur le corpus morphologique réel.

## Pièges linguistiques à traiter explicitement

| Piège | Exemple | Conséquence |
|---|---|---|
| Racine polysémique | ج ن ن : jardin (`جنة`), djinns (`جن`), folie (`مجنون`), fœtus (`جنين`) | compter le paradis par racine surévalue ; il faut ventiler par lemme |
| Homographes | `ملك` : ange, roi, royauté | requête vocalisée au niveau lemme |
| Pluriel supplétif | `نساء` n'a pas la racine de `امرأة` | compter les deux |
| Composés | `يومئذ`, `حينئذ` | axe des composés |
| Sens multiples | `يوم` : jour, Jour du Jugement, période | le décompte ne distingue pas les sens (limite de la méthode) |

## Comment c'est testé

1. **Tests unitaires** : valeurs attendues calculées à la main sur un mini-corpus avant exécution.
2. **Tests de propriétés** : chaque mot appartient aux décomptes de son propre radical, lemme exact et racine ; deux chemins de code (`count`, `type_counts`) concordent ; l'ordre des données ne change rien.
3. **Test différentiel** : le niveau forme est calculé par deux programmes indépendants (voir [02](02-normalization.md)) sur **tout le texte** : zéro désaccord.
4. **Test de mutation (manuel)** : 10 règles cassées volontairement ; les tests les détectent toutes.
