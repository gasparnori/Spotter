# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_recordUi.ui'
#
# Created: Mon Apr 09 19:19:21 2018
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

class Ui_tab_record(object):
    def setupUi(self, tab_record):
        tab_record.setObjectName(_fromUtf8("tab_record"))
        tab_record.resize(456, 433)
        self.gridLayout = QtGui.QGridLayout(tab_record)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.toolBox = QtGui.QToolBox(tab_record)
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
        self.DestFolderLabel = QtGui.QLabel(self.page_record)
        self.DestFolderLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.DestFolderLabel.setObjectName(_fromUtf8("DestFolderLabel"))
        self.verticalLayout.addWidget(self.DestFolderLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.DestFolderInput = QtGui.QLineEdit(self.page_record)
        self.DestFolderInput.setMaximumSize(QtCore.QSize(636, 16777215))
        self.DestFolderInput.setObjectName(_fromUtf8("DestFolderInput"))
        self.horizontalLayout.addWidget(self.DestFolderInput)
        self.DestFolderBtn = QtGui.QPushButton(self.page_record)
        self.DestFolderBtn.setObjectName(_fromUtf8("DestFolderBtn"))
        self.horizontalLayout.addWidget(self.DestFolderBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.FileNameLabel = QtGui.QLabel(self.page_record)
        self.FileNameLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.FileNameLabel.setObjectName(_fromUtf8("FileNameLabel"))
        self.verticalLayout.addWidget(self.FileNameLabel)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.FileNameInput = QtGui.QLineEdit(self.page_record)
        self.FileNameInput.setObjectName(_fromUtf8("FileNameInput"))
        self.horizontalLayout_2.addWidget(self.FileNameInput)
        self.FileNameBtn = QtGui.QPushButton(self.page_record)
        self.FileNameBtn.setObjectName(_fromUtf8("FileNameBtn"))
        self.horizontalLayout_2.addWidget(self.FileNameBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.SaveBtn = QtGui.QPushButton(self.page_record)
        self.SaveBtn.setObjectName(_fromUtf8("SaveBtn"))
        self.horizontalLayout_3.addWidget(self.SaveBtn)
        self.ResetBtn = QtGui.QPushButton(self.page_record)
        self.ResetBtn.setObjectName(_fromUtf8("ResetBtn"))
        self.horizontalLayout_3.addWidget(self.ResetBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_6.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_record, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.toolBox, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(tab_record)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)
        QtCore.QMetaObject.connectSlotsByName(tab_record)

    def retranslateUi(self, tab_record):
        tab_record.setWindowTitle(_translate("tab_record", "Form", None))
        self.DestFolderLabel.setText(_translate("tab_record", "Destination folder:", None))
        self.DestFolderBtn.setText(_translate("tab_record", "Reset to default", None))
        self.FileNameLabel.setText(_translate("tab_record", "File name:", None))
        self.FileNameBtn.setText(_translate("tab_record", "Clear", None))
        self.SaveBtn.setText(_translate("tab_record", "Save", None))
        self.ResetBtn.setText(_translate("tab_record", "Reset all", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_record), _translate("tab_record", "Recording parameters", None))

import images_rc
