---
name: verifier-affirmation
description: Procédure complète pour tester une affirmation numérique populaire sur le Coran (ex. « le mot X apparaît N fois », « X et Y apparaissent autant »). Pré-enregistrement, grille de règles, taux de coïncidence, relecture sceptique, verdict.
---
# Vérifier une affirmation populaire

1. **Citer la source** de l'affirmation si on la trouve (auteur, livre, URL). Sinon écrire « source non retrouvée ». Étiquette de départ : AFFIRMATION POPULAIRE.
2. **Pré-enregistrer** : `skills/preregistrer-hypothese` -> `hypotheses/Hxxx.md` (requête, cible, niveaux, règles, nul, seuil, famille) ; **commit avant tout comptage**. Le hook de commit refuse un rapport dont l'hypothèse est plus récente.
3. **Grille** : `quran_lab.multiverse.run(query, corpus, cfg, target=N)` -> 60 cellules. Compter les cellules qui valent N.
4. **Taux de coïncidence N5** : `quran_lab.stats.nulls.coincidence_rate` -> combien de types lexicaux tombent exactement sur N sans qu'on les ait choisis ? Si beaucoup, la cible n'a rien de remarquable.
5. **Texte** : si le chiffre n'apparaît que sur un texte différent de Tanzil -> NON REPRODUCTIBLE (règle « Tanzil seul »).
6. **Rapport généré** par `python -m quran_lab.cli verifie ...` (en-tête `generated_by`, hashes, tableau). Aucun chiffre tapé à la main.
7. **Relecture** : agent `statisticien-sceptique`, sans ton raisonnement.
8. **Verdict** : ROBUSTE / DÉPEND DE LA RÈGLE / NON SIGNIFICATIF / NON REPRODUCTIBLE. En Phase 1, sans modèles nuls N0-N4 implémentés, ROBUSTE est interdit : écrire « reproduction seule, nuls non évalués ».
