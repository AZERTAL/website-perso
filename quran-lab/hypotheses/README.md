# hypotheses/

Une hypothèse = un fichier. Elle est **commitée avant** tout résultat qui la cite ; `scripts/check_reports.py` refuse un rapport si le fichier d'hypothèse a été modifié après lui.

| Fichier | Hypothèse | Statut |
|---|---|---|
| `TEMPLATE.md` | gabarit | — |
| `H001.md` | « le mot jour (`يوم`) apparaît 365 fois », grille de règles | résultat partiel (niveau forme) |
| `H001-v2.md` | même affirmation, espace de 512 spécifications ; **post hoc**, déclarée comme telle | `DÉPEND DE LA RÈGLE` : 365 atteint, pas plus que ses voisins |

Pour modifier un test après avoir vu un résultat : créer `Hxxx-v2`. L'original reste visible, intact.
