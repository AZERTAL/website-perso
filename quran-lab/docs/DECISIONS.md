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
