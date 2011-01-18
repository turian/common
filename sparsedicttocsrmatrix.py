"""
Convert a sparse dict feature to a scipy.sparse.csr_matrix.
"""

import common.idmap

class SparseDictToCSRMatrix:
    def __init__(self):
        pass
    def train(features):
        keys = set()
        for f in features:
            keys.update(f.keys())
        print keys
