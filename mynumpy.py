"""
Numpy help.
"""

def to_vector(v):
    """
    Take a matrix with one row, and convert it to a vector.
    Or, if it is a vector, leave it unchanged.
    @note: This operation is destructive (I think).
    @note: Reshape is better than resize.
    """
    if len(v.shape) == 2:
        assert v.shape[0] == 1
        v.resize(v.size)
    assert len(v.shape) == 1
