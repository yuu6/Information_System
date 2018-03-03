#!/usr/bin/env python

import networkx
import os
import sys

from nose.tools import assert_almost_equal

from propagation.independent_cascade import independent_cascade


run_times = 10000
def test_independent_cascade(G,seeds):
    n_A = 0.0
    for i in range(run_times):
      A = independent_cascade(G, seeds, steps=1)
      for layer in A:
        n_A += len(layer)
    assert_almost_equal(n_A / run_times, 1.7, places=1)

    n_A = 0.0
    A = [ ]
    for i in range(run_times):
      A = independent_cascade(G, seeds, steps=2)
      for layer in A:
        n_A += len(layer)
    assert_almost_equal(n_A / run_times, 2.16, places=1)

    G = networkx.DiGraph()
    G.add_edges_from([(1,2), (1,3), (2,4), (3,4)], act_prob=0.4)
    n_A = 0.0
    A = [ ]
    for i in range(run_times):
      A = independent_cascade(G, seeds)
      for layer in A:
        n_A += len(layer)
    assert_almost_equal(n_A / run_times, 2.09, places=1)

def test_independent_cascade_without_attribute(G):

    n_A = 0.0
    A = [ ]
    for i in range(run_times):
      A = independent_cascade(G, [1], steps=1)
      for layer in A:
        n_A += len(layer)
    assert_almost_equal(n_A / run_times, 1.2, places=1)



