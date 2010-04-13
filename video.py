#!/usr/bin/python
"""
Grab frames from a video file.
"""

import sys
import tempfile
from PIL import Image

from common.misc import runcmd


def grab_frame(filename, framenumber, FPS=29.97):
    """
    Grab a certain from an video file, and return it as a PIL Image
    TODO: Don't hardcode FPS.
    TODO: Use a better library for this.
    """
    tmp = tempfile.NamedTemporaryFile(suffix=".png")
    framesec = 1. * framenumber / FPS
    cmd = "ffmpeg -i %s -vcodec png -vframes 1 -an -ss %f -f rawvideo %s" % (filename, framesec, tmp.name)
    print >> sys.stderr, cmd
    runcmd(cmd)
    im = Image.open(tmp.name)
    tmp.close()
    return im

if __name__ == "__main__":
    assert len(sys.argv) == 2
    grab_image(sys.argv[1], 0)
