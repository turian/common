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

Optional:
    If you want to run this script standalone and convert XML in sys.stdin
    to JSON on sys.stdout, you will need
    simplejson: http://www.undefined.org/python/#simplejson
Older requirement:
    cElementTree: http://effbot.org/zone/celementtree.htm
        Currently, we now use xml.etree.cElementTree, which should be
        installed by in the standard library of Python >= 2.5.

@todo: Regular expressions to find floats
"""

import re
intre = re.compile("^([\+\-])?[0-9]+$")
wsre = re.compile("^\s*$")

def _converthelp(tree):
    children = tree.getchildren()
    if len(children) == 0:
        if tree.text == None:
            return None
        elif intre.match(tree.text):
            return int(tree.text)
        else:
            return tree.text
    else:
        assert wsre.match(tree.text)
        cnames = {}
        for c in children: cnames[c.tag] = 1
        assert len(cnames) == 1 or len(cnames) == len(children)
        if len(cnames) == 1 and len(children) > 1:
            return [_converthelp(c) for c in children]
        else:
            v = {}
            for c in children:
                v[c.tag] = _converthelp(c)
            return v

def convert(element):
    return _converthelp(element)

def readxmlfile(file):
    """
    Read an XML file and convert it to an object in the Parker convention.
    """
    try:
        import xml.etree.cElementTree as ET
    except:
        import cElementTree as ET
    tree = ET.parse(sys.stdin)
    root = tree.getroot()
    return {root.tag: _converthelp(root) }

def convertxmlstring(str):
    """
    Read XML from a string and convert it to an object in the Parker convention.
    """
    import xml.etree.cElementTree as ET
    root = ET.fromstring(str)
    return {root.tag: _converthelp(root) }

if __name__ == "__main__":
    import sys
    import simplejson as json
    json.dump(readxmlfile(sys.stdin), sys.stdout, indent=4)
