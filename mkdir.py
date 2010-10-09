"""
mkdir -p
Code from: http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python/600612#600612
"""
import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
