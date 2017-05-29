#!/usr/bin/env python

"""
Using new to create an even integer

rounds the input to the nearest even integer.

will even convert a string to an int...

"""


class EvenInt(int):
    """
    An integer that is always even
    """
    def __new__(cls, n):
        print("in new:", n)
        n = float(n)
        if not (n % 2 == 0):
            print("not even")
            n = round(n / 2) * 2
        print(n)
        return super().__new__(cls, n)


