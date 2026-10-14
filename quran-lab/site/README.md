# site/

Page de suivi du projet.

| Fichier | Rôle |
|---|---|
| `status.template.html` | gabarit (HTML, CSS, JS) ; **aucun chiffre** : il lit `D`, un objet JSON injecté |
| `status.html` | page générée par `scripts/build_status_page.py` (`make site`) ; publiée comme artefact privé |

Les chiffres viennent de la base, de `reports/audit-tanzil.json`, du manifeste des sources, du registre et de git. Les éléments qui ne sortent pas d'un script sont marqués « manuel » dans la page.

Le site public (Next.js sur Vercel) est prévu en Phase 7, après accord.
