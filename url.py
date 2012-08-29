"""
To configure Privoxy+Tor:

    # Check tor:
    tsocks lynx https://check.torproject.org/

(I couldn't get Polipo working, so I used Privoxy)

https://groups.google.com/forum/?fromgroups#!topic/scrapy-users/WqMLnKbA43I

Make sure tor is running with control mode:
    In [1]: import telnetlib
    In [2]: tn = telnetlib.Telnet('127.0.0.1', 9051)
If not, edit the torrc:
    SocksPort 9050 # what port to open for local application connections
    SocksListenAddress 127.0.0.1 # accept connections only from localhost
    RunAsDaemon 1
    ControlPort 9051

Remember to edit /etc/socks/tsocks.conf (provided by tor)
and privoxy's config. Read the docs, it should at least include: forward-socks4a / localhost:9050 .


Start the spider with *tsocks* and persistence:

    tsocks scrapy crawl fullsite -s JOBDIR=crawls/fullsitespider-`date +'%F-%T'`
"""
import httplib
import urllib2
import sys
httplib.HTTPConnection.debuglevel = 1
#useragent = 'Mozilla/4.51 (Macintosh; U; PPC)'
useragent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)'
# see these: http://techpatterns.com/forums/about304.html

from common.str import percent

from StringIO import StringIO
import gzip

import telnetlib

TOR_WORKS = False

#def fetch(url, decode=False, timeout=15):
def fetch(url, decode=True, timeout=15):
    """
    Return the text of a particular URL
    If decode, then attempt to decode the text.
    """
    request = urllib2.Request(url)
    request.get_full_url()
    request.add_header('User-Agent', useragent)
    request.add_header('Accept-Encoding', 'gzip')
    opener = urllib2.build_opener()
    response = opener.open(request, timeout=timeout)
    if decode:
        return decode_response(response)
    else:
        data = response.read()
        return data

def torfetch(url, decode=True, timeout=60, retries=5):
    torcheck()
    for i in range(retries):
        try:
            html = _torfetch(url, decode=decode, timeout=timeout)
            return html
        except Exception, e:
            print >> sys.stderr, "torfetch(), try %s: %s %" % (percent(i+1, retries), type(e), e)
            if i < retries-1:
                torchange()
            else:
                raise

def torcheck():
    """
    Check that tor is working.
    """
    global TOR_WORKS
    if not TOR_WORKS:
        assert _torfetch("https://check.torproject.org/").find("Congratulations. Your browser is configured to use Tor.") != -1
        TOR_WORKS = True

def torchange():
    """
    Change the tor nym.
    """
#    log.msg('Changing proxy', level=log.INFO)
    print >> sys.stderr, "Changing proxy"
    tn = telnetlib.Telnet('127.0.0.1', 9051)
    tn.read_until("Escape character is '^]'.", 2)
    tn.write('AUTHENTICATE "267765"\r\n')
    tn.read_until("250 OK", 2)
    tn.write("signal NEWNYM\r\n")
    tn.read_until("250 OK", 2)
    tn.write("quit\r\n")
    tn.close()
#    time.sleep(3)
#    log.msg('Proxy changed', level=log.INFO)
    print >> sys.stderr, "Proxy changed"
    # Check that Tor works again.
    TOR_WORKS = None
    torcheck()


def _torfetch(url, decode=True, timeout=60):
    # This is broken
    proxy_support = urllib2.ProxyHandler({"http" : "127.0.0.1:8118", "https": "127.0.0.1:8118"})
    opener = urllib2.build_opener(proxy_support) 
    opener.addheaders = [('User-agent', useragent), ('Accept-Encoding', 'gzip')]
    response = opener.open(url, timeout=timeout)
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

    # Attempt to ungzip
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(text)
        f = gzip.GzipFile(fileobj=buf)
        text = f.read()

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
