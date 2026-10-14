# tests/

Lancer : `make test` (ou `uv run pytest -q`).

| Dossier | Type | Exemple |
|---|---|---|
| `unit/` | un test par règle, valeurs attendues **calculées à la main** avant exécution | basmala à trois états, ventilation par nombre |
| `property/` | lois vérifiées sur des entrées générées (`hypothesis`) | normaliser deux fois = normaliser une fois |
| `differential/` | deux implémentations indépendantes doivent concorder, jusque sur **tout** le texte | squelette (catégories Unicode) contre expressions régulières |
| `golden/` | versets témoins vérifiés un à un (à remplir avec la morphologie) | — |
| `fixtures/` | petits jeux de données de test | 16 lignes réelles du format du fork |

`conftest.py` construit un mini-corpus. Ses mots de la sourate 1 sont réels ; le reste est **synthétique** (cas limites) et ne dit rien du vrai Coran.

Marqueur `needs_data` : tests qui lisent `data/raw/` (versionné, donc exécutés aussi en CI).

Test de mutation (manuel) : dix règles cassées volontairement ont toutes été détectées ; un trou initial (tatwil isolé) a été comblé.
