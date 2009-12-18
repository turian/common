#!/usr/bin/env python
"""
Method to read PDF.

TODO: Try pdfminer? But it seems worse at extracting text in some circumstances.
"""

from common.misc import runcmd
import os.path

from pyPdf import PdfFileReader

def readfile(filename, pdftotext="/usr/bin/pdftotext"):
    """
    Read a PDF file and return a title, text tuple.
    """
    assert os.path.exists(filename)
    assert os.path.exists(pdftotext)
    text = runcmd("%s %s -" % (pdftotext, filename))
    title = PdfFileReader(file(filename, "rb")).getDocumentInfo().title
    return title, text


if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]: print readfile(f)
