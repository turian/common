
import scipy
if scipy.__version__ != "0.7.0":
    import sys
    print >> sys.stderr, "WARNING! scipy < 0.7 has BUGGY sparse implementation. Your version =", scipy.__version__
from scipy.sparse import *

