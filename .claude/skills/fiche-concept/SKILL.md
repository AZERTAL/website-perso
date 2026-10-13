---
name: fiche-concept
description: Produire la fiche d'un concept coranique (paradis, enfer, temps, ange, ...) avec chiffres à tous les niveaux, répartition, co-occurrences, versets clés et lectures étiquetées.
---
# Fiche concept

1. Lexique : entrée dans `config/themes.yaml` avec, pour chaque racine ou lemme, une justification et ses homographes connus. Le lexique est **gelé avant** de compter (commit).
2. Ventiler racine vs lemme : une racine polysémique surévalue le concept ; montrer les deux.
3. Chiffres : skill `compter-concept` pour chaque entrée, puis union des positions (un mot compté une seule fois).
4. Répartition par sourate, mecquoise/médinoise (référentiel cité), ordre chronologique (au moins 2 référentiels, signaler que l'ordre est débattu).
5. Co-occurrences : dans le même verset et dans une fenêtre de N versets, avec le nul de permutation (Phase 3).
6. Versets clés : 5 à 10, `sourate:verset`, choisis par une règle écrite (ex. plus forte densité), pas à la main.
7. Lectures : agent `chercheur-tafsir`, étiquetées INTERPRÉTATION ; sans source ouverte : « tafsir non rempli ».
8. Statut de chaque pattern : ROBUSTE / DÉPEND DE LA RÈGLE / NON SIGNIFICATIF / NON REPRODUCTIBLE.
