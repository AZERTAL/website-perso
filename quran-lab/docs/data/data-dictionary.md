# Dictionnaire de données

## Base DuckDB `data/quran.duckdb` (non versionnée, `make db`)

### Table `words` : un mot d'une orthographe Tanzil

| Colonne | Type | Signification |
|---|---|---|
| `variant` | texte | `uthmani` ou `simple` (les deux orthographes ont des positions **différentes**) |
| `sura` | entier | numéro de sourate, 1 à 114 |
| `aya` | entier | numéro du verset dans la sourate (numérotation Tanzil, lecture Hafs) |
| `word` | entier | rang du mot dans le verset, à partir de 1, pour **cette** orthographe |
| `text` | texte | le mot tel qu'écrit par Tanzil, **sans modification** |
| `header` | booléen | vrai pour les 4 mots de la basmala que Tanzil préfixe au verset 1 des sourates 2 à 114 (sauf 9) |

### Table `segments` : un segment morphologique (vide tant que la morphologie manque)

| Colonne | Signification |
|---|---|
| `sura`, `aya`, `word`, `seg` | position du mot dans le corpus morphologique et rang du segment dans le mot |
| `form` | forme du segment, avec diacritiques |
| `pos` | catégorie grammaticale |
| `seg_type` | `PREF` (préfixe), `STEM` (radical) ou `SUFF` (suffixe) |
| `root` | racine, lettres sans espaces (par exemple `يوم`) ; vide si non renseignée |
| `lemma` | lemme avec diacritiques |
| `feats` | traits morphologiques bruts, séparés par `|` |

La position `(sura, aya, word)` d'un mot de `words` et celle d'un mot de `segments` ne coïncident **pas** dans le verset 1 des sourates à basmala préfixée (décalage de 4 attendu). L'alignement est à faire à réception de la morphologie.

## Jeu de données exporté (`make dataset`, dossier `data/processed/`, non versionné)

| Fichier | Contenu | Lignes |
|---|---|---|
| `words.csv`, `words.parquet` | colonnes `variant, sura, aya, word, text, skeleton, header` ; `skeleton` est **dérivé** (`normalize.skeleton`) | une par mot et par orthographe |
| `suras.csv`, `suras.parquet` | colonnes `sura, name, tname, ayas, type, order` issues de `quran-data.xml` | une par sourate |
| `NOTICE.md` | avis de copyright Tanzil, à conserver avec les fichiers | — |

`type` (Meccan, Medinan) et `order` (ordre de révélation) sont ceux de Tanzil : **un référentiel parmi d'autres, débattu**. Toute analyse chronologique doit les comparer à d'autres référentiels.

## Fichiers de rapport

| Fichier | Contenu | Produit par |
|---|---|---|
| `reports/audit-tanzil.md` et `.json` | invariants, basmala, orthographes, test différentiel, inventaire Unicode | `scripts/audit_tanzil.py` |
| `reports/H001-yawm-365.md` | grille de règles niveau forme | `quran_lab.cli verifie` |
| `reports/H001-v2-espace-de-regles.md` | 512 spécifications | `scripts/run_h001_v2.py` |
| `reports/tests_ledger.csv` | registre des tests, en ajout seul | `scripts/ledger_add.py`, `run_h001_v2.py` |

### En-tête obligatoire d'un rapport

```
---
generated_by: <commande de reproduction>
data_manifest_sha256: <empreinte unique des sources brutes>
code_sha: <commit du code ; "-dirty" si du code n'était pas commité>
hypothesis: <identifiant pré-enregistré, si applicable>
---
```

Tout chiffre d'un rapport est dans un bloc `<!-- BEGIN generated:... -->` ... `<!-- END generated -->`. `scripts/check_reports.py` refuse un chiffre en dehors.

### Registre des tests (`tests_ledger.csv`)

`test_id, date, hypothesis, family, n_comparisons, statistic, p_raw, p_adjusted, status`. `n/a` quand le test n'a pas de p-value. Statuts : `ROBUSTE`, `DÉPEND DE LA RÈGLE`, `NON SIGNIFICATIF`, `NON REPRODUCTIBLE`, `PARTIEL`.
