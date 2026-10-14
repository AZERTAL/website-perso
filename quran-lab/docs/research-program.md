# Programme de recherche par domaines

Le projet ne se limite pas à compter des mots. Il cherche des **motifs** (où un thème apparaît, avec quoi, sous quelles formules, comment il évolue) dans plusieurs domaines, pour **mieux comprendre** le texte. Cette page dit ce que « mieux comprendre » veut dire ici, ce que le projet peut et ne peut pas faire, et comment chaque domaine est traité.

## Domaines

| Domaine | Questions guides | Premiers passages cherchés | Fichier de requêtes |
|---|---|---|---|
| **Temps** (voyage dans le temps) | comment le texte parle-t-il de durées, de la relativité des durées, du sommeil et du réveil, de l'heure ? | `ألف سنة`, `خمسين ألف سنة`, `لبثتم`, `يوما أو بعض يوم`, `الدهر` | [`config/queries/temps.yaml`](../config/queries/temps.yaml) |
| **Espace** (voyage dans l'espace) | comment parle-t-il du voyage, de l'ascension, des couches du ciel, des limites ? | `أسرى`, `المعارج`, `تعرج`, `أقطار`, `تنفذوا`, `سبع سماوات` | [`espace.yaml`](../config/queries/espace.yaml) |
| **Business** | commerce, mesure, dette, intérêt, bonne foi, subsistance | `تجارة`, `الربا`, `الكيل`, `الميزان`, `تداينتم بدين` | [`business.yaml`](../config/queries/business.yaml) |
| **Apprentissage** | savoir, écriture, lecture, réflexion, enseignement | `علم بالقلم`, `اقرأ`, `يتدبرون`, `الكتاب والحكمة` | [`apprentissage.yaml`](../config/queries/apprentissage.yaml) |
| **Intelligence** | raison, compréhension, discernement, mise en garde contre l'absence de réflexion | `تعقلون`, `أولي الألباب`, `يفقهون`, `يتفكرون` | [`intelligence.yaml`](../config/queries/intelligence.yaml) |
| **Et tout le reste** | mêmes outils pour tout domaine ajouté | à définir | un fichier YAML par domaine |

Ajouter un domaine = ajouter un fichier dans `config/queries/`, **le commiter avant de l'exécuter**, puis lancer `make passages`.

## Ce que « mieux comprendre » veut dire (quatre niveaux, du plus solide au plus fragile)

1. **Cartographier** (`FAIT`). Où le thème apparaît (versets, sourates), combien de fois, sous quelles formes exactes. Pas d'interprétation. *Implémenté pour la recherche de passages ; la cartographie par racine attend la morphologie.*
2. **Mesurer des motifs** (`FAIT` + statut statistique). Formules récurrentes, mots qui apparaissent ensemble, répartition par sourate et par période, comparaison à un modèle nul. *Planifié (Phases 3 à 6) ; la recherche de formules est implémentable dès maintenant.*
3. **Rapporter les lectures** (`INTERPRÉTATION`). Ce que disent les exégètes classiques et les lectures modernes, avec auteur et source. *Aucune source de tafsir acquise : non fait. Aucun tafsir n'est donné de mémoire.*
4. **Relier** (comparaisons). Entre domaines, entre périodes, entre le texte et d'autres corpus. *Planifié (Phases 5 et 6).*

## Ce que le projet peut et ne peut pas faire

**Il peut** : retrouver tous les passages qui contiennent une expression, montrer ce qui revient souvent ensemble, dire si un motif résiste à un modèle nul, séparer ce que dit le texte de ce que des lectures lui font dire.

**Il ne peut pas** :

- **démontrer** une thèse de physique (voyage dans le temps, relativité) ou d'économie à partir du texte. Il peut montrer qu'une lecture moderne *force* ou *respecte* le sens d'un mot arabe, en citant le lexique et les auteurs, étiquetée `INTERPRÉTATION` ;
- **donner des conseils** (financiers, éducatifs, médicaux, religieux) : ses sorties décrivent du texte ;
- **décider** si une lecture est vraie ou fausse. Il rapporte, tu conclus.

Pour les thèmes dits « scientifiques », la règle du cahier des charges s'applique : lister les versets, donner la lecture des exégètes classiques, puis les lectures modernes avec leurs auteurs, toutes étiquetées `INTERPRÉTATION`, et signaler quand une lecture moderne force le sens du mot.

## Le piège à éviter : trouver ce qu'on cherche

Dans un texte de 78 000 mots, on peut toujours trouver un passage qui « confirme » une idée. La parade du projet :

1. **Les requêtes sont fixées avant l'exécution** (commit séparé), y compris celles qui n'aboutiraient à rien. Une expression absente est un résultat.
2. **On rapporte aussi ce qui contredit** : les occurrences d'un mot dans un sens inattendu, les formes non reconnues.
3. **Un motif doit battre un modèle nul** avant d'être appelé motif (Phase 3). Une recherche de passages seule ne prouve aucun motif.
4. **Chaque affirmation populaire** (par exemple « le mot `عقل` n'apparaît que sous forme verbale ») devient une hypothèse pré-enregistrée avec sa règle de classement (voir H002).

## Pipeline d'un domaine

```
config/queries/<domaine>.yaml   (requêtes + justification, commité avant)
        │  make passages
        ▼
reports/passages/<domaine>.md   (par requête : nombre d'occurrences, versets, formes rencontrées)
reports/passages/<domaine>.json (liste complète)
        │  (morphologie acquise)
        ▼
fiche de concept : racines et lemmes, répartition par sourate, co-occurrences, nuls, lectures
```

## État

| Domaine | Recherche de passages | Motifs statistiques | Lectures (tafsir) |
|---|---|---|---|
| Temps | **exécutée** : [`reports/passages/temps.md`](../reports/passages/temps.md) | planifié | non acquis |
| Espace | **exécutée** : [`espace.md`](../reports/passages/espace.md) | planifié | non acquis |
| Business | **exécutée** : [`business.md`](../reports/passages/business.md) | planifié | non acquis |
| Apprentissage | **exécutée** : [`apprentissage.md`](../reports/passages/apprentissage.md) | planifié | non acquis |
| Intelligence | **exécutée** : [`intelligence.md`](../reports/passages/intelligence.md) ; **H002 et H002-v2** (formes de `عقل`) : [`H002-v2`](../reports/H002-v2-aql-candidats-elargis.md) | planifié | non acquis |

**Minorant, pas liste exhaustive.** Un passage dont l'expression est écrite autrement (préfixe non prévu, suffixe, variante orthographique) n'est pas trouvé. La première règle d'appariement (v1) a manqué 22:47 et 5 passages de `أولي الألباب` ; la règle v2 les trouve, et les deux sont rapportées côte à côte (voir [DECISIONS D16](DECISIONS.md)).

Le détail du plan par phase est dans la [feuille de route](roadmap.md).
