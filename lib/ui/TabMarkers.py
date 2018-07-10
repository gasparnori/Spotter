# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 14:19:24 2013
@author: <Ronny Eichler> ronny.eichler@gmail.com


"""
import logging

import cv2
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from tab_markersUi import Ui_tab_markers
import lib.utilities as utils
import sip
import math


class Tab(QtGui.QWidget, Ui_tab_markers):

    accept_events = False
    tab_type = "marker"
    current_range_hue = (None, None)

    def __init__(self, marker_ref, label=None, *args, **kwargs):
        #super(QtGui.QWidget, self).__init__(parent)
        QtGui.QWidget.__init__(self)
        self.log = logging.getLogger(__name__)
        self.setupUi(self)
        self.marker = marker_ref

        assert 'spotter' in kwargs
        self.spotter = kwargs['spotter']

        if label is None:
            self.label = self.marker.label
        else:
            self.label = label

        self.combo_label.setEditText(self.label)

        # Set spin boxes to the starting value of the represented marker
        self.spin_hue_min.setValue(self.marker.range_hue[0])
        self.spin_hue_max.setValue(self.marker.range_hue[1])
        self.spin_sat_min.setValue(self.marker.range_sat[0])
        self.spin_sat_max.setValue(self.marker.range_sat[1])
        self.spin_val_min.setValue(self.marker.range_val[0])
        self.spin_val_max.setValue(self.marker.range_val[1])
        self.spin_area_min.setValue(self.marker.range_area[0])
        self.spin_area_max.setValue(self.marker.range_area[1])

        # Connect spin boxes
        self.connect(self.spin_hue_min, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_hue_max, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_sat_min, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_sat_max, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_val_min, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_val_max, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_area_min, QtCore.SIGNAL('valueChanged(int)'), self.update_led)
        self.connect(self.spin_area_max, QtCore.SIGNAL('valueChanged(int)'), self.update_led)

        # Connect checkboxes
        self.ckb_track.setChecked(self.marker.detection_active)
        self.connect(self.ckb_track, QtCore.SIGNAL('stateChanged(int)'), self.update_led)
        self.ckb_fixed_pos.setChecked(self.marker.fixed_pos)
        self.connect(self.ckb_fixed_pos, QtCore.SIGNAL('stateChanged(int)'), self.update_led)
        self.ckb_marker.setChecked(self.marker.marker_visible)
        self.connect(self.ckb_marker, QtCore.SIGNAL('stateChanged(int)'), self.update_led)
        self.connect(self.btn_pick_color, QtCore.SIGNAL('toggled(bool)'), self.pick_color)
        #self.connect(self.filterSlider, QtCore.SIGNAL('valueChanged(int)'), self.marker.kalmanfilter.updateObservationCoeffVal)
        #self.recalibrateBtn.clicked.connect(self.marker.recalibrateFilter)
        self.connect(self.ckb_prediction, QtCore.SIGNAL('stateChanged(int)'), self.enablePred)
        self.connect(self.enable_filter, QtCore.SIGNAL('stateChanged(int)'), self.enableKF)
        self.connect(self.enable_adaptive, QtCore.SIGNAL('stateChanged(int)'), self.adaptiveKF)

        #filter related
        self.counterR = 0
        self.counterM = 0
        self.CalibMax = 100
        self.speed = 100
        self.connect(self.CalibRBtn, QtCore.SIGNAL('clicked()'), self.sensorCalib)
        self.connect(self.CalibQBtn, QtCore.SIGNAL('clicked()'), self.measurementCalib)
        self.CalibQBtn.setEnabled(False)
        self.sensorProgress.setVisible(False)
        self.sensorProgress.setMaximum(self.CalibMax)
        self.measurementProgress.setVisible(False)
        self.measurementProgress.setMaximum(self.CalibMax)
        #if the filter is enabled by default
        if self.marker.filtering_enabled:
            self.enable_filter.setChecked(True)
        if self.marker.guessing_enabled:
            self.ckb_prediction.setChecked(True)

        self.update()


    def sensorCalib(self):
        if len(self.spotter.tracker.leds) > 0:
            popup = QMessageBox.information(self, "Sensor calibration",
                                            "Please keep the LED's in a fixed position. The calibration takes less than a minute.",
                                            QMessageBox.Ok, QMessageBox.Cancel)
            if popup == QMessageBox.Ok:
                self.timerR = QtCore.QTimer()
                self.connect(self.timerR, QtCore.SIGNAL('timeout()'), self.sensorProg)
                self.timerR.start(self.speed)
                self.sensorProgress.setVisible(True)
                self.sensorProgress.setValue(0)
        else:
            popup = QMessageBox.information(self, "Sensor calibration",
                                            "In order to calibrate the sensor, you first need to define at least one marker",
                                            QMessageBox.Ok)

        # calib=CalibrationPopUp.CalibPopUp(self, 30)
        # calib.show()


    def measurementCalib(self):
        if len(self.spotter.tracker.leds) > 0:
            popup = QMessageBox.information(self, "Measurement calibration",
                                            "Please move the LED's around . The calibration takes half a minute.",
                                            QMessageBox.Ok, QMessageBox.Cancel)
            if popup==QMessageBox.Ok:
                self.timerM = QtCore.QTimer()
                self.connect(self.timerM, QtCore.SIGNAL('timeout()'), self.measureProg)
                self.timerM.start(self.speed)
                self.measurementProgress.setVisible(True)
                self.measurementProgress.setValue(0)
        else:
            popup = QMessageBox.information(self, "Measurement calibration",
                                            "In order to calibrate the sensor, you first need to define at least one marker",
                                            QMessageBox.Ok)


    def sensorProg(self):
        if self.counterR <= self.CalibMax:
            if self.marker.position is not None:
                self.marker.kalmanfilter.calibrateSensor(self.marker.position[0],
                                                     self.marker.position[1],
                                                     self.counterR,
                                                     self.CalibMax)
                # print self.counterR
                self.counterR = self.counterR + 1;
                self.sensorProgress.setValue(self.counterR)
                self.CalibRBtn.setEnabled(False)
        else:
            self.sensorProgress.setValue(self.CalibMax)
            print "calibration done"
            self.CalibRBtn.setEnabled(True)
            self.counterR = 0
            sip.delete(self.timerR)
        # self.update()


    def measureProg(self):
        if self.counterM <= self.CalibMax:
            if self.counterM == 1:
                self.CalibQBtn.setEnabled(False)
            self.marker.kalmanfilter.calibrateQ(self.counterM, self.CalibMax)
            # print self.counterM
            self.counterM = self.counterM + 1;
            self.measurementProgress.setValue(self.counterM)
        else:
            self.measurementProgress.setValue(self.CalibMax)
            print "calibration done"
            self.CalibQBtn.setEnabled(True)
            self.counterM = 0
            sip.delete(self.timerM)

    def update(self):
        if self.label is None:
            print "Empty tab! This should not have happened!"
            return

        if not self.label == self.marker.label:
            self.label = self.marker.label

        if self.marker.pos_hist and self.marker.pos_hist[-1]:
            self.lbl_x.setText(str(int(self.marker.pos_hist[-1][0])))
            self.lbl_y.setText(str(int(self.marker.pos_hist[-1][1])))
        else:
            self.lbl_x.setText('---')
            self.lbl_y.setText('---')

        self.update_color_space()
        self.update_zoom()


    def enablePred(self):
        self.marker.guessing_enabled=self.ckb_prediction.isChecked()

    def enableKF(self, state):
        if state:
            print "enabling kalman filter"
            initpoint = self.marker.pos_hist[-1] if len(self.marker.pos_hist) > 0 else None
            self.marker.kalmanfilter.start_filter(initpoint)
            # print "Rk", self.marker.kalmanfilter.Rk
            # print "Qk", self.marker.kalmanfilter.Qk
            self.marker.filtering_enabled = True
            self.ckb_prediction.setEnabled(True)
            #self.recalibrateBtn.setEnabled(True)
            self.enable_adaptive.setEnabled(True)
            self.CalibQBtn.setEnabled(True)

        else:
            self.marker.filtering_enabled = False
            self.marker.kalmanfilter.stop_filter()
            self.ckb_prediction.setEnabled(False)
            #self.recalibrateBtn.setEnabled(False)
            self.enable_adaptive.setEnabled(False)
            self.CalibQBtn.setEnabled(False)

    def adaptiveKF(self, state):
        self.marker.adaptiveKF=state

    def update_led(self):
        self.marker.range_hue = (self.spin_hue_min.value(), self.spin_hue_max.value())
        self.marker.range_sat = (self.spin_sat_min.value(), self.spin_sat_max.value())
        self.marker.range_val = (self.spin_val_min.value(), self.spin_val_max.value())
        self.marker.range_area = (self.spin_area_min.value(), self.spin_area_max.value())
        self.marker.detection_active = self.ckb_track.isChecked()
        self.marker.fixed_pos = self.ckb_fixed_pos.isChecked()
        self.marker.marker_visible = self.ckb_marker.isChecked()

    def update_color_space(self):
        """ Update fancy color thingy if range_hue of marker has changed. """
        if self.current_range_hue == self.marker.range_hue:
            return
        self.log.debug("Mowing unicorn meadows.")

        # base CSS string
        style_sheet = "background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0"

        self.current_range_hue = self.marker.range_hue
        min_h = int(self.current_range_hue[0]*2)
        max_h = int(self.current_range_hue[1]*2)

        sv_inner = 255
        sv_outer = 80

        if min_h > max_h:
            min_h, max_h = max_h, min_h
            sv_outer, sv_inner = sv_inner, sv_outer

        epsilon = 0.0001  # Uh, sure...

        stops_pos = [1.0/6*p for p in xrange(0, 7)]
        stops_hue = [(60*p) % 360 for p in xrange(0, 7)]
        stops_sv = [sv_outer]*len(stops_hue)

        stops = zip(stops_pos, stops_hue, stops_sv)

        # TODO: Check that min_h and max_h are not equal

        if min_h in stops_hue:
            idx = stops_hue.index(min_h)
            stops.insert(idx+1, (stops_pos[idx]+epsilon, min_h, sv_inner))
        else:
            idx = int(min_h/60+1)
            stops.insert(idx, (min_h/360., min_h, sv_outer))
            stops.insert(idx, (min_h/360.+epsilon, min_h, sv_inner))

        if max_h in stops_hue:
            idx = stops_hue.index(max_h)
            stops.insert(idx+1, (stops_pos[idx]-epsilon, max_h, sv_inner))
        else:
            idx = int(max_h/60+1) + (2 if min_h not in stops_hue else 1)
            stops.insert(idx, (max_h/360.-epsilon, max_h, sv_inner))
            stops.insert(idx+1, (max_h/360., max_h, sv_outer))

        for idx, stop in enumerate(stops):
            if min_h < stop[1] < max_h:
                stops[idx] = (stop[0], stop[1], sv_inner)
        for stop in stops:
            style_sheet += ", stop:{0[0]} hsva({0[1]}, {0[2]}, {0[2]}, 255)".format(stop)
        style_sheet += ");"
        self.lbl_colorspace.setStyleSheet(style_sheet)

    def pick_color(self, state):
        """ Enable forwarding of events to process for color picker. """
        self.accept_events = state

    def update_zoom(self, size=24):
        """ 'Zoom' is the little preview window of the detected marker. """
        size /= 2
        if not None in [self.spotter.newest_frame, self.marker.position]:
            x, y = map(int, self.marker.position)
            (ax, ay), (bx, by) = (x-size, y-size), (x+size, y+size)
            h, w = self.spotter.newest_frame.img.shape[0:2]

            # check if box is too far left or right:
            # Esther says to do it the stupid way as I am wasting my time...
            if ax < 0:
                ax = 0
            if bx >= w-1:
                bx = w-1

            if ay < 0:
                ay = 0
            if by >= h-1:
                by = h-1

            # grab slice/view from numpy image array
            cutout = self.spotter.newest_frame.img[ay:by, ax:bx, :]
            cutout = cv2.cvtColor(cutout, cv2.cv.CV_BGR2RGB)
            cutout = cv2.resize(cutout, (self.lbl_zoom.width(), self.lbl_zoom.height()), interpolation=cv2.INTER_NEAREST)

            #convert numpy matrix to QPixmap via QImage, which can be efficiently shown via a label
            if cutout is not None:
                img = QtGui.QImage(cutout.data, cutout.shape[1], cutout.shape[0], QtGui.QImage.Format_RGB888)
                self.lbl_zoom.setPixmap(QtGui.QPixmap.fromImage(img))

    def process_event(self, event_type, event):
        #print event_type
        if event_type == 'mousePress':
            x = int(event.x())
            y = int(event.y())
            pixel = self.spotter.newest_frame.img[y, x, :]
            #print pixel
            print "[X,Y][B G R](H, S, V):", [x, y], pixel, utils.BGRpix2HSV(pixel)

    def closeEvent(self, close_event):
        self.spotter.tracker.remove_led(self.marker)
