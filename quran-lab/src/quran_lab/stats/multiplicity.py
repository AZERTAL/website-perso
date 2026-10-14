"""Correction des comparaisons multiples.

Pourquoi : si l'on teste 100 000 paires de mots, environ 5 000 « tomberont juste » à 5 % par
pur hasard. Une p-value brute n'a de sens que pour UN test ; sur une famille de m tests, on
ajuste. Chaque fonction renvoie les p-values ajustées, dans l'ordre d'entrée.

- Bonferroni, Holm : contrôlent le risque de AU MOINS UNE fausse découverte (FWER).
- Benjamini-Hochberg : contrôle la proportion attendue de fausses découvertes (FDR),
  valide pour des tests indépendants ou positivement dépendants.
- Benjamini-Yekutieli : FDR sous dépendance quelconque (plus conservateur).
- Westfall-Young (max-T, une étape) : FWER par permutation, adapté aux tests corrélés
  (cas typique : toutes les paires de mots d'un même texte).
"""

from __future__ import annotations

import numpy as np


def _check(p: np.ndarray) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    if p.ndim != 1:
        raise ValueError("p doit être un vecteur")
    if np.isnan(p).any() or ((p < 0) | (p > 1)).any():
        raise ValueError("p-values hors de [0, 1] ou NaN")
    return p


def bonferroni(p) -> np.ndarray:
    p = _check(p)
    return np.minimum(1.0, p * len(p))


def holm(p) -> np.ndarray:
    """Descente de Holm : (m - rang) * p, puis maximum cumulé, plafonné à 1."""
    p = _check(p)
    m = len(p)
    order = np.argsort(p, kind="stable")
    adj = np.maximum.accumulate((m - np.arange(m)) * p[order])
    out = np.empty(m)
    out[order] = np.minimum(1.0, adj)
    return out


def benjamini_hochberg(p) -> np.ndarray:
    """Montée de BH : p * m / rang, puis minimum cumulé depuis le plus grand rang."""
    p = _check(p)
    m = len(p)
    order = np.argsort(p, kind="stable")
    ranked = p[order] * m / np.arange(1, m + 1)
    adj = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(m)
    out[order] = np.minimum(1.0, adj)
    return out


def benjamini_yekutieli(p) -> np.ndarray:
    """BH multiplié par c(m) = somme des 1/i, valide sous dépendance quelconque."""
    p = _check(p)
    m = len(p)
    if m == 0:
        return p
    c = float(np.sum(1.0 / np.arange(1, m + 1)))
    return np.minimum(1.0, benjamini_hochberg(p) * c)


def westfall_young_maxt(observed, null_stats) -> np.ndarray:
    """p-values ajustées par max-T (une étape), statistiques « grand = extrême ».

    observed : (m,) statistiques observées.
    null_stats : (B, m) statistiques de B permutations (mêmes m tests).
    p_i = (1 + #{b : max_j null[b, j] >= observed_i}) / (B + 1)  (Phipson-Smyth : jamais 0).
    """
    obs = np.asarray(observed, dtype=float)
    null = np.asarray(null_stats, dtype=float)
    if null.ndim != 2 or null.shape[1] != len(obs):
        raise ValueError("null_stats doit être de forme (B, m)")
    row_max = null.max(axis=1)
    counts = np.array([(row_max >= o).sum() for o in obs])
    return (1.0 + counts) / (len(row_max) + 1.0)
