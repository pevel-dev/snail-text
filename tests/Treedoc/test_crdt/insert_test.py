# import os
#
# import pytest
#
#
#
#
# @pytest.mark.parametrize("file_name", ["test_crdt/sample_files/simple.txt"])
# # "test_crdt/sample_files/40KB.txt"])
# def test_append_real_files(file_name):
#     print(os.getcwd())
#     with open(file_name, "r") as file:
#         lines = file.readlines()
#
#     s = Sequence(0)
#     c = 0
#     for line in lines:
#         for sign in line:
#             s.append_subseq(sign)
#             c += 1
#
#     assert s.get_seq() == ''.join(lines)
