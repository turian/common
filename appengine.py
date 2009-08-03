"""
Helper functions for app engine.
"""

from google.appengine.ext import db
import sys

BATCH_SIZE = 500
def delete_entire_model(model):
    """
    Delete all entries from a model.
    """
    keys = model.all(keys_only=True).fetch(BATCH_SIZE)
    start = 0
    print >> sys.stderr, "Deleting %d-%d entities from %s..." % (start, start+len(keys), model)
    while len(keys) > 0:
        start += len(keys)
        db.delete(keys)
        keys = model.all(keys_only=True).fetch(BATCH_SIZE)
        print >> sys.stderr, "Deleting %d-%d entities from %s..." % (start, start+len(keys), model)
    return True


def key_to_path(key):
    """
    Convert a key to a path.
    Code from David Wilson: http://osdir.com/ml/GoogleAppEngine/2009-05/msg01182.html
    """
    output = []
    while key:
        name = key.name()
        if name is None:
            assert key.has_id_or_name()
            output.append(key.id_or_name())
        else:
            output.append(name)
        output.append(key.kind())
        key = key.parent()

    output.reverse()
    return output
