
def decode_entities(string):
    """
    Decode HTML entities until there are no more to decode.
    """
    oldstring = ""
    while string != oldstring:
        oldstring = string
        string = decode_entities_help(oldstring)
    return string

def decode_entities_help(string):
    """
    From: http://snippets.dzone.com/posts/show/4569
    """
    import re
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            if ent[0] == 'x':   # e.g. &x0a;
                return unichr(int(ent[1:], 16))
            else:
                return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]
