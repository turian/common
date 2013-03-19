"""
readcsv.py
"""

import csv
from collections import OrderedDict

def readcsv(file):
    """
    Read a CSV from the file, and return it as an ordered dict.

    We assume the first line contains all the key names.

    Any column that has an empty key name is added to a list with key `_misc`.
    """

    keys = None
    rows = []
    reader = csv.reader(file)
    for row in reader:
        if not keys:
            keys = row
        else:
            r = OrderedDict()
            for k, v in zip(keys, row):
                if not k or k == "":
                    if "_misc" not in r: r["_misc"] = []
                    r["_misc"].append(v)
                else:
                    assert k not in r
                    r[k] = v
            rows.append(r)
    return rows
