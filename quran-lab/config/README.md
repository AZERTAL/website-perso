# config/

Données de configuration en YAML. **Ce ne sont pas des résultats** : ce sont des choix, versionnés et justifiés.

| Fichier | Contenu | État |
|---|---|---|
| `counting_rules.yaml` | versets composés de lettres isolées (muqatta'at) ; mots composés (`يومئذ` → `يوم`) | brouillon : la liste de versets est saisie de mémoire, à contrôler contre les annotations du corpus ; sans effet sur les résultats actuels |
| `sources.yaml` | URL de téléchargement, options choisies, notes de licence | à jour pour Tanzil ; la morphologie a `url: null` (formulaire à e-mail) |
| `themes.yaml` | lexiques de concepts (paradis, enfer, temps, ...) | **brouillon non validé** : `type: undecided` tant que `linguiste-morpho` n'a pas tranché racine ou lemme |

Règle : un lexique est **gelé par commit avant** d'être compté, avec une justification par entrée.
