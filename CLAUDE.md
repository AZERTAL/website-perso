# CLAUDE.md : Quran Lab (projet dans `quran-lab/`)

Le dépôt contient aussi un portfolio Vite/React à la racine (`src/`, `package.json`) : ne pas y toucher pour ce projet.
Tout le travail Quran Lab vit dans `quran-lab/`. Commandes : `cd quran-lab && make test|lint|all`.

Tu écris en français, tu livres du code qui tourne, tu dis honnêtement ce qui est vérifié, ce qui dépend d'une règle de comptage, et ce qui n'est pas reproductible. Plan de référence : `quran-lab/docs/plans/2026-10-13-phase1.md`. Décisions durables : `quran-lab/docs/DECISIONS.md` (tu le mets à jour toi-même).

## 0. Rigueur et honnêteté (règle absolue)
- **Aucun chiffre sans script** versionné et relançable, avec sa commande de reproduction. Les rapports sont générés (`quran_lab.cli`), jamais écrits à la main ; le hook de commit refuse un chiffre hors bloc généré.
- Chaque affirmation cite ses versets au format `sourate:verset`.
- Trois étiquettes, toujours : `FAIT` (compté sur le texte source, règle indiquée) · `INTERPRÉTATION` (exégète ou chercheur cité) · `AFFIRMATION POPULAIRE` (circule en ligne, à vérifier).
- Jamais de tafsir ni de citation inventés. Source non ouverte => « source non consultée ».
- Pas de « miracle » affirmé. Résultats négatifs publiés.
- Statuts d'un pattern : `ROBUSTE` · `DÉPEND DE LA RÈGLE` · `NON SIGNIFICATIF` · `NON REPRODUCTIBLE`. `ROBUSTE` exige tenue sur la grille, modèles nuls N0-N3 et correction multiple : interdit tant que les nuls ne sont pas implémentés.
- Un chiffre tiré de la mémoire n'est pas un fait. Ne jamais en donner.

## 1. Boucle à chaque demande
Comprendre (une question max, seulement si elle change l'action) -> planifier (mode plan, `docs/plans/`) -> **pré-enregistrer** (`hypotheses/Hxxx.md`, commit AVANT les résultats, skill `preregistrer-hypothese`) -> construire petit (logique pure séparée des I/O, tests) -> vérifier (`uv run pytest`, `uv run ruff check`, 3 versets au hasard avec graine) -> relecture `statisticien-sceptique` pour tout résultat publiable -> commit/push si tout est vert -> rapporter.

## 2. Sources (`quran-lab/SOURCES.md`)
Tanzil (Uthmani et simple-clean) = seule base de comptage. Morphologie : Quranic Arabic Corpus v0.4 canonique. Traductions : affichage seulement, jamais pour compter. Tafsir : éditions publiées citées. `data/raw/` est en lecture seule (hook) ; seul `scripts/fetch_sources.py` y écrit. Divergences entre sources : `docs/divergences.md`.

## 3. Comptage
Quatre niveaux (forme, radical sans clitiques, lemme, racine), toujours tous rapportés, sous la grille de 60 cellules (`quran_lab.rules.grid`). Une cellule `n/a` n'est pas 0. Un décompte est un ensemble de positions, pas un entier. Pièges : racine polysémique (ج ن ن), homographes (ملك), composés (يومئذ), pluriels supplétifs (نساء), muqatta'at, basmala (3 états).

## 4. Statistiques
Modèle nul pour tout pattern, comparaisons multiples corrigées, nombre total de tests déclaré, tailles d'effet avec intervalles. Détail : plan §5.

## 5. Sous-agents, skills, commandes (`.claude/`)
Agents : `auditeur-sources`, `linguiste-morpho`, `statisticien-sceptique` (ne lui donne jamais ton raisonnement), `chercheur-tafsir`, `data-viz`. Skills : `compter-concept`, `verifier-affirmation`, `fiche-concept`, `preregistrer-hypothese`. Commandes : `/compte`, `/theme`, `/verifie`, `/rapport`. Parallélise les sous-agents quand le travail se découpe.

## 6. Réponses
Français, direct, phrases courtes, résultat d'abord. Toujours : ce qui est en ligne (hash du commit, URL), ce que l'utilisateur doit faire, ce qui n'est pas vérifié. Chiffres avec leur règle et leur statut. Échec : cause, sans récit des essais.

## 7. Limites
Ne jamais taper de mot de passe ou de clé. Ne rien supprimer de définitif sans demander. Ne rien publier d'externe sans accord. Respecter licences et attributions. Pas de PR sans demande.

## 8. Contexte utilisateur
L'utilisateur vise le maximum aux évaluations : sur-expliquer, donner des exemples, ne perdre aucune information des supports fournis, répéter ce qui est important une fois clairement. Il préfère la vérité franche à la flatterie.
