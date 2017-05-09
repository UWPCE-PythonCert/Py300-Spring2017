#!/usr/bin/env python3

"""
tests for  json_save
"""

import json_save.json_save as js

import pytest


# A few simple examples to test
class SimpleClass(js.JsonSavable):

    a = js.Int()
    b = js.Float()

    def __init__(self, a=None, b=None):
        if a is not None:
            self.a = a
        if b is not None:
            self.b = b


class ClassWithList(js.JsonSavable):

    x = js.Int()
    l = js.List()

    def __init__(self, x, l):
        self.x = x
        self.l = l


@pytest.fixture
def nested_example():
    l = [SimpleClass(3, 4.5),
         SimpleClass(100, 5.2),
         SimpleClass(34, 89.1),
         ]

    return ClassWithList(34, l)


def test_simple_hasattr():
    ts = SimpleClass()
    # has the attribures even though no __init__ exists
    assert 'a' in ts.__dict__
    assert 'b' in ts.__dict__


def test_simple_save():

    ts = SimpleClass()
    ts.a = 5
    ts.b = 3.14

    saved = ts.to_json_compat()
    assert saved['a'] == 5
    assert saved['b'] == 3.14
    assert saved['__obj_type'] == 'SimpleClass'


def test_list_attr():

    cwl = ClassWithList(10, [1, 5, 2, 8])

    saved = cwl.to_json_compat()
    assert saved['x'] == 10
    assert saved['l'] == [1, 5, 2, 8]
    assert saved['__obj_type'] == 'ClassWithList'


def test_nested(nested_example):

    saved = nested_example.to_json_compat()

    print(saved)
    assert saved['x'] == 34
    assert len(saved['l']) == 3
    for obj in saved['l']:
        assert obj['__obj_type'] == 'SimpleClass'


def test_save_load_simple():
    sc = SimpleClass(5, 3.14)

    jc = sc.to_json_compat()

    # re-create it from the dict:
    sc2 = SimpleClass.from_json_dict(jc)

    assert sc == sc2


def test_save_load_nested(nested_example):

    jc = nested_example.to_json_compat()

    # re-create it from the dict:
    nested_example2 = ClassWithList.from_json_dict(jc)

    assert nested_example == nested_example2


def test_from_json_dict(nested_example):

    j_dict = nested_example.to_json_compat()

    reconstructed = js.from_json_dict(j_dict)

    assert reconstructed == nested_example


def test_from_json(nested_example):
    """
    can it be re-created from an actual json string?
    """

    json_str = nested_example.to_json()

    reconstructed = js.from_json(json_str)

    assert reconstructed == nested_example


def test_from_json_file(nested_example):
    """
    can it be re-created from an actual json file?
    """

    json_str = nested_example.to_json()
    with open("temp.json", 'w') as tempfile:
        tempfile.write(nested_example.to_json())

    with open("temp.json") as tempfile:
        reconstructed = js.from_json(tempfile)

    reconstructed = js.from_json(json_str)

    assert reconstructed == nested_example
