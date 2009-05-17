"""
Numpy help.
"""

def to_vector(v):
    """
    Take a matrix with one row, and convert it to a vector.
    Or, if it is a vector, leave it unchanged.
    Regardless, we call the .todense() method if it exists.
    @note: This operation is destructive (I think).
    @note: Reshape is better than resize.
    """
    if "todense" in dir(v):
        v = v.todense()
    if len(v.shape) == 2:
        assert v.shape[0] == 1
        v.resize(v.size)
    assert len(v.shape) == 1
    return v
