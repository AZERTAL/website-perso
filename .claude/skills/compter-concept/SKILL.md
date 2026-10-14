---
name: compter-concept
description: Procédure pour compter un mot, une racine ou un concept à tous les niveaux et sous toutes les règles, avec traçabilité aux versets. À utiliser pour tout décompte du projet Quran Lab.
---
# Compter à tous les niveaux

1. Prérequis : `quran-lab/data/quran.duckdb` existe ; sinon arrêt, pas de chiffre.
2. Résoudre la requête : mot (squelette sans diacritiques), racine (lettres, avec ou sans espaces), ou concept (`config/themes.yaml`).
3. Lancer la grille complète (60 cellules applicables, `quran_lab.multiverse.run`). Ne jamais présenter une seule cellule comme « le » chiffre.
4. Rapporter : tableau règle -> décompte, distribution des décomptes, variantes fusionnées (homographes !), ventilation S/D/P, cellules `n/a` nommées comme telles.
5. Tracer : tout décompte est un ensemble de positions ; fournir au moins 3 versets (`sourate:verset`) avec tokens et raison.
6. Pièges à vérifier à chaque fois : racine polysémique (ج ن ن), homographes (ملك), composés (يومئذ), pluriels supplétifs (نساء), muqatta'at, basmala.
7. Étiqueter FAIT (avec la règle). Tout autre statut passe par `verifier-affirmation`.
