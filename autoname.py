import sys
from theano import gof


class Graph:
    def __init__(self, table):
        for name, r in table.iteritems():
            if isinstance(r, gof.Result):
                if not r.name:
                    r.name = name
            setattr(self, name, r)


def theanify(function):
    """ 
    Decorator that puts all the locals of the function to which it is
    applied in a Graph (that sets the name fields of the Results to
    the name of the local variables which contain them)

    Returns the Graph object.
    """

    def exec_probe(function, args, kwargs):
        func_locals = {}
        n = []
        def probe_func(frame, event, arg):            
            if event == 'call':
                if n:
                    return None
                else:
                    n.append(None)
                    return probe_func
            if event == 'return':
                locals = frame.f_locals
                func_locals.update(locals)
                sys.settrace(None)
            return probe_func
        sys.settrace(probe_func)
        function(*args, **kwargs)
        return Graph(func_locals)

    def newf(*args, **kwargs):
        return exec_probe(function, args, kwargs)

    return newf


class AutoName(object):
    """
    By inheriting from this class, class variables which have a name attribute
    will have that name attribute set to the class variable name.
    """
    class __metaclass__(type):
         def __init__(cls, name, bases, dct):
             type.__init__(name, bases, dct)
             for key, val in dct.items():
                 assert type(key) is str
                 if hasattr(val, 'name'): 
                     val.name = key

def name_variables(dict, prefix=None):
    '''L{dict} is a dictionnary containing objects, indexed by the name
    of the corresponding variable. This method fills the 'name' field of
    every object, with the corresponding key.
    If L{prefix} is a string, it will append it in front of every key.
    Usually called by: "name_variables(local())'''
    # Name objects after their variable name
    if isinstance(prefix, str):
        prefix = '%s.' % prefix
    else:
        prefix = ''
    for key, val in dict.items():
        assert type(key) is str
        if hasattr(val, 'name') and val.name is None:
            val.name = prefix + key

def set_fields(obj, dict):
    '''Exports a dictionary into an object's variables namespace.
    Usually called by: "set_fields(self, locals())'''
    for key, val in dict.items():
        assert type(key) is str
        if key != 'self':
            setattr(obj, key, val)

