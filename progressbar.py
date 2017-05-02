import time
import multiprocessing
from PyQt4 import QtCore, QtGui


class ProgressBar(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ProgressBar, self).__init__(parent)
        layout = QtGui.QVBoxLayout(self)
        self.setWindowTitle("Loading ...")

        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setRange(0, 100)
        layout.addWidget(self.progressBar)

        self.gui = GUIThread()
        self.gui.progressbar = self
        self.gui.start()

        self.thread = LoadingThread()
        self.thread.start()
        self.connect(self.thread, QtCore.SIGNAL('BAR_PROGRESS'), self.onProgress)
        self.connect(parent, QtCore.SIGNAL('BAR_PROGRESS'), self.onProgress)

        print 'main thread:', multiprocessing.current_process().name

    def onProgress(self, i):
        if i is None:
            self.thread.terminate()
            self.accept()
        else:
            self.progressBar.setValue(i)


class LoadingThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(LoadingThread, self).__init__(parent)

    def run(self):
        print 'START: executing loading thread', multiprocessing.current_process().name
        i = 0
        while True:
            self.emit(QtCore.SIGNAL('BAR_PROGRESS'), i % 100)
            time.sleep(0.005)
            i += 1


class GUIThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(GUIThread, self).__init__(parent)
        self.progressbar = None

    def run(self):
        print 'START: executing gui thread', multiprocessing.current_process().name
        self.progressbar.exec_()
        print 'FINISH: executing gui thread', multiprocessing.current_process().name
