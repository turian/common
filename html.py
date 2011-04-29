
import w3lib.html
def clean(html):
    """
    Clean HTML, removing HTML entities, tags, and comments.
    """
    newhtml = w3lib.html.remove_comments(w3lib.html.remove_tags(w3lib.html.remove_entities(html)))
    while html != newhtml:
        html = newhtml
        newhtml = w3lib.html.remove_comments(w3lib.html.remove_tags(w3lib.html.remove_entities(html)))
    return newhtml
