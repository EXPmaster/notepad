# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Reward.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form_reward(object):
    def setupUi(self, Form_reward):
        Form_reward.setObjectName("Form_reward")
        Form_reward.resize(400, 300)
        self.graphicsView = QtWidgets.QGraphicsView(Form_reward)
        self.graphicsView.setGeometry(QtCore.QRect(80, 40, 231, 211))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_close = QtWidgets.QPushButton(Form_reward)
        self.pushButton_close.setGeometry(QtCore.QRect(260, 260, 112, 32))
        self.pushButton_close.setObjectName("pushButton_close")
        self.label = QtWidgets.QLabel(Form_reward)
        self.label.setGeometry(QtCore.QRect(140, 10, 111, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Form_reward)
        QtCore.QMetaObject.connectSlotsByName(Form_reward)

    def retranslateUi(self, Form_reward):
        _translate = QtCore.QCoreApplication.translate
        Form_reward.setWindowTitle(_translate("Form_reward", "Reward Us"))
        self.pushButton_close.setText(_translate("Form_reward", "Close"))
        self.label.setText(_translate("Form_reward", "支付宝打赏我们："))
