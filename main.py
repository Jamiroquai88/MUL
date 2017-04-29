#! /usr/bin/env python

import sys
import os
import copy

import datetime
import sounddevice as sd
import scipy.io.wavfile as wf
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTime

from form import Ui_Form
from main_window import Ui_MusicSplitter
from vad import VAD


class MyTableModel(QtCore.QAbstractTableModel):
    """ Table model class.
    
    """
    def __init__(self, datain, headerdata, parent=None, *args):
        """ Class constructor.
        
        """
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        """ Get number of rows.
        
        """
        return len(self.arraydata)

    def columnCount(self, parent):
        """ Get number of columns.
        
        """
        return 0 if self.arraydata == [] else len(self.arraydata[0])

    def data(self, index, role):
        """ Set data.
        
        """
        if not index.isValid():
            return QtCore.QVariant()
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, o, role):
        """ Set header data.
        
        """
        if o == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.headerdata[col])
        return QtCore.QVariant()

    @staticmethod
    def setupColumns(table):
        h = table.horizontalHeader()
        h.setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        h.setResizeMode(1, QtGui.QHeaderView.Stretch)
        h.setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        h.setResizeMode(3, QtGui.QHeaderView.ResizeToContents)


class MyForm(QtGui.QMainWindow):
    """ Main form class.
    
    """
    def __init__(self, parent=None):
        """ Class constructor. 
        
        """
        QtGui.QWidget.__init__(self, parent)
        # VAD class
        self.vad = VAD()
        threshold = 0.4
        length = 5
        bandStart = 50
        self.vad.music_start_band = 50
        bandEnd = 3000
        self.vad.music_end_band = 3000
        minSongLen = 10
        self.vad.min_song_len = 10
        self.foundSongs = None
        # UI setup
        self.ui = Ui_MusicSplitter()
        self.ui.setupUi(self)
        self.ui.browseButton.clicked.connect(self.HandleBrowseButton)
        self.ui.processButton.clicked.connect(self.HandleProcessButton)
        self.ui.saveButton.clicked.connect(self.HandleSaveButton)
        self.ui.levelBox.setValue(threshold)
        self.ui.lengthBox.setValue(length)
        self.ui.bandStartBox.setValue(bandStart)
        self.ui.bandEndBox.setValue(bandEnd)
        self.ui.songLenBox.setValue(minSongLen)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setSelectionBehavior(QtGui.QTableView.SelectRows);
        self.ui.tableView.clicked.connect(self.HandleTableClicked)
        self.ui.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableModel = None
        # Class members
        self.inputFile = None

    def HandleTableClicked(self, clickedIndex):
        """ Handle clicked table.

        """
        index = clickedIndex.row()
        print index
        form = EditForm(self)
        song = copy.deepcopy(self.foundSongs[index])
        song[1] = os.path.join(os.path.dirname(str(self.inputFile)), str(song[1]))
        form.Init(song, self.vad.data, self.vad.bitrate)
        form.exec_()
        print form.result
        if form.result == []:
            self.foundSongs.pop(index)
            self.SetupTable(self.foundSongs)
        elif form.result is None:
            pass
        else:
            form.result[1] = os.path.join(os.path.dirname(str(self.inputFile)), form.result[1])
            form.result[1] = os.path.relpath(form.result[1], os.path.dirname(str(self.inputFile)))
            self.foundSongs[index] = form.result
            self.SetupTable(self.foundSongs)

    def HandleBrowseButton(self):
        """ Handle browse button, select input wav file and open it.

        """
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
        """ Handle button for audio processing.
        
        """
        self.foundSongs = None
        self.vad.thr = self.ui.levelBox.value()
        self.vad.sil_len = self.ui.lengthBox.value()
        if self.vad.thr > 0 and self.vad.sil_len > 0 and self.inputFile is not None:
            self.vad.music_start_band = self.ui.bandStartBox.value()
            self.vad.music_end_band = self.ui.bandEndBox.value()
            self.vad.min_song_len = self.ui.songLenBox.value()
            songs_list = self.vad.ProcessFile(self.inputFile)
            print 'Songs:', songs_list
            if songs_list is None:
                self.ShowInformationDialog('Can not process input file!')
            elif not songs_list:
                self.ShowInformationDialog('No songs found in input wav file!')
            else:
                self.SetupTable(songs_list)
        else:
            self.ShowInformationDialog(
                'Please, set input file and appropriate level and length.')

    def HandleSaveButton(self):
        """ Handle save all files button.
        
        """
        if self.foundSongs is not None:
            for x in self.foundSongs:
                print x
                name = os.path.join(os.path.dirname(str(self.inputFile)), x[1])
                start = EditForm.Time2Frames(x[2], self.vad.bitrate)
                end = EditForm.Time2Frames(x[3], self.vad.bitrate)
                wf.write(name, self.vad.bitrate, self.vad.data[start:end])
        else:
            MyForm.ShowInformationDialog('No results to save!')

    def SetupTable(self, data):
        """ Initialize table with data.
        
            :param data: table data
            :type data: list
        """
        self.foundSongs = data
        header = ['Num', 'File Name', 'Start', 'End']
        self.tableModel = MyTableModel(data, header, self)
        self.ui.tableView.setModel(self.tableModel)
        MyTableModel.setupColumns(self.ui.tableView)

    @staticmethod
    def ShowInformationDialog(text):
        """ Show simple information dialog.

        """
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(text)
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.exec_()


class EditForm(QtGui.QDialog):
    """ Edit one song - small dialog.
    
    """
    def __init__(self, parent=None):
        """ Class constructor.
        
        """
        super(EditForm, self).__init__(parent)
        # UI setup
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.saveButton.clicked.connect(self.HandleSaveButton)
        self.ui.okButton.clicked.connect(self.HandleOkButton)
        self.ui.resetButton.clicked.connect(self.HandleResetButton)
        self.ui.deleteButton.clicked.connect(self.HandleDeleteButton)
        self.ui.musicButton.clicked.connect(self.HandleMusicButton)
        self.ui.saveFileButton.clicked.connect(self.HandleSaveFileButton)
        self.ui.startTime.setDisplayFormat('hh:mm:ss')
        self.ui.endTime.setDisplayFormat('hh:mm:ss')
        self.ui.startTime.setMinimumTime(QTime(0, 0, 0))
        # Class members
        self.song = None
        self.data = None
        self.resetData = None
        self.bitrate = None
        self.name = None
        self.result = None
        self.index = None
        self.isPlaying = False

    def Init(self, song, data, bitrate):
        """ Initialize with song.
        
            :param song: input song
            :type song: list
            :param data: input data from wav file
            :type data: numpy.array
            :param bitrate: bitrate of input file
            :type bitrate: int
        """
        print song
        self.song = copy.deepcopy(song)
        self.index = self.song[0]
        self.name = self.song[1]
        self.ui.saveButton.setText(self.name)
        self.data = data
        self.resetData = copy.deepcopy(song)
        self.bitrate = bitrate
        h, m, s = EditForm.ParseTime(self.song[2])
        self.ui.startTime.setTime(QTime(h, m, s))
        h, m, s = EditForm.ParseTime(self.song[3])
        self.ui.endTime.setTime(QTime(h, m, s))
        end_time = datetime.timedelta(seconds=int(self.data.shape[0] / self.bitrate))
        print end_time
        h, m, s = EditForm.ParseTime(str(end_time))
        self.ui.endTime.setMaximumTime(QTime(h, m, s))

    def HandleSaveButton(self):
        """ Handle save button. Saves separate file.
        
        """
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        if len(name) > 0:
            self.name = name
            self.ui.saveButton.setText(name)

    def HandleOkButton(self):
        """ Handle ok button. Save changes to parent window(table).
        
        """
        start = str(self.ui.startTime.time().toString())
        end = str(self.ui.endTime.time().toString())
        self.result = [self.index, str(self.name), start, end]
        self.accept()

    def HandleResetButton(self):
        """ Handle reset button. Resets to default configuration.
        
        """
        self.ui.saveButton.setText(self.resetData[1])
        h, m, s = EditForm.ParseTime(self.resetData[2])
        self.ui.startTime.setTime(QTime(h, m, s))
        h, m, s = EditForm.ParseTime(self.resetData[3])
        self.ui.endTime.setTime(QTime(h, m, s))

    def HandleDeleteButton(self):
        """ Handle delete button. Deletes input row from table.
        
        """
        self.result = []
        self.accept()

    def HandleMusicButton(self):
        """ Handle music playing button. Play/Stop music by input interval.
        
        """
        if not self.isPlaying:
            self.ui.musicButton.setText('Stop')
            start = EditForm.Time2Frames(str(self.ui.startTime.time().toString()), self.bitrate)
            end = EditForm.Time2Frames(str(self.ui.endTime.time().toString()), self.bitrate)
            print start, end
            sd.play(self.data[start:end], self.bitrate)
            self.isPlaying = True
        else:
            self.ui.musicButton.setText('Play')
            sd.stop()
            self.isPlaying = False

    def HandleSaveFileButton(self):
        """ Handle separated save file button.
        
        """
        start = EditForm.Time2Frames(str(self.ui.startTime.time().toString()), self.bitrate)
        end = EditForm.Time2Frames(str(self.ui.endTime.time().toString()), self.bitrate)
        wf.write(self.name, self.bitrate, self.data[start:end])

    @staticmethod
    def ParseTime(time):
        """ Parse time in format hh:mm:ss.
        
            :param time: input time
            :type time: str
            :returns: hours, minutes, seconds
            :rtype: tuple
        """
        f = time.find(':')
        l = time.rfind(':')
        h = time[:f]
        m = time[f + 1:l]
        s = time[l + 1:]
        return int(h), int(m), int(s)

    @staticmethod
    def Time2Frames(time, freq):
        """ Transfer time in h:m:s string to index by frequency.
        
            :param time: input time
            :type time: str
            :param freq: input frequency
            :type freq: int
        """
        time = EditForm.ParseTime(time)
        sec = time[0] * 3600 + time[1] * 60 + time[2]
        return sec * freq


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())
