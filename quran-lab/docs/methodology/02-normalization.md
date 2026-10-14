# 02 · Normalisation du texte arabe

Code : [`src/quran_lab/normalize.py`](../../src/quran_lab/normalize.py). Tests : [`tests/unit/test_normalize.py`](../../tests/unit/test_normalize.py), [`tests/property/test_normalize_props.py`](../../tests/property/test_normalize_props.py), [`tests/differential/`](../../tests/differential/).

## Pourquoi normaliser

Le texte coranique Uthmani porte des voyelles courtes, des signes de pause, des signes d'allongement. Pour savoir si deux mots sont « la même suite de lettres », on les ramène à leur **squelette consonantique** : les lettres de base, sans diacritiques.

Exemple : `يَوْمِ`, `يَوْمَ`, `يَوْمٌ` ont trois voyelles de fin différentes et le même squelette `يوم`.

## Ce que fait `skeleton(texte)`

Dans cet ordre exact :

1. **Alif + signe d'allongement (maddah, U+0653) → alif simple.** Avant toute recomposition Unicode.
2. **NFC** (jamais NFD).
3. **Tatwil portant une hamza combinante → lettre `ء`**, quelles que soient les voyelles intercalées.
4. **Alif wasla `ٱ` → `ا`.**
5. **Retrait** des marques combinantes (catégorie Unicode `Mn`), des signes coraniques non combinants (fin de verset, début de rub, prosternation, petit waw, petit ya), des caractères de contrôle de direction et du tatwil restant.
6. **Espaces** normalisés.

`skeleton` est une fonction pure, mémoïsée (`@cache`) : les mots se répètent massivement (14 814 types pour 77 881 occurrences en Uthmani).

## Ce que `skeleton` ne fait PAS (volontairement)

Il ne replie **pas** `أ`, `إ`, `آ` vers `ا`, ni `ى` vers `ي`, ni `ة` vers `ه`. Ces repliements changent la langue et créent des collisions. Ils existent comme options explicites (`normalize.fold(...)`), désactivées par défaut, jamais appliquées en silence.

## Les deux pièges trouvés sur le texte réel

Ces erreurs n'ont pas été vues en relisant le code. Elles sont apparues quand un **test différentiel** a comparé deux implémentations sur tout le texte Tanzil (voir [DECISIONS D11](../DECISIONS.md)).

### 1. La maddah devenait une lettre

Tanzil Uthmani écrit `الضَّالِّينَ` avec `ا` (U+0627) suivi du signe `ٓ` (U+0653). La recomposition NFC les fusionne en la **lettre** `آ` (U+0622). Le squelette obtenu était `الضآلين` au lieu de `الضالين` (l'orthographe simple). Correction : retirer le signe avant NFC.

### 2. NFC séparait le tatwil de sa hamza

Le fichier écrit pour `وبالآخرة` la séquence : tatwil (U+0640), hamza combinante (U+0654), fatha (U+064E). NFC réordonne les marques par « classe de combinaison » et met la fatha *avant* la hamza : le tatwil et la hamza ne sont plus adjacents, la règle ne se déclenchait plus et **la hamza disparaissait**. Correction : la règle accepte des voyelles entre le tatwil et la hamza.

Avant correction, 1 077 graphies distinctes (3 687 occurrences) divergeaient entre les deux implémentations *(mesure manuelle, consignée dans DECISIONS D11)*. Après correction : zéro désaccord sur tout le texte, dans les deux orthographes.

## Le test différentiel (méthode)

Deux programmes écrits **séparément** doivent donner le même résultat. S'ils divergent, l'un des deux a un bug.

| | A | B |
|---|---|---|
| Normalisation | `normalize.skeleton` (catégories Unicode, NFC) | `audit.naive_skeleton` (plages de code, expressions régulières, sans NFC) |
| Comptage | `count.type_counts` / `count.count` | `collections.Counter` sur les mots normalisés |

Exécution : `uv run python scripts/audit_tanzil.py` (rapport [`reports/audit-tanzil.md`](../../reports/audit-tanzil.md)), et le test `tests/differential/test_full_text.py`.

**Limite honnête.** A et B sont indépendants *entre eux*, mais je les ai écrits tous les deux. Ils détectent une erreur d'implémentation, pas une erreur de **conception** partagée (par exemple, ranger à tort deux orthographes dans la même catégorie). Une relecture linguistique reste nécessaire (agent `linguiste-morpho`, puis un humain spécialiste).

## Inventaire des caractères

`normalize.unicode_inventory` et le rapport d'audit listent chaque caractère non-ASCII du texte avec son nom et sa catégorie. Tout caractère inattendu doit être traité explicitement.
