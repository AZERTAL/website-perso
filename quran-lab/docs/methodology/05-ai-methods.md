# 05 · Couche IA (méthode prévue, non implémentée)

> **État : aucun code de cette page n'existe encore.** Elle décrit la méthode retenue et les critères de validation, pour que l'implémentation ne puisse pas être « ajustée » après coup. Elle sera implémentée en Phases 4 à 6 ([roadmap](../roadmap.md)).

## Principe directeur

Un modèle appris est un **instrument**, pas une preuve. Pour chaque instrument :

1. une **mesure de validité** contre une référence indépendante ;
2. un **contrôle négatif** : le même pipeline sur des données sans signal (versets mélangés) ; on rapporte combien de structure il invente quand même ;
3. un **test de stabilité** (graines, sous-échantillons).

Un thème qui apparaît dans le texte mais pas dans le contrôle négatif est un résultat. Sinon, c'est du bruit.

## Représentations du texte

| Représentation | Rôle | Remarque |
|---|---|---|
| Sacs de racines et de lemmes (TF-IDF, BM25) | base interprétable, invariante à la flexion | référence minimale que les modèles appris doivent battre ; exige la morphologie |
| Encodeurs arabes pré-entraînés (famille CAMeLBERT, dont la variante classique, AraBERT, MARBERT ; contrôles multilingues LaBSE, BGE-M3) | similarité de versets, regroupement | le registre coranique diffère de l'arabe moderne standard : on compare plusieurs modèles entre eux. Noms et disponibilité exacts **à vérifier** sur le hub avant usage |
| Embeddings entraînés sur le seul Coran | contrôle de cohérence uniquement | environ 78 000 mots : trop petit pour une représentation fiable |
| Traductions | affichage seulement | **jamais** utilisées pour compter |

Les poids viennent de `huggingface.co` (domaine autorisé dans l'environnement). La révision exacte de chaque modèle sera fixée (hash) dans le manifeste.

## Valider sans « vérité terrain »

Il n'existe pas de classement thématique du Coran qui fasse consensus. Instruments, du plus fort au plus faible :

1. **Ontologie de concepts du Quranic Arabic Corpus**, comme référence indépendante pour mesurer précision, rappel et F1 de nos lexiques et regroupements. *Existence et format de téléchargement à vérifier.*
2. **Versets parallèles ou répétés** : un bon embedding doit les rapprocher. Source à identifier ; sinon détection par n-grammes de racines, et on le dit.
3. **Proxy faible** : prédire mecquois/médinois à partir de l'embedding d'un verset, avec une validation croisée **groupée par sourate** (sinon des versets voisins fuient entre entraînement et test). On compare à un classifieur trivial « longueur du verset + rime » : si l'embedding ne le bat pas, il n'apporte rien de sémantique.
4. **Accord entre modèles** : recouvrement des k plus proches voisins entre encodeurs.

> **Fuite d'information** : valider un modèle sur des données qui contiennent des voisins de ses données d'entraînement. Exemple : deux versets de la même sourate, un dans l'entraînement, un dans le test. D'où la validation groupée par sourate.

## Modélisation de thèmes

LDA, NMF et BERTopic sur des lemmes (fenêtres de N versets). Le nombre de thèmes K est choisi par **stabilité** (appariement hongrois des thèmes entre graines, indice de Jaccard) et par cohérence (NPMI), jamais par la cohérence seule. Contrôle négatif : le même pipeline sur versets mélangés.

## Regroupement

HDBSCAN et regroupement hiérarchique sur embeddings. Validité : silhouette, ARI contre l'ontologie et contre mecquois/médinois, stabilité par ré-échantillonnage, permutation des étiquettes.

## Réseau de concepts et cycles

- **Arêtes** : co-occurrence dans le verset et dans une fenêtre de N versets, pondérée par PMI normalisée ou G² de Dunning (la fréquence brute favorise les mots communs).
- **Nul** : modèle de configuration (degrés conservés) par permutation ; communautés (Louvain ou Leiden) avec consensus sur 100 graines.
- **Cycles** : un cycle est un motif séquentiel ordonné (par exemple vent, nuage, pluie, eau, végétation, mort, résurrection). On les cherche par fouille de motifs séquentiels avec fenêtre bornée, comparés aux nuls N1 et N4. **Un cycle est une hypothèse de lecture, pas un résultat**, tant qu'il ne bat pas le nul. Le motif est fixé *avant* de regarder (pré-enregistrement), sinon c'est du choix après coup.

## Structure formelle

Longueur des versets (série et autocorrélation), rime de fin de verset (fāṣila) par extraction des dernières lettres, répétitions et formules (n-grammes de racines, distance de compression normalisée), entropie. L'analyse formulaïque (Parry-Lord) est un cadre de lecture, pas une conclusion.

## Usage d'un grand modèle de langage

Un LLM peut **proposer** des candidats (élargir un lexique, suggérer des motifs), jamais certifier. Toute sortie est consignée (entrée, sortie, date). Toute proposition devient un test pré-enregistré avant d'être évaluée. Aucune citation de tafsir n'est générée de mémoire : sans source ouverte, on écrit « source non consultée ».

## Reproductibilité des expériences

Graines fixées, versions épinglées (`uv.lock`), révision de modèle fixée, exécution CPU déterministe quand possible (le non-déterminisme résiduel est signalé), scripts relançables plutôt que carnets, journal d'expériences en JSONL (paramètres, graine, hash des données, métriques, durée).
