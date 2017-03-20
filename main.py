#! /usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui

from main_window import Ui_MusicSplitter
from vad import VAD


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # UI setup
        self.ui = Ui_MusicSplitter()
        self.ui.setupUi(self)
        self.ui.browseButton.clicked.connect(self.HandleBrowseButton)
        self.ui.processButton.clicked.connect(self.HandleProcessButton)
        self.ui.levelBox.setValue(0.6)
        self.ui.lengthBox.setValue(5)
        # VAD class
        self.vad = VAD()
        # Class members
        self.inputFile = None

    def HandleBrowseButton(self):
        ''' Handle browse button, select input wav file and open it.

        '''
        f = QtGui.QFileDialog.getOpenFileName(self)
        try:
            self.inputFile = open(f, 'r')
            self.inputFile.close()
            self.inputFile = f
            self.ui.chosenFile.setText(f)
        except IOError:
            self.ShowInformationDialog('Can not open input file!')
            self.inputFile = None

    def HandleProcessButton(self):
        level = self.ui.levelBox.value()
        length = self.ui.lengthBox.value()
        if level > 0 and length > 0 and self.inputFile is not None:
            if self.vad.ProcessFile(self.inputFile, level, length) is None:
                self.ShowInformationDialog('Can not process input file!')
        else:
            self.ShowInformationDialog(
                'Please, set input file and appropriate level and length.')

    def ShowInformationDialog(self, text):
        ''' Show simple information dialog.

        '''
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(text)
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
