from crdt.Sequence import Sequence


def test_simple():
    text = "I am crdt!"

    a = Sequence(0)
    b = Sequence(1)

    for i in range(len(text)):
        a.add(text[i], i)
        b.add(text[i], i)

    assert a.get_seq() == text
    assert b.get_seq() == text

    a.add("X", 4.5)
    b.add("I", 4.7)
    assert a.get_seq() == "I am Xcrdt!"
    assert b.get_seq() == "I am Icrdt!"

    b.merge(a)
    assert b.get_seq() == "I am XIcrdt!"
    b.add("A", 4.6)
    assert b.get_seq() == "I am XAIcrdt!"


def test_simple_2():
    text = "I am crdt!"

    a = Sequence(0)
    b = Sequence(1)

    for i in range(len(text)):
        a.add(text[i], i)
        b.add(text[i], i)

    b.add("I", 4.7)
    a.add("X", 4.5)
    assert a.get_seq() == "I am Xcrdt!"
    assert b.get_seq() == "I am Icrdt!"

    b.merge(a)
    assert b.get_seq() == "I am XIcrdt!"


def test_simple_3():
    text = "I am crdt!"

    a = Sequence(0)
    b = Sequence(1)

    for i in range(len(text)):
        a.add(text[i], i)
        b.add(text[i], i)

    b.add("X", 4.5)
    a.add("X", 4.5)
    assert a.get_seq() == "I am Xcrdt!"
    assert b.get_seq() == "I am Xcrdt!"

    b.merge(a)

    assert b.get_seq() == "I am Xcrdt!"
