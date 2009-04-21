"""
Tab-separated values.
Code from Shannon -jj Behrens: http://markmail.org/message/qeo4tyuqxsoziael
"""

import csv

DEFAULT_KARGS = dict(dialect='excel-tab', lineterminator='\n')

def create_default_reader(iterable):
    """Return a csv.reader with our default options."""
    return csv.reader(iterable, **DEFAULT_KARGS)

def create_default_writer(iterable):
    """Return a csv.writer with our default options."""
    return csv.writer(iterable, **DEFAULT_KARGS)
