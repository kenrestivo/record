#! /usr/bin/env python

import sys
import os
from time import sleep
from subprocess import Popen, PIPE, check_call
from tempfile import mkdtemp

import gst

from optparse import OptionParser

class Audio(object):

    def __init__(self, filename):
        self._pipe = gst.parse_launch("""alsasrc ! audioconvert ! flacenc !  filesink location=%s""" % filename)
        self._pipe.set_state(gst.STATE_PLAYING)

    def stop(self):
        self._pipe.set_state(gst.STATE_NULL)

class Video(object):

    def __init__(self, filename, win_id=None):
        """
        Starts capturing the video and saves it to a file 'filename'.

        win_id ... the window id to capture, if None, it automatically runs
                xwininfo and parses the output to capture the windows id
        """
        if win_id is None:
            win_id = self.get_window_id()
        self._pipe = Popen(["/usr/bin/recordmydesktop", "--no-sound",
            "-windowid", "%s" % win_id, "-o", "%s" % filename],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
        #p.communicate()

    def __del__(self):
        self._pipe.kill()

    def stop(self):
        self._pipe.terminate()

    def get_window_id(self):
        p = Popen("xwininfo", stdout=PIPE)
        out = p.communicate()[0]
        if p.returncode != 0:
            raise Exception("xwininfo failed")
        s = "Window id: "
        i1 = out.find(s) + len(s)
        i2 = out.find(" ", i1)
        id = out[i1: i2]
        return id

def encode(audio, video, output):
    """
    Combines the audio and video to a resulting file.
    """
    check_call(["mencoder", "-audiofile", audio, "-oac", "lavc", "-ovc",
        "lavc", video, "-o", output])

def wait_for_ctrl_c():
    """
    Waits until CTRL-C is pressed.
    """
    try:
        while 1:
            pass
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", default="out.avi",
            help="save to FILE [default: %default]", metavar="FILE")
    #parser.add_option("-w", "--window", dest="window", action="store_true"
    #        help="ask which window to capture", default=True)
    options, args = parser.parse_args()

    tmp_dir = mkdtemp()
    video_file = os.path.join(tmp_dir, "video.ogv")
    audio_file = os.path.join(tmp_dir, "audio.flac")
    print "work dir:", tmp_dir
    print "select a window to capture"
    v = Video(video_file)
    a = Audio(audio_file)
    print "press CTRL-C to stop"
    try:
        wait_for_ctrl_c()
    finally:
        v.stop()
        a.stop()
    print "waiting 1s"
    sleep(1)
    encode(audio_file, video_file, options.filename)
    print "output saved to:", options.filename