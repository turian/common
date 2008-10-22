def vars(module, regex="^[A-Za-z]"):
    """
    Dump the variables in a module.
    I use this to dump the hyperparameters, for logging.
    @todo: Use inspect module?
    """
    import re
    varre = re.compile(regex)
    s = ""
    for var in module.__dict__:
        if varre.match(var[0]): s += "%s %s %s\n" % (("%s.%s" % (module.__name__, var)).ljust(50), "=", module.__dict__[var])
    return s

def vars_seq(modules, regex="^[A-Za-z]"):
    """
    Dump the variables in several modules.
    I use this to dump the hyperparameters, for logging.
    @todo: Use inspect module?
    """
    s = ""
    for m in modules:
        s += vars(m, regex)
    return s

def open_canonical_directory(modules):
    """
    For these modules, create a canonical directory to hold this run's output.
    Write the module values to 'run-HASH/parameters.txt'
    @note: Directory is a hash for right now.
    @todo: Make the directory name as human-readable as possible, maybe
    with optional human-readable parameters in the name.
    """
    import sys, os, os.path, hashlib
    s = vars_seq(modules)
    d = "run-%s" % hashlib.sha224(s).hexdigest()
    sys.stderr.write("Opening canonical directory: %s\n" % d)
    if not os.path.exists(d): os.mkdir(d)
    assert os.path.exists(d)
    params = os.path.join(d, "parameters.txt")
    if not os.path.exists(params): open(params, "wt").write(s)
    assert open(params, "rt").read() == s
    return d
