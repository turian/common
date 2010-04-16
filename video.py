#!/usr/bin/python
"""
Grab frames from a video file.
"""

import os
import os.path
import re
import shutil
import sys
import tempfile
#from PIL import Image

import common.misc
from common.stats import stats

#def grab_frame(filename, framenumber, FPS=29.97):
#    """
#    Grab a certain from an video file, and return it as a PIL Image
#    TODO: Don't hardcode FPS.
#    TODO: Use a better library for this.
#    """
#    tmp = tempfile.NamedTemporaryFile(suffix=".png")
#    framesec = 1. * framenumber / FPS
#    cmd = "ffmpeg -i %s -y -vcodec png -vframes 1 -an -ss %f -f rawvideo %s" % (filename, framesec, tmp.name)
#    print >> sys.stderr, cmd
#    runcmd(cmd)
#    im = Image.open(tmp.name)
#    tmp.close()
#    return im

def frames(filename, maxframes=None):
    """
    Iterate over the frames in a video file.
    Yields (frame number, PNG filename, total frames).
    maxframes: Maximum number of frames to return.
    TODO: Use a better library for this.
    """
    dir = tempfile.mkdtemp()
    inre = re.compile("in.*.jpg")
    try:
        # Decompose video into images
        # I learned this command from here: http://electron.mit.edu/~gsteele/ffmpeg/
        if maxframes is None:
            cmd = "ffmpeg -sameq -y -r 30 -i %s %s" % (filename, os.path.join(dir, 'in%05d.jpg'))
        else:
            cmd = "ffmpeg -sameq -y -vframes %d -r 30 -i %s %s" % (maxframes, filename, os.path.join(dir, 'in%05d.jpg'))
        print >> sys.stderr, "Decomposing video to images:", cmd, "\n"
        common.misc.runcmd(cmd)
        print >> sys.stderr, stats()
        
        # Find all files to process
        infiles = []
        for f in os.listdir(dir):
            if inre.match(f):
                infiles.append(f)
        infiles.sort()

        for i, f in enumerate(infiles):
            yield i, os.path.join(dir, f), len(infiles)


    finally:
        print >> sys.stderr, "Removing dir %s" % dir
        shutil.rmtree(dir)

if __name__ == "__main__":
    assert len(sys.argv) == 2
    grab_image(sys.argv[1], 0)

