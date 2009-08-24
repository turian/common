"""
Dict helper functions.
"""

def sort(d, increasing=False):
    """
    Sort a dict in decreasing order.
    @note: this function might have sideeffects
    """
    d = [(d[k], k) for k in d]
    d.sort()
    if not increasing: d.reverse()
    return d

def threshold(dict, min):
    """
    Remove from dict all keys less than this value, and return it.
    @note: this function might have sideeffects
    """
    keys = dict.keys()
    for k in keys:
        if dict[k] < min: del dict[k]
    return dict
