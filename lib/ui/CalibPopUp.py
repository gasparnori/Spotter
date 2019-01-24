# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CalibPopUp.ui'
#
# Created: Thu Jan 24 13:08:13 2019
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

class Ui_PopUp(object):
    def setupUi(self, PopUp):
        PopUp.setObjectName(_fromUtf8("PopUp"))
        PopUp.resize(600, 291)
        PopUp.setAutoFillBackground(False)
        self.gridLayoutWidget = QtGui.QWidget(PopUp)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 70, 556, 91))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progressBar = QtGui.QProgressBar(self.gridLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 1)
        self.StartBtn = QtGui.QPushButton(PopUp)
        self.StartBtn.setGeometry(QtCore.QRect(120, 190, 75, 23))
        self.StartBtn.setObjectName(_fromUtf8("StartBtn"))
        self.label = QtGui.QLabel(PopUp)
        self.label.setGeometry(QtCore.QRect(20, 60, 554, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.CancelBtn = QtGui.QPushButton(PopUp)
        self.CancelBtn.setGeometry(QtCore.QRect(300, 190, 75, 23))
        self.CancelBtn.setObjectName(_fromUtf8("CancelBtn"))

        self.retranslateUi(PopUp)
        QtCore.QMetaObject.connectSlotsByName(PopUp)

    def retranslateUi(self, PopUp):
        PopUp.setWindowTitle(_translate("PopUp", "Sensor calibration", None))
        self.StartBtn.setText(_translate("PopUp", "Start", None))
        self.label.setText(_translate("PopUp", "Please keep the LED\'s in a fixed position during calibration.", None))
        self.CancelBtn.setText(_translate("PopUp", "Cancel", None))

