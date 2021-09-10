#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import numpy as np
import socket
import threading
import tkinter
from PIL import Image
from PIL import ImageTk

import libh264decoder

#
w = 960
h = 720

#
class MyTelloVideo():

    #
    def __init__(self):
        #
        self.SIZE_SOCK_R = 1024 * 2
        self.host_adrs = ""
        self.host_port = 11111

        self.decoder = libh264decoder.H264Decoder()

        return

    #
    def setTk(self, obj):
        self.tkObject = obj
        return

    #
    def updateMyTelloVideo(self):
        #
        print("[DBG]create socket")
        sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        print("[DBG]sock.bind(%s:%d)" % (self.host_adrs, self.host_port))
        sock.bind((self.host_adrs, self.host_port))

        #
        telloVideoData = b''
        while (True):
            (rbuf, radrs) = sock.recvfrom(self.SIZE_SOCK_R)
            telloVideoData += rbuf
            if (len(rbuf) != 1460):
                # comple image data
                lstFrameData = self.decoder.decode(telloVideoData)
                for frameData in lstFrameData:
                    (frame, w, h, ls) = frameData
                    if (frame is None):
                        continue

                    lstFrame = np.frombuffer(frame, dtype=np.ubyte, count=len(frame))
                    lstFrameReshaped = (lstFrame.reshape((h, int(ls / 3), 3)))
                    frame = lstFrameReshaped[:, :w, :]

                    image = Image.fromarray(frame)
                    pImage = ImageTk.PhotoImage(image)

                    self.tkObject.configure(image=pImage)
                    self.tkObject.image = pImage
                # for : end

                telloVideoData = b''
            # if : end
        # while : end

        return

    #
    def startMyTelloVideo(self):

        t = threading.Thread(target=self.updateMyTelloVideo, daemon=True)
        t.start()

#
if (__name__ == '__main__'):

    #
    tkRoot = tkinter.Tk()
    tkRoot.title(u"TelloVideo")
    tkRoot.geometry("%dx%d" % (w, h))
    tkLabel = tkinter.Label(tkRoot, width = w, height = h)
    tkLabel.pack()

    #
    myTelloVideo = MyTelloVideo()
    myTelloVideo.setTk(tkLabel)
    myTelloVideo.startMyTelloVideo()

    #
    tkRoot.mainloop()

# eof
