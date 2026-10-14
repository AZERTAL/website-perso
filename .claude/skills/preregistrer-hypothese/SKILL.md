---
name: preregistrer-hypothese
description: Crée et commite une hypothèse pré-enregistrée (hypotheses/Hxxx.md) AVANT toute analyse. À utiliser avant tout test de pattern.
---
# Pré-enregistrer

1. Prendre le prochain identifiant libre `Hnnn` (ne jamais réutiliser). Copier `quran-lab/hypotheses/TEMPLATE.md`.
2. Remplir TOUS les champs : hypothèse, définition opérationnelle, requête, niveaux et règles, statistique, modèle nul, seuil, famille de tests et correction, nombre de requêtes.
3. Commit seul, message `prereg: Hnnn`, avant de lancer le moindre comptage.
4. Pour changer un test après avoir vu un résultat : créer `Hnnn-v2`. L'original reste, intact et visible.
