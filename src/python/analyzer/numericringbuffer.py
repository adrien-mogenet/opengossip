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

import math
from ringbuffer import  RingBuffer

class NumericRingBuffer(RingBuffer):
    """Extends RingBuffer for implementing some calculs on numeric elements"""

    def mean(self):
        """Compute the current mean value"""

        total = 0
        if self.size == 0: return 0
        for elt in self:
            total += elt
        return float(total / float(self.size))

    def p_x(self, x):
        """Get probablity of seeing 'x' into the buffer"""

        if self.size == 0: return 0
        return float(self.count(x) / float(self.size))

    def expected_value(self):
        """Get current expected value"""

        result = 0.0
        if self.size == 0: return 0
        for elt in self.distinct():
            result += self.p_x(elt) * elt
        return result

    def shannon_entropy(self, base=2, blur=0):
        """Get current entropy of values within the current buffer. Getting '0'
           means there is no surprise, we still get the same value.
           FIXME: Use a blur parameter? (or should it be applied at an higher
           level ?"""

        entropy = 0.0
        X = self.distinct()
        n = len(X)
        for i in range(n):
            X_i = X[i]
            P_i = self.p_x(X_i)
            entropy += P_i * math.log(P_i, base)
        return -entropy

    def variance(self):
        """Get current variance"""

        variance = 0.0
        mean = self.mean()
        for i in range(self.size):
            X_i = self.get(i)
            variance += self.p_x(X_i) * ((X_i - mean)**2)
        return variance

    def percentage(self, percentage):
        """Get the value under which there are xx% of the values."""

        sorted = self.sort()
        size = len(sorted)
        index = min(size - 1, int(size * float(percentage / 100.0)))
        return sorted[index]

    def min(self):
        result = self[0]
        for elt in self:
            if elt < result:
                result = elt
        return result

    def max(self):
        result = self[0]
        for elt in self:
            if elt > result:
                result = elt
        return result
