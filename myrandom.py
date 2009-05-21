"""
Random sampling routines.

Here is an example:

from common.myrandom import build, weighted_sample
keys = "ABC"
weights = [1., 3., 2.]
indexed_weights = build(weights)
print keys[weighted_sample(indexed_weights)]
print keys[weighted_sample(indexed_weights)]
"""

def build(weights):
    """
    Create an index of weights. Must be done prior to calling weighted_sample.
    """
    indexed_weights = []
    sum = 0.
    for w in weights:
        indexed_weights.append(sum)
        sum += w
    return ("indexed_weights", indexed_weights, sum)

def weighted_sample(indexed_weights):
    """
    Sample an index, according to the weights in indexed_weights.
    indexed_weights must be obtained from the build() functon.
    """
    assert len(indexed_weights) == 3 
    assert indexed_weights[0] == "indexed_weights"
    tot = indexed_weights[2]
    indexed_weights = indexed_weights[1]
    from bisect import bisect
    import random
    v = random.random()
    v *= tot
    idx = bisect(indexed_weights, v)
    idx -= 1
    assert idx >= 0 and idx < len(indexed_weights)
    return idx
