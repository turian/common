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
    reader = csv.reader(open(filename))
    for row in reader:
        if not keys:
            keys = row
        else:
            row = OrderedDict()
            for k, v in zip(keys, row):
                if not key or key == "":
                    if "_misc" not in row: row["_misc"] = []
                    row["_misc"].append(v)
                else:
                    assert k not in row
                    row[k] = v
            rows.append(row)
    return rows
