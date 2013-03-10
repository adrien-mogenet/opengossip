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
import math
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
from numericringbuffer import NumericRingBuffer
import unittest


class NumericRingBufferTest(unittest.TestCase):

    def test_mean(self):
        buffer = NumericRingBuffer(10)
        self.assertEqual(buffer.mean(), 0)
        buffer.append(42)
        self.assertEqual(buffer.mean(), 42.0)
        buffer.append(5)
        self.assertEqual(buffer.mean(), 23.5)

    def test_probability(self):
        buffer = NumericRingBuffer(10)
        self.assertEqual(buffer.p_x(0), 0)
        buffer.append(42)
        self.assertEqual(buffer.p_x(42), 1)
        buffer.append(1234567890)
        self.assertEqual(buffer.p_x(42), 0.5)

    def test_expected_value(self):
        buffer = NumericRingBuffer(10)
        self.assertEqual(buffer.expected_value(), 0)
        buffer.append(42)
        self.assertEqual(buffer.expected_value(), 42)
        buffer.append(21)
        self.assertEqual(buffer.expected_value(), 31.5)
        buffer.append(21)
        self.assertEqual(buffer.expected_value(), 28)

    def test_entropy(self):
        """Check some entropies properties"""
        buffer = NumericRingBuffer(10000)
        self.assertEqual(buffer.shannon_entropy(), 0)
        buffer.append(10)
        self.assertEqual(buffer.shannon_entropy(), 0)
        import random
        for i in range(10000):
            buffer.append(random.randint(0,1000))
        self.assertTrue(buffer.shannon_entropy(2) != 0)
        self.assertTrue(buffer.shannon_entropy(10) != 0)
        self.assertTrue(buffer.shannon_entropy(2) < math.log(1000, 2))

    def test_variance(self):
        buffer = NumericRingBuffer(10)
        self.assertEqual(buffer.variance(), 0)

    def test_distribution(self):
        buffer = NumericRingBuffer(100)
        for i in range(100):
            buffer.append(100 - i)
        self.assertEqual(buffer.percentage(0), 1)
        self.assertEqual(buffer.percentage(90), 91)
        self.assertEqual(buffer.percentage(100), 100)
        self.assertEqual(buffer.percentage(101), 100)

if __name__ == '__main__':
    unittest.main()
