"""
Feature mapping.

A feature map is identified by a unique name, e.g. "parsing features, experiment 35".
This unique name also determines the name of the on-disk version of the feature map.

@todo: This should be rewritten to be more Pythonic. Perhaps use a class?
@todo: Maybe look at older C++ Id/Vocab code? Id could have a __str__ method
@todo: Clearer documentation.
@todo: Create an fmap directory
@todo: Use cPickle, not pickle

@todo: Autosynchronize mode: Each time a new entry is added
to a L{FeatureMap}, the on-disk version of the feature map is
updated. Alternately, synchronize to disk when the object is destroyed.
"""

from common.file import myopen
import pickle
import sys

# We want this map to be a singleton
name_to_fmap = {}

def get(name=None, synchronize=True):
    """
    Get the L{FeatureMap} for a particular feature name.
    """
    global name_to_fmap
    if name not in name_to_fmap:
        # Create a new L{FeatureMap}
        name_to_fmap[name] = FeatureMap(name, synchronize)
    fmap = name_to_fmap[name]
    assert fmap.name == name
    assert fmap.synchronize == synchronize
    return fmap

def free_memory():
    """
    Free the memory associated with all feature maps.
    """
    global name_to_fmap
    name_to_fmap = {}

class KeyError(Exception):
    """Exception raised for keys missing from a readonly FeatureMap
    Attributes:
        name -- Name of the FeatureMap raising the error.
        key -- Key not present.
    """
    def __init__(self, name, key):
        self.name = name
        self.key = key


class FeatureMap:
    """
    Map from a feature string to a numerial ID (starting from 0).
    
    If synchronize is False, the feature map is considered temporary
    and we never actually synchronize it with disk. It expires with the
    lifetime of this execution.

    @warning: Do not construct this directly. Instead, use the global get() method.
    @todo: More documentation
    """

#    name = None
#    synchronize = True
#    map = {}
#    readonly = False        # If True, then each time we look for an ID
                            # that is not present we throw a ValueError
    def __init__(self, name=None, synchronize=True):
        self.name = name
        self.synchronize = synchronize
        self.map = {}
        self.reverse_map = {}
        self.readonly = False

        # There must be a name provided, or we cannot perform synchronization
        assert self.name or not self.synchronize

        if self.synchronize:
            # Try loading map from disk
            self.load()

    def exists(self, str):
        """ Return True iff this str is in the map """
        return str in self.map

    def id(self, str, can_add=False):
        """
        Get the ID for this string.
        @param can_add: Add a new ID if not is available.
        @todo: Don't want to synchronize every add, this may be too slow.
        """
        if can_add and str not in self.map:
            if self.readonly: raise KeyError(self.name, str)
            l = self.len
            self.map[str] = l
            self.reverse_map[l] = str
            assert l+1 == self.len
            return l
        else: return self.map[str]

    def str(self, id):
        """ Get the string for this ID. """
        return self.reverse_map[id]

    # This next function should just convert a list to a list
#    def ids(self, lst):
#        """ Get the IDs for the elements of a list. Return the ID numbers of these keys as a map. """
#        idset = {}
#        for k in lst:
#            try:
#                idset[self.id(k)] = True
#            except KeyError, e:
#                print "Feature map '%s' does not contain key '%s'. Skipping..." % (e.name, e.key)
#        return idset

    len = property(lambda self: len(self.map), doc="Number of different feature IDs")
    filename = property(lambda self: "fmap.%s.pkl.gz" % self.name, doc="The on-disk file synchronized to this feature map.")

    def load(self):
        """ Load the map from disk. """
        assert self.synchronize
        try:
            f = myopen(self.filename, "rb")
            (self.map, self.reverse_map) = pickle.load(f)
        except IOError: sys.stderr.write("Could not load from %s\n" % self.filename)

    def dump(self):
        """ Dump the map to disk. """
        assert self.synchronize
        f = myopen(self.filename, "wb")
        pickle.dump((self.map, self.reverse_map), f)
