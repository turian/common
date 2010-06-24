#!/usr/bin/python

"""
Deterministic uniform random numbers, with 32-bits of precision.
We provide random access given a particular key.

WARNING:
    * This is random access to an RNG. Instead of using a pseudo-RNG
    as such (which might be slow for random access), we use hashing to
    provide no-memory random access to random numbers. I can't promise
    that this hashing provides "strong" random numbers.

    * We use Murmur, a Python-wrapped C implementation of murmurhash. This
    is probably not the latest or most bugfixed implementation of
    MurmurHash 2.0.
"""

import murmur

MAX_UNSIGNED_LONG = 2**32

def deterministicrandom(x):
    """
    Convert x (any Python value) to a deterministic uniform random number
    in [0, 1), with 32-bits of precision.

    TODO: Should check that murmur.string_hash returns an unsigned long
    int (32-bit), which is what we expect.
    """

    unsigned_long_value = unsigned_long_hash(x)

#   import types
#   print type(long_value)
#   assert type(long_value) ==  types.LongType

    assert unsigned_long_value >= 0 and unsigned_long_value < MAX_UNSIGNED_LONG

    r = 1.0 * unsigned_long_value / MAX_UNSIGNED_LONG
    return r

def unsigned_long_hash(x):
    return murmur.string_hash(`x`)

if __name__ == "__main__":
    array = [deterministicrandom(i) for i in range(1000)]
    import numpy
    print "mean (should be 0.5) = ", numpy.mean(array)

    import sys, os
    import struct
    print >> sys.stderr, "Writing 500000 bytes of random output to randomoutput.bin"
    f = open("randomoutput.bin", "wb")
    for i in range(1250000):
        f.write(struct.pack("L", unsigned_long_hash(i)))
    os.system("ent randomoutput.bin")
