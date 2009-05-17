"""
Numpy help.
"""

def to_vector(v):
    """
    Take a matrix with one row, and convert it to a vector.
    Or, if it is a vector, leave it unchanged.
    Regardless, we call the .todense() method if it exists.
    @note: This operation is destructive (I think).
    @note: Reshape is better than resize.
    """
    if "todense" in dir(v):
        v = v.todense()
    if len(v.shape) == 2:
        assert v.shape[0] == 1
        v.resize(v.size)
    assert len(v.shape) == 1
    return v

def batch_apply(f, x, batchsize=1024, verbose=True):
    """
    Slice x in batches of size batchsize, run f on x, and return a list of results.
    @warning: The function should *NOT* return any indexes because f receives
    index numbers that are wrong. (The indexes should adjust for the current min.)
    """
    import sys
    from common.stats import stats

    ret = []
    min = 0
    max = batchsize
    while min < x.shape[0]:
        if max > x.shape[0]: max = x.shape[0]
        if verbose:
            print >> sys.stderr, "Running on %d:%d..." % (min, max)
            print >> sys.stderr, stats()

        tmpx = x[min:max]
        ret.append(f(tmpx))
        min += batchsize
        max += batchsize

    return ret
