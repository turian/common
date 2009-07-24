"""
Pstats convenience function.
"""

def read(filename, len=25):
    import pstats
    return pstats.Stats(filename).sort_stats('cumulative').print_stats(len)
