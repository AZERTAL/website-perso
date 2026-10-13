---
generated_by: cd quran-lab && uv run python scripts/build_db.py && uv run python scripts/audit_tanzil.py
data_manifest_sha256: 6b8d4d7d4f226b38179f9cb62e57bbbcf0d1d83adc4220d90cc1833d61f4095a
code_sha: 9bf95076c423-dirty
---
# Audit des sources Tanzil

Source : Tanzil Project v1.1, licence CC BY 3.0, texte non modifié. Fichiers, hash et options : `SOURCES.md`. <!-- allow-number: version de licence, pas un résultat -->

Étiquette : tout ce qui suit est `FAIT` (compté par `scripts/audit_tanzil.py` sur les fichiers de `data/raw/`). La morphologie n'est pas encore acquise.

## 1. Invariants par rapport aux métadonnées officielles (`quran-data.xml`)
<!-- BEGIN generated:quran_lab.audit.verse_invariants -->
| orthographe | sourates | versets | sourates au nb de versets ≠ métadonnées | versets vides | sourates sans basmala préfixée (hors 1 et 9) |
|---|---|---|---|---|---|
| uthmani | 114 | 6236 | aucune | aucun | [95, 97] |
| simple-clean | 114 | 6236 | aucune | aucun | aucune |

| type (métadonnées) | sourates |
|---|---|
| Meccan | 86 |
| Medinan | 28 |
<!-- END generated -->

## 2. La basmala est préfixée au verset 1 de 113 sourates sur 114
<!-- BEGIN generated:quran_lab.load.build_words -->
| orthographe | mots d'en-tête (header=True) | mots au total |
|---|---|---|
| uthmani | 440 | 77881 |
| simple | 448 | 78248 |
<!-- END generated -->

Conséquence : le texte Tanzil contient déjà la basmala devant le verset 1 des sourates 2 à 114 (sauf 9). Le corpus morphologique ne les contient pas (à vérifier à réception). L'axe « basmala » et l'exclusion des muqatta'at en tiennent compte (DECISIONS D9). <!-- allow-number: numéros de sourates cités dans le texte, pas un résultat -->

## 3. Les deux orthographes n'ont pas les mêmes mots
<!-- BEGIN generated:quran_lab.audit.word_diffs -->
| mesure | valeur |
|---|---|
| versets au nombre de mots différent | 363 |
| mots en plus dans simple-clean (somme) | 367 |
| versets où simple-clean a MOINS de mots | 0 |

| sourate | verset | mots Uthmani | mots simple-clean |
|---|---|---|---|
| 2 | 21 | 11 | 12 |
| 2 | 33 | 22 | 23 |
| 2 | 35 | 18 | 19 |
| 2 | 40 | 13 | 14 |
| 2 | 47 | 11 | 12 |
| 2 | 54 | 26 | 27 |
| 2 | 55 | 14 | 15 |
| 2 | 61 | 59 | 60 |
| 2 | 104 | 12 | 13 |
| 2 | 122 | 11 | 12 |
<!-- END generated -->

Conséquence : une position de mot n'a de sens que dans sa propre orthographe. Le modèle n'apparie jamais les mots entre orthographes.

## 4. Test différentiel sur TOUT le texte (deux implémentations indépendantes)
<!-- BEGIN generated:quran_lab.audit.differential_full_text -->
| orthographe | occurrences | types (A) | types (B) | types au décompte différent | échantillon | désaccords sur l'échantillon | mots au squelette différent A/B |
|---|---|---|---|---|---|---|---|
| uthmani | 77881 | 14814 | 14814 | aucun | 100 | aucun | 0 |
| simple | 78248 | 14868 | 14868 | aucun | 100 | aucun | 0 |
<!-- END generated -->

A = `normalize.skeleton` + `type_counts`/`count` ; B = regex par plages de code. Échantillon tiré avec la graine inscrite dans `audit.differential_full_text`.

## 5. Inventaire des caractères non-ASCII
### Uthmani
<!-- BEGIN generated:quran_lab.audit.unicode_table -->
| code | nom | catégorie | occurrences |
|---|---|---|---|
| U+0621 | ARABIC LETTER HAMZA | Lo | 2782 |
| U+0623 | ARABIC LETTER ALEF WITH HAMZA ABOVE | Lo | 8900 |
| U+0624 | ARABIC LETTER WAW WITH HAMZA ABOVE | Lo | 706 |
| U+0625 | ARABIC LETTER ALEF WITH HAMZA BELOW | Lo | 5088 |
| U+0626 | ARABIC LETTER YEH WITH HAMZA ABOVE | Lo | 921 |
| U+0627 | ARABIC LETTER ALEF | Lo | 25184 |
| U+0628 | ARABIC LETTER BEH | Lo | 11603 |
| U+0629 | ARABIC LETTER TEH MARBUTA | Lo | 2344 |
| U+062A | ARABIC LETTER TEH | Lo | 10520 |
| U+062B | ARABIC LETTER THEH | Lo | 1414 |
| U+062C | ARABIC LETTER JEEM | Lo | 3317 |
| U+062D | ARABIC LETTER HAH | Lo | 4364 |
| U+062E | ARABIC LETTER KHAH | Lo | 2497 |
| U+062F | ARABIC LETTER DAL | Lo | 5991 |
| U+0630 | ARABIC LETTER THAL | Lo | 4932 |
| U+0631 | ARABIC LETTER REH | Lo | 12627 |
| U+0632 | ARABIC LETTER ZAIN | Lo | 1599 |
| U+0633 | ARABIC LETTER SEEN | Lo | 6122 |
| U+0634 | ARABIC LETTER SHEEN | Lo | 2124 |
| U+0635 | ARABIC LETTER SAD | Lo | 2074 |
| U+0636 | ARABIC LETTER DAD | Lo | 1686 |
| U+0637 | ARABIC LETTER TAH | Lo | 1273 |
| U+0638 | ARABIC LETTER ZAH | Lo | 853 |
| U+0639 | ARABIC LETTER AIN | Lo | 9405 |
| U+063A | ARABIC LETTER GHAIN | Lo | 1221 |
| U+0640 | ARABIC TATWEEL | Lm | 6848 |
| U+0641 | ARABIC LETTER FEH | Lo | 8747 |
| U+0642 | ARABIC LETTER QAF | Lo | 7034 |
| U+0643 | ARABIC LETTER KAF | Lo | 10497 |
| U+0644 | ARABIC LETTER LAM | Lo | 38550 |
| U+0645 | ARABIC LETTER MEEM | Lo | 27071 |
| U+0646 | ARABIC LETTER NOON | Lo | 27380 |
| U+0647 | ARABIC LETTER HEH | Lo | 14962 |
| U+0648 | ARABIC LETTER WAW | Lo | 24970 |
| U+0649 | ARABIC LETTER ALEF MAKSURA | Lo | 6603 |
| U+064A | ARABIC LETTER YEH | Lo | 18334 |
| U+064B | ARABIC FATHATAN | Mn | 3741 |
| U+064C | ARABIC DAMMATAN | Mn | 2519 |
| U+064D | ARABIC KASRATAN | Mn | 2633 |
| U+064E | ARABIC FATHA | Mn | 123396 |
| U+064F | ARABIC DAMMA | Mn | 37320 |
| U+0650 | ARABIC KASRA | Mn | 46642 |
| U+0651 | ARABIC SHADDA | Mn | 23016 |
| U+0652 | ARABIC SUKUN | Mn | 37372 |
| U+0653 | ARABIC MADDAH ABOVE | Mn | 5376 |
| U+0654 | ARABIC HAMZA ABOVE | Mn | 773 |
| U+0670 | ARABIC LETTER SUPERSCRIPT ALEF | Mn | 9838 |
| U+0671 | ARABIC LETTER ALEF WASLA | Lo | 13819 |
| U+06DC | ARABIC SMALL HIGH SEEN | Mn | 2 |
| U+06DF | ARABIC SMALL HIGH ROUNDED ZERO | Mn | 3988 |
| U+06E0 | ARABIC SMALL HIGH UPRIGHT RECTANGULAR ZERO | Mn | 66 |
| U+06E2 | ARABIC SMALL HIGH MEEM ISOLATED FORM | Mn | 510 |
| U+06E3 | ARABIC SMALL LOW SEEN | Mn | 1 |
| U+06E5 | ARABIC SMALL WAW | Lm | 1257 |
| U+06E6 | ARABIC SMALL YEH | Lm | 957 |
| U+06E7 | ARABIC SMALL HIGH YEH | Mn | 38 |
| U+06E8 | ARABIC SMALL HIGH NOON | Mn | 1 |
| U+06EA | ARABIC EMPTY CENTRE LOW STOP | Mn | 1 |
| U+06EB | ARABIC EMPTY CENTRE HIGH STOP | Mn | 1 |
| U+06EC | ARABIC ROUNDED HIGH STOP WITH FILLED CENTRE | Mn | 1 |
| U+06ED | ARABIC SMALL LOW MEEM | Mn | 99 |
<!-- END generated -->

### simple-clean
<!-- BEGIN generated:quran_lab.audit.unicode_table -->
| code | nom | catégorie | occurrences |
|---|---|---|---|
| U+0621 | ARABIC LETTER HAMZA | Lo | 1578 |
| U+0622 | ARABIC LETTER ALEF WITH MADDA ABOVE | Lo | 1511 |
| U+0623 | ARABIC LETTER ALEF WITH HAMZA ABOVE | Lo | 9119 |
| U+0624 | ARABIC LETTER WAW WITH HAMZA ABOVE | Lo | 673 |
| U+0625 | ARABIC LETTER ALEF WITH HAMZA BELOW | Lo | 5108 |
| U+0626 | ARABIC LETTER YEH WITH HAMZA ABOVE | Lo | 1182 |
| U+0627 | ARABIC LETTER ALEF | Lo | 43875 |
| U+0628 | ARABIC LETTER BEH | Lo | 11603 |
| U+0629 | ARABIC LETTER TEH MARBUTA | Lo | 2344 |
| U+062A | ARABIC LETTER TEH | Lo | 10520 |
| U+062B | ARABIC LETTER THEH | Lo | 1414 |
| U+062C | ARABIC LETTER JEEM | Lo | 3317 |
| U+062D | ARABIC LETTER HAH | Lo | 4364 |
| U+062E | ARABIC LETTER KHAH | Lo | 2497 |
| U+062F | ARABIC LETTER DAL | Lo | 5991 |
| U+0630 | ARABIC LETTER THAL | Lo | 4932 |
| U+0631 | ARABIC LETTER REH | Lo | 12627 |
| U+0632 | ARABIC LETTER ZAIN | Lo | 1599 |
| U+0633 | ARABIC LETTER SEEN | Lo | 6124 |
| U+0634 | ARABIC LETTER SHEEN | Lo | 2124 |
| U+0635 | ARABIC LETTER SAD | Lo | 2072 |
| U+0636 | ARABIC LETTER DAD | Lo | 1686 |
| U+0637 | ARABIC LETTER TAH | Lo | 1273 |
| U+0638 | ARABIC LETTER ZAH | Lo | 853 |
| U+0639 | ARABIC LETTER AIN | Lo | 9405 |
| U+063A | ARABIC LETTER GHAIN | Lo | 1221 |
| U+0641 | ARABIC LETTER FEH | Lo | 8747 |
| U+0642 | ARABIC LETTER QAF | Lo | 7034 |
| U+0643 | ARABIC LETTER KAF | Lo | 10497 |
| U+0644 | ARABIC LETTER LAM | Lo | 38639 |
| U+0645 | ARABIC LETTER MEEM | Lo | 27071 |
| U+0646 | ARABIC LETTER NOON | Lo | 27382 |
| U+0647 | ARABIC LETTER HEH | Lo | 14962 |
| U+0648 | ARABIC LETTER WAW | Lo | 24813 |
| U+0649 | ARABIC LETTER ALEF MAKSURA | Lo | 2595 |
| U+064A | ARABIC LETTER YEH | Lo | 22085 |
<!-- END generated -->

## Reproduction
```
cd quran-lab && uv run python scripts/build_db.py && uv run python scripts/audit_tanzil.py
```

