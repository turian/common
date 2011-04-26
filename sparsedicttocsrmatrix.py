"""
Convert a sparse dict feature to a scipy.sparse.csr_matrix.
"""

import common.idmap
import scipy.sparse
import numpy

import logging
import common.str

class SparseDictToCSRMatrix:
    def __init__(self):
        return
    def train(self, features, mincount=None):
#        print features
        if mincount is None:
            keys = set()
            for f in features:
                keys.update(f.keys())
        else:
            keycnt = defaultdict(int)
            for fvec in features:
                for f in fvec:
                    keycnt[f] += 1
            tot = 0
            for f in keycnt.keys():
                if keycnt[f] < mincount:
                    del keycnt[f]
            print >> sys.stderr, "SparseDictToCSRMatrix.train kept %s features with mincount threshold %d" % (common.str.percent(len(keycnt), tot), mincount)
            keys = keycnt.keys()
        self.idmap = common.idmap.IDmap(keys)
        return self.__call__(features)

    def __call__(self, features):
        data = []
        row = []
        col = []
        for k, f in enumerate(features):
            keyvalues = []
            for key in f:
                if not self.idmap.exists(key):
                    logging.debug("KEY %s does not exist" % key)
                    continue
                keyvalues.append((self.idmap.id(key), f[key]))
            keyvalues.sort()
            for key, value in keyvalues:
                data.append(value)
                row.append(k)
                col.append(key)
        return scipy.sparse.csr_matrix((data, (row, col)), shape=(len(features), self.idmap.len))
