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

import re
xmlprocre = re.compile("(\s*<[\?\!])")
def add_toplevel_tag(string):
    """
    After all the XML processing instructions, add an enclosing top-level <DOC> tag, and return it.
    e.g.
        <?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE FOO BAR "foo.dtd" [ <!ENTITY ...> <!ENTITY ...> <!ENTITY ...> ]> <ARTICLE> ...
         </ARTICLE> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE>
      =>
        <?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE FOO BAR "foo.dtd" [ <!ENTITY ...> <!ENTITY ...> <!ENTITY ...> ]><DOC> <ARTICLE> ...
         </ARTICLE> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE></DOC>
    """
    def _advance_proc(string, idx):
        # If possible, advance over whitespace and one processing
        # instruction starting at string index idx, and return its index.
        # If not possible, return None
        # Find the beginning of the processing instruction
        m = xmlprocre.match(string[idx:])
        if m is None: return None
        #print "Group", m.group(1)
        idx = idx + len(m.group(1))
        #print "Remain", string[idx:]

        # Find closing > bracket
        bracketdebt = 1
        while bracketdebt > 0:
            if string[idx] == "<": bracketdebt += 1
            elif string[idx] == ">": bracketdebt -= 1
            idx += 1
        #print "Remain", string[idx:]
        return idx
    loc = 0
    while 1:
        # Advance one processing instruction
        newloc = _advance_proc(string, loc)
        if newloc is None: break
        else: loc = newloc
    return string[:loc] + "<DOC>" + string[loc:] + "</DOC>"

if __name__ == "__main__":
    import xml.etree.cElementTree as ET
    print allsubtext(ET.fromstring("<doc><p>1 <b>2<i>3</i> 4</b> 5 <b>6</b></p></doc>").findall("./p")[0])
    print allsubtext(ET.fromstring("<doc><p>1 <b>2<i>3</i> <p>4</p></b> 5 <b>6</b></p></doc>").findall("./p")[0])
    print add_toplevel_tag('<?xml version="1.0" encoding="UTF-8"?> <!DOCTYPE FOO BAR "foo.dtd" [ <!ENTITY ...> <!ENTITY ...> <!ENTITY ...> ]> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE> <ARTICLE> ... </ARTICLE>')

