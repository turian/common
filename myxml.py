"""
Output an object in XML.
"""

from xml.dom.minidom import Document

def toxml(obj):
    doc = Document()
    elem = doc.createElement("document")
    doc.appendChild(elem)
    _toxml_help(obj, doc, elem)
    return elem.toprettyxml(indent="  ")

def tostring(value):
    assert type(value) is not dict
    assert type(value) is not list
    if type(value) is str or type(value) is unicode:
        return value
    else:
        return `value`

def _toxml_help(obj, doc, parent):
    if type(obj) is dict:
        for key in obj:
            elem = doc.createElement(tostring(key))
            value = obj[key]
            if type(value) is dict:
                _toxml_help(value, doc, elem)
            elif type(value) is list:
                assert key[-1] == "s"
                for child in value:
                    childelem = doc.createElement(key[:-1])
                    _toxml_help(child, doc, childelem)
                    elem.appendChild(childelem)
            else:
                elem.appendChild(doc.createTextNode(tostring(value)))
            parent.appendChild(elem)
    elif type(obj) is list:
        assert 0 # Think this case through
    else:
        parent.appendChild(doc.createTextNode(tostring(obj)))

if __name__ == "__main__":
    print toxml({"terms": [{"value": "cool", "weight": 2.}, "cool", 2, {"foo": "bar"}]}).encode("utf-8")
