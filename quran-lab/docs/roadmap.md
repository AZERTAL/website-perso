# Feuille de route et traçabilité du cahier des charges

Chaque exigence du cahier des charges, son état réel et l'endroit où elle vit. État : **fait** (code et tests), **partiel**, **non fait**, **bloqué** (dépend d'une action externe).

## Phases

| Phase | Contenu | État |
|---|---|---|
| 0 | Plan validé | fait ([`plans/`](plans/)) |
| **1** | Squelette, sources, base, 4 niveaux de comptage, H001, fiche « paradis » | **en cours** : sources Tanzil et niveau forme faits ; morphologie **bloquée** (e-mail) ; `/theme paradis` non fait |
| 2 | Moteur multivers complet, 15 à 20 affirmations populaires | non fait |
| 3 | Modèles nuls N0 à N4, bootstrap, calibration du testeur | partiel : correction multiple, registre, N5 faits ; nuls non faits |
| 4 | Lexiques de 12 concepts validés contre l'ontologie du corpus | brouillon de lexique, non validé |
| 5 | Embeddings, thèmes, regroupements, contrôles négatifs | non fait |
| 6 | Réseau de concepts, cycles, rimes, formules | non fait |
| 7 | Tafsir, site public, automatisation nocturne | non fait (une page de suivi privée existe) |
| 8 | Rapport technique, résultats négatifs inclus | non fait |

## Section 0 · Rigueur et honnêteté

| Exigence | État | Où |
|---|---|---|
| Aucun chiffre sans script | **fait** : rapports générés, refus de commit sinon | `checks.py`, hook de commit |
| Chaque affirmation cite ses versets | partiel : les rapports actuels ne portent pas de versets (comptes agrégés) | à faire : lister les versets d'un décompte dans les rapports |
| Trois étiquettes | **fait** | rapports, `CLAUDE.md` |
| Jamais de tafsir inventé | **fait** (aucun tafsir produit) | `chercheur-tafsir` |
| Pas de « miracle » affirmé | **fait** | [éthique](methodology/07-ethics.md) |
| Résultats négatifs publiés | **fait** (H001, H001-v2) | `reports/` |

## Section 1 · La boucle

| Étape | État |
|---|---|
| Plan écrit dans `docs/plans/` | fait |
| Pré-enregistrement avant résultat | **fait et vérifié par git** (H001, H001-v2) |
| Petit, propre, testé | fait |
| Vérifier : tests, lint, 3 versets au hasard | tests et lint faits ; **les 3 versets au hasard avec graine ne sont pas encore produits** |
| Relecture par `statisticien-sceptique` | **faite** pour H001 (verdict FRAGILE, traité) |
| Commit et push | fait |
| Rapport au format demandé | fait dans la conversation |

## Section 2 · Sources

| Source | État |
|---|---|
| Tanzil Uthmani et simple-clean | **acquis**, hash dans `SOURCES.md` |
| Quranic Arabic Corpus v0.4 | **bloqué** : formulaire à adresse e-mail |
| Métadonnées | partiel : noms, type mecquois/médinois, nombre de versets, ordre (Tanzil) ; juz', hizb, sajda non chargés ; un seul référentiel d'ordre chronologique |
| Traductions (Hamidullah, Sahih International) | non acquises |
| Tafsir | non acquis |
| Sources brutes en lecture seule, SHA-256, licence | **fait** (hook + `chmod`) |
| `docs/divergences.md` | tenu à jour (divergences connues du fork ; divergences réelles à venir) |

## Section 3 · Règles de comptage

| Exigence | État |
|---|---|
| 4 niveaux | implémentés ; seul « forme » est évaluable |
| Options (singulier/pluriel, basmala, lettres isolées, orthographe, composés) | **fait** ; le nombre devient une ventilation et non un axe (D4) |
| `config/counting_rules.yaml` | fait (valeurs de lettres isolées à valider) |
| Affirmation populaire reproduite sous chaque règle | **fait** pour le niveau forme (H001) et un espace de formes (H001-v2) |

## Section 4 · Statistiques et anti-biais

| Exigence | État |
|---|---|
| Modèle nul pour chaque pattern | partiel : N5 et espace de spécifications ; N0 à N4 non faits |
| Comparaisons multiples corrigées, nombre de tests indiqué | fonctions et registre **faits** ; pas encore appliqués à une famille réelle |
| Tailles d'effet et intervalles | non fait |
| Statut final de chaque pattern | **fait** (voir [04](methodology/04-statistics.md)) |

## Section 5 · Thèmes, notions, cycles

| Exigence | État |
|---|---|
| Lexique des concepts (`themes.yaml`) | brouillon non validé |
| Recherche de passages par domaine (temps, espace, business, apprentissage, intelligence) | **faite** : [programme de recherche](research-program.md) ; minorants, requêtes pré-enregistrées |
| Analyses par concept (fréquence, répartition, co-occurrences, graphe) | non fait |
| Modélisation de thèmes, embeddings | non fait ([05](methodology/05-ai-methods.md)) |
| Thèmes « scientifiques » avec lectures étiquetées | non fait |

## Section 6 · Architecture technique

| Exigence | État |
|---|---|
| Python avec `uv`, DuckDB, polars, pytest, ruff | **fait** |
| `camel-tools`, `networkx`, `statsmodels`, `matplotlib` | non installés |
| Pipeline `make all` | partiel : `make test lint db audit h001 h001-v2 dataset site` |
| Site public Next.js sur Vercel | non fait (une page de suivi privée, générée par script) |
| Arborescence demandée | **fait** (adaptée : `quran-lab/` dans ce dépôt, voir [D1](DECISIONS.md)) |

## Section 7 · Claude Code

| Exigence | État |
|---|---|
| 5 sous-agents | **faits** ; `statisticien-sceptique` utilisé |
| Skills (3 demandés) | **faits** (4) |
| Commandes `/compte`, `/theme`, `/verifie`, `/rapport` | écrites, non exercées dans l'interface |
| Hooks (protection, qualité, commit) | **faits et testés** |
| Connecteurs GitHub, Vercel, Supabase, Drive | GitHub et Vercel selon la session ; Supabase absent |
| Mode non interactif `claude -p`, Actions nocturnes, tâche hebdomadaire, worktrees | non faits |
| `docs/DECISIONS.md` tenu à jour | **fait** (D1 à D15) |

## Section 8 · Livrables

| Livrable | État |
|---|---|
| Fiche par concept | non fait |
| Fiche par affirmation populaire | partiel : H001 et H001-v2 |
| Rapports Markdown avec commande de reproduction | **fait** |
| Site public sur Vercel | non fait |
| Jeu de données (CSV, Parquet) avec documentation | **fait** (`make dataset`, `NOTICE.md`, [dictionnaire](data/data-dictionary.md)) ; non publié |

## Prochaines étapes, par ordre

1. Acquérir la morphologie (décision sur l'adresse e-mail du formulaire, ou dépôt manuel du fichier).
2. Valider le lecteur du format v0.4 sur le vrai fichier, aligner Tanzil et corpus, relancer H001 en `H001-v3`.
3. `/theme paradis` : lexique gelé, ventilation racine / lemme.
4. Modèles nuls N0 à N4 et calibration du testeur (Phase 3).
5. Produire les 3 versets témoins au hasard (graine inscrite) dans chaque rapport.
