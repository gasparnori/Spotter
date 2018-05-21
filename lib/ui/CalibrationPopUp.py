from PyQt4 import QtCore, QtGui
from time import sleep
import sys, os
import sip
from CalibPopUp import Ui_PopUp

class CalibPopUp(QtGui.QWidget, Ui_PopUp):
    def __init__(self, parent=None, max_time=30):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(max_time)
        self.progressBar.setValue(0)
        self.counter = 0
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'),self.update_progress)
        self.CancelBtn.clicked.connect(self.cancel)
        self.StartBtn.clicked.connect(self.onStart)
        self.max=max_time

    def cancel(self):
        sip.delete(self.timer)
        self.close()

    def update_progress(self):
        if self.counter<self.max:
            self.counter=self.counter+1;
            self.progressBar.setValue(self.counter)
        else:
            self.progressBar.setValue(self.max)
            sip.delete(self.timer)
            self.close()

    def onStart(self):
        #self.progressBar.setRange(0,0)
        self.progressBar.setValue(0)
        print "timer started"
        self.timer.start(100)

if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     window = CalibPopUp()
     window.resize(640, 480)
     window.show()
     sys.exit(app.exec_())