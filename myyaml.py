"""
Yaml wrappers.
@note: Not yet working.
"""

import yaml
import sys
try:
    sys.stderr.write("Sweet, we can use the libyaml C implementation.\n")
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    sys.stderr.write("WARNING: Could not load libyaml C implementation.\n")
    from yaml import Loader, Dumper

def dump(var):
    return yaml.dump(var, Dumper=Dumper)

#def load(*args, **kwargs):
#    return yaml.load(args, kwargs, Loader=Loader)

#def load_all(*args, **kwargs):
#    return yaml.load(args, kwargs, Loader=Loader)
#
#def dump(*args, **kwargs):
#    return yaml.dump(args, kwargs, Dumper=Dumper)
#
#def dump_all(*args, **kwargs):
#    return yaml.dump_all(args, kwargs, Dumper=Dumper)
