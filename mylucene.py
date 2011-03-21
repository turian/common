
import sys

analyzer = None
searcher = None

from lucene import \
    QueryParser, IndexSearcher, StandardAnalyzer, FSDirectory, Hit, \
    VERSION, initVM, CLASSPATH

def init(lucenedir):
    global analyzer, searcher
    assert analyzer is None and searcher is None

    initVM(CLASSPATH)
    print >> sys.stderr, 'lucene', VERSION

    print >> sys.stderr, "Storing lucene directory in: %s" % lucenedir

    directory = FSDirectory.getDirectory(lucenedir, False)
    searcher = IndexSearcher(directory)
    analyzer = StandardAnalyzer()
    assert analyzer is not None and searcher is not None

def close():
    global analyzer, searcher
    assert analyzer is not None and searcher is not None
    searcher.close()
    analyzer = None
    searcher = None
    assert analyzer is None and searcher is None
