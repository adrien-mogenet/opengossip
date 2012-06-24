#!/usr/bin/env

class RingBuffer(object):
    """Circular buffer, implementing convenient methods. Suppose to contain
       numerical values"""

    def __init__(self, max_size):
        """Init with max size"""
        self.max_size = max_size
        self.data = [None for i in xrange(max_size)]
        self.size = 0

    def append(self, x):
        """Append a new element"""
        self.data.pop(0)
        self.data.append(x)
        if (self.size < self.max_size):
            self.size += 1

    def get_data(self):
        """Get raw data"""
        return self.data

    def get(self, pos):
        """Retrieve element a given position"""
        return self.data[self.max_size - 1 - pos]

    def last(self):
        """Get last element"""
        if (self.size == 0):
            return None
        else:
            return self.data[self.max_size - 1]

    def count(self, x):
        """Count occurrences of x"""
        return self.data.count(x)

    def distinct(self):
        """Retrieve list of distinct elements"""
        return dict.fromkeys(self.data).keys()
