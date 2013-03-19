"""
readcsv.py
"""

import csv
from collections import OrderedDict

def readcsv(file, **fmtparams):
    """
    Read a CSV from the file, and return it as an ordered dict.

    We assume the first line contains all the key names.

    Any column that has an empty key name is added to a list with key `_misc`.
    Any column with empty key and row element is ignored.
    """

    keys = None
    rows = []
    reader = csv.reader(file, **fmtparams)
    for row in reader:
        if not keys:
            keys = row
        else:
            r = OrderedDict()
            assert len(keys) == len(row)
            for k, v in zip(keys, row):
                if not k or k == "":
                    if not v or v == "": continue
                    if "_misc" not in r: r["_misc"] = []
                    r["_misc"].append(v)
                else:
                    assert k not in r
                    r[k] = v
            rows.append(r)
    return rows
