# Dispositif Claude Code

Le dépôt contient une configuration Claude Code (dossier `.claude/` à la racine, exigé par l'outil) qui **impose** les règles du projet au lieu de les rappeler. Règle de fond : *aucun chiffre sans script, test pré-enregistré, résultats négatifs publiés* (voir [`CLAUDE.md`](../../../CLAUDE.md)).

## Agents (`.claude/agents/`)

Chaque agent a un rôle, des outils limités et des consignes « n'invente jamais ».

| Agent | Rôle | Outils |
|---|---|---|
| `auditeur-sources` | version, licence, hash, intégrité, divergences entre sources | lecture, shell, web |
| `linguiste-morpho` | tranche segmentation, racine, lemme, homographes, avec justification grammaticale | lecture, shell |
| `statisticien-sceptique` | relit un résultat **sans avoir vu le raisonnement de l'auteur** et essaie de le casser | lecture, shell |
| `chercheur-tafsir` | rassemble lectures classiques et modernes d'un verset, sources citées | lecture, web |
| `data-viz` | figures et pages à partir de tables du projet | lecture, écriture limitée |

**Exemple réel** : `statisticien-sceptique` a relu H001, rendu un verdict FRAGILE et trouvé huit faiblesses (dont une combinaison de formes donnant exactement 365, trouvée après coup). Le traitement point par point est dans [DECISIONS D15](../DECISIONS.md).

## Skills (`.claude/skills/`)

Procédures réutilisables : `compter-concept`, `verifier-affirmation` (pré-enregistrer, grille, relecture, verdict), `fiche-concept`, `preregistrer-hypothese`.

## Commandes (`.claude/commands/`)

`/compte <mot ou racine>`, `/theme <concept>`, `/verifie "<affirmation>"`, `/rapport`. Elles appellent des scripts, pas du raisonnement libre. **Limite** : elles sont écrites mais n'ont pas été exercées de bout en bout dans l'interface ; les scripts qu'elles appellent le sont.

## Hooks (`.claude/settings.json`)

| Hook | Déclencheur | Effet | Testé |
|---|---|---|---|
| Protection des sources brutes | avant écriture ou commande shell | refuse toute modification du dossier des sources brutes | oui, 4 refus et 2 autorisations |
| Contrôle de qualité | après modification de `src/` ou `tests/` | lance `ruff` puis `pytest`, bloque en cas d'échec | oui (a bloqué des lignes trop longues pendant le développement) |
| Contrôle de commit | avant `git commit` | refuse un rapport avec un chiffre hors bloc généré, un test non pré-enregistré, ou un registre réécrit | oui, sur un faux rapport |

**Limites connues** :

- La protection est volontairement conservatrice : elle refuse toute commande shell qui cite le dossier des sources brutes à côté d'un verbe modificateur, même dans un simple texte (faux positif possible : écrire alors le fichier avec l'outil d'écriture). Un script Python qui écrirait dans ce dossier ne serait pas détecté ; la défense en profondeur est `chmod a-w` après téléchargement.
- Les hooks s'appliquent aux sessions Claude Code. Pour les contributeurs humains, le hook git équivalent est `.githooks/pre-commit` (activation : `make hooks`).

## Connecteurs

GitHub (dépôt, pull requests) et Vercel (déploiement du futur site) sont utilisés ou prévus ; leur disponibilité varie selon la session. Supabase n'est pas branché (inutile tant qu'il n'y a pas de recherche dynamique).
