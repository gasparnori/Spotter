# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Spotter_development\lib\ui\tab_sourceUi.ui'
#
# Created: Mon Nov 06 20:29:50 2017
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_tab_source(object):
    def setupUi(self, tab_source):
        tab_source.setObjectName(_fromUtf8("tab_source"))
        tab_source.resize(245, 432)
        self.gridLayout = QtGui.QGridLayout(tab_source)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.toolBox = QtGui.QToolBox(tab_source)
        self.toolBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtGui.QFrame.Plain)
        self.toolBox.setLineWidth(0)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_source = QtGui.QWidget()
        self.page_source.setGeometry(QtCore.QRect(0, 0, 243, 409))
        self.page_source.setObjectName(_fromUtf8("page_source"))
        self.gridLayout_6 = QtGui.QGridLayout(self.page_source)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 50, -1, 50)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButton = QtGui.QPushButton(self.page_source)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.FrameSettingsLabel = QtGui.QLabel(self.page_source)
        self.FrameSettingsLabel.setObjectName(_fromUtf8("FrameSettingsLabel"))
        self.verticalLayout.addWidget(self.FrameSettingsLabel, QtCore.Qt.AlignBottom)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.HeightInput = QtGui.QSpinBox(self.page_source)
        self.HeightInput.setMinimum(1)
        self.HeightInput.setMaximum(1200)
        self.HeightInput.setProperty("value", 720)
        self.HeightInput.setObjectName(_fromUtf8("HeightInput"))
        self.gridLayout_3.addWidget(self.HeightInput, 1, 1, 1, 1)
        self.WidthInput = QtGui.QSpinBox(self.page_source)
        self.WidthInput.setMinimum(1)
        self.WidthInput.setMaximum(1280)
        self.WidthInput.setProperty("value", 1280)
        self.WidthInput.setObjectName(_fromUtf8("WidthInput"))
        self.gridLayout_3.addWidget(self.WidthInput, 0, 1, 1, 1)
        self.FrameHeightLabel = QtGui.QLabel(self.page_source)
        self.FrameHeightLabel.setObjectName(_fromUtf8("FrameHeightLabel"))
        self.gridLayout_3.addWidget(self.FrameHeightLabel, 1, 0, 1, 1)
        self.FrameWidthLabel = QtGui.QLabel(self.page_source)
        self.FrameWidthLabel.setObjectName(_fromUtf8("FrameWidthLabel"))
        self.gridLayout_3.addWidget(self.FrameWidthLabel, 0, 0, 1, 1)
        self.FPSLabel = QtGui.QLabel(self.page_source)
        self.FPSLabel.setObjectName(_fromUtf8("FPSLabel"))
        self.gridLayout_3.addWidget(self.FPSLabel, 2, 0, 1, 1)
        self.FPSInput = QtGui.QSpinBox(self.page_source)
        self.FPSInput.setMinimum(1)
        self.FPSInput.setMaximum(300)
        self.FPSInput.setProperty("value", 200)
        self.FPSInput.setObjectName(_fromUtf8("FPSInput"))
        self.gridLayout_3.addWidget(self.FPSInput, 2, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 4, 0, 1, 1)
        self.scaleInput = QtGui.QDoubleSpinBox(self.page_source)
        self.scaleInput.setMaximum(1.0)
        self.scaleInput.setSingleStep(0.1)
        self.scaleInput.setProperty("value", 0.5)
        self.scaleInput.setObjectName(_fromUtf8("scaleInput"))
        self.gridLayout_3.addWidget(self.scaleInput, 3, 1, 1, 1)
        self.scaleLabel = QtGui.QLabel(self.page_source)
        self.scaleLabel.setObjectName(_fromUtf8("scaleLabel"))
        self.gridLayout_3.addWidget(self.scaleLabel, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.SaveBtn = QtGui.QPushButton(self.page_source)
        self.SaveBtn.setObjectName(_fromUtf8("SaveBtn"))
        self.horizontalLayout_2.addWidget(self.SaveBtn)
        self.ResetBtn = QtGui.QPushButton(self.page_source)
        self.ResetBtn.setObjectName(_fromUtf8("ResetBtn"))
        self.horizontalLayout_2.addWidget(self.ResetBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_6.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_source, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.toolBox, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(tab_source)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)
        QtCore.QMetaObject.connectSlotsByName(tab_source)

    def retranslateUi(self, tab_source):
        tab_source.setWindowTitle(_translate("tab_source", "Form", None))
        self.pushButton.setText(_translate("tab_source", "Get current settings", None))
        self.FrameSettingsLabel.setText(_translate("tab_source", "Frame settings:", None))
        self.FrameHeightLabel.setText(_translate("tab_source", "Frame Height", None))
        self.FrameWidthLabel.setText(_translate("tab_source", "Frame Width", None))
        self.FPSLabel.setText(_translate("tab_source", "FPS", None))
        self.scaleLabel.setText(_translate("tab_source", "Resize scale", None))
        self.SaveBtn.setText(_translate("tab_source", "Save", None))
        self.ResetBtn.setText(_translate("tab_source", "Reset to default", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_source), _translate("tab_source", "Frame source parameters", None))

import images_rc
