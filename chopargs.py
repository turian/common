"""
Module for chopping args into tuples of particular lengths.
"""

def chopargs(args, lengths):
    """
    Chopping args into tuples of particular lengths.
    If a tuple has length "0", return a single item.

    >>> chopargs(range(7), (0,3,1,2))
    [0, (1, 2, 3), (4,), (5, 6)]
    """
    r = []
    idx = 0
    for l in lengths:
        if l == 0:
            r.append(args[idx])
        else:
            r.append(tuple(args[idx:idx+l]))
        idx += l
    assert idx == len(args)
    assert len(r) == len(lengths)
    return r
