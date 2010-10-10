"""
Convert strings into URL slugs.
"""

import re
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    (from http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python/295466#295466)
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value
