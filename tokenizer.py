#!/usr/bin/env python
"""
Tokenize a text into one-sentence-per-line (a list of sentences) using splitta.

NOTE:
    * After you import common.tokenizer, you need the following line:
        from sbd import SVM_Model
    Otherwise, you will get the following error:
        AttributeError: 'module' object has no attribute 'SVM_Model'
        
    * Unfortunately, there need to be a handful of changes made to
    splitta to get it to work.  First, you have to rename its util.py
    to sbd_util.py (this may not be necessary).
    Second, you need to add parameter files_already_opened to sbd.get_data.

    * I recommend the latest release version of splitta, 1.0.2.
    Dan Gillick, the author of splitta, says that SVN HEAD has
    models trained on slightly more data. However, I see one or two
    minor bugs in SVN HEAD, e.g. util.py should be named sbd_util.py or
    you get an ImportError.
"""

SPLITTA_DIR = "/home/joseph/utils/src/splitta-1.02/"
#SPLITTA_DIR = "/home/joseph/utils/src/splitta.svn/"

import os, os.path, sys, string
assert os.path.isdir(SPLITTA_DIR)
sys.path.append(SPLITTA_DIR)

import StringIO

import sbd      # The splitta module
import string

from sbd import SVM_Model, NB_Model

models = {}

def tokenize(text, tokenize=False, model_path="model_svm"):
#def tokenize(text, tokenize=False, model_path="model_nb"):
#def tokenize(text, tokenize=False, model_path="/home/joseph/utils/src/splitta.svn/model_svm"):
    oldwd = os.getcwd()
    assert os.path.isdir(SPLITTA_DIR)
    os.chdir(SPLITTA_DIR)

    if not model_path.endswith('/'): model_path += '/'
    assert os.path.isdir(model_path)

    # Cache model so it need not be repeatedly reloaded.
    if model_path not in models: 
        models[model_path] = sbd.load_sbd_model(model_path)
    model = models[model_path]

    test = sbd.get_data(StringIO.StringIO(text), tokenize=True, files_already_opened=True)
    test.featurize(model)
    model.classify(test)
    output = StringIO.StringIO()
    test.segment(use_preds=True, tokenize=tokenize, output=output)

    os.chdir(oldwd)
    return string.split(output.getvalue(), "\n")

if __name__ == "__main__":
    import sys
    txt = sys.stdin.read()
    print tokenize(txt)
