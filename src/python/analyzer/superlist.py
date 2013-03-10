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

class SuperList(list):

    """
    Simple custom list, extending original class to add some methods.
    """

    def __init__(self):
        pass

    def percentage(self, percentage, reverse=False):
        """Get the value under/over which there are xx% of the values."""

        sorted = list(self)
        sorted.sort(reverse=reverse)
        size = len(sorted)
        index = min(size - 1, int(size * float(percentage / 100.0)))
        return sorted[index]

    def percentage_lower_than(self, value):
        sorted = list(self)
        sorted.sort()
        pos = 0
        while pos < len(self) and sorted[pos] < value:
            pos = pos + 1
        return 100.0 * float(pos) / float(len(self))

    def percentage_greater_than(self, value):
        return 100 - self.percentage_lower_than(value)
