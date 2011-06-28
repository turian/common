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
from common.str import percent

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

def loadoneperline(f, verbose=True):
    """
    Read a JSON file object, one JSON object per line, and return a
    dictionary containing everything.
    Useful for JSON files that are big and crash simplejson when then
    are loaded into memory.
    """
    obj = {}
    i = 0
    if verbose:
        print >> sys.stderr, "loadoneperline(%s)..." % f
        print >> sys.stderr, stats()
    for l in f:
        i += 1
        try:
            o = loads(l)
            assert len(o.keys()) == 1
            key = o.keys()[0]
            obj[key] = o[key]
        except:
            print >> sys.stderr, "Problem with:", l
        if i % 1000000 == 0:
            print >> sys.stderr, "\t...loadoneperline read %d lines..." % i
            print >> sys.stderr, "\t%s" % stats()
    if verbose:
        print >> sys.stderr, "...loadoneperline(%s)" % f
        print >> sys.stderr, stats()
    return obj


def dumponeperline(obj, f, verbose=True):
    """
    Write a JSON file object, one JSON object per line.
    Useful for JSON objects that are big and use a lot of memory when
    converted into strings.
    """
    if verbose:
        print >> sys.stderr, "dumponeperline(%s)..." % f
        print >> sys.stderr, stats()
    i = 0
    for k in obj:
        i += 1
        o = {k: obj[k]}
        # TODO: Make sure that dumps returns only one line?
        f.write(dumps(o) + "\n")

        if i % 1000000 == 0:
            print >> sys.stderr, "\t...dumponeperline wrote %s lines..." % percent(i, len(obj))
            print >> sys.stderr, "\t%s" % stats()
    if verbose:
        print >> sys.stderr, "...dumponeperline(%s)" % f
        print >> sys.stderr, stats()


try:
    import jsonlib
    def fastloads(str): return jsonlib.read(str, use_float=True)
    fastdumps = jsonlib.write
    def fastloadfile(filename): return jsonlib.read(myopen(filename).read(), use_float=True)
    def fastload(file): return jsonlib.read(file.read(), use_float=True)
except:
    pass
