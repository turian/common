"""
Wrapper for hash database functions.
Uses Tokyo Cabinet hashdb.
"""

from pytc import HDB, HDBOWRITER, HDBOCREAT, HDBTBZIP, HDBOREADER
import os.path
import common.json

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

def create(filename):
    """
    Create a hashdb with this filename.
    Abort if this file already exists.
    """
    assert not os.path.exists(filename)
    hdb = JSONHDB()
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
    hdb.open(filename, HDBOCREAT | HDBOWRITER)
    return hdb

def read(filename):
    """
    A generator that iterates over the (key, value) pairs in the TCH in filename.
    We assume that each value is a JSON object.
    """
    hdb = JSONHDB()
    hdb.open(filename, HDBOREADER)
    
    # traverse records
    hdb.iterinit()
    for key in hdb.keys():
        value = hdb.get(key)
        yield (key, value)
    hdb.close()
