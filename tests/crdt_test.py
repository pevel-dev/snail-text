from crdt.Sequence import Sequence


# region simple
def test_simple():
    text = "I am crdt!"

    a = Sequence(0)
    b = Sequence(1)

    for i in range(len(text)):
        a._add(text[i], i)
        b._add(text[i], i)

    assert a.get_seq() == text
    assert b.get_seq() == text

    a._add("X", 4.5)
    b._add("I", 4.7)
    assert a.get_seq() == "I am Xcrdt!"
    assert b.get_seq() == "I am Icrdt!"

    b.merge(a)
    assert b.get_seq() == "I am XIcrdt!"
    b._add("A", 4.6)
    assert b.get_seq() == "I am XAIcrdt!"


def test_simple_2():
    text = "I am crdt!"

    a = Sequence(0)
    b = Sequence(1)

    for i in range(len(text)):
        a._add(text[i], i)
        b._add(text[i], i)

    b._add("I", 4.7)
    a._add("X", 4.5)
    assert a.get_seq() == "I am Xcrdt!"
    assert b.get_seq() == "I am Icrdt!"

    b.merge(a)
    assert b.get_seq() == "I am XIcrdt!"


def test_simple_3():
    text = "I am crdt!"

    a = Sequence(0)
    b = Sequence(1)

    for i in range(len(text)):
        a._add(text[i], i)
        b._add(text[i], i)

    b._add("X", 4.5)
    a._add("X", 4.5)
    assert a.get_seq() == "I am Xcrdt!"
    assert b.get_seq() == "I am Xcrdt!"

    b.merge(a)

    assert b.get_seq() == "I am Xcrdt!"


# endregion

# region insert
def test_insert():
    text = "Code is stolen"
    s = Sequence(0)
    actions = []

    actions += s.insert(text, 0)

    actions += s.insert("not ", 7)
    assert s.get_seq() == "Code is not stolen"

    actions += s.insert('!', -1)
    assert s.get_seq() == "Code is not stolen!"

    from random import shuffle
    s2 = Sequence(1)
    shuffle(actions)
    for oper in actions:
        s2.insert_tuple(oper)

    assert s.get_seq() == s2.get_seq()

# endregion
