#!/usr/bin/env python
"""
Tokenize a text into one-sentence-per-line (a list of sentences) using splitta.

NOTE:
    * I use the SVN r20 version of splitta. Previously, I used 1.0.3,
    but that required the subsequent patches.

    * If you have splitta 1.0.3 or splitta SVN < r20, there need to be
    some changes made to splitta to get it to work. See Splitta issue
    #2 and #3 for patches you should apply:

        http://code.google.com/p/splitta/issues/detail?id=2
        http://code.google.com/p/splitta/issues/detail?id=3

    * Previous to the 1.0.3 release, I recommend SVN_HEAD, writing:
    "Models in 1.0.2 are stored as pickle files, which make it very
    difficult to load the models from outside the original splitta code."

    * I chdir into the splitta dir and the chdir to the original working
    directory. This is vestigial code from my 1.02 API and might not
    be necessary anymore. BUG: It is also going to leave you in the
    wrong directory if there is an exception.

    * splitta_dir is added to the sys.path automatically, which is
    probably bad behavior.
"""


# Import Psyco if available
import sys
try:
    import psyco
    psyco.full()
    print >> sys.stderr, "Imported psyco. Sweet!"
except ImportError:
    print >> sys.stderr, "Cannot import psyco"


import os, os.path, string, sys
import StringIO

#from sbd import SVM_Model, NB_Model

models = {}

def tokenize(text, tokenize=False, splitta_dir=os.path.join(os.environ["UTILS"], "src/splitta.svn/"), model_path="model_nb", verbose=False):
    # Use model_nb (Naive Bayes) not SVM by default, since SVM requires svmlight (licensing restrictions)
    assert os.path.isdir(splitta_dir)
    if splitta_dir not in sys.path:
        sys.path.append(splitta_dir)
    import sbd      # The splitta module

    oldwd = os.getcwd()
    assert os.path.isdir(splitta_dir)
    os.chdir(splitta_dir)

    if not model_path.endswith('/'): model_path += '/'
    assert os.path.isdir(model_path)

    # Cache model so it need not be repeatedly reloaded.
    if model_path not in models: 
        # Load the model, it is not cached
        if 'svm' in model_path: svm = True
        else: svm = False
        models[model_path] = sbd.load_sbd_model(model_path, svm)
    model = models[model_path]

    test = sbd.get_data([StringIO.StringIO(text)], tokenize=True, files_already_opened=True)
    test.featurize(model, verbose=verbose)
    model.classify(test, verbose=verbose)
    output = StringIO.StringIO()
    test.segment(use_preds=True, tokenize=tokenize, output=output)

    os.chdir(oldwd)
    return string.split(output.getvalue(), "\n")

if __name__ == "__main__":
    txt = sys.stdin.read()
    for l in tokenize(txt.decode("utf-8")):
        print l.encode("utf-8")
