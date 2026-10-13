"""Normalisation du texte arabe.

Fonctions pures et idempotentes. Aucune ne replie silencieusement les variantes
de hamza, d'alif maqsura ou de ta marbuta : ces repliements sont des options
explicites (`fold`), jamais appliquées par défaut.

Piège évité : on ne passe PAS par NFD. NFD décompose `أ` en `ا` + hamza combinante,
et retirer les marques combinantes replierait alors `أ` en `ا` sans le dire.
"""

from __future__ import annotations

import re
import unicodedata
from functools import cache

TATWEEL = chr(0x0640)
ALIF = chr(0x0627)
ALIF_WASLA = chr(0x0671)
HAMZA = chr(0x0621)
HAMZA_ABOVE = chr(0x0654)
HAMZA_BELOW = chr(0x0655)
MADDAH = chr(0x0653)

# Tatwil portant une hamza combinante, quelles que soient les voyelles intercalées (NFC réordonne
# les marques : la source écrit tatwil, hamza, fatha ; après NFC on obtient tatwil, fatha, hamza).
_TATWEEL_HAMZA = re.compile(
    f"{TATWEEL}[\u064b-\u065f\u0670]*[{HAMZA_ABOVE}{HAMZA_BELOW}][\u064b-\u065f\u0670]*"
)

# Signes coraniques qui ne sont pas des marques combinantes (catégorie != Mn) mais
# qui ne font pas partie du squelette consonantique.
_EXTRA_STRIP = frozenset(
    {
        TATWEEL,
        "\N{ARABIC END OF AYAH}",
        "\N{ARABIC START OF RUB EL HIZB}",
        "\N{ARABIC PLACE OF SAJDAH}",
        "\N{ARABIC SMALL WAW}",
        "\N{ARABIC SMALL YEH}",
        "\N{ZERO WIDTH NON-JOINER}",
        "\N{ZERO WIDTH JOINER}",
        "\N{LEFT-TO-RIGHT MARK}",
        "\N{RIGHT-TO-LEFT MARK}",
    }
)


def _drop(ch: str) -> bool:
    return unicodedata.category(ch) == "Mn" or ch in _EXTRA_STRIP


@cache  # fonction pure ; les mots se répètent (types << occurrences)
def skeleton(text: str) -> str:
    """Squelette consonantique : lettres de base seulement.

    Règles, dans l'ordre :
    1. Alif + maddah (signe d'allongement) -> alif simple, avant NFC.
    2. NFC (jamais NFD, voir l'en-tête du module).
    3. Tatwil portant une hamza combinante (orthographe uthmani de `شيئا`, `الآخرة`) -> `ء`.
    3. Alif wasla `ٱ` -> `ا`.
    4. Retrait des diacritiques, signes coraniques et tatwil restants.
    5. Espaces normalisés.
    """
    # Signe d'allongement (maddah) sur un alif : ce n'est PAS la lettre « alif madda » `آ`, c'est
    # un alif simple marqué (Tanzil Uthmani écrit `ا` + U+0653, jamais `آ`). À retirer AVANT NFC,
    # qui recomposerait `ا` + `ٓ` en la lettre `آ` (constaté sur 3 687 occurrences du texte réel).
    s = text.replace(ALIF + MADDAH, ALIF)
    s = unicodedata.normalize("NFC", s)
    s = _TATWEEL_HAMZA.sub(HAMZA, s)
    s = s.replace(ALIF_WASLA, ALIF)
    s = "".join(ch for ch in s if not _drop(ch))
    return " ".join(s.split())


def fold(
    text: str,
    *,
    alif_hamza: bool = False,
    alif_maqsura: bool = False,
    ta_marbuta: bool = False,
) -> str:
    """Repliements optionnels, appliqués APRÈS `skeleton`. Tous désactivés par défaut."""
    s = text
    if alif_hamza:
        for ch in "أإآ":  # أ إ آ
            s = s.replace(ch, ALIF)
    if alif_maqsura:
        s = s.replace("ى", "ي")  # ى -> ي
    if ta_marbuta:
        s = s.replace("ة", "ه")  # ة -> ه
    return s


def words(text: str) -> list[str]:
    """Découpage en mots par espaces (définition d'un mot Tanzil)."""
    return text.split()


def unicode_inventory(texts: list[str]) -> dict[str, int]:
    """Inventaire des caractères non-ASCII d'un jeu de textes : `U+XXXX NOM (cat)` -> effectif.

    Sert à auditer une source réelle : tout caractère inattendu doit être traité
    explicitement, pas ignoré.
    """
    inv: dict[str, int] = {}
    for t in texts:
        for ch in t:
            if ord(ch) < 128:
                continue
            key = f"U+{ord(ch):04X} {unicodedata.name(ch, '?')} ({unicodedata.category(ch)})"
            inv[key] = inv.get(key, 0) + 1
    return dict(sorted(inv.items()))
