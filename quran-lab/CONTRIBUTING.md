# Contribuer à Quran Lab

## Règles qui ne se négocient pas

1. **Aucun chiffre sans script.** Un rapport est généré, jamais écrit à la main.
2. **Pré-enregistrer avant de calculer.** Une hypothèse = un fichier `hypotheses/Hxxx.md`, commité **seul**, avant tout résultat. Pour changer un test : `Hxxx-v2`.
3. **Tester sur le vrai texte.** Les données ont déjà contredit trois hypothèses de conception.
4. **Ne jamais modifier les sources brutes.** `data/raw/` est en lecture seule ; seul `scripts/fetch_sources.py` y écrit.
5. **Publier les résultats négatifs.**
6. **Ne jamais inventer** un tafsir, une citation, une référence, ni citer un chiffre de mémoire.

## Mise en place

```bash
cd quran-lab
uv sync
make hooks      # active .githooks/pre-commit (vérification des rapports avant chaque commit)
make test lint
```

## Cycle de travail

1. Écrire l'hypothèse (`hypotheses/TEMPLATE.md`), la commiter seule : `prereg: Hxxx`.
2. Écrire ou étendre le code dans `src/quran_lab/` (logique pure) avec ses tests.
3. `make test lint` (le hook Claude Code et la CI le font aussi).
4. Générer le rapport avec le script ; **commiter le code avant**, car `cli verifie` refuse un arbre modifié.
5. Inscrire le test au registre (`scripts/ledger_add.py`) : une ligne par test, en ajout seul.
6. Faire relire par `statisticien-sceptique` avant toute publication.
7. Consigner toute décision durable (et toute erreur corrigée) dans `docs/DECISIONS.md`.

## Où mettre quoi

| Je veux... | Je modifie |
|---|---|
| ajouter une règle de comptage | `src/quran_lab/rules.py`, `count.py`, `config/counting_rules.yaml`, **tests**, `docs/methodology/01-counting-rules.md` |
| ajouter une source | `config/sources.yaml`, `SOURCES.md` (par `fetch_sources.py`), `docs/data/sources.md` |
| ajouter un concept | `config/themes.yaml` avec justification par entrée, validé par `linguiste-morpho`, gelé par commit avant tout comptage |
| ajouter une statistique | `src/quran_lab/stats/`, tests avec valeurs calculées à la main, `docs/methodology/04-statistics.md` |
| ajouter un rapport | un script dans `scripts/` qui écrit dans `reports/`, avec l'en-tête obligatoire |

## Style

Python 3.12, `ruff` (100 colonnes), types lorsqu'ils clarifient, fonctions pures dans `src/`, entrées/sorties dans `scripts/` et `load.py`/`db.py`. Les constantes de caractères arabes combinants s'écrivent avec des codes (`chr(0x0654)`) ou des noms Unicode : les marques combinantes littérales sont illisibles en relecture.

## Commits

Message en français, à l'impératif ou au constat, qui dit **pourquoi**. Préfixe `prereg:` pour une hypothèse. Un commit = une idée.

## Licence

Aucune licence n'est encore déclarée pour le code : tous droits réservés par défaut, jusqu'à décision de l'auteur. Les sources gardent leurs licences ([`docs/data/sources.md`](docs/data/sources.md)).
