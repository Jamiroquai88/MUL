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
        self.centralWidget = QtGui.QWidget(MusicSplitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalWidget = QtGui.QWidget(self.centralWidget)
        self.verticalWidget.setGeometry(QtCore.QRect(0, 0, 400, 300))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setObjectName(_fromUtf8("verticalWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_4 = QtGui.QLabel(self.verticalWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.chosenFile = QtGui.QLabel(self.verticalWidget)
        self.chosenFile.setText(_fromUtf8(""))
        self.chosenFile.setObjectName(_fromUtf8("chosenFile"))
        self.horizontalLayout_2.addWidget(self.chosenFile)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.browseButton = QtGui.QPushButton(self.verticalWidget)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.verticalLayout.addWidget(self.browseButton)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setMargin(11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.verticalWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.levelBox = QtGui.QDoubleSpinBox(self.verticalWidget)
        self.levelBox.setMaximum(1.0)
        self.levelBox.setSingleStep(0.1)
        self.levelBox.setObjectName(_fromUtf8("levelBox"))
        self.horizontalLayout.addWidget(self.levelBox)
        self.label_2 = QtGui.QLabel(self.verticalWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lengthBox = QtGui.QDoubleSpinBox(self.verticalWidget)
        self.lengthBox.setObjectName(_fromUtf8("lengthBox"))
        self.horizontalLayout.addWidget(self.lengthBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.processButton = QtGui.QPushButton(self.verticalWidget)
        self.processButton.setObjectName(_fromUtf8("processButton"))
        self.verticalLayout.addWidget(self.processButton)
        self.tableView = QtGui.QTableView(self.verticalWidget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        MusicSplitter.setCentralWidget(self.centralWidget)

        self.retranslateUi(MusicSplitter)
        QtCore.QMetaObject.connectSlotsByName(MusicSplitter)

    def retranslateUi(self, MusicSplitter):
        MusicSplitter.setWindowTitle(_translate("MusicSplitter", "MainWindow", None))
        self.label_4.setText(_translate("MusicSplitter", "File:", None))
        self.browseButton.setText(_translate("MusicSplitter", "Browse file ...", None))
        self.label.setText(_translate("MusicSplitter", "Silence level", None))
        self.label_2.setText(_translate("MusicSplitter", "Silence length", None))
        self.processButton.setText(_translate("MusicSplitter", "Process audio", None))

