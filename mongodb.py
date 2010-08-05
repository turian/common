"""
Mongo Database of documents.
"""

import logging
from common.str import percent
from common.stats import stats

from common.movingaverage import MovingAverage

_connection = None
_collection = {}
_db = {}

def collection(DATABASE, name="documents"):
    """
    Return a database collection (MongoDB Collection).
    """
    global _collection
    if DATABASE not in _collection: _collection[DATABASE] = {}
    if name not in _collection[DATABASE]: _collection[DATABASE][name] = db(DATABASE)[name]
    return _collection[DATABASE][name]

def db(DATABASE, HOSTNAME=None, PORT=None):
    global _connection, _db
    if DATABASE not in _db:
        # Open the collection, since it is not yet open.
    
        from pymongo.connection import Connection
        # Each of these are equivalent, the first two make use of default arguments.
        if HOSTNAME is None:
            assert PORT is None
            _connection = Connection()
        else:
            _connection = Connection(HOSTNAME, PORT)
        _db[DATABASE] = _connection[DATABASE]
    assert DATABASE in _db
    return _db[DATABASE]

def findall(DATABASE, matchfn, matchfn_description="match", title="", logevery=1000, timeout=False):
    """
    Iterate over the document collection, and yield all documents for which matchfn(doc) is true.
    Periodically output statistics about how many match, using matchfn_description (a plural verb, e.g. "match")
    """
    matchcnt = MovingAverage()
    from collections import defaultdict
    for i, doc in enumerate(collection(DATABASE).find(timeout=timeout)):
        if i % logevery == 0 and i > 0 and i <= collection(DATABASE).count():
            logging.info("%s Done with %s of documents, %s of documents %s" % (title, percent(i, collection(DATABASE).count()), matchcnt, matchfn_description))
            logging.info(stats())

        if not matchfn(doc):
            matchcnt.add(0)
            continue
        else:
            matchcnt.add(1)

        yield doc

    logging.info("DONE iterating and matching documents that %s" % matchfn_description)
    logging.info(stats())
