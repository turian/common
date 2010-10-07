#!/usr/bin/python
"""
Rough parser for bad XML into JSON.
We assume the outer container is OUTERLABEL and each inner document label is DOCLABEL
"""

OUTERLABEL = "newdataset"
DOCLABEL = "vw_incidentpipeline_report"

import sys
import re
opentag = re.compile("<([^\/>]*)>")
closetag = re.compile("<\/([^>]*)>")

from common.json import dump
from common.stats import stats
import string

docs = []
currentdoc = {}
curtag = ""
curval = ""

first = True

print "["
for l in sys.stdin:
    if opentag.search(l):
#        print "OPEN", l
        m = opentag.search(l)
        tag = m.group(1)
        if tag == OUTERLABEL:
            pass
        elif tag == DOCLABEL:
            pass
        else:
            curtag = tag
    elif closetag.search(l):
#        print "CLOSE", l
        m = closetag.search(l)
        tag = m.group(1)
        if tag == OUTERLABEL:
            pass
        elif tag == DOCLABEL:
            if len(currentdoc) > 0:
                if first:
                    first = False
                else:
                    print ","
                docs.append(currentdoc)
                dump(currentdoc, sys.stdout, indent=4)
            currentdoc = {}
        else:
            currentdoc[curtag] = string.strip(curval)
            curtag = ""
            curval = ""
    else:
        curval += l
print "]"
print >> sys.stderr, stats()
#dump(docs, sys.stdout)
