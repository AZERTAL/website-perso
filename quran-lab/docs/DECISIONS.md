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
