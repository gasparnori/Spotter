# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_calibrationUi.ui'
#
# Created: Wed May 30 18:12:27 2018
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_tab_calibrate(object):
    def setupUi(self, tab_calibrate):
        tab_calibrate.setObjectName(_fromUtf8("tab_calibrate"))
        tab_calibrate.resize(456, 433)
        self.gridLayout = QtGui.QGridLayout(tab_calibrate)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.toolBox = QtGui.QToolBox(tab_calibrate)
        self.toolBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtGui.QFrame.Plain)
        self.toolBox.setLineWidth(0)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_record = QtGui.QWidget()
        self.page_record.setGeometry(QtCore.QRect(0, 0, 454, 410))
        self.page_record.setObjectName(_fromUtf8("page_record"))
        self.gridLayout_6 = QtGui.QGridLayout(self.page_record)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, 50, -1, 50)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.ResetBtn = QtGui.QPushButton(self.page_record)
        self.ResetBtn.setObjectName(_fromUtf8("ResetBtn"))
        self.gridLayout_3.addWidget(self.ResetBtn, 5, 1, 1, 1)
        self.SaveBtn = QtGui.QPushButton(self.page_record)
        self.SaveBtn.setObjectName(_fromUtf8("SaveBtn"))
        self.gridLayout_3.addWidget(self.SaveBtn, 5, 0, 1, 1)
        self.CalibQBtn = QtGui.QPushButton(self.page_record)
        self.CalibQBtn.setObjectName(_fromUtf8("CalibQBtn"))
        self.gridLayout_3.addWidget(self.CalibQBtn, 3, 0, 1, 1)
        self.CalibRBtn = QtGui.QPushButton(self.page_record)
        self.CalibRBtn.setObjectName(_fromUtf8("CalibRBtn"))
        self.gridLayout_3.addWidget(self.CalibRBtn, 0, 0, 1, 1)
        self.measurementProgress = QtGui.QProgressBar(self.page_record)
        self.measurementProgress.setProperty("value", 24)
        self.measurementProgress.setObjectName(_fromUtf8("measurementProgress"))
        self.gridLayout_3.addWidget(self.measurementProgress, 3, 1, 1, 1)
        self.sensorProgress = QtGui.QProgressBar(self.page_record)
        self.sensorProgress.setProperty("value", 24)
        self.sensorProgress.setObjectName(_fromUtf8("sensorProgress"))
        self.gridLayout_3.addWidget(self.sensorProgress, 0, 1, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_6.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_record, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.toolBox, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(tab_calibrate)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)
        QtCore.QMetaObject.connectSlotsByName(tab_calibrate)

    def retranslateUi(self, tab_calibrate):
        tab_calibrate.setWindowTitle(_translate("tab_calibrate", "Form", None))
        self.ResetBtn.setText(_translate("tab_calibrate", "Reset all", None))
        self.SaveBtn.setText(_translate("tab_calibrate", "Save", None))
        self.CalibQBtn.setText(_translate("tab_calibrate", "Calibrate measurement", None))
        self.CalibRBtn.setText(_translate("tab_calibrate", "Calibrate sensor error", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_record), _translate("tab_calibrate", "Recording parameters", None))

import images_rc
