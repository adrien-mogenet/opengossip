#!/usr/bin/env python

# This file is part of OpenGossip.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from superlist import SuperList
import unittest

class SuperListTest(unittest.TestCase):

    def test_percentage(self):
        sl = SuperList()
        for i in range(100):
            sl.append(100 - i)
        self.assertEqual(sl.percentage(0), 1)
        self.assertEqual(sl.percentage(90), 91)
        self.assertEqual(sl.percentage(100), 100)
        self.assertEqual(sl.percentage(101), 100)

    def test_percentage_lower_than(self):
        sl = SuperList()
        for i in range(100):
            sl.append(100 - i)
        self.assertEqual(sl.percentage_lower_than(-1), 0)
        self.assertEqual(sl.percentage_lower_than(11), 10)
        self.assertEqual(sl.percentage_lower_than(33.3), 33)
        self.assertEqual(sl.percentage_lower_than(101), 100)
        sl.append(4)
        self.assertTrue(sl.percentage_lower_than(5) > 4.95
                        and sl.percentage_lower_than(5) < 4.96)

    def test_percentage_greater_than(self):
        sl = SuperList()
        for i in range(100):
            sl.append(100 - i)
        self.assertEqual(sl.percentage_greater_than(-1), 100)
        self.assertEqual(sl.percentage_greater_than(11), 90)
        self.assertEqual(sl.percentage_greater_than(101), 0)

if __name__ == '__main__':
    unittest.main()
