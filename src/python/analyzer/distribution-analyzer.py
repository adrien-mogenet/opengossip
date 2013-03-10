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

import sys
from superlist import SuperList
from optparse import OptionParser


class DistributionAnalyzer:

    def __init__(self):
        self.list = SuperList()

    def add(self, value):
        self.list.append(value)

    def get_size(self):
        return len(self.list)

    def print_percentage(self, percentage):
        value = self.list.percentage(percentage)
        print(str(percentage) + "% under " + str(value))

    def print_default_percentages(self):
        self.print_percentage(50)
        self.print_percentage(75)
        self.print_percentage(90)
        self.print_percentage(99)
        self.print_percentage(100)

    def find_percentage_lower_than(self, value):
        p = self.list.percentage_lower_than(value)
        print("%.2f%% of values are < %s" % (p, value))

    def find_percentage_greater_than(self, value):
        p = self.list.percentage_greater_than(value)
        print("%.2f%% of values are > %s" % (p, value))

    def find_percentage_between(self, low, high):
        low, high = min(low, high), max(low, high)
        a = self.list.percentage_greater_than(high)
        b = self.list.percentage_lower_than(low)
        result = 100.0 - (a + b)
        print("%.2f of values are in [ %s, %s ]" % (result, low, high))


def parse_args(argv):
    parser = OptionParser(description='Get an overview of your dataset.')
    parser.add_option('-c', '--column-index', default=0, dest='cindex', type='int',
                      help='Index of data to consider, starting from 0.')
    parser.add_option('-l', '--lower-than', dest='lt', metavar='VALUE',
                      type='float',
                      help='Get percentage of values lower than the supplied value.')
    parser.add_option('-g', '--greater-than', dest='gt', metavar='VALUE',
                      type='float',
                      help='Get percentage of values greater than the supplied value.')
    parser.add_option('-f', '--file', dest='file', metavar='FILEPATH')
    return parser.parse_args(args=argv)


if __name__ == "__main__":
    (options, args) = parse_args(sys.argv[1:])
    if options.file is None:
        parser.print_help()
        parser.error('No input file.')
    analyzer = DistributionAnalyzer()
    action_performed = False
    index = options.cindex
    f = open(options.file, 'rb')
    for line in f:
        try:
            analyzer.add(float(line.split(' ')[index].replace(',', '.')))
        except IndexError as e:
            print("Ignored line, column %i not found." % index)
    f.close()
    if analyzer.get_size() == 0:
        print("No valid lines, exit.")
        sys.exit(2)
    if options.lt is not None:
        analyzer.find_percentage_lower_than(options.lt)
        action_performed = True
    if options.gt is not None:
        analyzer.find_percentage_greater_than(options.gt)
        action_performed = True
    if options.lt is not None and options.gt is not None:
        analyzer.find_percentage_between(options.gt, options.lt)
    if not action_performed:
        analyzer.print_default_percentages()
