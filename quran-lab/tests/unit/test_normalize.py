from quran_lab.normalize import fold, skeleton, unicode_inventory, words


def U(hexes: str) -> str:
    """Chaîne depuis des codes hexadécimaux (les marques combinantes sont illisibles en clair)."""
    return "".join(chr(int(h, 16)) for h in hexes.split())


def test_strip_harakat_and_shadda():
    assert skeleton("يَوْمِ") == "يوم"
    assert skeleton("ٱللَّهِ") == "الله"  # alif wasla -> alif, shadda et voyelles retirées


def test_dagger_alif_removed():
    assert skeleton("ٱلرَّحْمَٰنِ") == "الرحمن"


def test_hamza_letters_are_kept_not_folded():
    # Piège NFD : `أ` ne doit PAS devenir `ا`.
    assert skeleton("أَيَّامٍ") == "أيام"
    assert skeleton("إِبْرَٰهِيمَ") == "إبراهيم".replace("ا", "")  # dagger alif retiré, pas remplacé


def test_tatweel_plus_hamza_carrier_becomes_letter_hamza():
    # Orthographe uthmani de « شيئا » : شَيْـٔٗا
    assert skeleton("شَيْـٔٗا") == "شيءا"


def test_quranic_signs_removed():
    assert skeleton("يَوْمِ۝") == "يوم"  # fin de verset
    assert skeleton("قَالَۖ") == "قال"  # signe de pause


def test_fold_is_opt_in():
    assert fold("أيام") == "أيام"
    assert fold("أيام", alif_hamza=True) == "ايام"
    assert fold("رحمة", ta_marbuta=True) == "رحمه"
    assert fold("على", alif_maqsura=True) == "علي"


def test_words_split():
    assert words("بِسْمِ ٱللَّهِ") == ["بِسْمِ", "ٱللَّهِ"]


def test_inventory_lists_codepoints():
    inv = unicode_inventory(["يَوْمِ"])
    assert any(k.startswith("U+064E") for k in inv)
    assert all(not k.startswith("U+0061") for k in inv)  # pas d'ASCII


def test_standalone_tatweel_removed():
    assert skeleton("كتـــاب") == "كتاب"


# Séquences relevées TELLES QUELLES dans data/raw/quran-uthmani.txt (1:7 et 2:4).
def test_madda_sign_on_alif_is_not_the_letter_alif_madda():
    word = U("0671 0644 0636 0651 064E 0627 0653 0644 0651 0650 064A 0646 064E")  # الضالين, 1:7
    assert skeleton(word) == U("0627 0644 0636 0627 0644 064A 0646")  # ا ل ض ا ل ي ن
    assert skeleton(word) == skeleton("الضالين")  # = l'orthographe simple


def test_precomposed_alif_madda_letter_is_kept():
    # la lettre `آ` (U+0622) fournie telle quelle est une vraie lettre : on ne la touche pas
    assert skeleton(U("0622 0645 0646")) == U("0622 0645 0646")


def test_tatweel_hamza_survives_nfc_reordering():
    # 2:4 « بالآخرة » : tatwil, hamza, fatha dans la source ; NFC met la fatha avant la hamza
    word = U("0648 064E 0628 0650 0671 0644 0652 0640 0654 064E 0627 062E 0650 0631 064E 0629 0650")
    assert skeleton(word) == U("0648 0628 0627 0644 0621 0627 062E 0631 0629")  # وبالءاخرة
