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
       numerical values.

       TODO: Put array logic into a traditional array structure.
       """

    def __init__(self, max_size):
        """Init with max size"""

        self.max_size = max_size
        # FIXME: Use zeros()
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

    def __iter__(self):
        """Allow to iterate over the buffer. Beware that we are returning a new
           list"""

        result = []
        for i in range(self.size):
            result.append(self.get(i))
        return result.__iter__()

    def get(self, pos):
        """Retrieve element a given position"""

        return self.data[self.max_size - 1 - pos]

    def __getitem__(self, key):
        """Override the [] operator"""

        if isinstance(key, slice):
            return [self.get(pos) for pos in range(key.start, key.stop)]
        else:
            return self.get(key)

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
        """Retrieve list of distinct elements. We do not consider the
           initial 'None' elements."""

        if self.size < self.max_size:
            list = [self.get(i) for i in range(self.size)]
        else:
            list = self.data
        return dict.fromkeys(list).keys()

    def sort(self):
        """Retrieve list of sorted data."""

        sorted = self[0:self.size]
        sorted.sort()
        return sorted
