#!/usr/bin/env python

"""
some simple testing examples
"""

import unittest
import math


class TestAlmostEqual(unittest.TestCase):

    def setUp(self):
        pass

    def test_floating_point(self):
        self.assertEqual(3 * .15, .45)

    def test_almost_equal(self):
        self.assertAlmostEqual(3 * .15, .45, places=7)

    def test_almost_equal_tiny(self):
        # these should be very differnt, but the rounding makes them both zero!
        self.assertAlmostEqual(4 * .15e-30, .45e-30, places=7)

    def test_almost_equal_huge(self):
        # these are very close differnt, but the rounding is only done for less than zero!
        self.assertAlmostEqual(3 * .15 * 1e30, .45 * 1e30, places=7)

    def test_isclose_tiny(self):
        # these should be very differnt, but the rounding makes them both zero!
        self.assertTrue(math.isclose(4 * .15e-30, .45e-30))

    def test_isclose_huge(self):
        # these are very close differnt, but the rounding is only done for less than zero!
        self.assertTrue(math.isclose(3 * .15 * 1e30, .45 * 1e30))

def test_floats():
    assert math.isclose(3 * .15 * 1e30, .45 * 1e30, rel_tol=1e-16)


if __name__ == '__main__':
    unittest.main()
