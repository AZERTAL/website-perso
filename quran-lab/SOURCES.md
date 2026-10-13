# Sources

Aucune source n'est encore téléchargée : les domaines `tanzil.net` et `corpus.quran.com` sont
refusés (HTTP 403) par la politique réseau de l'environnement au 2026-10-13.

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
(aucune source téléchargée)
<!-- END sources-table -->
