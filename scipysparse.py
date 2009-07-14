
import scipy
if scipy.__version__ != "0.7.0":
    import sys
    print >> sys.stderr, "WARNING! scipy < 0.7 has BUGGY sparse implementation. Your version =", scipy.__version__
from scipy.sparse import *

import sys
from common.stats import stats
import common.str

def threshold_csr(x, min):
    """
    Take x, convert it to a lil_matrix, remove all data less than min, and convert to a CSR matrix.
    """
    removed = 0
    tot = 0
    x = scipy.sparse.lil_matrix(x)
    print >> sys.stderr, "Applying threshold %.3f to %d rows\n\tCurrently %d nonzeros (%.3f nonzeros per row)..." % (min, x.shape[0], x.nnz, 1.*x.nnz/x.shape[0])
    print >> sys.stderr, stats()
    (row, col) = x.nonzero()
    for i, (r,c) in enumerate(zip(row.tolist(), col.tolist())):
        if x[r,c] < min:
            x[r,c] = 0
            removed += 1
        tot += 1
        if i % 100000 == 0:
            print >> sys.stderr, "\t%s nonzeros done" % common.str.percent(i, len(row))
            print >> sys.stderr, stats()
    x = scipy.sparse.csr_matrix(x)
    x.eliminate_zeros()
    print >> sys.stderr, "..done applying threshold %.3f to %d rows\n\tCurrently %d nonzeros (%.3f nonzeros per row)..." % (min, x.shape[0], x.nnz, 1.*x.nnz/x.shape[0])
    print >> sys.stderr, "\t%s of entries were pruned\n" % common.str.percent(removed, tot)
    print >> sys.stderr, stats()
