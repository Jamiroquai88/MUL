# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MUL/mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_MusicSplitter(object):
    def setupUi(self, MusicSplitter):
        MusicSplitter.setObjectName(_fromUtf8("MusicSplitter"))
        MusicSplitter.resize(400, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MusicSplitter.sizePolicy().hasHeightForWidth())
        MusicSplitter.setSizePolicy(sizePolicy)
        self.centralWidget = QtGui.QWidget(MusicSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setMargin(11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.chosenFile = QtGui.QLabel(self.centralWidget)
        self.chosenFile.setText(_fromUtf8(""))
        self.chosenFile.setObjectName(_fromUtf8("chosenFile"))
        self.horizontalLayout_2.addWidget(self.chosenFile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.levelBox = QtGui.QDoubleSpinBox(self.centralWidget)
        self.levelBox.setMaximum(1.0)
        self.levelBox.setSingleStep(0.1)
        self.levelBox.setObjectName(_fromUtf8("levelBox"))
        self.horizontalLayout.addWidget(self.levelBox)
        self.label_2 = QtGui.QLabel(self.centralWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lengthBox = QtGui.QDoubleSpinBox(self.centralWidget)
        self.lengthBox.setObjectName(_fromUtf8("lengthBox"))
        self.horizontalLayout.addWidget(self.lengthBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.browseButton = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.browseButton.sizePolicy().hasHeightForWidth())
        self.browseButton.setSizePolicy(sizePolicy)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.verticalLayout_2.addWidget(self.browseButton)
        self.processButton = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processButton.sizePolicy().hasHeightForWidth())
        self.processButton.setSizePolicy(sizePolicy)
        self.processButton.setObjectName(_fromUtf8("processButton"))
        self.verticalLayout_2.addWidget(self.processButton)
        self.tableView = QtGui.QTableView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_2.addWidget(self.tableView)
        MusicSplitter.setCentralWidget(self.centralWidget)

        self.retranslateUi(MusicSplitter)
        QtCore.QMetaObject.connectSlotsByName(MusicSplitter)

    def retranslateUi(self, MusicSplitter):
        MusicSplitter.setWindowTitle(_translate("MusicSplitter", "MainWindow", None))
        self.label_4.setText(_translate("MusicSplitter", "File:", None))
        self.label.setText(_translate("MusicSplitter", "Silence level", None))
        self.label_2.setText(_translate("MusicSplitter", "Silence length", None))
        self.browseButton.setText(_translate("MusicSplitter", "Browse file ...", None))
        self.processButton.setText(_translate("MusicSplitter", "Process audio", None))

