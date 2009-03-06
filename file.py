import gzip, bz2
import os, os.path, sys

def myopen(filename, mode="r", bufsize=-1):
    """
    open(), detecting .gz and .bz2 file suffixes
    """
    if filename[-3:] == ".gz":
        return gzip.open(filename, mode, bufsize)
    elif filename[-4:] == ".bz2":
        return bz2.open(filename, mode, bufsize)
    else:
        return open(filename, mode, bufsize)

def find_files(dir, shuffle=False):
    """
    Find all files in dir by recursively directory walking.
    @param shuffle: Randomly shuffle the files before returning them.
    """
    all = []
    assert os.path.isdir(dir)
    for root, dirs, files in os.walk(dir):
        #sys.stderr.write("Walking %s...\n" % root)
        for f in files:
            all.append(os.path.join(root, f))
    if shuffle:
        import random
        random.shuffle(all)
    return all 

def ensuredir(dir):
    """
    Create dir if it does not exist (including all parents).
    Do nothing if it does.
    """
    if not os.path.exists(dir):
       sys.stderr.write("Creating directory: %s\n" % dir)
       os.makedirs(dir)
    assert os.path.isdir(dir)

def ascend_find(name, dir=os.getcwd()):
    """
    Crawl up the directory hierarchy from dir towards root, and return
    the first time we find a file 'name'.
    """
    p = os.path.join(dir, name)
    if os.path.exists(p): return p
    updir = os.path.dirname(dir)
    assert updir != dir
    return ascend_find(name, dir=updir)
