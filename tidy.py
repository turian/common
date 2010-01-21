#!/usr/bin/env python
"""
Run Tidy on XML and HTML.

ISSUES: I may have the character encodings wrong :(
See http://github.com/turian/common-scripts/blob/master/html2text/README.txt
for more information.

TODO: Trap stderr output.
"""

from common.misc import runcmd

def tidy(markup, xml=False, forceoutput=False, veryquiet=True, indent=True, nowrap=False):
    """
    If veryquiet, all errors and warnings from tidy are written to /dev/null.
    """
    tidyoptions = ""
    if forceoutput: tidyoptions += " --force-output yes"
    if veryquiet: tidyoptions += " -f /dev/null"
    if xml: tidyoptions += " -xml"
    if indent: tidyoptions += " -indent"
    if nowrap: tidyoptions += " -w 0"
    tidymarkup = runcmd("tidy -quiet %s" % tidyoptions, input=markup.encode("utf-8"), acceptable_return_codes=[0,1])
    return tidymarkup
