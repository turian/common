#!/usr/bin/python
"""
This Box-Muller code for obtaining Normal random variables is based upon
code from
    http://www.mas.ncl.ac.uk/~ndjw1/teaching/sim/transf/norm.py 
by Darren Wilkinson.

Box-Muller was recommended by Ian Goodfellow:
    http://metaoptimize.com/qa/questions/37/how-do-i-deterministically-transform-an-integer-to-a-standard-normal-gaussian-distribution-value
"""

import math
import deterministicrandom

def from_probability(x):
    """
    Deterministically convert x (each in range [0, 1)) to a single
    standard Normal value.
    We do this by deterministically picking an x2 uniformly in [0, 1)
    based upon x.
    """
    x2 = deterministicrandom.deterministicrandom(`x` + "-x2")
    return from_two_probabilities(x, x2)

def from_two_probabilities(x1, x2):
    """
    Deterministically convert x1 and x2 (each uniform in range [0, 1))
    to a single standard Normal value.
    """
    assert x1 >= 0 and x1 < 1
    assert x2 >= 0 and x2 < 1

    theta = x1*2*math.pi
    rsq = genexp(x2,0.5)
    y = math.sqrt(rsq)*math.cos(theta)
    return y

def genexp(u,lamb):
    x=(-1.0/lamb)*math.log(u)
    return x


if __name__ == "__main__":
    import random
    import numpy
    random.seed(0)
    array = [from_probability(random.random()) for i in range(1000)]
    print "mean (should be 0)=%f" % numpy.mean(array)
    print "stddev (should be 1)=%f" % numpy.std(array)
