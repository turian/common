"""
JSON convenience routines.

We use python-cjson because it is far faster than simplejson on certain installs:
    http://blog.metaoptimize.com/2009/03/22/fast-deserialization-in-python/

Note that cjson 1.0.5 is buggy:
    http://blog.extracheese.org/2007/07/when-json-isnt-json.html
    http://www.vazor.com/cjson.html
"""

import cjson
if cjson.__version__ != "1.0.6":
    import sys
    print >> sys.stderr, "WARNING: cjson < 1.0.6 is buggy (your version=%s)" % cjson.__version__
    print >> sys.stderr, "    http://blog.extracheese.org/2007/07/when-json-isnt-json.html"
    print >> sys.stderr, "    http://www.vazor.com/cjson.html"

encode = cjson.encode
decode = cjson.decode

from common.file import myopen
def loadfile(filename):
    return decode(myopen(filename).read())
def dumpfile(filename, object):
    return myopen(file, "wb").write(encode(filename, object))
