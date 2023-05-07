def test_delete_one_sign(sequence):
    text = str(sequence.get_seq())
    text = text[:5] + text[6:]
    sequence.remove_at(5)
    assert text == str(sequence.get_seq())


def test_delete_many_sign_from_start(sequence):
    text = str(sequence.get_seq())
    text = text[5:]
    for i in range(5):
        sequence.remove_at(0)
    assert text == str(sequence.get_seq())


def test_delete_many_sign_from_end(sequence):
    text = str(sequence.get_seq())
    text = text[len(text) - 5:]
    for i in range(1, 6):
        sequence.remove_at(len(text) - i)
    assert text == str(sequence.get_seq())
