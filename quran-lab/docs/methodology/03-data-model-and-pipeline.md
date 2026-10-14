# 03 · Modèle de données et pipeline

Code : [`model.py`](../../src/quran_lab/model.py), [`load.py`](../../src/quran_lab/load.py), [`db.py`](../../src/quran_lab/db.py), [`validate.py`](../../src/quran_lab/validate.py), [`scripts/build_db.py`](../../scripts/build_db.py).

## Vue d'ensemble

```
tanzil.net ──fetch_sources.py──▶ data/raw/*.txt|xml  (lecture seule, hash dans SOURCES.md)
corpus.quran.com (en attente) ─▶ data/raw/quranic-corpus-morphology-0.4.txt
                                       │
                          build_db.py (load.py: parse_tanzil, build_words, parse_morphology)
                                       ▼
                              data/quran.duckdb  (tables words, segments)
                                       │
         count.py / multiverse.py / stats/ / audit.py ──▶ reports/*.md, reports/*.json
                                       │
                          build_status_page.py ──▶ site/status.html
```

Principe : **la logique est pure** (aucune lecture de fichier dans `count.py`, `normalize.py`, `rules.py`) ; les entrées/sorties sont dans `load.py`, `db.py` et `scripts/`.

## Les objets

| Objet | Contenu | Remarque |
|---|---|---|
| `Word` | un mot d'**une** orthographe Tanzil : `sura, aya, word, text, variant, header` | `variant` ∈ `uthmani`, `simple` |
| `Segment` | un segment morphologique : forme, catégorie, type (`PREF`/`STEM`/`SUFF`), racine, lemme, traits | n'existe qu'avec la morphologie |
| `Corpus` | l'ensemble des `Word` et des `Segment`, avec index | `has_morphology` |
| `Loc` | position `(sourate, verset, rang du mot)` | verset `0` = en-tête de basmala virtuel |

## Trois faits du texte réel qui ont façonné le modèle

### 1. Deux orthographes = deux listes de mots différentes

363 versets n'ont pas le même nombre de mots en Uthmani et en simple-clean (par exemple 2:21). Cause typique : `يَـٰٓأَيُّهَا` est **un** mot en Uthmani et **deux** (`يا أيها`) en simple. Un appariement des mots par position aurait supprimé ces versets en silence. Décision ([DECISIONS D10](../DECISIONS.md)) : chaque orthographe a ses propres `Word` et ses propres positions, et on n'apparie jamais entre elles.

### 2. La basmala est préfixée au verset 1 de 113 sourates

`load._header_len` la détecte *par comparaison* avec les mots de 1:1 dans la même orthographe (aucune longueur n'est supposée) et marque ces mots `header=True`. Le rapport d'audit vérifie qu'aucune sourate (hors 1 et 9) n'échappe à la règle. Voir [01 · Règles de comptage](01-counting-rules.md).

### 3. Les positions Tanzil et corpus diffèrent

Le corpus morphologique ne contient pas les en-têtes de basmala (à vérifier à réception du fichier) : dans le verset 1 des sourates concernées, les positions du corpus sont décalées de 4 par rapport à Tanzil. L'alignement fera partie du chargement de la morphologie (`docs/divergences.md`).

## La base DuckDB

`data/quran.duckdb` est reconstruite par `build_db.py` (≈ 2 s). Elle n'est pas versionnée. Schéma : [dictionnaire de données](../data/data-dictionary.md).

Insertion en bloc via Arrow : `executemany` insérait ligne par ligne et prenait plusieurs minutes pour 156 000 mots.

## Invariants contrôlés

Assertés par `scripts/audit_tanzil.py` (échec si rompus) :

- 114 sourates ; nombre de versets de chaque sourate égal à celui de `quran-data.xml` ;
- aucun verset vide ;
- chaque sourate hors 1 et 9 commence par la basmala ;
- zéro désaccord entre les deux implémentations de la normalisation.

Prévus pour la morphologie (`validate.py`) : tout mot a au moins un segment radical ; chaque lemme exact n'a qu'une racine.

## Ce qui n'est pas fait

- Chargement de la morphologie sur le **vrai** fichier. Le lecteur du format v0.4 est écrit de mémoire et n'a pas été validé ; seul le format du fork a été validé sur 16 lignes réelles.
- Alignement Tanzil ↔ corpus mot à mot.
- Métadonnées enrichies (juz', hizb, sajda) : `quran-data.xml` les contient, elles ne sont pas encore chargées.
