def vars(module, regex="^[A-Za-z]"):
    """
    Dump the variables in a module.
    I use this to dump the hyperparameters, for logging.
    @todo: Use inspect module?
    """
    import re
    varre = re.compile(regex)
    for var in module.__dict__:
        if varre.match(var[0]): print ("%s.%s" % (module.__name__, var)).ljust(50), "=", module.__dict__[var]
