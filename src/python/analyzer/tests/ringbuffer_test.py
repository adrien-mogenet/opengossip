#!/usr/bin/env

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
from ringbuffer import RingBuffer
import unittest


class RingBufferTest(unittest.TestCase):

    def test_append(self):
        buffer = RingBuffer(10)
        buffer.append(42)
        self.assertEqual(buffer.last(), 42)
        buffer.append(21)
        self.assertEqual(buffer.last(), 21)

    def test_get(self):
        buffer = RingBuffer(10)
        self.assertEqual(buffer.get(0), None)
        try:
            buffer.get(11)
            self.assertTrue(False, "Should throw exception")
        except:
            self.assertTrue(True, "Should throw exception")
        buffer.append(42)
        self.assertEqual(buffer.get(0), 42)
        buffer.append('21')
        self.assertEqual(buffer.get(0), '21')
        self.assertEqual(buffer.get(1), 42)

    def test_size(self):
        buffer = RingBuffer(10)
        self.assertEqual(buffer.size, 0)
        buffer.append(42)
        self.assertEqual(buffer.size, 1)
        for i in range(11):
            buffer.append(i)
        self.assertEqual(buffer.size, 10)

if __name__ == '__main__':
    unittest.main()
