"""
Dict helper functions.
"""

def sort(d, increasing=False):
    """
    Sort a dict in decreasing order.
    """
    d = [(d[k], k) for k in d]
    d.sort()
    if not increasing: d.reverse()
    return d
