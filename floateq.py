#
# Determine if floating point numbers are very close
###########

import math

DEFAULT_SANITY_CHECK_EPSILON = 1e-6

def floateq(a, b, epsilon=DEFAULT_SANITY_CHECK_EPSILON):
    """
    Compare two floats, with some epsilon tolerance.
    """
    return absolute_relative_error(a, b) < epsilon

def absolute_relative_error(a, b, epsilon=DEFAULT_SANITY_CHECK_EPSILON):
    return abs(a - b) / (abs(a) + abs(b) + epsilon)

def double_epsilon_multiplicative_eq(a, b, epsilon=DEFAULT_SANITY_CHECK_EPSILON):
    """
    Determine if doubles are equal to within a multiplicative factor of
    L{epsilon}.
    @note: This function should be preferred over
    L{double_epsilon_additive_eq}, unless the values to be compared may
    have differing signs.
    @precondition: sign(a) == sign(b)
    @rtype: bool
    """
    if a == b: return True
    if a == 0 and b == 0: return True
    assert a != 0
    assert b != 0
    assert sign(a) == sign(b)
    if a > b: d = a / b
    else: d = b / a
    assert d >= 1
    return True if d <= 1 + SANITY_CHECK_EPSILON else False

def double_epsilon_additive_eq(a, b):
    """
    Determine if doubles are equal to within an additive factor of
    L{SANITY_CHECK_EPSILON}.
    @note: Prefer L{double_epsilon_multiplicative_eq} to this function
    unless the values to be compared may have differing signs.
    """
    if a == b: return True
    if a == 0 and b == 0: return True
    assert sign(a) != sign(b)   # Should use SANITY_CHECK_EPSILON
    d = math.fabs(a - b)
    return d <= SANITY_CHECK_EPSILON
