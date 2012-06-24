#!/usr/bin/env
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
