"""
Mongo Database of documents.
"""

import logging
from common.str import percent
from common.stats import stats

import sys
import os.path
try:
    import lucene
except:
    print >> sys.stderr, "Could not import lucene"

from common.movingaverage import MovingAverage
import common.mylucene

_connection = None
_collection = {}
_db = {}

def collection(DATABASE, name="documents", HOSTNAME=None, PORT=None):
    """
    Return a database collection (MongoDB Collection).
    """
    global _collection
    if DATABASE not in _collection: _collection[DATABASE] = {}
    if name not in _collection[DATABASE]: _collection[DATABASE][name] = db(DATABASE, HOSTNAME=HOSTNAME, PORT=PORT)[name]
    return _collection[DATABASE][name]

def db(DATABASE, HOSTNAME=None, PORT=None):
    global _db
    if DATABASE not in _db:
        # Open the collection, since it is not yet open.
        _db[DATABASE] = connection(HOSTNAME, PORT)[DATABASE]
    assert DATABASE in _db
    return _db[DATABASE]

def connection(HOSTNAME=None, PORT=None):
    global _connection
    if _connection is None:
    # TODO: one connection per HOSTNAME, PORT
        from pymongo.connection import Connection
        # Each of these are equivalent, the first two make use of default arguments.
        if HOSTNAME is None:
            assert PORT is None
            _connection = Connection()
        else:
            _connection = Connection(HOSTNAME, PORT)
    assert _connection is not None
    return _connection

def findall_with_field(collection, field, title="", logevery=1000, timeout=False):
    """
    Find all documents that have some field.
    """
    for doc in findall(collection, spec={field: {"$exists": True}}, matchfn_description="Document contains field %s" % repr(field), title=title, logevery=logevery, timeout=timeout):
        yield doc

def findall(collection, spec=None, matchfn=lambda doc: True, matchfn_description="match", title="", logevery=1000, timeout=False):
    """
    Iterate over a document collection, and yield all documents for which matchfn(doc) is true AND that match spec.
    NB: Spec is faster than matchfn, because it is run server-side.
    Periodically output statistics about how many match, using matchfn_description (a plural verb, e.g. "match")
    """
    matchcnt = MovingAverage()
    from common.defaultdict import defaultdict
    for i, doc in enumerate(collection.find(spec=spec, timeout=timeout)):
        if i % logevery == 0 and i > 0 and i <= collection.count():
            logging.info("%s Done with %s of documents, %s of documents %s" % (title, percent(i, collection.count()), matchcnt, matchfn_description))
            logging.info(stats())

        if not matchfn(doc):
            matchcnt.add(0)
            continue
        else:
            matchcnt.add(1)

        yield doc

    logging.info("DONE iterating and matching documents that %s" % matchfn_description)
    logging.info(stats())

def to_lucene(collection, store_fields, content_field, lucene_dir, matchfn=lambda doc: True, matchfn_description="match", title="", logevery=1000, timeout=False):
    """
    Convert a MongoDB to Lucene, running findall over the collection.
    A field called "content" is created.
    store_fields: list. store, don't index, this field.
    content_field: string. index, don't store, this field.
    TODO: Don't assume we convert Lucene "id" into an *INT* MongoDB "_id" ?
    """
    print >> sys.stderr, "Storing lucene directory in: %s" % lucene_dir

    if not os.path.exists(lucene_dir):
        os.mkdir(lucene_dir)
    store = lucene.FSDirectory.getDirectory(lucene_dir, True)
    analyzer = lucene.StandardAnalyzer()
    writer = lucene.IndexWriter(store, analyzer, True)
    writer.setMaxFieldLength(1048576)

    assert "content" not in store_fields
    for i, origdoc in enumerate(findall(collection, matchfn, matchfn_description, title, logevery, timeout)):
        doc = lucene.Document()

        # Add the Mongo "_id" as the Lucene "id", but we assume this is an int.
        assert isinstance(origdoc["_id"], int)
        value = origdoc["_id"]
        if not isinstance(value, str):
            value = `value`
        doc.add(lucene.Field("id", value,
                                 lucene.Field.Store.YES,
                                 lucene.Field.Index.UN_TOKENIZED))

        for f in store_fields:
            value = origdoc[f]
            if not isinstance(value, str):
                value = `value`
            doc.add(lucene.Field(f, value,
                                 lucene.Field.Store.YES,
                                 lucene.Field.Index.UN_TOKENIZED))

        if content_field in origdoc:
            content = origdoc[content_field]
            doc.add(lucene.Field("content", content,
                                 lucene.Field.Store.YES,
                                 lucene.Field.Index.TOKENIZED))
        writer.addDocument(doc)

        if (i+1) % 1000 == 0:
            print >> sys.stderr, "Inserted %d docs into lucene, which now has %d documents" % (i+1, writer.docCount())
            print >> sys.stderr, stats()

    print >> sys.stderr, "Done inserting %d docs into lucene, which now has %d documents" % (i+1, writer.docCount())
    print >> sys.stderr, stats()
    print >> sys.stderr, 'optimizing index',
    writer.optimize()
    writer.close()
    print >> sys.stderr, 'done'

def search_lucene(querytext, mongodb_collection):
    """
    Search Lucene, and key the ids against the MongoDB.
    Yield a list of (score, mongodoc).
    TODO: Don't assume we convert Lucene "id" into an *INT* MongoDB "_id" ?
    """
    query = lucene.QueryParser("content", common.mylucene.analyzer).parse(querytext)
    hits = common.mylucene.searcher.search(query)
    print >> sys.stderr, "%s total matching documents for query %s" % (hits.length(), query)

    if len(hits) > 0:
        for i, hit in enumerate(hits):
            hit = lucene.Hit.cast_(hit)
#            print hit.getScore()
            doc = hit.getDocument()

            mongodoc = mongodb_collection.find_one({"_id": int(doc.get("id"))})
            assert mongodoc is not None
            yield hit.getScore(), mongodoc
