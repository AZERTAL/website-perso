# Décisions durables

Format : date · décision · pourquoi · comment l'appliquer.

## D1 · 2026-10-13 · Tout le projet vit dans `quran-lab/`
Pourquoi : le dépôt contient déjà un portfolio Vite dont `src/` entre en conflit avec `src/quran_lab/`. Le portfolio n'est pas touché.
Appliquer : `CLAUDE.md` et `.claude/` restent à la racine (exigé par Claude Code) et pointent vers `quran-lab/`. Migration vers un dépôt séparé possible plus tard (le site public Next.js n'a rien à faire dans un portfolio).

## D2 · 2026-10-13 · Python 3.12 épinglé (`.python-version`)
Pourquoi : compatibilité de `camel-tools` avec 3.13 inconnue. Phase 5 seulement.

## D3 · 2026-10-13 · Le fork `mustafa0x/quran-morphology` n'est jamais base de comptage
Pourquoi : c'est une version modifiée (`يومئذ` découpé, racines corrigées), licence non trouvée. Seul un extrait de 16 lignes sert de fixture de parseur.
Appliquer : usage futur = axe de sensibilité « version d'annotation », fichier non commité.

## D4 · 2026-10-13 · La grille compte 60 cellules, pas 128 (écart ASSUMÉ avec le plan v2)
Le plan v2 annonçait « au plus 128 cellules ». À l'implémentation :
- l'axe **texte** (Uthmani / simple) n'a de sens que pour le niveau `form` (le corpus morphologique n'existe qu'en une orthographe) -> `n/a` aux trois autres niveaux ;
- l'axe **basmala** a trois états, pas deux : `as_text` (le texte tel que fourni, basmala numérotée 1:1 seulement), `all` (+112 en-têtes non numérotés, sourates 2 à 114 sauf 9), `none` (1:1 exclue). Sans `as_text` on ne reproduit pas ce que comptent la plupart des outils ;
- l'axe **nombre** (S/D/P) n'est plus un axe de grille : le « séparé/regroupé » du plan était ambigu au niveau des formes. Chaque résultat porte une **ventilation S/D/P/?** systématique (heuristique `number_of`, à valider sur le vrai corpus).
Total : form 3×2×2×2 = 24 ; stem, lemma, root 3×2×1×2 = 12 chacun ; soit 60. Test : `tests/unit/test_rules.py`.

## D5 · 2026-10-13 · Valeurs de configuration saisies de mémoire = brouillon
`config/counting_rules.yaml` (versets des muqatta'at, composés) et `config/themes.yaml` ne sont pas des résultats. Contrôle prévu dès réception des sources : les versets de muqatta'at doivent coïncider avec les mots de tag `INL` du corpus.

## D6 · 2026-10-13 · Règles de normalisation (`normalize.skeleton`)
NFC, jamais NFD (NFD ferait de `أ` un `ا` sans le dire). Tatwil + hamza combinante -> `ء` (orthographe uthmani de `شيئا`). Alif wasla -> alif. Diacritiques et signes coraniques retirés. Aucun repliement de hamza / alif maqsura / ta marbuta sans option explicite (`fold`).
Découvert par test : le corpus écrit la fatha avant la shadda, Buckwalter l'inverse ; NFC unifie (équivalence canonique Unicode).

## D7 · 2026-10-13 · Les rapports sont générés, jamais écrits à la main
Pourquoi : « aucun chiffre sans script ». `quran_lab.checks` refuse tout chiffre hors bloc `<!-- BEGIN generated:... -->` et exige `generated_by`, `data_manifest_sha256`, `code_sha`. Rendu déterministe (pas d'horodatage).

## D8 · 2026-10-13 · Réseau : tanzil.net et corpus.quran.com refusés (403)
Conséquence : la Phase 1 est arrêtée avant l'étape 3 (téléchargement). Aucun chiffre sur le vrai texte n'existe. Action utilisateur : autoriser les domaines.

## D9 · 2026-10-13 · Basmala : Tanzil la préfixe au verset 1 de 113 sourates (modèle corrigé)
Constaté sur les fichiers réels (`reports/audit-tanzil.md`) : le texte Tanzil contient la basmala devant le verset 1 de toutes les sourates sauf la 9 ; 1:1 est la basmala elle-même. Le modèle initial (D4) supposait l'inverse et aurait compté deux fois la basmala. Nouveaux états de l'axe : `all_113` (les 113 basmalas), `numbered_only` (seulement 1:1), `none`. Au niveau forme, les 112 en-têtes sont de vrais mots (`Word.header=True`) ; aux niveaux morphologiques (le corpus n'a pas d'en-têtes, à vérifier) `all_113` ajoute des copies virtuelles. Exclure les muqatta'at d'un verset ne retire jamais sa basmala. L'état `as_text` de H001 se lit « basmala telle qu'imprimée par la source » (= `all_113` au niveau forme) : H001 n'est pas modifiée, l'interprétation est fixée ici. Grille : toujours 60 cellules.

## D10 · 2026-10-13 · Les deux orthographes Tanzil n'ont pas les mêmes mots ni les mêmes positions
Constaté : 363 versets n'ont pas le même nombre de mots en Uthmani et en simple-clean (ex. 2:21). Le modèle n'apparie donc JAMAIS les mots entre orthographes ; `Word` porte sa `variant`. Un appariement par position aurait supprimé 363 versets sans bruit.

## D11 · 2026-10-13 · `skeleton` : deux corrections trouvées par le test différentiel sur le texte réel
(1) Alif + maddah (U+0627 U+0653) = alif simple, à traiter AVANT NFC (qui le recomposait en lettre `آ`). (2) Tatwil + hamza combinante survit au réordonnancement NFC. Avant correction : 1 077 formes distinctes (3 687 occurrences) divergeaient entre les deux implémentations. Après : 0 désaccord sur tout le texte, dans les deux orthographes. Tests construits sur les codes exacts relevés dans le fichier.

## D12 · 2026-10-13 · Le corpus morphologique exige une adresse e-mail de contact
La page de téléchargement de corpus.quran.com demande un e-mail « pour vérification, non public ». Je n'envoie pas l'adresse de l'utilisateur à un site tiers sans son accord explicite. Tant que ce n'est pas résolu : mode « texte seul », niveaux stem/lemma/root déclarés NON ÉVALUÉS (jamais 0). Licence lue sur la page : GNU GPL, copie verbatim, attribution et lien vers corpus.quran.com.

## D13 · 2026-10-13 · Options Tanzil retenues
Tanzil v1.1 (février 2021), CC BY 3.0, texte non modifié. Sans signes de pause, sajdah, rub-el-hizb ni tanweens séquentiels (une marque séparée par un espace deviendrait un faux mot) ; avec tatwil (défaut de la page). Format `sourate|verset|texte`.

## D14 · 2026-10-13 · Le hook de protection des sources brutes est volontairement conservateur
Il bloque toute commande shell qui mentionne le dossier des sources brutes à côté d'un verbe modificateur, même dans un texte. Faux positifs possibles : écrire les documents via l'outil d'écriture, pas via un heredoc shell.

## D15 · 2026-10-14 · Relecture sceptique de H001 (verdict FRAGILE) : ce qui est corrigé, ce qui reste
Le relecteur indépendant n'avait pas vu notre raisonnement. Il a relancé le rapport (résultat identique) et recompté le mot dans le texte brut sans notre code (217 et 282, identiques). Il a relevé huit faiblesses ; traitement :

1. **« Aucune cellule ne donne 365 » masquait que le niveau forme ne voit pas les formes à clitiques** (haute). Corrigé : section « Ce que ce niveau ne voit pas » dans le rapport H001 ; nouvelle hypothèse **H001-v2** qui balaie 512 spécifications. Résultat : 365 atteint par 5 spécifications, son voisin 364 par 8 → non remarquable. Statut `DÉPEND DE LA RÈGLE`.
2. **La grille oublie les formes à clitiques, à `يوما`, au duel, aux suffixes** (haute). Traité par H001-v2 (interrupteurs T1 à T8) ; à refaire sur les vrais radicaux quand la morphologie sera acquise (`H001-v3`).
3. **Contradiction D4 / D9 sur `as_text`** (moyenne-haute). Reconnue : D4 (avant les données) définissait `as_text` comme `numbered_only`, D9 (après) comme `all_113` au niveau forme, en affirmant que H001 n'était pas modifiée. C'était une réinterprétation après coup, qui aurait dû passer par `H001-v2`. Aucun effet sur ce mot (aucune cellule ne varie avec la basmala : vérifié par `inert_axes`), mais la règle de modification est désormais appliquée à la lettre (toute reformulation passe par une nouvelle version). **Reste à faire** : marquer la cellule primaire dans les rapports générés (le rapport ne la désigne pas encore).
4. **Cellules gonflées par des axes sans effet** (moyenne). Corrigé : le rapport affiche le nombre de décomptes distincts (2) et les axes sans effet (basmala, muqatta'at, orthographe).
5. **N5 sans pouvoir discriminant** (moyenne). Reconnu. La mesure pertinente est la comparaison aux nombres voisins dans l'espace des règles (H001-v2).
6. **Registre des tests absent** (moyenne). Corrigé : `stats/ledger.py`, `reports/tests_ledger.csv`, vérification d'ajout seul via git, total affiché dans les rapports.
7. **`code_sha` « -dirty »** (basse). Le rapport avait été produit avec du code non commité. Corrigé : `cli verifie` refuse désormais (`--allow-dirty` explicite) ; rapport régénéré sur arbre propre.
8. **Tableau des variantes limité aux formes sans clitiques** (basse). Corrigé par H001-v2 (toutes les formes reconnues sont listées, avec leurs classes ; les non reconnues aussi).

**Ce que le relecteur a aussi montré, et qu'on n'a pas le droit d'oublier** : une combinaison précise de formes (préfixes et article inclus, `يوما` inclus, duel et suffixes exclus) donne exactement 365. Elle a été trouvée en regardant le résultat. Le test pré-enregistré mesure si 365 est plus facile à atteindre que ses voisins : ce n'est pas le cas dans l'espace défini.

**Reste ouvert** : refaire le test avec la vraie morphologie (H001-v3), nuls N0 à N4, et relecture humaine. Les horodatages de `27f05e6` et `9bf9507` sont identiques à la seconde : l'ordre repose sur la topologie git (déjà prouvé par le fichier non modifié).

## D16 · 2026-10-14 · Recherche de passages : règle d'appariement v2 après un faux négatif constaté
Les requêtes des cinq domaines ont été commitées avant exécution (`908c6ed`). Leur première exécution avec la règle v1 (le premier mot d'une expression ne peut porter que `و` ou `ف`) a manqué 22:47, où l'expression est `كألف سنة` (préfixe `ك`). Constaté par une recherche exploratoire, étiquetée comme telle. Réponse : règle **v2** (premier mot avec `ب`, `ل`, `ك` possibles) ; les deux règles sont rapportées côte à côte dans chaque rapport de domaine, pour montrer exactement ce que v1 manquait. Les requêtes elles-mêmes n'ont pas changé. Limite qui reste : un mot suffixé (`ألفهم`) ou une variante orthographique non prévue n'est pas trouvé ; tout résultat de recherche est un **minorant** des passages, jamais une liste exhaustive.
