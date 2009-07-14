
import scipy
if scipy.__version__ != "0.7.0":
    import sys
    print >> sys.stderr, "WARNING! scipy < 0.7 has BUGGY sparse implementation. Your version =", scipy.__version__
from scipy.sparse import *

import sys
from common.stats import stats
import common.str

def threshold(x, min):
    """
    Take x and remove all data less than min.
    """
    removed = 0
    tot = 0
    print >> sys.stderr, "Applying threshold %.3f to %d rows\nCurrently %d nonzeros (%.3f nonzeros per row)..." % (min, x.shape[0], x.nnz, 1.*x.nnz/x.shape[0])
    print >> sys.stderr, stats()
    for i in range(len(x.data)):
        if x.data[i] < min:
            x.data[i] = 0
            removed += 1
        tot += 1
        if (i+1) % 1000000 == 0:
            print >> sys.stderr, "\t%s nonzeros done" % common.str.percent(i+1, len(x.data))
            print >> sys.stderr, stats()
    x.eliminate_zeros()
    print >> sys.stderr, "..done applying threshold %.3f to %d rows\nCurrently %d nonzeros (%.3f nonzeros per row)..." % (min, x.shape[0], x.nnz, 1.*x.nnz/x.shape[0])
    print >> sys.stderr, "\t%s of entries were pruned\n" % common.str.percent(removed, tot)
    print >> sys.stderr, stats()
    return x
