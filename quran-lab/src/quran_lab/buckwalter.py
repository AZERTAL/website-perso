"""Translittération Buckwalter -> arabe (format du Quranic Arabic Corpus v0.4).

Table de base : Buckwalter standard. Table d'extension (signes coraniques) : écrite
de mémoire, NON VÉRIFIÉE contre le fichier réel. Tout symbole inconnu lève une
erreur au lieu de passer silencieusement : le premier chargement du vrai fichier
dira quels symboles manquent.
"""

from __future__ import annotations

import unicodedata

CORE = {
    "'": 0x0621,  # ARABIC LETTER HAMZA
    "|": 0x0622,  # ARABIC LETTER ALEF WITH MADDA ABOVE
    ">": 0x0623,  # ARABIC LETTER ALEF WITH HAMZA ABOVE
    "&": 0x0624,  # ARABIC LETTER WAW WITH HAMZA ABOVE
    "<": 0x0625,  # ARABIC LETTER ALEF WITH HAMZA BELOW
    "}": 0x0626,  # ARABIC LETTER YEH WITH HAMZA ABOVE
    "A": 0x0627,  # ARABIC LETTER ALEF
    "b": 0x0628,  # ARABIC LETTER BEH
    "p": 0x0629,  # ARABIC LETTER TEH MARBUTA
    "t": 0x062A,  # ARABIC LETTER TEH
    "v": 0x062B,  # ARABIC LETTER THEH
    "j": 0x062C,  # ARABIC LETTER JEEM
    "H": 0x062D,  # ARABIC LETTER HAH
    "x": 0x062E,  # ARABIC LETTER KHAH
    "d": 0x062F,  # ARABIC LETTER DAL
    "*": 0x0630,  # ARABIC LETTER THAL
    "r": 0x0631,  # ARABIC LETTER REH
    "z": 0x0632,  # ARABIC LETTER ZAIN
    "s": 0x0633,  # ARABIC LETTER SEEN
    "$": 0x0634,  # ARABIC LETTER SHEEN
    "S": 0x0635,  # ARABIC LETTER SAD
    "D": 0x0636,  # ARABIC LETTER DAD
    "T": 0x0637,  # ARABIC LETTER TAH
    "Z": 0x0638,  # ARABIC LETTER ZAH
    "E": 0x0639,  # ARABIC LETTER AIN
    "g": 0x063A,  # ARABIC LETTER GHAIN
    "_": 0x0640,  # ARABIC TATWEEL
    "f": 0x0641,  # ARABIC LETTER FEH
    "q": 0x0642,  # ARABIC LETTER QAF
    "k": 0x0643,  # ARABIC LETTER KAF
    "l": 0x0644,  # ARABIC LETTER LAM
    "m": 0x0645,  # ARABIC LETTER MEEM
    "n": 0x0646,  # ARABIC LETTER NOON
    "h": 0x0647,  # ARABIC LETTER HEH
    "w": 0x0648,  # ARABIC LETTER WAW
    "Y": 0x0649,  # ARABIC LETTER ALEF MAKSURA
    "y": 0x064A,  # ARABIC LETTER YEH
    "F": 0x064B,  # ARABIC FATHATAN
    "N": 0x064C,  # ARABIC DAMMATAN
    "K": 0x064D,  # ARABIC KASRATAN
    "a": 0x064E,  # ARABIC FATHA
    "u": 0x064F,  # ARABIC DAMMA
    "i": 0x0650,  # ARABIC KASRA
    "~": 0x0651,  # ARABIC SHADDA
    "o": 0x0652,  # ARABIC SUKUN
    "`": 0x0670,  # ARABIC LETTER SUPERSCRIPT ALEF
    "{": 0x0671,  # ARABIC LETTER ALEF WASLA
}

# Extension coranique : NON VÉRIFIÉE (voir l'en-tête).
EXTENSION_UNVERIFIED = {
    "^": 0x0653,  # ARABIC MADDAH ABOVE
    "#": 0x0654,  # ARABIC HAMZA ABOVE
    ":": 0x06DC,  # ARABIC SMALL HIGH SEEN
    "@": 0x06DF,  # ARABIC SMALL HIGH ROUNDED ZERO
    '"': 0x06E0,  # ARABIC SMALL HIGH UPRIGHT RECTANGULAR ZERO
    "[": 0x06E2,  # ARABIC SMALL HIGH MEEM ISOLATED FORM
    ";": 0x06E3,  # ARABIC SMALL LOW SEEN
    ",": 0x06E5,  # ARABIC SMALL WAW
    ".": 0x06E6,  # ARABIC SMALL YEH
    "!": 0x06E8,  # ARABIC SMALL HIGH NOON
    "-": 0x06EA,  # ARABIC EMPTY CENTRE LOW STOP
    "+": 0x06EB,  # ARABIC EMPTY CENTRE HIGH STOP
    "%": 0x06EC,  # ARABIC ROUNDED HIGH STOP WITH FILLED CENTRE
    "]": 0x06ED,  # ARABIC SMALL LOW MEEM
}


def bw_to_ar(text: str, *, allow_unverified_extension: bool = True) -> str:
    """Convertit du Buckwalter en arabe. Lève ValueError sur un symbole inconnu."""
    table = {k: chr(v) for k, v in CORE.items()}
    if allow_unverified_extension:
        table.update({k: chr(v) for k, v in EXTENSION_UNVERIFIED.items()})
    out = []
    unknown = []
    for ch in text:
        if ch in table:
            out.append(table[ch])
        else:
            unknown.append(ch)
    if unknown:
        raise ValueError(f"symboles Buckwalter inconnus : {sorted(set(unknown))!r} dans {text!r}")
    # NFC : Buckwalter écrit shadda puis voyelle, le corpus réel voyelle puis shadda.
    # Les deux sont canoniquement équivalents ; NFC les ramène à un ordre unique.
    return unicodedata.normalize("NFC", "".join(out))
