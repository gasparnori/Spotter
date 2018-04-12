# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statusBarUi.ui'
#
# Created: Thu Apr 12 11:53:22 2018
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

class Ui_statusBar(object):
    def setupUi(self, statusBar):
        statusBar.setObjectName(_fromUtf8("statusBar"))
        statusBar.resize(960, 40)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(statusBar)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lbl_fps = QtGui.QLabel(statusBar)
        self.lbl_fps.setMinimumSize(QtCore.QSize(55, 0))
        self.lbl_fps.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbl_fps.setObjectName(_fromUtf8("lbl_fps"))
        self.horizontalLayout_2.addWidget(self.lbl_fps)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.state = QtGui.QLabel(statusBar)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.state.setFont(font)
        self.state.setAutoFillBackground(False)
        self.state.setScaledContents(True)
        self.state.setObjectName(_fromUtf8("state"))
        self.horizontalLayout_2.addWidget(self.state)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.retranslateUi(statusBar)
        QtCore.QMetaObject.connectSlotsByName(statusBar)

    def retranslateUi(self, statusBar):
        statusBar.setWindowTitle(_translate("statusBar", "Form", None))
        self.lbl_fps.setToolTip(_translate("statusBar", "Interface refresh rate, NOT the acquisition rate if grabbing from a camera.", None))
        self.lbl_fps.setText(_translate("statusBar", "FPS: 100.0", None))
        self.state.setText(_translate("statusBar", "Camera", None))

