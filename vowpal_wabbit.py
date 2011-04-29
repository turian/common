def features(fdict):
    """
    Convert a dict to vw feature string.
    """
    vwstring = "|features "
    # Remove colon, space, and pipe, which are invalid in Vowpal Wabbit features.
    new_features = {}
    for f in fdict:
        vwstring += "%s:%g " % (f.replace(" ", "*SPACE*").replace(":", "*COLON*").replace("|", "*PIPE*"), fdict[f])
    vwstring += "const:0.1"
    return vwstring

