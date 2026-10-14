# config/queries/

Un fichier YAML par domaine de recherche. Chaque requête est une expression arabe cherchée dans le texte **simple-clean** de Tanzil, comparée au squelette consonantique.

- `kind: word` : un mot, avec ses clitiques possibles (`و`, `ف`, `ب`, `ل`, `ك`, `ال` devant le mot).
- `kind: phrase` : mots consécutifs dans un même verset ; le premier mot peut porter `و` ou `ف`.

**Règle** : ces fichiers sont commités AVANT d'être exécutés (`make passages`). Les requêtes ont été choisies de mémoire, avant d'avoir regardé le texte ; une expression qui ne figure pas dans le texte est un résultat, pas une erreur à corriger après coup. Pour ajouter une requête après avoir vu des résultats : ouvrir un nouveau fichier ou une nouvelle version, jamais modifier silencieusement.

`why` dit seulement pourquoi la requête est dans le domaine. Il ne contient aucune interprétation.
