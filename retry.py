"""
Retry a function several times.
Useful for when several processes want to read/write the same file, sort of like a quasi-lock.
"""

def retry(f, msg, RETRIES=3, BASEWAIT=0, WAITVAR=0, WAITINC=5.):
    """
    Attempt to run f for RETRIES+1 times.
    If there is a problem, catch and output the exception and msg, and retry.
    Wait BASEWAIT + random.random() * WAITVAR seconds before running.
    Each retry, add WAITINC to BASEWAIT and WAITVAR.
    """
    import sys
    if BASEWAIT != 0 or WAITVAR != 0:
        import time, random
        s = BASEWAIT + random.Random().random() * WAITINC
        sys.stderr.write("Sleeping for %f seconds before retry...\n" % s)
        time.sleep(s)
    assert RETRIES >= 0
    if RETRIES==0: return f()
    try:
        return f()
    except Exception as e:
        print >> sys.stderr, "%s:" % msg, type(e), e, ". %d retries left..." % RETRIES
        return retry(f, msg, RETRIES-1, BASEWAIT+WAITINC, WAITVAR+WAITINC, WAITINC)
