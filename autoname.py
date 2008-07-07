

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

