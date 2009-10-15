#!/usr/bin/env python
"""
Method to convert html2text.

It uses the same procedure discussed in:
    http://github.com/turian/common-scripts/blob/master/html2text/README.txt
See that file, to understand the requirements.
Essentially, we pass the HTML through tidy then Bayer's html2text utility
(not aaronsw's html2text.py, mind you).

ISSUES: I may have the character encodings wrong :(
See http://github.com/turian/common-scripts/blob/master/html2text/README.txt
for more information.

TODO: Trap stderr output.
"""

from common.misc import runcmd
import os.path

def html2text(html, html2textrc=os.path.expanduser("~/dev/common-scripts/html2text/html2textrc"), forceoutput=True, veryquiet=True):
    """
    If veryquiet, all errors and warnings from tidy are written to /dev/null.
    """
    assert os.path.exists(html2textrc)
    tidyoptions = ""
    if forceoutput: tidyoptions += " --force-output yes"
    if veryquiet: tidyoptions += " -f /dev/null"
    tidyhtml = runcmd("tidy -quiet %s" % tidyoptions, input=html.encode("utf-8"), acceptable_return_codes=[0,1])
    text = runcmd("html2text -nobs -style pretty  -rcfile %s" % html2textrc, input=tidyhtml)
    return text

if __name__ == "__main__":
    import sys
    print html2text(sys.stdin.read())
