

import re
entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
def decode_entities(string):
    """
    From: http://snippets.dzone.com/posts/show/4569
    """
    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]
