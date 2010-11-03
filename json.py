"""
JSON convenience routines.
"""

import simplejson

loads = simplejson.loads
dumps = simplejson.dumps
load = simplejson.load
dump = simplejson.dump

from common.file import myopen
def loadfile(filename):
    """
    Load JSON from a filename.
    """
    return load(myopen(filename))
def dumpfile(object, filename, **kwargs):
    """
    Dump JSON to a filename.
    """
    return dump(object, myopen(filename, "wb"), **kwargs)

try:
    import jsonlib
    def fastloads(str): return jsonlib.read(str, use_float=True)
    fastdumps = jsonlib.write
    def fastloadfile(filename): return jsonlib.read(myopen(filename).read(), use_float=True)
    def fastload(file): return jsonlib.read(file.read(), use_float=True)
except:
    pass
