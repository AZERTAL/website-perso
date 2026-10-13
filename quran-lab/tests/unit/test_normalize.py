from quran_lab.normalize import fold, skeleton, unicode_inventory, words


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
