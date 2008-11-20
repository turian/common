import re
slashre = re.compile("\\\/")
def preprocess(origw):
    """
    Preprocess a word out of Penn treebank format.
    """
    if origw == "-LRB-": w = "("
    elif origw == "-RRB-": w = ")"
    elif origw == "-LCB-": w = "{"
    elif origw == "-RCB-": w = "}"
    elif origw == "-LSB-": w = "["
    elif origw == "-RSB-": w = "]"
    else: w = slashre.sub("/", origw)
    return w
