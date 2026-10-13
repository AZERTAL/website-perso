from hypothesis import given, settings
from hypothesis import strategies as st

from quran_lab.normalize import skeleton

arabic_chars = st.characters(min_codepoint=0x0600, max_codepoint=0x06FF) | st.just(" ")
arabic = st.text(arabic_chars, max_size=40)


@settings(max_examples=500)
@given(arabic)
def test_skeleton_is_idempotent(s):
    assert skeleton(skeleton(s)) == skeleton(s)


@settings(max_examples=500)
@given(arabic)
def test_skeleton_never_longer_than_nfc_input(s):
    import unicodedata

    # hormis tatwil+hamza -> ء (1 caractère de moins que 2), jamais plus long
    assert len(skeleton(s)) <= len(unicodedata.normalize("NFC", s))


@settings(max_examples=500)
@given(arabic)
def test_no_combining_marks_remain(s):
    import unicodedata

    assert all(unicodedata.category(c) != "Mn" for c in skeleton(s))
