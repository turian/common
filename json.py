"""
JSON convenience routines.
"""

import simplejson

loads = simplejson.loads
dumps = simplejson.dumps
load = simplejson.load
dump = simplejson.dump

from common.stats import stats
from common.file import myopen

import sys

def loadfile(filename, verbose=False):
    """
    Load JSON from a filename.
    """
    if verbose: print >> sys.stderr, "common.json.loadfile(%s)...\n%s" % (repr(filename), stats())
    object = load(myopen(filename))
    if verbose: print >> sys.stderr, "...common.json.loadfile(%s)\n%s" % (repr(filename), stats())
    return object
def dumpfile(object, filename, verbose=False, **kwargs):
    """
    Dump JSON to a filename.
    """
    if verbose: print >> sys.stderr, "common.json.dumpfile(object, %s)...\n%s" % (repr(filename), stats())
    r = dump(object, myopen(filename, "wb"), **kwargs)
    if verbose: print >> sys.stderr, "...common.json.dumpfile(object, %s)\n%s" % (repr(filename), stats())
    return r

try:
    import jsonlib
    def fastloads(str): return jsonlib.read(str, use_float=True)
    fastdumps = jsonlib.write
    def fastloadfile(filename): return jsonlib.read(myopen(filename).read(), use_float=True)
    def fastload(file): return jsonlib.read(file.read(), use_float=True)
except:
    pass
