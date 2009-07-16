"""
Module for chopping args into tuples of particular lengths.
"""

def chopargs(args, lengths):
    """
    Chopping args into tuples of particular lengths.

    >>> chopargs(range(7), (1,3,1,2))
    [0, (1, 2, 3), 4, (5, 6)]
    """
    r = []
    idx = 0
    for l in lengths:
        if l == 1:
            r.append(args[idx])
        else:
            r.append(tuple(args[idx:idx+l]))
        idx += l
    assert idx == len(args)
    assert len(r) == len(lengths)
    return r
