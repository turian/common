"""
Command-line options.
"""

def reparse(values, parser=None):
    """
    Given a dict of values, construct an OptionParser and attempt to
    override its values with any command-line arguments.
    We return the overriden dictionary.
    We also return a string contain all keys and their values that were overriden.

    If parser is given, we use the values in it but update using value.
    @warning: We potentially clobber existing values in parser.

    Here is a common usage:
        import common.hyperparameters, common.options
        HYPERPARAMETERS = common.hyperparameters.read("sparse_input")
        HYPERPARAMETERS, options, args, newkeystr = common.options.reparse(HYPERPARAMETERS)
    """
    if parser is None:
        from optparse import OptionParser
        parser = OptionParser()
    assert parser is not None

    import re
    wsre = re.compile("\s+")

    # We don't want hyperparameters to be read more than once before
    # reparsing them. Otherwise, other modules that read the
    # hyperparameters could have stale values.
    if "__suffix" in values:
        import common.hyperparameters
        assert common.hyperparameters._readcount[values["__suffix"]] == 1

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
#    newkeys = {}
    newkeystr = ""
    for newkey in newkey_to_key:
        key = newkey_to_key[newkey]
        newvalue = getattr(options, key)
        if newvalue != values[key]:
            print >> sys.stderr, "common.options.reparse: %s %s => %s" % (key, values[key], newvalue)
            values[key] = newvalue
            newkeystr += ".%s=%s" % (key, newvalue)
#            newkeys[key] = True

    return values, options, args, newkeystr
