"""
Read Zip files, recursively reading zip files therein.
NOTE: Designed to work with Python < 2.6 (or 2.6). Ideally, we'd use
z.open, but this is only in Python 2.6. So, we have a high memory
consumption, because we don't stream internal files.
"""

import zipfile
import logging
import sys
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

def process(filename):
    """
    Given a .zip filename, open it and read all files within.
    Any .zip/.ZIP file within, open it and recurse.
    For other files, yield (filenames, StringIO) objects.
    filenames in the yield is a list of the zip files and final file that were extracted to get to this StringIO.
    """
    assert filename[-4:] == ".zip" or filename[-3:] == ".ZIP"
    z = zipfile.ZipFile(filename, "r")
    for i in _process_help(z, [filename]):
        yield i


def _process_help(zipf, filenames):
    """
    Given a ZipFile, recursively process it and yield (filenames, StringIO) objects.
    filenames in the parameter is a list of the zip files that were extracted to get to this zipf.
    filenames in the yield is a list of the zip files and final file that were extracted to get to this StringIO.
    """
    print >> sys.stderr, "Processing", filenames
    for newf in zipf.namelist():
        if newf[-4:] == ".zip" or newf[-4:] == ".ZIP":
            logging.debug("Opening %s in %s" % (newf, filenames))
            # Ideally, we'd use z.open, but this is only in Python 2.6
            #newzipf = zipfile.ZipFile(zipf.open(newf), "r")
            newzipf = zipfile.ZipFile(StringIO(zipf.read(newf)), "r")
            for i in _process_help(newzipf, filenames + [newf]):
                yield i
        else:
            logging.debug("About to read %s" % (filenames + [newf]))
            try:
                fileio = StringIO(zipf.read(newf))
                yield (filenames + [newf], fileio)
            except Exception, e:
                print >> sys.stderr, "COULD NOT OPEN", filenames + [newf], "SKIPPING.", type(e), e, sys.exc_info()[0]
