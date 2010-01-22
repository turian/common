"""
ElementTree helper functions.
"""

import sys

def findone(tree, path, debug=False):
    """
    Find an XML path, which must be unique, and return it.
    """
    t = tree.findall(path)
    if len(t) != 1:
        if debug:
            print >> sys.stderr, "ERROR: len(t) = %d when searching for path %s in %s with children %s" % (len(t), path, tree, tree.getchildren())
            return None
        else:
            assert 0
    return t[0]

def allsubtext(tag, avoid=None):
    """
    Return all subtext from within a tag.
    We will print warnings if any sub-tag is the same as this tag.
    """
    if avoid == None: avoid = tag.tag
    elif tag.tag == avoid: print >> sys.stderr, "WARNING: Found sub-tag %s in tag %s" % (tag.tag, avoid)
        
    children = ""
    for t in tag.getchildren():
        children += allsubtext(t, avoid=avoid)
    text = tag.text
    if text == None: text = ""
    tail = tag.tail
    if tail == None: tail = ""
    return text + children + tail

def findallsubtext(tree, path, debug=False):
    return allsubtext(findone(tree, path, debug=debug))

if __name__ == "__main__":
    import xml.etree.cElementTree as ET
    print allsubtext(ET.fromstring("<doc><p>1 <b>2<i>3</i> 4</b> 5 <b>6</b></p></doc>").findall("./p")[0])
    print allsubtext(ET.fromstring("<doc><p>1 <b>2<i>3</i> <p>4</p></b> 5 <b>6</b></p></doc>").findall("./p")[0])
