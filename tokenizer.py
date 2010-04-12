#!/usr/bin/env python
"""
Tokenize a text into one-sentence-per-line (a list of sentences) using splitta.

NOTE:
    * Unfortunately, there need to be some changes made to
    splitta to get it to work.
    You need to add parameter files_already_opened to sbd.get_data.

    * I use the 1.0.3 version of splitta.

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

def tokenize(text, tokenize=False, splitta_dir="/u/turian/utils/src/splitta-1.03/", model_path="model_svm", verbose=False):
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
    print tokenize(txt)
