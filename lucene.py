

def from_mongodb(collection, store_fields, content_field, lucene_dir):
    """
    Convert a MongoDB to Lucene, running findall over the collection.
    A field called "content" is created.
    store_fields: list. store, don't index, this field.
    content_field: string. index, don't store, this field.
    """
    print >> sys.stderr, "Storing lucene directory in: %s" % lucene_dir

    if not os.path.exists(lucene_dir):
        os.mkdir(lucene_dir)
    store = lucene.FSDirectory.getDirectory(lucene_dir, True)
    analyzer = lucene.StandardAnalyzer()
    writer = lucene.IndexWriter(store, analyzer, True)
    writer.setMaxFieldLength(1048576)

    assert "content" not in store_fields
    for i, origdoc in enumerate(common.mongodb.findall(collection, matchfn, matchfn_description, title, logevery, timeout)):
        doc = lucene.Document()
        for f in store_fields:
            doc.add(lucene.Field(f, origdoc[f],
                                 lucene.Field.Store.YES,
                                 lucene.Field.Index.UN_TOKENIZED))

        content = origdoc[content_field]
        doc.add(lucene.Field("content", content,
                             lucene.Field.Store.YES,
                             lucene.Field.Index.TOKENIZED))
        writer.addDocument(doc)

        if (i+1) % 1000 == 0:
            print >> sys.stderr, "Inserted %d docs into lucene, which now has %d documents" % (i+1, writer.docCount())
            print >> sys.stderr, stats()

    print >> sys.stderr, "Done inserting %d docs into lucene, which now has %d documents" % (i+1, writer.docCount())
    print >> sys.stderr, stats()
    print >> sys.stderr, 'optimizing index',
    writer.optimize()
    writer.close()
    print >> sys.stderr, 'done'

