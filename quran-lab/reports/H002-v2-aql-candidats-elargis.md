---
generated_by: cd quran-lab && uv run python scripts/run_h002_v2.py
data_manifest_sha256: 6b8d4d7d4f226b38179f9cb62e57bbbcf0d1d83adc4220d90cc1833d61f4095a
code_sha: 82b96585a741
hypothesis: H002-v2
---
# H002-v2 : formes de la racine `عقل`, candidats élargis

Étiquette : `AFFIRMATION POPULAIRE` au départ ; décomptes `FAIT` (texte Tanzil). Essai de réfutation de H002 : le filtre de candidats accepte les lettres intercalées (`عاقل`, `عقول`).

## Verdict (lecture pré-enregistrée)
<!-- BEGIN generated:scripts.run_h002_v2.verdict -->
REPRODUIT sur ce périmètre
<!-- END generated -->

## Décomptes par classe et par orthographe
<!-- BEGIN generated:quran_lab.stats.form_classes.classify -->
| orthographe | verbal | nominal | autre |
|---|---|---|---|
| simple | 49 | 0 | 0 |
| uthmani | 49 | 0 | 0 |
<!-- END generated -->

## Formes rencontrées (simple)
<!-- BEGIN generated:quran_lab.stats.form_classes.forms -->
| classe | forme (squelette) | occurrences |
|---|---|---|
| verbal | تعقلون | 24 |
| verbal | يعقلون | 22 |
| verbal | عقلوه | 1 |
| verbal | يعقلها | 1 |
| verbal | نعقل | 1 |
<!-- END generated -->

## Formes rencontrées (uthmani)
<!-- BEGIN generated:quran_lab.stats.form_classes.forms -->
| classe | forme (squelette) | occurrences |
|---|---|---|
| verbal | تعقلون | 24 |
| verbal | يعقلون | 22 |
| verbal | عقلوه | 1 |
| verbal | يعقلها | 1 |
| verbal | نعقل | 1 |
<!-- END generated -->

## Limites
- Approximation par expressions régulières ; le sens n'est pas distingué.
- Les faux positifs (mots d'une autre racine) sont listés dans la classe « autre ».
- Lecture Hafs ʿan ʿĀṣim, texte Tanzil uniquement.

## Reproduction
```
cd quran-lab && uv run python scripts/run_h002_v2.py
```
