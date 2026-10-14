---
description: Fiche complète d'un concept (paradis, enfer, temps, ...) à tous les niveaux
argument-hint: <concept défini dans quran-lab/config/themes.yaml>
---
Produis la fiche du concept `$ARGUMENTS` en suivant la skill `fiche-concept`.

Contraintes : le concept doit exister dans `quran-lab/config/themes.yaml` avec une justification par entrée ; sinon propose-le, fais-le valider par l'agent `linguiste-morpho`, et gèle-le AVANT de compter. Chiffres uniquement via les scripts. Tafsir uniquement via l'agent `chercheur-tafsir` ; sans source ouverte, écris « tafsir non rempli ».
