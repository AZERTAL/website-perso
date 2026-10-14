# Glossaire (avec exemples)

## Langue et texte

**Squelette consonantique.** Les lettres de base d'un mot, sans voyelles ni signes. *Exemple* : `يَوْمِ`, `يَوْمَ` et `يَوْمٌ` ont le même squelette `يوم`.

**Diacritiques (tashkīl).** Voyelles courtes, shadda (doublement), sukūn : marques placées au-dessus ou au-dessous des lettres.

**Uthmani / simple-clean.** Deux orthographes du même texte chez Tanzil. L'Uthmani suit l'écriture du Mushaf de Médine (nombreux signes) ; le simple-clean est l'orthographe courante sans diacritiques. *Exemple* : `يَـٰٓأَيُّهَا` (un mot en Uthmani) s'écrit `يا أيها` (deux mots) en simple.

**Basmala.** La formule `بسم الله الرحمن الرحيم`. Tanzil la préfixe au verset 1 de 113 sourates sur 114.

**Muqatta'at (lettres isolées).** Lettres qui ouvrent certaines sourates (par exemple `الم`). Elles forment un « mot » sans sens lexical à compter.

**Clitique.** Petit élément collé à un mot : conjonction (`و`), préposition (`ب`, `ل`), article (`ال`), pronom suffixé (`هم`). *Exemple* : `واليوم` = `و` + `ال` + `يوم`.

**Racine, lemme, radical, forme.** Quatre niveaux d'abstraction. *Exemple pour « jour »* : forme `يوم` ; radical `يوم` (clitiques retirés) ; lemme `يوم` regroupant `يومين`, `أيام` ; racine `ي و م`.

**Homographes.** Mots écrits pareil, de sens différents. *Exemple* : `مَلَك` (ange), `مَلِك` (roi), `مُلْك` (royauté) ont le même squelette `ملك`.

**Normalisation Unicode NFC.** Une forme canonique d'écriture des caractères. Elle recompose certaines séquences : `ا` + signe d'allongement devient la lettre `آ`. Piège réel trouvé dans ce projet (voir [02](methodology/02-normalization.md)).

## Comptage

**Multivers (analyse multivers).** Calculer le résultat sous tous les choix défendables et montrer la dispersion, au lieu de choisir celui qui arrange. *Exemple* : 217 ou 282 occurrences de `يوم` selon qu'on inclut ou non `يومئذ`.

**Cellule.** Une combinaison de règles. La grille compte 60 cellules applicables.

**`n/a` (non applicable) et « non évalué ».** Une cellule sans objet, ou impossible à calculer faute de données. Ce n'est **pas** zéro.

**Position.** `(sourate, verset, rang du mot)`. Un décompte est un ensemble de positions : chaque chiffre est traçable.

## Statistiques

**Modèle nul.** Un monde simulé où l'effet étudié n'existe pas. *Exemple* : mélanger au hasard tous les mots du texte, des milliers de fois, et regarder à quelle fréquence on obtient « par hasard » un chiffre aussi frappant.

**Permutation.** Mélanger sans remplacement. Elle casse la structure testée (par exemple l'ordre des versets) en gardant le reste (les fréquences).

**p-value.** Probabilité d'observer un résultat au moins aussi extrême si le modèle nul est vrai. **Ce n'est pas** la probabilité que l'affirmation soit vraie.

**Comparaisons multiples.** Si l'on teste 100 000 paires, 5 % (soit 5 000) paraissent « significatives » par pur hasard. Les corrections (Holm, Benjamini-Hochberg, etc.) ajustent le seuil.

**FWER / FDR.** FWER : probabilité d'au moins une fausse découverte. FDR : proportion attendue de fausses découvertes parmi les découvertes déclarées.

**Pré-enregistrement.** Écrire l'hypothèse, le test et le seuil **avant** de voir le résultat, pour que le résultat ne puisse pas influencer le test. Vérifié ici par les dates git.

**Degrés de liberté du chercheur / bifurcations.** Toutes les petites décisions (quelle règle, quel seuil) qui permettent, sans le vouloir, de trouver ce qu'on cherche. *Exemple* : la combinaison de formes qui donne exactement 365 a été trouvée **après** avoir vu le résultat.

**Burstiness.** Un mot apparaît par grappes (une histoire le répète). Sa variance dépasse celle d'un tirage au hasard (loi de Poisson).

**Bootstrap par grappes.** Ré-échantillonner des sourates entières plutôt que des mots, car les mots d'une même sourate se ressemblent.

**Contrôle négatif.** Lancer la méthode sur des données sans signal pour voir combien de « structure » elle invente.

**Test différentiel.** Deux programmes écrits séparément doivent donner le même résultat ; sinon, l'un des deux a un bug.

**Test de propriétés.** Au lieu de vérifier un cas, on vérifie une loi sur beaucoup d'entrées générées. *Exemple* : normaliser deux fois = normaliser une fois.

**Test de mutation.** Casser volontairement le code pour vérifier que les tests le détectent.

**N(T).** Dans H001-v2, nombre de spécifications dont le décompte vaut exactement T. Sert à comparer 365 à ses voisins.

## IA

**Embedding.** Représentation numérique d'un texte telle que des textes proches ont des vecteurs proches.

**Fuite d'information.** Valider un modèle sur des données trop proches de celles qui l'ont entraîné. *Exemple* : deux versets d'une même sourate, un à l'entraînement, un au test.

**Modèle de thèmes (LDA, NMF, BERTopic).** Méthodes qui regroupent des textes en thèmes sans étiquettes.

## Projet

**Hafs ʿan ʿĀṣim.** La lecture (qirā'a) du texte de référence. Les décomptes ne se transposent pas aux autres lectures.

**Tanzil / Quranic Arabic Corpus.** Les deux sources : le texte, et son annotation grammaticale.

**`FAIT`, `INTERPRÉTATION`, `AFFIRMATION POPULAIRE`.** Les trois étiquettes obligatoires.

**`ROBUSTE`, `DÉPEND DE LA RÈGLE`, `NON SIGNIFICATIF`, `NON REPRODUCTIBLE`, `PARTIEL`.** Les statuts d'un résultat ([04](methodology/04-statistics.md)).
