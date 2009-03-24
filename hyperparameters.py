"""
Module for reading hyperparameters.

@todo: Maybe ensure that script locations are executable.
"""

_HYPERPARAMETERS = {}

def read(suffix=None):
    """
    suffix is the name of these hyperparameters, e.g. "nlpreprocess"
    for the "hyperparameters.nlpreprocess.yaml" file.
    """
    if suffix in _HYPERPARAMETERS: return _HYPERPARAMETERS[suffix]

    import common.file, os.path, yaml, sys
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
    
    print >> sys.stderr, "# BEGIN %s HYPERPARAMETERS" % suffix
    print >> sys.stderr, yaml.dump({suffix: h}),
    print >> sys.stderr, "# END %s HYPERPARAMETERS" % suffix

    _HYPERPARAMETERS[suffix] = h
    return _HYPERPARAMETERS[suffix]
