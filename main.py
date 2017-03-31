#! /usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui

from main_window import Ui_MusicSplitter
from vad import VAD


class MyTableModel(QtCore.QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, o, role):
        if o == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        # VAD class
        self.vad = VAD()
        threshold = 0.4
        length = 5
        # UI setup
        self.ui = Ui_MusicSplitter()
        self.ui.setupUi(self)
        self.ui.browseButton.clicked.connect(self.HandleBrowseButton)
        self.ui.processButton.clicked.connect(self.HandleProcessButton)
        self.ui.levelBox.setValue(threshold)
        self.ui.lengthBox.setValue(length)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows);
        self.ui.tableView.clicked.connect(self.HandleTableClicked)
        self.ui.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # Class members
        self.inputFile = None

    def HandleTableClicked(self, clickedIndex):
        ''' Handle clicked table.

        '''
        print clickedIndex.row()

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
            songs_list = self.vad.ProcessFile(self.inputFile, level, length)
            print 'Songs:', songs_list
            if songs_list is None:
                self.ShowInformationDialog('Can not process input file!')
            elif songs_list == []:
                self.ShowInformationDialog('No songs found in input wav file!')
            else:
                header = ['Number', 'Name', 'Start', 'End']
                table_model = MyTableModel(songs_list, header, self)
                self.ui.tableView.setModel(table_model)
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
