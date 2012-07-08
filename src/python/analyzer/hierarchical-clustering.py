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

# Adapted from Jan Erik Solem
# Link:
#   http://www.janeriksolem.net/2009/04/hierarchical-clustering-in-python.html
# Partially taken and modified from the example in "Programming Collective
# Intelligence" by Toby Segaran (O'Reilly Media 2007, page 33).

import sys
import math
import numpypy # Comment if you don't use pypy
from numpy import *
from ringbuffer import RingBuffer
from numericringbuffer import NumericRingBuffer

BUFFER_SIZE = 100

def squared_euclidian(v, w):
    """Square euclidian distance function between two vectors"""

    return sum((v - w) ** 2)


def euclidian(v, w):
    """Standard euclidian distance function, for standard use"""

    return sqrt(sum((v - w) ** 2))


def merge_vectors(v, w):
    """Compute an average merged vector from v and w."""

    return [(v[i] + w[i]) / 2.0 for i in range(len(v))]


class ClusterNode:
    """Represents a node of hierarchical tree that will be built by our
       algorithm."""

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None,
                 meta={}):
        """Ctor
        Args:
           vector:   vector of features
           left:     left ClusterNode's child
           right:    right ClusterNode's child
           distance: current's distance
           id:       used when clustering. Positive id means it's a leaf
           count:    used for weighted average
           meta:     map of extra metadata."""

        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
        self.meta = meta


class HierarchicalClassifier(object):

    def __init__(self, output_folder):
        """Constructor. 'Counter' is the number of values we have added
           so far."""

        self.values = NumericRingBuffer(BUFFER_SIZE)
        self.nodes = []
        self.counter = 0
        self.output = open(output_folder + '/anomalies.dat', 'wb')
        self.orig = open(output_folder + '/original-serie.dat', 'wb')

    def __del__(self):
        """Destructor. Properly close opened file descriptors."""

        self.output.close()
        self.orig.close()

    def add(self, value):
        """Add a new value. We store the current number of the value in the
           map of metadata in 'n' key."""

        self.values.append(value)
        self.counter += 1
        if self.values.size > 1:
            self.orig.write(str(value) + '\n')
            vector = [
                self.values.mean(),
                self.values.shannon_entropy(),
                self.values.variance(),
                self.values.expected_value(),
            ]
            metadata = { 'n': self.counter, 'v': value }
            self.nodes.append(ClusterNode(vec=vector, meta=metadata))

    def build_set_rec(self, tree, marker):
        """Fill an array recursively from given tree."""

        if not tree:
            return []
        current = []
        if tree.id > 0:
            current = [(tree.meta['n'], marker)]
        return current + self.build_set_rec(tree.left, marker) \
            + self.build_set_rec(tree.right, marker)

    def build_sets(self, tree):
        """Build two classes from the given tree."""

        return [] + self.build_set_rec(tree.left, 0) \
            + self.build_set_rec(tree.right, 1)

    def find_anomalies(self):
        """Try to find anomalies according to what we have seen so far."""

        tree = self.hcluster(self.nodes, squared_euclidian)
        sets = self.build_sets(tree)
        sets = sorted(sets, key = lambda elt: elt[0])
        for elt in sets:
            self.output.write(str(int(elt[0])) + ' ' + str(elt[1]) + '\n')

    def hcluster(self, nodes, distance=euclidian):
        """Classif list of elements.
           Principle: each row start within it's individual cluster, then the
           matrix is processed to find closest rows until each row fits in a
           global hierarchical tree.

        Args:
           nodes:      array of ClusterNode's
           distance:  function computing distance between 2 vectors"""

        distances = {}  # cache of (v, w) distances
        currentclustid = -1

        # clusters are initially just the individual rows
        clust = [ClusterNode(vec=array(nodes[i].vec), id=i,
                             meta=nodes[i].meta) \
                     for i in range(len(nodes))]

        while len(clust) > 1:
            lowestpair = (0, 1)
            closest = distance(clust[0].vec, clust[1].vec)

            # loop through every pair looking for the smallest distance
            # v_id and w_id are made local variable to avoid slow lookup
            # several times. The try/except statement is prefered as well
            # for performance issues (compared to `key not in distances`)
            for i in range(len(clust)):
                for j in range(i + 1, len(clust)):
                    v_id = clust[i].id
                    w_id = clust[j].id
                    try:
                        d = distances[(v_id, w_id)]
                    except KeyError:
                        distances[(v_id, w_id)] = \
                            distance(clust[i].vec, clust[j].vec)
                        d = distances[(v_id, w_id)]
                    if d < closest:
                        closest = d
                        lowestpair = (i, j)

            # calculate the average of the two clusters
            merged_vector = merge_vectors(clust[lowestpair[0]].vec,
                                          clust[lowestpair[1]].vec)

            # create the new cluster
            newcluster = ClusterNode(array(merged_vector),
                                     left=clust[lowestpair[0]],
                                     right=clust[lowestpair[1]],
                                     distance=closest,
                                     id=currentclustid)

            # cluster ids that weren't in the original set are negative
            currentclustid -= 1
            del clust[lowestpair[1]]
            del clust[lowestpair[0]]
            clust.append(newcluster)

        return clust[0]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: hierarchical-clustering.py INPUT OUTPUT_FOLDER')
        sys.exit(1)
    filename = sys.argv[1]
    output = sys.argv[2]
    c = HierarchicalClassifier(output)
    f = open(filename, 'rb')
    for line in f:
        c.add(float(line.split(' ')[1].replace(',', '.')))
    c.find_anomalies()
    f.close()
