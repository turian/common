#!/usr/bin/python

"""
Deterministic uniform random numbers, with 32-bits of precision.
We provide random access given a particular key.

WARNING:
    * This is random access to an RNG. Instead of using a pseudo-RNG
    as such (which might be slow for random access), we use hashing to
    provide no-memory random access to random numbers. To test the
    randomness of this stream, use the following command:
        ./deterministicrandom.py -s | dieharder -g 200 -a

    * We use Murmur, a Python-wrapped C implementation of murmurhash. This
    is probably not the latest or fastest implementation of
    MurmurHash 2.0.

TODO:
    * Make sure that we get a 4-byte value from murmurhash!!!
"""

import sys
import murmur

# We expect the hash to be 4 bytes long
HASH_BYTES = 4
MAX_HASH_VALUE = 2**(8*HASH_BYTES)

def deterministicrandom(x):
    """
    Convert x (any Python value) to a deterministic uniform random number
    in [0, 1), with 32-bits of precision.
    """

    i = hash_value(x)

    r = 1.0 * i / MAX_HASH_VALUE
    return r

def hash_value(x):
    """
    TODO: Make sure that we get a 4-byte value!!!
    """
    i = murmur.string_hash(`x`)
#    assert sys.sizeof(i) == HASH_BYTES
    assert i >= 0 and i < MAX_HASH_VALUE
    return i

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--stream", action="store_true", default=False, dest="stream", help="stream random numbers to stdout")
    (options, args) = parser.parse_args()
    assert len(args) == 0

    import os
    import struct
    # Make sure that packing to a struct of type I (unsigned int) is
    # 4 bytes, which is the length of the murmurhash output. (Actually,
    # we don't sanity check that.) The Python documentation for struct
    # erroneously saying that L (unsigned long) is 4 bytes. In fact,
    # it is 8 (http://bugs.python.org/issue1789)
    assert len(struct.unpack("cccc", struct.pack("I", hash_value(0)))) == HASH_BYTES

    if not options.stream:
        array = [deterministicrandom(i) for i in range(1000)]
        import numpy
        print "mean (should be 0.5) = ", numpy.mean(array)

        print >> sys.stderr, "Writing 500000 bytes of random output to randomoutput.bin"
        f = open("randomoutput.bin", "wb")
        for i in range(1250000):
            f.write(struct.pack("I", hash_value(i)))
#            f.write(struct.pack("L", hash_value(i)))
        os.system("ent randomoutput.bin")
    else:
        i = 0
        import common.stats
        while 1:
            sys.stdout.write(struct.pack("I", hash_value(i)))
#            sys.stdout.write(struct.pack("L", hash_value(i)))
            i += 1
#            if i % 1000000 == 0: print >> sys.stderr, i, common.stats.stats()
