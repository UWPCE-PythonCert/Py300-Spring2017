#!/usr/bin/env python3

"""
tests for  json_save
"""

import json_save as js

# try making a JsonSavable object


def test_simple():
    class TestClass(js.JsonSavable):
        pass

    tc = TestClass()

    assert False
