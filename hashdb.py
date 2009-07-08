"""
Wrapper for hash database functions.
Uses Tokyo Cabinet hashdb.

@note This code is part of Joseph Turian's common python library.
Please contact him if you would like him to share the rest of the library.
"""

from pytc import HDB, HDBOWRITER, HDBOCREAT, HDBTBZIP, HDBOREADER
#from tc import HDB, HDBOWRITER, HDBOCREAT, HDBTBZIP, HDBOREADER
import os.path
import common.json
import common.retry

class JSONHDB(HDB):
    """
    A hashdb wrapper, which automatically converts values to- and from- JSON.
    """
    def __getitem__(self, key):
        return common.json.loads(HDB.__getitem__(self, key))
    def __setitem__(self, key, value):
        return HDB.__setitem__(self, key, common.json.dumps(value))
    def get(self, key):
        return common.json.loads(HDB.get(self, key))
    def put(self, key, value):
        return HDB.put(self, key, common.json.dumps(value))
    def values(self):
        return [common.json.loads(v) for v in HDB.values(self)]
    def random_key(self):
        import random
        return random.choice(self.keys())
    def close(self):
        return HDB.close(self)

def tune(hdb):
    """
    @todo: Unfortunately, the current pytc.hdb.tune doesn't contain
    default arguments.
    """
    #     bnum - the number of elements of the bucket array. If it is
    #     not more than 0, the default value is specified. The default value
    #     is 131071. Suggested size of the bucket array is about from 0.5
    #     to 4 times of the number of all records to be stored.
    #     apow - the size of record alignment by power of 2. If it is
    #       negative, the default value is specified. The default value is
    #       4 standing for 2^4=16.
    #     fpow - the maximum number of elements of the free block pool
    #       by power of 2. If it is negative, the default value is
    #       specified. The default value is 10 standing for 2^10=1024.
    hdb.tune(bnum=131071, apow=4, fpow=10, opts=HDBTBZIP)
    #hdb.tune(bnum=131071, apow=4, fpow=10, opts=0)

def write_open(filename):
    """
    Open a hashdb with this filename for writing.
    """
    hdb = JSONHDB()
    tune(hdb)
    hdb.open(filename, HDBOCREAT | HDBOWRITER)
    return hdb

def create(filename):
    """
    Create a hashdb with this filename.
    Abort if this file already exists.
    """
    assert not os.path.exists(filename)
    return write_open(filename)

def read_open(filename):
    """
    Open a hashdb with this filename for writing.
    """
    hdb = JSONHDB()
    def hdbopen():
        hdb.open(filename, HDBOREADER)
    common.retry.retry(hdbopen, "Could not HDB open %s" % filename)
    return hdb

def read(filename):
    """
    A generator that iterates over the (key, value) pairs in the TCH in filename.
    We assume that each value is a JSON object.
    @todo: Is there a better way to traverse all pairs?
    """
    hdb = read_open(filename) 
    # traverse records
    hdb.iterinit()
    for key in hdb.keys():
        value = hdb.get(key)
        yield (key, value)
    hdb.close()
