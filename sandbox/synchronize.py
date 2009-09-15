"""
Module for named objects, synchronized to disk.
When an object is named, we can also retrieve it on the basis of this name.
The object's name is also its filename. When we initially retrieve the
object, we attempt to load the object from its file. If the file doesn't
exist, we create the object from scratch.
To save the object to disk, use the .save method.
"""

_name_to_obj = {}

import os
def get(name, init, directory=os.getcwd()):
    """
    Get the Object with a particular name.
    If the Object doesn't exist, create it with init.
    """
    global _name_to_obj
    fullname = (name, directory)
    if fullname not in _name_to_obj:
        # Create a new L{FeatureMap}
        name_to_fmap[name] = FeatureMap(name, synchronize)
    fmap = name_to_fmap[name]
    assert fmap.name == name
    assert fmap.synchronize == synchronize
    return fmap

