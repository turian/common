"""
Read documents from Wackypedia.
"""

from common.file import myopen
from common.stats import stats
import common.str
import common.json

#import xml.sax.saxutils

import sys
import string
import re
import os.path
WACKYDIR = os.path.expanduser("~/data/wikipedia/wackypedia_en/")
#WACKYDIR = os.path.expanduser("~/data/wikipedia/wackpedia-INCOMPLETE/")

WACKYFILES = ["wackypedia_en%d.gz" % i for i in range(1, 4+1)]

titlere = re.compile('<text id="wikipedia:([^">]*)">')

def wackydocs():
    """
    Read all Wackypedia docs. Yield a generator.
    Each doc is a list of sentence strings.
    """
    for i, fil in enumerate(WACKYFILES):
        print >> sys.stderr, "Reading wackypedia file %s %s..." % (fil, common.str.percent(i+1, len(WACKYFILES)))
        print >> sys.stderr, stats()
        for doc in wackydocs_in_file(fil):
            yield doc

def wackydocs_in_file(fil):
    f = myopen(os.path.join(WACKYDIR, fil))
    doc = {}
    sentence = []
    for l in f:
        l = l.decode('ISO-8859-2')
        if l[:5] == "<text":
            m = titlere.match(l)
            assert m
            doc = {}
            doc["title"] = m.group(1)
            doc["sentences"] = []
        elif l[:6] == "</text":
            yield doc
        elif l[:3] == "<s>":
            sentence = []
        elif l[:4] == "</s>":
            doc["sentences"].append(string.join(sentence))
        else:
            (word, stem, a, b, c, d) = string.split(l)
            sentence.append(word)

def load_into_mongodb(database="wackypedia_en", collection="wackypedia_en"):
    import common.mongodb
    collection = common.mongodb.collection(DATABASE=database, name=collection)
    for i, d in enumerate(wackydocs()):
        d["_id"] = d["title"]
        try:
            collection.insert(d)
        except Exception, e:
            print >> sys.stderr, "ERROR. Could not insert doc into mongodb: %s" % repr(d), type(e), e
        if (i+1) % 1000 == 0:
            print >> sys.stderr, "Extracted %d wackydocs, mongo collection has %d docs" % (i+1, collection.count())
            print >> sys.stderr, stats()

if __name__ == "__main__":
    load_into_mongodb()
#    for i, d in enumerate(wackydocs()):
#        if i % 10 == 0: print i, common.json.dumps(d)
##        if i > 100: break
#        print d
