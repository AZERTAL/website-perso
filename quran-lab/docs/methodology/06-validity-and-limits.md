# 06 · Validité et limites

Pour chaque menace : ce qui peut fausser les résultats, et ce que le projet fait (ou ne fait pas encore) contre.

| Type | Menace | Parade | État |
|---|---|---|---|
| Construit | un « concept » n'est pas la somme de ses mots (polysémie, métaphore) | lexique validé contre l'ontologie du corpus ; lecture d'un échantillon de contextes | planifié |
| Construit | lexique circulaire (on choisit les mots qui donnent le résultat) | lexique gelé par commit **avant** de compter ; justification par entrée | `config/themes.yaml` en brouillon, non gelé |
| Interne | bug de comptage | tests unitaires, de propriétés, différentiel sur tout le texte, mutation manuelle | **fait** (niveau forme) |
| Interne | erreur d'annotation morphologique | axe de sensibilité entre versions d'annotation ; relecture `linguiste-morpho` | planifié (morphologie non acquise) |
| Interne | normalisation qui crée ou perd des lettres | test différentiel sur tout le texte | **fait**, a déjà trouvé deux défauts réels |
| Statistique | degrés de liberté du chercheur | pré-enregistrement vérifié par git, registre des tests | **fait** ; a déjà servi (H001-v2) |
| Statistique | comparaisons multiples | fonctions de correction, registre | fonctions faites, famille réelle à venir |
| Statistique | non-indépendance des mots d'une sourate | bootstrap par sourates, nuls qui préservent la structure | planifié |
| Statistique | cellules gonflées par des axes sans effet | `inert_axes`, nombre de décomptes distincts | **fait** |
| Externe | résultats propres à la lecture Hafs et à une numérotation | écrit dans chaque rapport | **fait** |
| Externe | ordre chronologique des sourates contesté | au moins deux référentiels côte à côte | planifié (seul l'ordre Tanzil est disponible) |
| Biais de confirmation | voir des motifs partout | contrôles négatifs obligatoires, résultats négatifs publiés | contrôles négatifs planifiés |
| Source | affirmation fondée sur un texte modifié | règle « Tanzil seul » : un chiffre qui n'apparaît que sur un texte altéré est `NON REPRODUCTIBLE` | **fait** (règle) |

## Limites connues du moteur actuel

- **Le sens n'est pas distingué.** `يوم` désigne le jour calendaire, le Jour du Jugement ou une période : le décompte les additionne.
- **Niveaux morphologiques absents.** Radical, lemme, racine ne sont pas évaluables : tout verdict est `PARTIEL` tant que la morphologie manque.
- **Les expressions régulières de H001-v2 approchent la morphologie** sans la remplacer.
- **Le format de la morphologie v0.4 n'est pas validé** sur le vrai fichier (non acquis).
- **Heuristique singulier/duel/pluriel** non validée.
- **La liste des versets de lettres isolées** (muqatta'at) est saisie de mémoire : elle n'a aucun effet sur les résultats actuels, mais doit être contrôlée contre les annotations du corpus.
- **Un seul relecteur** (un agent) : une relecture humaine spécialisée reste nécessaire avant toute publication.

## Ce qui a déjà été contredit par les données

Les données réelles ont contredit trois hypothèses de conception écrites avant de les voir : la basmala (113 occurrences préfixées, pas une), les deux orthographes (363 versets de mots différents) et la normalisation (lettres créées ou perdues). Voir [DECISIONS D9, D10, D11](../DECISIONS.md). C'est le meilleur argument pour tester sur le texte réel avant de conclure.
