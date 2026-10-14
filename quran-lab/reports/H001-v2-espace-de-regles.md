---
generated_by: cd quran-lab && uv run python scripts/run_h001_v2.py
data_manifest_sha256: 6b8d4d7d4f226b38179f9cb62e57bbbcf0d1d83adc4220d90cc1833d61f4095a
code_sha: 7567af44050c
hypothesis: H001-v2
---
# H001-v2 : espace de règles de forme et de clitiques

Étiquette : `AFFIRMATION POPULAIRE` au départ. Test **post hoc**, déclaré comme tel dans `hypotheses/H001-v2.md`. Les décomptes sont des `FAIT` (texte Tanzil, analyse par expressions régulières, approximation de la morphologie).

## Verdict (lecture pré-enregistrée)
<!-- BEGIN generated:quran_lab.stats.spec_space.verdict -->
DÉPEND DE LA RÈGLE : atteint, mais pas plus que ses voisins (non remarquable)
<!-- END generated -->

Le statut ne peut pas dépasser `DÉPEND DE LA RÈGLE` : la règle atteignant la cible a été trouvée après lecture du résultat, et les modèles nuls ne sont pas implémentés.

## N(T) : combien de spécifications donnent exactement T
<!-- BEGIN generated:quran_lab.stats.spec_space.n_of -->
| T | N(T) | rôle |
|---|---|---|
| 340 | 0 |  |
| 341 | 5 |  |
| 342 | 3 |  |
| 343 | 2 |  |
| 344 | 5 |  |
| 345 | 3 |  |
| 346 | 2 |  |
| 347 | 4 |  |
| 348 | 4 |  |
| 349 | 6 |  |
| 350 | 2 |  |
| 351 | 4 |  |
| 352 | 6 |  |
| 353 | 0 |  |
| 354 | 6 |  |
| 355 | 4 |  |
| 356 | 0 |  |
| 357 | 6 |  |
| 358 | 4 |  |
| 359 | 4 |  |
| 360 | 5 | voisin |
| 361 | 5 | voisin |
| 362 | 4 | voisin |
| 363 | 3 | voisin |
| 364 | 8 | voisin |
| 365 | 5 | cible |
| 366 | 0 | voisin |
| 367 | 5 | voisin |
| 368 | 5 | voisin |
| 369 | 0 | voisin |
| 370 | 5 | voisin |
| 371 | 6 |  |
| 372 | 1 |  |
| 373 | 3 |  |
| 374 | 7 |  |
| 375 | 4 |  |
| 376 | 1 |  |
| 377 | 4 |  |
| 378 | 3 |  |
| 379 | 1 |  |
| 380 | 4 |  |
| 381 | 4 |  |
| 382 | 1 |  |
| 383 | 1 |  |
| 384 | 4 |  |
| 385 | 1 |  |
| 386 | 1 |  |
| 387 | 2 |  |
| 388 | 1 |  |
| 389 | 1 |  |
| 390 | 3 |  |
<!-- END generated -->

<!-- BEGIN generated:quran_lab.stats.spec_space.summary -->
| mesure | valeur |
|---|---|
| spécifications | 512 |
| décomptes distincts | 171 |
| interrupteurs sans effet | aucun |
| N(cible) | 5 |
| max N(voisins) | 8 |
<!-- END generated -->

## La spécification citée par le relecteur
<!-- BEGIN generated:quran_lab.stats.spec_space.reviewer_mask -->
| texte | interrupteurs actifs | décompte |
|---|---|---|
| simple | T1, T2, T3, T4 | 365 |
| uthmani | T1, T2, T3, T4 | 365 |
<!-- END generated -->

Cette spécification n'est qu'une parmi toutes ; elle a été trouvée en regardant le résultat. Sa valeur ne prouve rien tant qu'on ne sait pas combien de spécifications atteignent aussi les nombres voisins (tableau N(T) ci-dessus).

## Interrupteurs
| code | classe de formes incluse |
|---|---|
| T1 | conjonction (و, ف) |
| T2 | préposition (ب, ل, ك) |
| T3 | article (ال) |
| T4 | accusatif indéfini (ـا) |
| T5 | duel (ـين, ـان) |
| T6 | pronom suffixé |
| T7 | composé (يومئذ) |
| T8 | pluriel (أيام) |

## Formes reconnues (texte simple)
<!-- BEGIN generated:quran_lab.stats.spec_space.parse_form -->
| forme | occurrences | classes |
|---|---|---|
| يوم | 217 | base |
| يومئذ | 65 | T7 |
| ويوم | 44 | T1 |
| اليوم | 41 | T3 |
| واليوم | 23 | T1, T3 |
| أيام | 20 | T8 |
| يوما | 16 | T4 |
| ليوم | 8 | T2 |
| فاليوم | 8 | T1, T3 |
| يومكم | 5 | T6 |
| يومهم | 5 | T6 |
| بيوم | 5 | T2 |
| فيومئذ | 4 | T1, T7 |
| يومين | 3 | T5 |
| الأيام | 2 | T3, T8 |
| باليوم | 2 | T2, T3 |
| وباليوم | 1 | T1, T2, T3 |
| بأيام | 1 | T2, T8 |
| ويومئذ | 1 | T1, T7 |
<!-- END generated -->

## Mots contenant la séquence mais non reconnus (listés, jamais ignorés)
<!-- BEGIN generated:quran_lab.stats.spec_space.unmatched -->
| forme | occurrences (texte simple, puis uthmani) |
|---|---|
| القيوم | 3 / 3 |
<!-- END generated -->

## Limites
- Approximation par expressions régulières : ne remplace pas le corpus morphologique ; le test sera refait sur les vrais radicaux (`H001-v3`).
- Le sens (jour calendaire, Jour du Jugement, période) n'est pas distingué.
- Lecture Hafs ʿan ʿĀṣim, texte Tanzil uniquement.

## Reproduction
```
cd quran-lab && uv run python scripts/run_h001_v2.py
```
