# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_markersUi.ui'
#
# Created: Tue Aug 28 10:36:50 2018
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

class Ui_tab_markers(object):
    def setupUi(self, tab_markers):
        tab_markers.setObjectName(_fromUtf8("tab_markers"))
        tab_markers.resize(813, 613)
        self.gridLayout = QtGui.QGridLayout(tab_markers)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.toolBox = QtGui.QToolBox(tab_markers)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_marker_detection = QtGui.QWidget()
        self.page_marker_detection.setGeometry(QtCore.QRect(0, 0, 811, 553))
        self.page_marker_detection.setObjectName(_fromUtf8("page_marker_detection"))
        self.gridLayout_6 = QtGui.QGridLayout(self.page_marker_detection)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.layout_feature_parameters = QtGui.QGridLayout()
        self.layout_feature_parameters.setSpacing(0)
        self.layout_feature_parameters.setObjectName(_fromUtf8("layout_feature_parameters"))
        self.spin_hue_min = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_hue_min.setWrapping(True)
        self.spin_hue_min.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_hue_min.setAccelerated(True)
        self.spin_hue_min.setMaximum(179)
        self.spin_hue_min.setObjectName(_fromUtf8("spin_hue_min"))
        self.layout_feature_parameters.addWidget(self.spin_hue_min, 1, 2, 1, 1)
        self.lbl_max = QtGui.QLabel(self.page_marker_detection)
        self.lbl_max.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_max.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_max.setObjectName(_fromUtf8("lbl_max"))
        self.layout_feature_parameters.addWidget(self.lbl_max, 0, 3, 1, 1)
        self.lbl_min = QtGui.QLabel(self.page_marker_detection)
        self.lbl_min.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lbl_min.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_min.setObjectName(_fromUtf8("lbl_min"))
        self.layout_feature_parameters.addWidget(self.lbl_min, 0, 2, 1, 1)
        self.spin_sat_min = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_sat_min.setWrapping(True)
        self.spin_sat_min.setFrame(True)
        self.spin_sat_min.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_sat_min.setAccelerated(True)
        self.spin_sat_min.setMaximum(255)
        self.spin_sat_min.setObjectName(_fromUtf8("spin_sat_min"))
        self.layout_feature_parameters.addWidget(self.spin_sat_min, 2, 2, 1, 1)
        self.spin_area_max = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_area_max.setMaximum(99999)
        self.spin_area_max.setObjectName(_fromUtf8("spin_area_max"))
        self.layout_feature_parameters.addWidget(self.spin_area_max, 4, 3, 1, 1)
        self.spin_val_min = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_val_min.setWrapping(True)
        self.spin_val_min.setFrame(True)
        self.spin_val_min.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_val_min.setAccelerated(True)
        self.spin_val_min.setMaximum(255)
        self.spin_val_min.setObjectName(_fromUtf8("spin_val_min"))
        self.layout_feature_parameters.addWidget(self.spin_val_min, 3, 2, 1, 1)
        self.spin_hue_max = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_hue_max.setWrapping(True)
        self.spin_hue_max.setFrame(True)
        self.spin_hue_max.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_hue_max.setAccelerated(True)
        self.spin_hue_max.setMaximum(179)
        self.spin_hue_max.setObjectName(_fromUtf8("spin_hue_max"))
        self.layout_feature_parameters.addWidget(self.spin_hue_max, 1, 3, 1, 1)
        self.lbl_sat = QtGui.QLabel(self.page_marker_detection)
        self.lbl_sat.setMargin(2)
        self.lbl_sat.setObjectName(_fromUtf8("lbl_sat"))
        self.layout_feature_parameters.addWidget(self.lbl_sat, 2, 1, 1, 1)
        self.lbl_val = QtGui.QLabel(self.page_marker_detection)
        self.lbl_val.setMargin(2)
        self.lbl_val.setObjectName(_fromUtf8("lbl_val"))
        self.layout_feature_parameters.addWidget(self.lbl_val, 3, 1, 1, 1)
        self.lbl_min_area = QtGui.QLabel(self.page_marker_detection)
        self.lbl_min_area.setMargin(2)
        self.lbl_min_area.setObjectName(_fromUtf8("lbl_min_area"))
        self.layout_feature_parameters.addWidget(self.lbl_min_area, 4, 1, 1, 1)
        self.lbl_hue = QtGui.QLabel(self.page_marker_detection)
        self.lbl_hue.setMargin(2)
        self.lbl_hue.setObjectName(_fromUtf8("lbl_hue"))
        self.layout_feature_parameters.addWidget(self.lbl_hue, 1, 1, 1, 1)
        self.spin_sat_max = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_sat_max.setWrapping(True)
        self.spin_sat_max.setFrame(True)
        self.spin_sat_max.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_sat_max.setAccelerated(True)
        self.spin_sat_max.setMaximum(255)
        self.spin_sat_max.setObjectName(_fromUtf8("spin_sat_max"))
        self.layout_feature_parameters.addWidget(self.spin_sat_max, 2, 3, 1, 1)
        self.spin_val_max = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_val_max.setWrapping(True)
        self.spin_val_max.setFrame(True)
        self.spin_val_max.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.spin_val_max.setAccelerated(True)
        self.spin_val_max.setMaximum(255)
        self.spin_val_max.setObjectName(_fromUtf8("spin_val_max"))
        self.layout_feature_parameters.addWidget(self.spin_val_max, 3, 3, 1, 1)
        self.line_2 = QtGui.QFrame(self.page_marker_detection)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.layout_feature_parameters.addWidget(self.line_2, 0, 4, 8, 1)
        self.spin_area_min = QtGui.QSpinBox(self.page_marker_detection)
        self.spin_area_min.setMaximum(99999)
        self.spin_area_min.setObjectName(_fromUtf8("spin_area_min"))
        self.layout_feature_parameters.addWidget(self.spin_area_min, 4, 2, 1, 1)
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.lbl_xlbl = QtGui.QLabel(self.page_marker_detection)
        self.lbl_xlbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_xlbl.setObjectName(_fromUtf8("lbl_xlbl"))
        self.gridLayout_5.addWidget(self.lbl_xlbl, 1, 0, 1, 1)
        self.lbl_x = QtGui.QLabel(self.page_marker_detection)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_x.sizePolicy().hasHeightForWidth())
        self.lbl_x.setSizePolicy(sizePolicy)
        self.lbl_x.setMinimumSize(QtCore.QSize(32, 0))
        self.lbl_x.setMaximumSize(QtCore.QSize(32, 16777215))
        self.lbl_x.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_x.setMargin(1)
        self.lbl_x.setObjectName(_fromUtf8("lbl_x"))
        self.gridLayout_5.addWidget(self.lbl_x, 1, 1, 1, 1)
        self.lbl_y_lbl = QtGui.QLabel(self.page_marker_detection)
        self.lbl_y_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_y_lbl.setObjectName(_fromUtf8("lbl_y_lbl"))
        self.gridLayout_5.addWidget(self.lbl_y_lbl, 1, 2, 1, 1)
        self.lbl_y = QtGui.QLabel(self.page_marker_detection)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_y.sizePolicy().hasHeightForWidth())
        self.lbl_y.setSizePolicy(sizePolicy)
        self.lbl_y.setMinimumSize(QtCore.QSize(32, 0))
        self.lbl_y.setMaximumSize(QtCore.QSize(32, 16777215))
        self.lbl_y.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_y.setMargin(1)
        self.lbl_y.setObjectName(_fromUtf8("lbl_y"))
        self.gridLayout_5.addWidget(self.lbl_y, 1, 3, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.lbl_zoom = QtGui.QLabel(self.page_marker_detection)
        self.lbl_zoom.setMinimumSize(QtCore.QSize(96, 96))
        self.lbl_zoom.setMaximumSize(QtCore.QSize(96, 96))
        self.lbl_zoom.setText(_fromUtf8(""))
        self.lbl_zoom.setScaledContents(True)
        self.lbl_zoom.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_zoom.setObjectName(_fromUtf8("lbl_zoom"))
        self.gridLayout_4.addWidget(self.lbl_zoom, 0, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 2, 0, 1, 4)
        self.layout_feature_parameters.addLayout(self.gridLayout_5, 0, 5, 6, 1)
        self.btn_pick_color = QtGui.QPushButton(self.page_marker_detection)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_pick_color.sizePolicy().hasHeightForWidth())
        self.btn_pick_color.setSizePolicy(sizePolicy)
        self.btn_pick_color.setCheckable(True)
        self.btn_pick_color.setFlat(False)
        self.btn_pick_color.setObjectName(_fromUtf8("btn_pick_color"))
        self.layout_feature_parameters.addWidget(self.btn_pick_color, 5, 1, 1, 3)
        self.gridLayout_6.addLayout(self.layout_feature_parameters, 9, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setContentsMargins(2, 0, -1, -1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.ckb_track = QtGui.QCheckBox(self.page_marker_detection)
        self.ckb_track.setChecked(True)
        self.ckb_track.setObjectName(_fromUtf8("ckb_track"))
        self.gridLayout_3.addWidget(self.ckb_track, 0, 0, 1, 1)
        self.ckb_marker = QtGui.QCheckBox(self.page_marker_detection)
        self.ckb_marker.setChecked(True)
        self.ckb_marker.setObjectName(_fromUtf8("ckb_marker"))
        self.gridLayout_3.addWidget(self.ckb_marker, 2, 0, 1, 1)
        self.ckb_fixed_pos = QtGui.QCheckBox(self.page_marker_detection)
        self.ckb_fixed_pos.setObjectName(_fromUtf8("ckb_fixed_pos"))
        self.gridLayout_3.addWidget(self.ckb_fixed_pos, 3, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_3, 7, 0, 1, 1)
        self.line = QtGui.QFrame(self.page_marker_detection)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_6.addWidget(self.line, 8, 0, 1, 1)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.lbl_colorspace = QtGui.QLabel(self.page_marker_detection)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_colorspace.sizePolicy().hasHeightForWidth())
        self.lbl_colorspace.setSizePolicy(sizePolicy)
        self.lbl_colorspace.setMaximumSize(QtCore.QSize(16777215, 32))
        self.lbl_colorspace.setStyleSheet(_fromUtf8("background-color:qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,stop:0 hsva(0, 255, 255, 255),stop:0.49 hsva(60, 255, 255, 255),stop:0.5 hsva(60, 255, 255, 255),stop:1 hsva(180, 255, 255, 255));"))
        self.lbl_colorspace.setFrameShape(QtGui.QFrame.StyledPanel)
        self.lbl_colorspace.setText(_fromUtf8(""))
        self.lbl_colorspace.setIndent(0)
        self.lbl_colorspace.setObjectName(_fromUtf8("lbl_colorspace"))
        self.verticalLayout_4.addWidget(self.lbl_colorspace)
        self.gridLayout_6.addLayout(self.verticalLayout_4, 10, 0, 1, 1)
        self.toolBox.addItem(self.page_marker_detection, _fromUtf8(""))
        self.page_feature_IO = QtGui.QWidget()
        self.page_feature_IO.setGeometry(QtCore.QRect(0, 0, 235, 124))
        self.page_feature_IO.setObjectName(_fromUtf8("page_feature_IO"))
        self.gridLayout_7 = QtGui.QGridLayout(self.page_feature_IO)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.pushButton_12 = QtGui.QPushButton(self.page_feature_IO)
        self.pushButton_12.setEnabled(False)
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.gridLayout_9.addWidget(self.pushButton_12, 1, 1, 1, 1)
        self.pushButton_13 = QtGui.QPushButton(self.page_feature_IO)
        self.pushButton_13.setEnabled(False)
        self.pushButton_13.setObjectName(_fromUtf8("pushButton_13"))
        self.gridLayout_9.addWidget(self.pushButton_13, 2, 1, 1, 1)
        self.pushButton_14 = QtGui.QPushButton(self.page_feature_IO)
        self.pushButton_14.setEnabled(False)
        self.pushButton_14.setObjectName(_fromUtf8("pushButton_14"))
        self.gridLayout_9.addWidget(self.pushButton_14, 2, 0, 1, 1)
        self.pushButton_15 = QtGui.QPushButton(self.page_feature_IO)
        self.pushButton_15.setEnabled(False)
        self.pushButton_15.setObjectName(_fromUtf8("pushButton_15"))
        self.gridLayout_9.addWidget(self.pushButton_15, 1, 0, 1, 1)
        self.combo_label = QtGui.QComboBox(self.page_feature_IO)
        self.combo_label.setEnabled(False)
        self.combo_label.setEditable(True)
        self.combo_label.setObjectName(_fromUtf8("combo_label"))
        self.gridLayout_9.addWidget(self.combo_label, 0, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem, 3, 0, 2, 2)
        self.gridLayout_7.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_feature_IO, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.toolBox, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(tab_markers)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)
        QtCore.QMetaObject.connectSlotsByName(tab_markers)
        tab_markers.setTabOrder(self.spin_hue_min, self.spin_hue_max)
        tab_markers.setTabOrder(self.spin_hue_max, self.spin_sat_min)
        tab_markers.setTabOrder(self.spin_sat_min, self.spin_sat_max)
        tab_markers.setTabOrder(self.spin_sat_max, self.spin_val_min)
        tab_markers.setTabOrder(self.spin_val_min, self.spin_val_max)
        tab_markers.setTabOrder(self.spin_val_max, self.spin_area_min)
        tab_markers.setTabOrder(self.spin_area_min, self.spin_area_max)
        tab_markers.setTabOrder(self.spin_area_max, self.btn_pick_color)
        tab_markers.setTabOrder(self.btn_pick_color, self.pushButton_12)
        tab_markers.setTabOrder(self.pushButton_12, self.pushButton_13)
        tab_markers.setTabOrder(self.pushButton_13, self.pushButton_14)
        tab_markers.setTabOrder(self.pushButton_14, self.pushButton_15)
        tab_markers.setTabOrder(self.pushButton_15, self.combo_label)

    def retranslateUi(self, tab_markers):
        tab_markers.setWindowTitle(_translate("tab_markers", "Form", None))
        self.lbl_max.setText(_translate("tab_markers", "Max", None))
        self.lbl_min.setText(_translate("tab_markers", "Min", None))
        self.lbl_sat.setText(_translate("tab_markers", "Sat", None))
        self.lbl_val.setText(_translate("tab_markers", "Val", None))
        self.lbl_min_area.setText(_translate("tab_markers", "<html><head/><body><p>px<span style=\" vertical-align:super;\">2</span></p></body></html>", None))
        self.lbl_hue.setText(_translate("tab_markers", "Hue", None))
        self.lbl_xlbl.setText(_translate("tab_markers", "x:", None))
        self.lbl_x.setText(_translate("tab_markers", "---", None))
        self.lbl_y_lbl.setText(_translate("tab_markers", "y:", None))
        self.lbl_y.setText(_translate("tab_markers", "---", None))
        self.btn_pick_color.setToolTip(_translate("tab_markers", "Pick thresholds from image by dragging frame around the spot of interest", None))
        self.btn_pick_color.setStatusTip(_translate("tab_markers", "Pick range from image", None))
        self.btn_pick_color.setText(_translate("tab_markers", "&Pick", None))
        self.ckb_track.setText(_translate("tab_markers", "Detection Active", None))
        self.ckb_marker.setText(_translate("tab_markers", "Show Marker", None))
        self.ckb_fixed_pos.setText(_translate("tab_markers", "Fixed Position", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_marker_detection), _translate("tab_markers", "Detection", None))
        self.pushButton_12.setText(_translate("tab_markers", "Save", None))
        self.pushButton_13.setText(_translate("tab_markers", "Delete", None))
        self.pushButton_14.setText(_translate("tab_markers", "Clone", None))
        self.pushButton_15.setText(_translate("tab_markers", "Open", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_feature_IO), _translate("tab_markers", "In/Out", None))

