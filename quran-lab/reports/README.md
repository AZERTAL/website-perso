# reports/

Rapports **générés par script**. On ne les édite jamais à la main : tout chiffre est dans un bloc `<!-- BEGIN generated:... -->` et l'en-tête donne la commande de reproduction, l'empreinte des données et le commit du code.

| Fichier | Produit par |
|---|---|
| `audit-tanzil.md`, `audit-tanzil.json` | `scripts/audit_tanzil.py` |
| `H001-yawm-365.md` | `python -m quran_lab.cli verifie ...` (`make h001`) |
| `H001-v2-espace-de-regles.md` | `scripts/run_h001_v2.py` (`make h001-v2`) |
| `tests_ledger.csv` | `scripts/ledger_add.py` et `run_h001_v2.py` ; **ajout seul** |

Reproduction : [`docs/reproducibility.md`](../docs/reproducibility.md).
