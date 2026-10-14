# Reproductibilité

Objectif : partir d'un dépôt cloné et retrouver chaque résultat, avec les mêmes chiffres.

## Pipeline complet

```bash
cd quran-lab
uv sync                          # environnement exact (uv.lock)
make verify-sources              # les sources brutes ont les empreintes de sources_manifest.json
make db                          # data/raw -> data/quran.duckdb
make test                        # lint, tests unitaires, de propriétés, différentiels
make audit                       # reports/audit-tanzil.md et .json
make h001                        # reports/H001-yawm-365.md        (arbre git propre exigé)
make h001-v2                     # reports/H001-v2-espace-de-regles.md
make dataset                     # data/processed/*.csv, *.parquet, NOTICE.md
make site                        # site/status.html
```

`make help` liste les cibles.

## Ce qui est déterministe

| Résultat | Déterministe ? | Remarque |
|---|---|---|
| Décomptes, tables, N(T), taux N5 | **oui** | aucune graine : calcul exact sur des fichiers fixes |
| Test différentiel sur échantillon | oui | graine fixée dans `audit.differential_full_text` |
| Rapports | oui **sauf** l'en-tête | `code_sha` change à chaque commit : comparer un rapport régénéré en ignorant `code_sha` et `generated_by` si le chemin de sortie diffère |
| Page de suivi | oui à commit égal | le nombre de tests est lu en exécutant la suite |
| Modèles appris (Phases 5 et 6) | **à garantir** | graines, versions et révisions de modèles figées ; non-déterminisme CPU signalé |

## Comment vérifier

1. **Les sources** : `make verify-sources` recalcule les SHA-256. Un téléchargement répété donne les mêmes empreintes (vérifié).
2. **Un rapport** : exécuter la commande de la ligne `generated_by`, vers un fichier temporaire, puis comparer. Seuls `generated_by` et `code_sha` doivent différer. (Un relecteur indépendant l'a fait pour H001 : tableau identique.)
3. **Le comptage** : recompter le mot avec un script indépendant sans importer `quran_lab` (découpage par espaces, retrait des marques). Le relecteur l'a fait : 217 et 282, identiques.
4. **Le pré-enregistrement** : `git log --format='%h %ci %s' -- hypotheses/H001.md reports/H001-yawm-365.md` : l'hypothèse précède le rapport, et `git diff <commit-prereg> HEAD -- hypotheses/H001.md` est vide.
5. **Le registre des tests** : `git log -p -- reports/tests_ledger.csv` ne montre que des lignes ajoutées.

## Empreintes de provenance

- `data_manifest_sha256` : SHA-256 de la liste triée `(nom de fichier, SHA-256)` du dossier des sources brutes.
- `code_sha` : commit court de `HEAD` ; suffixe `-dirty` si `quran-lab/src` ou `quran-lab/config` contiennent des modifications non commitées. `cli verifie` refuse d'écrire un rapport dans ce cas.

## Limites

- Les hooks et l'automatisation vivent dans la configuration Claude Code ; sans elle, `make hooks` active le hook git équivalent.
- La CI n'a pas été vérifiée dans cette session ([`tools/ci.md`](tools/ci.md)).
- Les résultats de la morphologie, des modèles nuls et de la couche IA n'existent pas encore.
