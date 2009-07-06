"""
Dump job options and parameters to RUNDIR-hash/parameters.txt
@todo: Make this cleaner.
@todo: Allow user to choose dump file.
"""

import myyaml

def create_canonical_directory(*vars):
    """
    For these variables, create a canonical directory to hold this run's output.
    Write the module values to 'LOGS.NOBACKUP/run-HASH/jobparameters.yaml'
    @note: Directory is a hash for right now.
    @todo: Make the directory name as human-readable as possible, maybe
    with optional human-readable parameters in the name.
    """
    import sys, os, os.path, hashlib
    s = myyaml.dump(vars)
    d = "LOGS.NOBACKUP/run-%s" % hashlib.sha224(s).hexdigest()
    sys.stderr.write("common.dump.create_canonical_directory: Opening canonical directory: %s\n" % d)
    sys.stderr.write("common.dump.create_canonical_directory: for following values\n%s\n" % s)
    if not os.path.exists(d): os.mkdir(d)
    assert os.path.exists(d)
    params = os.path.join(d, "jobparameters.yaml")
    if not os.path.exists(params): open(params, "wt").write(s)
    assert open(params, "rt").read() == s
    return d

def load_canonical_directory(d):
    """
    Open this run directory, and return a YAML string containing those parameters.

    Common usage:
        import common.dump, yaml
        parameters = common.dump.load_canonical_directory(options.modeldir)
        import common.hyperparameters
        common.hyperparameters.set(parameters, "attardi07_english_ptb")
    """
    import os.path
    assert os.path.exists(d)
    params = os.path.join(d, "jobparameters.yaml")
    assert os.path.exists(params)
    return open(params, "rt").read()

from types import *
def vars(module, regex="^[A-Za-z]"):
    """
    Get the variables in a module, and insert them as elements in a dict.
    I use this to dump the hyperparameters, for logging.
    @todo: Use inspect module?

    @note: Loading this may be a total PITA.
[17:46] <twas> In a human readable format
[17:46] <twas>     for var in module.__dict__:
[17:46] <twas>         if varre.match(var[0]): s += "%s %s %s\n" % (("%s.%s" % (module.__name__, var)).ljust(50), "=", module.__dict__[var])
[17:46] <twas> is what I am doing currently
[17:46] <nosklo> argh
[17:46] <ironfroggy_> why
[17:46] * nosklo throws up.
[17:46] <nosklo> my stomach is very sensible today
[17:47] <eggy_> twas: "%r" (and some other... adjustments)
[17:47] <Crys_> I've seen worse code ...
[17:47] <Crys_> twas: for a
[17:47] <-- joedj has left this server (Read error: 110 (Connection timed out)).
[17:47] <Sonderblade> well it looks safe to me if you pass eval the globals and locals arguments
[17:47] <Crys_> twas: for name, value in vars(module).iteritems(): ...
[17:47] <-- Kaedenn has left this server ("Black holes are nothing more than gigantic galactic segfaults.").
[17:48] <hiptobecubic> does anyone know how to tell pynotify to use a specific dbus session bus? I have a script that runs as root but needs to make user notifications
[17:48] <arkanes> if you're serious about doing this, using a more explicit mechanism to save, use, and restore your computation state would be a good idea
[17:48] <arkanes> especially if you ever need to control or version this state
[17:48] <-- radarek has left this server ("Leaving").
[17:48] <-- TDT has left this server ("leaving").
[17:48] <-- kov has left this server ("Ex-Chat").
[17:48] <nosklo> twas, if you want to keep with this, write the repr() of the variable instead, that will keep quotes right.
[17:49] <twas> Okay
[17:49] <twas> I am willing to rethink the entire design
[17:49] <nosklo> twas, but it is better to look at a serialization format, and maybe not store those variables in the module in first place
[17:49] <Crys_> arkanes: We have released another weapon against threads today. :]
[17:49] <nosklo> twas, wow! great idea!!!
[17:49] <twas> Because this is turning into a major PITA for me.
[17:49] <ironfroggy_> Crys_: oh?
[17:49] <nosklo> twas, maybe some config file
[17:49] <Crys_> Jesse, Skip and I have ported the multiprocessing module to 2.4 and 2.5.
[17:49] <nosklo> twas: http://docs.python.org/library/configparser.html
[17:49] <arkanes> twas: the way you're doing it is pretty much doomed to be a PITA
    """
    import re
    d = {}
#    s = ""
#    for name, value in vars(module).iteritems():
#        s += "%s %s %r\n" % (("%s.%s" % (module.__name__, name)).ljust(50), "=", value)
    varre = re.compile(regex)
    for var in module.__dict__:
        value = module.__dict__[var]
        if type(value) in [FunctionType, ModuleType]: continue
        if varre.match(var[0]):
            d[var] = value
#           s += "%s %s %r\n" % (("%s.%s" % (module.__name__, var)).ljust(50), "=", value)
#    if s != "":
#        s = "import %s\n" % module.__name__ + s
#    return s
    return d

def vars_seq(modules, regex="^[A-Za-z]"):
    """
    Dump the variables in several modules into a dict.
    I use this to dump the hyperparameters, for logging.
    @todo: Use inspect module?
    """
#    s = ""
#    for m in modules:
#        s += vars(m, regex)
#    return s
    d = {}
    for m in modules:
        d[m.__name__] = vars(m, regex)
    return d
