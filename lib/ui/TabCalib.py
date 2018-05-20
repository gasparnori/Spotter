# -*- coding: utf-8 -*-
"""
Created on Sun Jan 18 21:13:54 2013
@author: <Ronny Eichler> ronny.eichler@gmail.com


"""
import logging

from PyQt4 import QtGui
from PyQt4.QtGui import QMessageBox
from tab_calibrationUi import Ui_tab_calibrate
from PyQt4 import QtCore
import numpy as np
import CalibrationPopUp
import sip

class Tab(QtGui.QWidget, Ui_tab_calibrate):

    label = None
    serial = None
    accept_events = False
    tab_type = "calibration"

    def __init__(self, writer_ref, label=None, *args, **kwargs):
        QtGui.QWidget.__init__(self)
        self.log = logging.getLogger(__name__)
        self.setupUi(self)
        self.writer = writer_ref

        assert 'spotter' in kwargs
        self.spotter = kwargs['spotter']

        self.label = "Calibration"

        assert 'update_all_tabs' in kwargs
        self.refresh_sidebar = kwargs['update_all_tabs']

        self.counterR=0
        self.counterM=0
        self.max=100
        self.speed=100
        self.connect(self.CalibRBtn, QtCore.SIGNAL('clicked()'), self.sensorCalib)
        self.connect(self.CalibQBtn, QtCore.SIGNAL('clicked()'), self.measurementCalib)
        self.sensorProgress.setVisible(False)
        self.sensorProgress.setMaximum(self.max)
        self.measurementProgress.setVisible(False)
        self.measurementProgress.setMaximum(self.max)


        #self.update()
    def sensorCalib(self):
        if len(self.spotter.tracker.leds)>0:
            popup=QMessageBox.information(self, "Sensor calibration",
                                          "Please keep the LED's in a fixed position. The calibration takes half a minute.",
                                          QMessageBox.Ok)
            self.timerR = QtCore.QTimer()
            self.connect(self.timerR, QtCore.SIGNAL('timeout()'), self.sensorProg)
            self.timerR.start(self.speed)
            self.sensorProgress.setVisible(True)
            self.sensorProgress.setValue(0)
        else:
            popup = QMessageBox.information(self, "Sensor calibration",
                                            "In order to calibrate the sensor, you first need to define at least one Feature",
                                            QMessageBox.Ok)

        #calib=CalibrationPopUp.CalibPopUp(self, 30)
        #calib.show()
    def measurementCalib(self):
        if len(self.spotter.tracker.leds) > 0:
            popup = QMessageBox.information(self, "Measurement calibration",
                                            "Please move the LED's around . The calibration takes half a minute.",
                                            QMessageBox.Ok)
            self.timerM = QtCore.QTimer()
            self.connect(self.timerM, QtCore.SIGNAL('timeout()'), self.measureProg)
            self.timerM.start(self.speed)
            self.measurementProgress.setVisible(True)
            self.measurementProgress.setValue(0)
        else:
            popup = QMessageBox.information(self, "Measurement calibration",
                                            "In order to calibrate the sensor, you first need to define at least one Feature",
                                            QMessageBox.Ok)

    def sensorProg(self):
        if self.counterR <= self.max:
            for led in self.spotter.tracker.leds:
                if led.position is not None:
                   # print led.position[0], led.position[1], self.speed
                    led.kalmanfilter.calibrateSensor(led.position[0],
                                                     led.position[1],
                                                     self.speed,
                                                     self.counterR,
                                                     self.max)
            #print self.counterR
            self.counterR = self.counterR + 1;
            self.sensorProgress.setValue(self.counterR)
            self.CalibRBtn.setEnabled(False)
        else:
            self.sensorProgress.setValue(self.max)
            print "calibration done"
            self.CalibRBtn.setEnabled(True)
            self.counterR = 0
            sip.delete(self.timerR)
        #self.update()
    def measureProg(self):
        if self.counterM <= self.max:
            for led in self.spotter.tracker.leds:
                if led.position is not None:
                   # print led.position[0], led.position[1], self.speed
                    led.kalmanfilter.calibrateQ(led.position[0],
                                                     led.position[1],
                                                     self.speed,
                                                     self.counterM,
                                                     self.max)
            #print self.counterM
            self.counterM = self.counterM + 1;
            self.measurementProgress.setValue(self.counterM)
            self.CalibQBtn.setEnabled(False)
        else:
            self.measurementProgress.setValue(self.max)
            print "calibration done"
            self.CalibQBtn.setEnabled(True)
            self.counterM = 0
            sip.delete(self.timerM)
        #self.update()

    def update(self):

        pass
        #if self.serial.is_connected():
        #    if not self.btn_serial_connect.isChecked():
        #        self.btn_serial_connect.setText('Disconnect')
        #        self.btn_serial_connect.setChecked(True)
        #    # Human readable values of bytes sent/received
        #    tx = utils.binary_prefix(self.serial.bytes_tx())
        #    rx = utils.binary_prefix(self.serial.bytes_rx())
        #    self.lbl_bytes_sent.setText(tx)
        #    self.lbl_bytes_received.setText(rx)
        #else:
        #    self.btn_serial_connect.setText('Connect')
        #    self.btn_serial_connect.setChecked(False)

    #def refresh_port_list(self):
    #    """ Populates the list of available serial ports in the machine.
    #    May not work under windows at all. Would then require the user to
    #    provide the proper port. Either via command line or typing it into the
    #    combobox.
    #    """
    #    candidate = None
    #    for i in range(self.combo_serialports.count()):
    #        self.combo_serialports.removeItem(0)
    #    for p in utils.get_port_list():
    #        if len(p) > 2 and "USB" in p[2]:
    #            candidate = p
    #        self.combo_serialports.addItem(p[0])
    #    if candidate:
    #        self.combo_serialports.setCurrentIndex(self.combo_serialports.findText(candidate[0]))

    #def toggle_connection(self):
    #    """
    #    Toggle button to either connect or disconnect serial connection.
    #    """
    #    # This test is inverted. When the function is called the button is
    #    # already pressed, i.e. checked -> representing future state, not past
    #    if not self.btn_serial_connect.isChecked():
    #        self.btn_serial_connect.setText('Connect')
    #        self.btn_serial_connect.setChecked(False)
    #        self.serial.close()
    #        # FIXME: Missing! Connect signal to trigger
    #        self.update_all_tabs()
    #    else:
    #        self.serial.serial_port = str(self.combo_serialports.currentText())
    #        try:
    #            sc = self.serial.auto_connect(self.serial.serial_port)
    #        except Exception, e:
    #            print e
    #            self.btn_serial_connect.setChecked(False)
    #            return
    #        if sc:
    #            self.btn_serial_connect.setText('Disconnect')
    #            self.btn_serial_connect.setChecked(True)
    #            # FIXME: Missing! Connect signal to trigger
    #            self.update_all_tabs()

    def closeEvent(self, QCloseEvent):
        # Source tab shall be invincible!
        return False