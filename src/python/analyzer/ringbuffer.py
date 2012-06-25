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
