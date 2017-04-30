#!/usr/bin/env python

"""
Simple iterator example

This is a solution to an class-based iterator that
simulates the range() built in.

The range() API:

range(stop) -> range object

range(start, stop[, step]) -> range object

Return an object that produces a sequence of integers from start (inclusive)
to stop (exclusive) by step.  range(i, j) produces i, i+1, i+2, ..., j-1.
start defaults to 0, and stop is omitted!  range(4) produces 0, 1, 2, 3.
These are exactly the valid indices for a list of 4 elements.
When step is given, it specifies the increment (or decrement).

NOTE: this is a bit of an tricky API:

With one argument, the value is the "stop" value

With two or three arguments, the first value is "start", and the second "stop"

That isn't really relevent to the iterator issue, but still a good thing to know about.

"""


class MyRange(object):
    """
    About as simple an iterator as you can get:

    returns the sequence of numbers from zero to 4
    ( like range(4) )
    """
    def __init__(self, start, stop=None, step=1):
        if stop is None:
            stop = start
            start = 0
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        # reset on re-iterating
        self.current = self.start - self.step
        return self

    def __next__(self):
        try:
            self.current += self.step
        except AttributeError:
            raise TypeError("MyRange is not an iterator")
        if self.current < self.stop:
            return self.current
        else:
            raise StopIteration

# putting the tests in teh same module 
# usually one would putthe tests in a separate module, but this is small enough

# they can be run with pytest:
# $ pytest iterator_solution.py

# whilethe most common way to use an iterator is a for loop, you can also pass an
# iterator to many other funcitons, such as the list() constructor
#
# list() is used in the tests, as it's a lot easier to test if you get the list
# expected than if a for loop ran correctly.
#
# in this case, we can compare to what hte built-in range does...

import pytest

@pytest.mark.parametrize('stop', [3, 10, 0])
def test_just_stop(stop):
    """
    The MyRange object should produce a list that's the right length
    and have all integers in it.
    """

    assert list(MyRange(stop)) == list(range(stop))


def test_renter():
    """
    iterating part way through, and then again should reset the iterator
    """

    r = MyRange(10)
    for i in r:
        if i > 5:
            break

    assert list(r) == list(range(10))

def test_start_stop():
    """
    what if there is a start an a stop value?
    """

    assert list(MyRange(2, 10)) == list(range(2, 10))

@pytest.mark.parametrize("start, stop, step",[(0, 10, 1),
                                              (3, 10, 2)])
def test_start_stop_step(start, stop, step):
    """
    What if there is a start, stop and step value?
    """

    assert list(MyRange(start, stop, step)) == list(range(start, stop, step))


