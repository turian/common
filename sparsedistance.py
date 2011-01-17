

def sqrerr(repr1, repr2):
    """
    Compute the sqrerr between two reprs.
    The reprs are each a dict from feature to feature value.
    """
    keys = frozenset(repr1.keys() + repr2.keys())
    sqrerr = 0.
    for k in keys:
        diff = repr1.get(k, 0.) - repr2.get(k, 0.)
        sqrerr += diff * diff
    return sqrerr
