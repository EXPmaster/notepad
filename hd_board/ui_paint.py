# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paint.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_paint_window(object):
    def setupUi(self, paint_window):
        paint_window.setObjectName("paint_window")
        paint_window.resize(500, 500)
        paint_window.setMinimumSize(QtCore.QSize(500, 500))
        paint_window.setMaximumSize(QtCore.QSize(500, 500))
        paint_window.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(paint_window)
        self.centralwidget.setObjectName("centralwidget")
        self.r = QtWidgets.QFrame(self.centralwidget)
        self.r.setGeometry(QtCore.QRect(15, 15, 340, 340))
        self.r.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.r.setFrameShadow(QtWidgets.QFrame.Raised)
        self.r.setObjectName("r")
        self.pushButton_clear = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_clear.setGeometry(QtCore.QRect(30, 380, 71, 41))
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.comboBox_color = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_color.setGeometry(QtCore.QRect(210, 400, 91, 21))
        self.comboBox_color.setObjectName("comboBox_color")
        self.comboBox_color.addItem("")
        self.comboBox_color.addItem("")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 380, 54, 12))
        self.label.setObjectName("label")
        self.radioButton_Eraser = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_Eraser.setGeometry(QtCore.QRect(410, 400, 61, 16))
        self.radioButton_Eraser.setObjectName("radioButton_Eraser")
        self.comboBox_line = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_line.setGeometry(QtCore.QRect(320, 400, 69, 22))
        self.comboBox_line.setObjectName("comboBox_line")
        self.comboBox_line.addItem("")
        self.comboBox_line.addItem("")
        self.comboBox_line.addItem("")
        self.comboBox_line.addItem("")
        self.comboBox_line.addItem("")
        self.comboBox_line.addItem("")
        self.label_line = QtWidgets.QLabel(self.centralwidget)
        self.label_line.setGeometry(QtCore.QRect(320, 380, 131, 16))
        self.label_line.setObjectName("label_line")
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(120, 382, 71, 41))
        self.pushButton_back.setObjectName("pushButton_back")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(385, 20, 70, 70))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        paint_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(paint_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 23))
        self.menubar.setObjectName("menubar")
        paint_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(paint_window)
        self.statusbar.setObjectName("statusbar")
        paint_window.setStatusBar(self.statusbar)

        self.retranslateUi(paint_window)
        QtCore.QMetaObject.connectSlotsByName(paint_window)

    def retranslateUi(self, paint_window):
        _translate = QtCore.QCoreApplication.translate
        paint_window.setWindowTitle(_translate("paint_window", "画板"))
        self.pushButton_clear.setText(_translate("paint_window", "Clear"))
        self.comboBox_color.setItemText(0, _translate("paint_window", "Black"))
        self.comboBox_color.setItemText(1, _translate("paint_window", "Blue"))
        self.label.setText(_translate("paint_window", "Color"))
        self.radioButton_Eraser.setText(_translate("paint_window", "Eraser"))
        self.comboBox_line.setItemText(0, _translate("paint_window", "5"))
        self.comboBox_line.setItemText(1, _translate("paint_window", "7"))
        self.comboBox_line.setItemText(2, _translate("paint_window", "9"))
        self.comboBox_line.setItemText(3, _translate("paint_window", "11"))
        self.comboBox_line.setItemText(4, _translate("paint_window", "13"))
        self.comboBox_line.setItemText(5, _translate("paint_window", "15"))
        self.label_line.setText(_translate("paint_window", "Pen/Eraser thickness"))
        self.pushButton_back.setText(_translate("paint_window", "Back"))

