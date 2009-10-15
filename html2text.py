#!/usr/bin/env python
"""
Method to convert html2text.

It uses the same procedure discussed in:
    http://github.com/turian/common-scripts/blob/master/html2text/README.txt
See that file, to understand the requirements.
Essentially, we pass the HTML through tidy then Bayer's html2text utility
(not aaronsw's html2text.py, mind you).
"""

from common.misc import runcmd
import os.path

def html2text(html, html2textrc=os.path.expanduser("~/dev/common-scripts/html2text/html2textrc")):
    assert os.path.exists(html2textrc)
    tidyhtml = runcmd("tidy -quiet", input=html, acceptable_return_codes=[0,1])
    text = runcmd("html2text -nobs -style pretty  -rcfile %s" % html2textrc, input=tidyhtml)
    return text

if __name__ == "__main__":
    import sys
    print html2text(sys.stdin.read())
