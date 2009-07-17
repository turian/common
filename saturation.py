"""
Check neural net units for saturation.
"""

def stats(presquash, MAX=3):
    import numpy
    """
    Given a 2-D numpy array of presquash values, (examples, units),
    convert to absolute values, and return:
        * The median value over units of the median value over all examples.
        * The top 3 values over units of the top value over all examples.
    """
    assert presquash.ndim == 2
    abs_presquash = numpy.abs(presquash)
    med = numpy.median(numpy.median(abs_presquash, axis=0))
    abs_presquash = abs_presquash.max(axis=0)
    abs_presquash = abs_presquash.tolist()
    abs_presquash.sort()
    abs_presquash.reverse()
    return med, abs_presquash[:MAX]

"""
The following old code is for the 1-D case:
        (score, prehidden) = m.verbose_predict(ve)
        abs_prehidden = numpy.abs(prehidden)
        med = numpy.median(abs_prehidden)
        abs_prehidden = abs_prehidden.tolist()
        assert len(abs_prehidden) == 1
        abs_prehidden = abs_prehidden[0]
        abs_prehidden.sort()
        abs_prehidden.reverse()
        print >> sys.stderr, cnt, "AbsPrehidden median =", med, "max =", abs_prehidden[:5]
        if i > 5: break
"""
