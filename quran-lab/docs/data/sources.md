# Sources et licences

La provenance exacte (URL, date, SHA-256) est dans [`SOURCES.md`](../../SOURCES.md) et `data/sources_manifest.json`, écrits par `scripts/fetch_sources.py`. `make verify-sources` recalcule les empreintes.

## Priorité des sources

1. **Texte arabe : Tanzil** (Uthmani et simple-clean). C'est la **seule** base de comptage.
2. **Morphologie : Quranic Arabic Corpus** (segments, racine, lemme, catégorie).
3. **Métadonnées** : sourates, mecquoise/médinoise, ordre, nombre de versets (fichier de Tanzil).
4. **Traductions** : affichage seulement, jamais pour compter.
5. **Tafsir** : uniquement des éditions publiées et citées.

## Tanzil (acquis)

| Élément | Valeur |
|---|---|
| Version | 1.1 (février 2021) |
| Licence | Creative Commons Attribution 3.0 |
| Termes (lus sur la page officielle) | copie verbatim autorisée ; **modification interdite** ; source à indiquer avec un lien vers tanzil.net ; l'avis de copyright doit être reproduit dans les fichiers dérivés |
| Format | `sourate|verset|texte` |
| Options choisies | sans signes de pause, sajdah, rub-el-hizb ni tanweens séquentiels ; avec tatwil (défaut de la page) |
| Pourquoi sans signes de pause | un signe séparé par une espace deviendrait un faux « mot » au découpage par espaces |
| Types de texte | « Uthmani » (écriture du Mushaf de Médine) et « Simple (Clean) » (sans diacritiques) |

Constats sur les fichiers réels : voir [`reports/audit-tanzil.md`](../../reports/audit-tanzil.md) et [03 · Modèle de données](../methodology/03-data-model-and-pipeline.md).

## Quranic Arabic Corpus (non acquis)

| Élément | Valeur |
|---|---|
| Version visée | 0.4, morphologie |
| Licence (lue sur la page) | GNU General Public License ; copie verbatim ; **modification interdite** ; source à indiquer avec un lien vers corpus.quran.com ; avis de copyright à reproduire |
| Obstacle | le formulaire de téléchargement demande une adresse e-mail de contact. Elle n'est pas saisie sans l'accord explicite de la personne concernée |
| Conséquence | niveaux radical, lemme et racine **non évalués** ([01 · Règles de comptage](../methodology/01-counting-rules.md)) |

**Question de licence à trancher.** La GPL est « copyleft » : les œuvres dérivées peuvent devoir être distribuées sous la même licence. Avant d'intégrer la morphologie dans des fichiers publiés, il faut décider de la licence du code et des données dérivées de Quran Lab.

## Source de comparaison non canonique

`mustafa0x/quran-morphology` est un **fork modifié** du corpus v0.4 : `يومئذ` découpé, racines corrigées, tags simplifiés. Son fichier de licence est introuvable. Il n'est **jamais** une base de comptage, n'est pas versionné dans ce dépôt, et servira uniquement d'axe de sensibilité « version d'annotation ». Un extrait de 16 lignes (versets 1:1 à 1:5) sert de fixture de test du lecteur de format.
