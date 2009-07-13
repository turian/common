"""
Module for reading hyperparameters.

@warning: Want to make HYPERPARAMETERS read-only after someone accesses
values in it. Otherwise, one module could call hyperparameters.read()
and use HYPERPARAMETERS values, then another module could call 
options.reparse(hyperparameters) and change the HYPERPARAMETERS.
However, this protecton is not yet offered.

@todo: Maybe ensure that script locations are executable.
"""

import sys, yaml

_HYPERPARAMETERS = {}
from collections import defaultdict
_readcount = defaultdict(int)

def read(suffix=None):
    """
    suffix is the name of these hyperparameters, e.g. "nlpreprocess"
    for the "hyperparameters.nlpreprocess.yaml" file.

    Each time we read a set of hyperparameters, we increment
    _readcount[suffix].
    """
    global _HYPERPARAMETERS

    _readcount[suffix] += 1
    if suffix in _HYPERPARAMETERS:
        return _HYPERPARAMETERS[suffix]
    print >> sys.stderr, "Reading hyperparameters for suffix", suffix

    import common.file, os.path
    if suffix: f = "hyperparameters.%s.yaml" % suffix
    else: f = "hyperparameters.yaml" % suffix
    __file = common.file.ascend_find(f)
    h = yaml.load(open(__file).read())
    if os.path.realpath(__file) != __file:
        print >> sys.stderr, "NOTE: os.path.realpath(%s) = %s" % (__file, os.path.realpath(__file))
    h["basedir"] = os.path.dirname(os.path.realpath(__file))
    
    # Prepend basedir to all relative locations
    if "locations" not in h: h["locations"] = {}
    if "relative locations" in h:
        for l in h["relative locations"]:
            h["locations"][l] = os.path.join(h["basedir"], h["relative locations"][l])
        # Now delete relative locations, since we only care about the absolute ones
        del h["relative locations"]
    
    # Expand ~ and check if locations exist
    for l in h["locations"]:
        h["locations"][l] = os.path.expanduser(h["locations"][l])
        loc = h["locations"][l]
        if not os.path.exists(loc):
            print >> sys.stderr, "WARNING . Location for %s does not exist: %s" % (`l`, loc)
    
    # Prepend work dir to all work locations
    if "work locations" in h:
        for l in h["work locations"]:
            h["locations"][l] = os.path.join(h["locations"]["work dir"], h["work locations"][l])
        # Now delete relative locations, since we only care about the absolute ones
        del h["work locations"]
    
#    print >> sys.stderr, "# BEGIN %s HYPERPARAMETERS" % suffix
#    print >> sys.stderr, yaml.dump({suffix: h}),
#    print >> sys.stderr, "# END %s HYPERPARAMETERS" % suffix

    _HYPERPARAMETERS[suffix] = h
    _HYPERPARAMETERS[suffix]["__suffix"] = suffix
    return _HYPERPARAMETERS[suffix]

def set(yamlparams, suffix=None):
    """
    Set the hyperparameters for a particular suffix, using these YAML values.
    """
    global _HYPERPARAMETERS
    print >> sys.stderr, "Setting hyperparameters for suffix", suffix
    assert suffix not in _HYPERPARAMETERS
    params = yaml.load(yamlparams)

    assert len(params) == 1     # WHY IS THIS NECESSARY?
    params = params[0]

    _HYPERPARAMETERS[suffix] = params
