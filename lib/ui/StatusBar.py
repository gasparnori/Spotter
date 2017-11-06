"""
Created on Sun Jan 13 14:19:24 2013
@author: <Ronny Eichler> ronny.eichler@gmail.com

Status Bar widget holding fps counter, frame buffer indicator, etc.
"""

from PyQt4 import QtGui, QtCore
from statusBarUi import Ui_statusBar
import cv2
import lib.core.grabber


class StatusBar(QtGui.QWidget, Ui_statusBar):
    gui_fps = 150
    fps_low = False
    fps_low_now = False

    def __init__(self, parent):
        super(QtGui.QWidget, self).__init__(parent)
        self.setupUi(self)
    def updateState(self, val):
        if val=='device':
            self.state.setText('Camera')
        elif val=='file':
            self.state.setText('Playback')
        else:
            self.state.setText('sleeping...')
    def update_fps(self, fps):
       # if t != 0:
        self.gui_fps=fps
            #self.gui_fps =self.gui_fps*0.95 + 0.05*1000./t
            #self.gui_fps=spotter.grabber.capture.get(cv2.cv.CV_CAP_PROP_FPS)
        if self.gui_fps > 100:
            self.lbl_fps.setText('FPS: {:.0f}'.format(self.gui_fps))
        else:
            self.lbl_fps.setText('FPS: {:.1f}'.format(self.gui_fps))

        # self.fps_low_now = self.gui_fps < 30
        #
        # if self.fps_low_now != self.fps_low:
        #     if self.fps_low_now:
        #         self.fps_low = True
        #         self.lbl_fps.setStyleSheet(' QLabel {color: red}')
        #     else:
        #         self.fps_low = False
        #         self.lbl_fps.setStyleSheet(' QLabel {color: black}')