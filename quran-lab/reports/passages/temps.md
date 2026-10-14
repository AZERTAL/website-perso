---
generated_by: cd quran-lab && uv run python scripts/run_passages.py
data_manifest_sha256: 6b8d4d7d4f226b38179f9cb62e57bbbcf0d1d83adc4220d90cc1833d61f4095a
code_sha: 82b96585a741
---
# Domaine : Temps, durées, sommeil et réveil, heure

Étiquette : `FAIT` (recherche de passages dans le texte Tanzil simple-clean, squelette consonantique). Cartographie, pas interprétation : aucune lecture de tafsir n'est incluse (aucune source acquise). Un motif exige un modèle nul (phase ultérieure).

Requêtes : `config/queries/temps.yaml`, commitées avant l'exécution. Une expression absente du texte est un résultat.

## Vue d'ensemble
<!-- BEGIN generated:quran_lab.passages.search -->
| id | type | expression | occurrences v1 | occurrences v2 | versets v2 | sourates v2 |
|---|---|---|---:|---:|---:|---:|
| temps-01 | phrase | ألف سنة | 4 | 5 | 5 | 5 |
| temps-02 | phrase | خمسين ألف سنة | 1 | 1 | 1 | 1 |
| temps-03 | word | مقداره | 2 | 2 | 2 | 2 |
| temps-04 | word | لبثتم | 8 | 8 | 7 | 5 |
| temps-05 | word | لبثوا | 5 | 5 | 5 | 3 |
| temps-06 | phrase | يوما أو بعض يوم | 3 | 3 | 3 | 3 |
| temps-07 | phrase | مائة عام | 2 | 2 | 1 | 1 |
| temps-08 | word | وازدادوا | 1 | 1 | 1 | 1 |
| temps-09 | word | الدهر | 2 | 2 | 2 | 2 |
| temps-10 | word | الساعة | 39 | 39 | 35 | 23 |
| temps-11 | word | سنين | 12 | 12 | 12 | 9 |
| temps-12 | word | والعصر | 1 | 1 | 1 | 1 |
| temps-13 | word | أمد | 1 | 1 | 1 | 1 |
<!-- END generated -->

## Ce que la règle v1 manquait
La règle v1 (pré-enregistrée) n'accepte que `و` ou `ف` devant le premier mot d'une expression ; la règle v2 accepte aussi `ب`, `ل`, `ك` (DECISIONS D16).
<!-- BEGIN generated:quran_lab.passages.search -->
temps-01 (ألف سنة) : versets ajoutés par v2 : 22:47
<!-- END generated -->

## Détail par requête
### temps-01 : ألف سنة
Pourquoi dans ce domaine : durée longue exprimée en années.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 2:96, 22:47, 29:14, 32:5, 70:4
formes rencontrées : ألف سنة (4); كألف سنة (1)

> 2:96 : ولتجدنهم أحرص الناس على حياة ومن الذين أشركوا يود أحدهم لو يعمر ألف سنة وما هو بمزحزحه من العذاب أن يعمر والله بصير بما يعملون
> 22:47 : ويستعجلونك بالعذاب ولن يخلف الله وعده وإن يوما عند ربك كألف سنة مما تعدون
> 29:14 : ولقد أرسلنا نوحا إلى قومه فلبث فيهم ألف سنة إلا خمسين عاما فأخذهم الطوفان وهم ظالمون
<!-- END generated -->

### temps-02 : خمسين ألف سنة
Pourquoi dans ce domaine : durée très longue exprimée en années.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 70:4
formes rencontrées : خمسين ألف سنة (1)

> 70:4 : تعرج الملائكة والروح إليه في يوم كان مقداره خمسين ألف سنة
<!-- END generated -->

### temps-03 : مقداره
Pourquoi dans ce domaine : terme de mesure d'une durée.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 32:5, 70:4
formes rencontrées : مقداره (2)

> 32:5 : يدبر الأمر من السماء إلى الأرض ثم يعرج إليه في يوم كان مقداره ألف سنة مما تعدون
> 70:4 : تعرج الملائكة والروح إليه في يوم كان مقداره خمسين ألف سنة
<!-- END generated -->

### temps-04 : لبثتم
Pourquoi dans ce domaine : verbe « demeurer, rester », deuxième personne.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 17:52, 18:19, 20:103, 20:104, 23:112, 23:114, 30:56
formes rencontrées : لبثتم (8)

> 17:52 : يوم يدعوكم فتستجيبون بحمده وتظنون إن لبثتم إلا قليلا
> 18:19 : وكذلك بعثناهم ليتساءلوا بينهم قال قائل منهم كم لبثتم قالوا لبثنا يوما أو بعض يوم قالوا ربكم أعلم بما لبثتم فابعثوا أحدكم بورقكم هذه إلى المدينة فلينظر أيها أزكى طعاما فليأتكم برزق منه وليتلطف ولا يشعرن بكم أحدا
> 20:103 : يتخافتون بينهم إن لبثتم إلا عشرا
<!-- END generated -->

### temps-05 : لبثوا
Pourquoi dans ce domaine : verbe « demeurer, rester », troisième personne.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 18:12, 18:25, 18:26, 30:55, 34:14
formes rencontrées : لبثوا (4); ولبثوا (1)

> 18:12 : ثم بعثناهم لنعلم أي الحزبين أحصى لما لبثوا أمدا
> 18:25 : ولبثوا في كهفهم ثلاث مائة سنين وازدادوا تسعا
> 18:26 : قل الله أعلم بما لبثوا له غيب السماوات والأرض أبصر به وأسمع ما لهم من دونه من ولي ولا يشرك في حكمه أحدا
<!-- END generated -->

### temps-06 : يوما أو بعض يوم
Pourquoi dans ce domaine : estimation d'une durée de séjour.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 2:259, 18:19, 23:113
formes rencontrées : يوما أو بعض يوم (3)

> 2:259 : أو كالذي مر على قرية وهي خاوية على عروشها قال أنى يحيي هذه الله بعد موتها فأماته الله مائة عام ثم بعثه قال كم لبثت قال لبثت يوما أو بعض يوم قال بل لبثت مائة عام فانظر إلى طعامك وشرابك لم يتسنه وانظر إلى حمارك ولنجعلك آية للناس وانظر إلى العظام كيف ننشزها ثم نكسوها لحما فلما تبين له قال أعلم أن الله على كل شيء قدير
> 18:19 : وكذلك بعثناهم ليتساءلوا بينهم قال قائل منهم كم لبثتم قالوا لبثنا يوما أو بعض يوم قالوا ربكم أعلم بما لبثتم فابعثوا أحدكم بورقكم هذه إلى المدينة فلينظر أيها أزكى طعاما فليأتكم برزق منه وليتلطف ولا يشعرن بكم أحدا
> 23:113 : قالوا لبثنا يوما أو بعض يوم فاسأل العادين
<!-- END generated -->

### temps-07 : مائة عام
Pourquoi dans ce domaine : durée d'un siècle.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 2:259
formes rencontrées : مائة عام (2)

> 2:259 : أو كالذي مر على قرية وهي خاوية على عروشها قال أنى يحيي هذه الله بعد موتها فأماته الله مائة عام ثم بعثه قال كم لبثت قال لبثت يوما أو بعض يوم قال بل لبثت مائة عام فانظر إلى طعامك وشرابك لم يتسنه وانظر إلى حمارك ولنجعلك آية للناس وانظر إلى العظام كيف ننشزها ثم نكسوها لحما فلما تبين له قال أعلم أن الله على كل شيء قدير
<!-- END generated -->

### temps-08 : وازدادوا
Pourquoi dans ce domaine : verbe « ajouter », contexte de durée.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 18:25
formes rencontrées : وازدادوا (1)

> 18:25 : ولبثوا في كهفهم ثلاث مائة سنين وازدادوا تسعا
<!-- END generated -->

### temps-09 : الدهر
Pourquoi dans ce domaine : terme de temps long.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 45:24, 76:1
formes rencontrées : الدهر (2)

> 45:24 : وقالوا ما هي إلا حياتنا الدنيا نموت ونحيا وما يهلكنا إلا الدهر وما لهم بذلك من علم إن هم إلا يظنون
> 76:1 : هل أتى على الإنسان حين من الدهر لم يكن شيئا مذكورا
<!-- END generated -->

### temps-10 : الساعة
Pourquoi dans ce domaine : l'heure, le moment.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 6:31, 6:40, 7:187, 12:107, 15:85, 16:77, 18:21, 18:36, 19:75, 20:15, 21:49, 22:1, 22:7, 22:55, 25:11, 30:12, 30:14, 30:55, 31:34, 33:63, 34:3, 40:46, 40:59, 41:47, 41:50, 42:17, 42:18, 43:66, 43:85, 45:27, 45:32, 47:18, 54:1, 54:46, 79:42
formes rencontrées : الساعة (35); بالساعة (2); والساعة (2)

> 6:31 : قد خسر الذين كذبوا بلقاء الله حتى إذا جاءتهم الساعة بغتة قالوا يا حسرتنا على ما فرطنا فيها وهم يحملون أوزارهم على ظهورهم ألا ساء ما يزرون
> 6:40 : قل أرأيتكم إن أتاكم عذاب الله أو أتتكم الساعة أغير الله تدعون إن كنتم صادقين
> 7:187 : يسألونك عن الساعة أيان مرساها قل إنما علمها عند ربي لا يجليها لوقتها إلا هو ثقلت في السماوات والأرض لا تأتيكم إلا بغتة يسألونك كأنك حفي عنها قل إنما علمها عند الله ولكن أكثر الناس لا يعلمون
<!-- END generated -->

### temps-11 : سنين
Pourquoi dans ce domaine : années.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 7:130, 10:5, 12:42, 12:47, 17:12, 18:11, 18:25, 20:40, 23:112, 26:18, 26:205, 30:4
formes rencontrées : سنين (9); السنين (2); بالسنين (1)

> 7:130 : ولقد أخذنا آل فرعون بالسنين ونقص من الثمرات لعلهم يذكرون
> 10:5 : هو الذي جعل الشمس ضياء والقمر نورا وقدره منازل لتعلموا عدد السنين والحساب ما خلق الله ذلك إلا بالحق يفصل الآيات لقوم يعلمون
> 12:42 : وقال للذي ظن أنه ناج منهما اذكرني عند ربك فأنساه الشيطان ذكر ربه فلبث في السجن بضع سنين
<!-- END generated -->

### temps-12 : والعصر
Pourquoi dans ce domaine : terme de temps, serment.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 103:1
formes rencontrées : والعصر (1)

> 103:1 : والعصر
<!-- END generated -->

### temps-13 : أمد
Pourquoi dans ce domaine : terme d'échéance.

<!-- BEGIN generated:quran_lab.passages.search -->
versets : 57:16
formes rencontrées : الأمد (1)

> 57:16 : ألم يأن للذين آمنوا أن تخشع قلوبهم لذكر الله وما نزل من الحق ولا يكونوا كالذين أوتوا الكتاب من قبل فطال عليهم الأمد فقست قلوبهم وكثير منهم فاسقون
<!-- END generated -->

## Reproduction
```
cd quran-lab && uv run python scripts/run_passages.py
```
