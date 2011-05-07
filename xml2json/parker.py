#!/usr/bin/env python
"""
Parker convention for XML2JSON

This module converts an XML object to the Parker convention:
    http://code.google.com/p/xml2json-xslt/wiki/TransformingRules
This module might deviate from this specification.
However, it seems to produce the same output for me.

I wrote this package because xml2json-xlst
(http://code.google.com/p/xml2json-xslt/) produces good output, but
there are certain XML files it cannot grok.

KEEPNONE determines whether we keep keys with no value (null in JSON) or not.

Optional:
    If you want to run this script standalone and convert XML in sys.stdin
    to JSON on sys.stdout, you will need
    simplejson: http://www.undefined.org/python/#simplejson
Older requirement:
    cElementTree: http://effbot.org/zone/celementtree.htm
        Currently, we now use xml.etree.cElementTree, which should be
        installed by in the standard library of Python >= 2.5.

@todo: Regular expressions to find floats
@todo: KEEPNONE = command line param
"""

import re
intre = re.compile("^([\+\-])?[0-9]+$")
wsre = re.compile("^\s*$")

def _converthelp(tree, KEEPNONE):
    children = tree.getchildren()
    if len(children) == 0:
        if tree.text == None:
            return None
        elif intre.match(tree.text):
            return int(tree.text)
        else:
            return tree.text
    else:
        assert tree.text is None or wsre.match(tree.text)
        cnames = {}
        for c in children: cnames[c.tag] = 1
        if not (len(cnames) == 1 or len(cnames) == len(children)):
            print >> sys.stderr, cnames, children
        assert len(cnames) == 1 or len(cnames) == len(children)
        if len(cnames) == 1 and len(children) > 1:
            return [_converthelp(c, KEEPNONE) for c in children]
        else:
            v = {}
            for c in children:
                cval = _converthelp(c, KEEPNONE)
                if cval is not None or KEEPNONE:
                    v[c.tag] = cval
            return v

def convert(element, KEEPNONE):
    return _converthelp(element, KEEPNONE)

def readxmlfile(file, KEEPNONE):
    """
    Read an XML file and convert it to an object in the Parker convention.
    """
    try:
        import xml.etree.cElementTree as ET
    except:
        import cElementTree as ET
    tree = ET.parse(file)
    root = tree.getroot()
    return {root.tag: _converthelp(root, KEEPNONE) }

def convertxmlstring(str, KEEPNONE):
    """
    Read XML from a string and convert it to an object in the Parker convention.
    """
    import xml.etree.cElementTree as ET
    root = ET.fromstring(str)
    return {root.tag: _converthelp(root, KEEPNONE) }

if __name__ == "__main__":
    import sys
    import simplejson as json
    json.dump(readxmlfile(sys.stdin, KEEPNONE=False), sys.stdout, indent=4)
#    json.dump(readxmlfile(sys.stdin, KEEPNONE=True), sys.stdout, indent=4)
