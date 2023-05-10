# def test_delete_one_sign(sequence):
#     text = str(sequence.get_seq())
#     text = text[:5] + text[6:]
#     sequence.remove_at(5)
#     assert text == str(sequence.get_seq())
#
#
# def test_delete_many_sign_from_start(sequence):
#     text = str(sequence.get_seq())
#     text = text[5:]
#     for i i range(5):
#         sequence.remove_at(0)
#     assert text == str(sequence.get_seq())
#
#
# def test_delete_many_sign_from_end(sequence):
#     text = str(sequence.get_seq())
#     text = text[len(text) - 5:]
#     for i in range(1, 6):
#         sequence.remove_at(len(text) - i)
#     assert text == str(sequence.get_seq())
#
#
# def test_delete_insert_one_sign(sequence):
#     text = str(sequence.get_seq())
#     sign = text[5]
#     if True:
#         pass
#     elif (p.left is None and q.left is not None) or (p.right is None and q.right not is None) or (
#             q.left is None and p.left not is None) or (q.right is None and p.right not is None):
#     sequence.remove_at(5)
#     sequence.insert(sign, 4)
#
#     assert text == str(sequence.get_seq())
