"""
Command-line options.
"""

def reparse(values):
    """
    Given a dict of values, construct an OptionParser and attempt to
    override its values with any command-line arguments.
    We return the overriden dictionary.
    """
    from optparse import OptionParser
    parser = OptionParser()

    import re
    wsre = re.compile("\s+")

    newkey_to_key = {}
    for key in values:
        v = values[key]
        if type(v) == type("string"):
            ty = "string"
        elif type(v) == type(1.0):
            ty = "float"
        elif type(v) == type(1):
            ty = "int"
        elif type(v) == type(True):
            ty = "bool"
        else:
            import sys
            print >> sys.stderr, "common.options.reparse: Skipping %s, with type %s" % (key, type(v))
            continue
        newkey = wsre.sub("_", key)
        newkey_to_key[newkey] = key
        if ty != "bool":
            parser.add_option("--%s" % newkey, dest=key, default=v, action="store", type=ty)
        else:
            parser.add_option("--%s" % newkey, action="store_true", dest=key, default=v)
            parser.add_option("--no_%s" % newkey, action="store_false", dest=key, default=v)

    (options, args) = parser.parse_args()
    for newkey in newkey_to_key:
        key = newkey_to_key[newkey]
        newvalue = getattr(options, key)
        if newvalue != values[key]:
            print >> sys.stderr, "common.options.reparse: %s %s => %s" % (key, values[key], newvalue)
            values[key] = newvalue

    return values

