# Sources

Téléchargées le 2026-10-13 : les trois fichiers Tanzil (Uthmani, simple-clean, métadonnées).
**Pas encore acquis : la morphologie du Quranic Arabic Corpus v0.4.** Sa page de téléchargement
exige une adresse e-mail de contact (DECISIONS D12) ; en attendant, seuls les décomptes au niveau
« forme » sont possibles.
Attribution (CC BY 3.0, texte non modifié) : Tanzil Project, https://tanzil.net. L'avis de copyright
figure dans les fichiers sources et doit être reproduit dans tout fichier dérivé.

Ordre de priorité (section 2 du cahier des charges) : Tanzil (seule base de comptage) ->
Quranic Arabic Corpus (morphologie) -> métadonnées -> traductions (affichage seulement) -> tafsir.

Procédure : `uv run python scripts/fetch_sources.py` (seul script autorisé à écrire dans `data/raw/`).
Le tableau ci-dessous est écrit par ce script. Une licence marquée « à confirmer » n'a pas été lue.

## Source de comparaison (non canonique, non commitée)

`mustafa0x/quran-morphology` (fork de la v0.4, accessible via raw.githubusercontent.com) :
`يومئذ` découpé, racines corrigées, tags modifiés, fichier `LICENSE` introuvable (404 le 2026-10-13).
Utilisation prévue : axe de sensibilité « version d'annotation » uniquement. Jamais base de comptage,
jamais republié dans ce dépôt tant que sa licence n'est pas établie. Un extrait de 16 lignes
(1:1 à 1:5) est utilisé dans `tests/fixtures/fork_sample.txt` pour valider le parseur.

<!-- BEGIN sources-table -->
| id | fichier | URL | téléchargé le | SHA-256 | licence (à confirmer) |
|---|---|---|---|---|---|
| tanzil_uthmani | quran-uthmani.txt | https://tanzil.net/pub/download/index.php?quranType=uthmani&outType=txt-2&tatweel=true&agree=true | 2026-10-13 | `457cf2fe5bfb2121f158d2d377b4e6efcf5cc62d70d6265206d579d0443a3158` | CC BY 3.0 (lu sur tanzil.net/docs/Text_License le 2026-10-13) : copie verbatim, modification interdite, attribution à Tanzil Project + lien tanzil.net, avis de copyright à reproduire dans les fichiers dérivés. |
| tanzil_simple_clean | quran-simple-clean.txt | https://tanzil.net/pub/download/index.php?quranType=simple-clean&outType=txt-2&tatweel=true&agree=true | 2026-10-13 | `228df2a717671aeb9d2ff573002bd28d6b3f973f4bc7153554e3a81663d67610` | CC BY 3.0, voir tanzil_uthmani. |
| tanzil_metadata | quran-data.xml | https://tanzil.net/res/text/metadata/quran-data.xml | 2026-10-13 | `8867c1d88191472adec9db694b3cd9f135b1a2ef580574d32cf888dcb22c5c7a` | À lire sur la page officielle. Non confirmée. |
<!-- END sources-table -->
