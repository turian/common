
import httplib
import urllib2
import sys
httplib.HTTPConnection.debuglevel = 1
#useragent = 'Mozilla/4.51 (Macintosh; U; PPC)'
useragent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
# see these: http://techpatterns.com/forums/about304.html

def fetch(url, decode=False, timeout=15):
    """
    Return the text of a particular URL
    If decode, then attempt to decode the text.
    """
    request = urllib2.Request(url)
    request.get_full_url()
    request.add_header('User-Agent', useragent)
    opener = urllib2.build_opener()
    response = opener.open(request, timeout=timeout)
    if decode:
        return decode_response(response)
    else:
        data = response.read()
        return data

def decode_response(response):
    """
    The proper decoding technique is described here:
        http://stackoverflow.com/questions/1495627/how-to-download-any-webpage-with-correct-charset-in-python
    We skip some of the steps, though.
    1. See if there is a charset in the HTTP header.
    2. [skipped] An encoding discovered in the document itself: for
    instance, in an XML declaration or (for HTML documents) an http-equiv
    META tag. If Beautiful Soup finds this kind of encoding within the
    document, it parses the document again from the beginning and gives
    the new encoding a try. The only exception is if you explicitly
    specified an encoding, and that encoding actually worked: then it
    will ignore any encoding it finds in the document.
    3. chardet predicted encoding.
    4. utf-8
    5. windows-1252
    """
    text = response.read()

    charset = response.headers.getparam('charset')
    if charset is not None:
        (worked, decoded_text) = attempt_decode(charset, text)
        if worked: return decoded_text

    # BeautifulSoup goes here

    # Try chardet
    import chardet
    charset = chardet.detect(text)["encoding"]
    if charset is not None:
        (worked, decoded_text) = attempt_decode(charset, text)
        if worked: return decoded_text

    # Try utf-8
    (worked, decoded_text) = attempt_decode("utf-8", text)
    if worked: return decoded_text

    # Try windows-1252
    (worked, decoded_text) = attempt_decode("windows-1252", text)
    if worked: return decoded_text

    assert 0

def attempt_decode(charset, text):
    """
    Attempt to decode text with this charset.
    Return (worked, decoded_text), where worked is True if we could successfully decode.
    """
    try:
        decoded_text = text.decode(charset)
        return (True, decoded_text)
    except Exception, e:
        print >> sys.stderr, "Could not decode with %s, SKIPPING." % charset, type(e), e
        return (False, None)
