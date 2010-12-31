"""
Read documents from Wackypedia.
"""

from common.file import myopen
from common.stats import stats
import common.str

import sys
import string
import re
import os.path
WACKYDIR = os.path.expanduser("~/data/wikipedia/wackypedia_en/")

WACKYFILES = ["wackypedia_en%d.gz" % i for i in range(1, 4+1)]

#titlere = "<text id=

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
    doc = []
    sentence = []
    for l in f:
#        l = l.decode('utf-8')
        if l[:5] == "<text":
#        <text id="wikipedia:Anarchism">
            doc = []
        elif l[:6] == "</text":
            yield doc
        elif l[:3] == "<s>":
            sentence = []
        elif l[:4] == "</s>":
            doc.append(string.join(sentence))
        else:
            (word, stem, a, b, c, d) = string.split(l)
            sentence.append(word)

if __name__ == "__main__":
    for i, d in enumerate(wackydocs()):
        if i % 10 == 0: print i, d
        if i > 100: break
#        print d
