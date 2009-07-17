"""
Bidirectional map from object to unique ID.
Useful, for example, when making a map of feature names <=> IDs.
"""

class KeyError(Exception):
    """
    Exception raised for keys missing from a readonly FeatureMap
    Attributes:
        key -- Key not present.
    """
    def __init__(self, key):
        self.key = key

_unknown_key = "*UNKNOWN*"
class IDmap:
    """
    Map from an objection to a unique numerial ID.
    The IDs are sequential, starting from 0.
    If allow_unknown=True (False by default), then all unknown words get mapped
    to one OOV token id.
    """
    def __init__(self, keys, allow_unknown=False):
        self.allow_unknown = allow_unknown
        self.map = {}
        self.reverse_map = []
        if self.allow_unknown:
            assert _unknown_key not in keys
            self.map[_unknown_key] = len(self.reverse_map)
            self.reverse_map.append(_unknown_key)
            assert self.exists(_unknown_key) and self.key(self.id(_unknown_key)) == _unknown_key
        for key in keys:
            self.map[key] = len(self.reverse_map)
            self.reverse_map.append(key)
            assert self.exists(key) and self.key(self.id(key)) == key

    def exists(self, key):
        """ Return True iff this key is in the map, or if self.allow_unknown is True """
        return key in self.map or self.allow_unknown

    def id(self, key):
        """
        Get the ID for this string.
        """
        if key in self.map: return self.map[key]
        if self.allow_unknown: return self.map[_unknown_key]
        raise KeyError(key)

    def key(self, id):
        """ Get the key for this ID. """
        return self.reverse_map[id]

    @property
    def all(self):
        """ All keys. """
        return self.reverse_map

    @property
    def len(self):
        assert len(self.map) == len(self.reverse_map)
        return len(self.map)
