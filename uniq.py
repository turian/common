"""
Unique methods.
"""

def count(l, name="value"):
    """
    For the elements of list l, count the occurrences of each value,
    and return a list sorted in decreasing order of {name: "value", count: count}
    """
    from collections import defaultdict
    cnt = defaultdict(int)
    for j in l: cnt[j] += 1
    s = [(cnt[j], j) for j in cnt]
    s.sort()
    s.reverse()
    return [{name: i[1], "count": i[0]} for i in s]
