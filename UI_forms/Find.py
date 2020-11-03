# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Find.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_Find(object):
    def setupUi(self, Find):
        Find.setObjectName("Find")
        Find.resize(633, 448)

        """整个窗口网格布局，放入一个TabWidget"""
        self.gridLayoutWidget = QtWidgets.QWidget(Find)
        #self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 631, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        #self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget_replace_find = QtWidgets.QTabWidget(self.gridLayoutWidget)
        self.tabWidget_replace_find.setObjectName("tabWidget_replace_find")
        Find.setCentralWidget(self.gridLayoutWidget)

        """-----------tab_find----------------"""
        self.tab_find = QtWidgets.QWidget()
        self.tab_find.setObjectName("tab_find")
        self.gridLayout_find = QtWidgets.QGridLayout(self.tab_find)
        self.label_find_target = QtWidgets.QLabel(self.tab_find)
        #self.label_find_target.setGeometry(QtCore.QRect(30, 50, 111, 31))
        self.label_find_target.setObjectName("label_find_target")
        self.gridLayout_find.addWidget(self.label_find_target,0,0)
        self.lineEdit_find_find = QtWidgets.QLineEdit(self.tab_find)
        #self.lineEdit_find_find.setGeometry(QtCore.QRect(150, 50, 251, 31))
        self.lineEdit_find_find.setObjectName("lineEdit_find_find")
        self.gridLayout_find.addWidget(self.lineEdit_find_find,0,1)
        self.textBrowser_find = QtWidgets.QTextBrowser(self.tab_find)
        self.gridLayout_find.addWidget(self.textBrowser_find,1,0,2,2)
    
        #self.verticalLayoutWidget = QtWidgets.QWidget(self.tab_find)
        #self.verticalLayoutWidget.setGeometry(QtCore.QRect(430, 10, 160, 291))
        #self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        #self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        #self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_find_next = QtWidgets.QPushButton(self.tab_find)
        self.pushButton_find_next.setObjectName("pushButton_find_next")
        self.gridLayout_find.addWidget(self.pushButton_find_next,0,2)
        #self.verticalLayout.addWidget(self.pushButton_find_next)
        self.pushButton_find_count = QtWidgets.QPushButton(self.tab_find)
        self.pushButton_find_count.setObjectName("pushButton_find_count")
        self.gridLayout_find.addWidget(self.pushButton_find_count,1,2)
        #self.verticalLayout.addWidget(self.pushButton_find_count)
        self.pushButton_find_cancel = QtWidgets.QPushButton(self.tab_find)
        self.pushButton_find_cancel.setObjectName("pushButton_find_cancel")
        self.gridLayout_find.addWidget(self.pushButton_find_cancel,2,2)
        #self.verticalLayout.addWidget(self.pushButton_find_cancel)
        self.tabWidget_replace_find.addTab(self.tab_find, "")

        """-----------tab_relace--------------"""
        self.gridLayout.setColumnStretch
        self.tab_replace = QtWidgets.QWidget()
        self.tab_replace.setObjectName("tab_replace")
        self.gridLayout_replace = QtWidgets.QGridLayout(self.tab_replace)
        self.label_replace_target = QtWidgets.QLabel(self.tab_replace)
        #self.label_repalce_target.setGeometry(QtCore.QRect(30, 50, 121, 31))
        self.label_replace_target.setObjectName("label_replace_target")
        self.gridLayout_replace.addWidget(self.label_replace_target,0,0)

        self.lineEdit_replace_target = QtWidgets.QLineEdit(self.tab_replace)
        #self.lineEdit_repalce_target.setGeometry(QtCore.QRect(160, 50, 251, 31))
        self.lineEdit_replace_target.setObjectName("lineEdit_replace_target")
        self.gridLayout_replace.addWidget(self.lineEdit_replace_target,0,1)

        self.label_replace_with = QtWidgets.QLabel(self.tab_replace)
        #self.label_replace_with.setGeometry(QtCore.QRect(30, 110, 111, 18))
        self.label_replace_with.setObjectName("label_replace_with")
        self.gridLayout_replace.addWidget(self.label_replace_with,1,0)
        self.lineEdit_replace_with = QtWidgets.QLineEdit(self.tab_replace)
        #self.lineEdit_replace_with.setGeometry(QtCore.QRect(160, 100, 251, 31))
        self.lineEdit_replace_with.setObjectName("lineEdit_replace_with")
        self.gridLayout_replace.addWidget(self.lineEdit_replace_with,1,1)
        self.textBrowser_replace = QtWidgets.QTextBrowser(self.tab_find)
        self.gridLayout_replace.addWidget(self.textBrowser_replace,2,0,2,2)
        #self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.tab_replace)
        #self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(430, 30, 160, 261))
        #self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        #self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        #self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_replace_next = QtWidgets.QPushButton(self.tab_replace)
        self.pushButton_replace_next.setObjectName("pushButton_replace_next")
        self.gridLayout_replace.addWidget(self.pushButton_replace_next,0,2)
        
        #self.verticalLayout_2.addWidget(self.pushButton_replace_all_2)
        self.pushButton_replace_replace = QtWidgets.QPushButton(self.tab_replace)
        self.pushButton_replace_replace.setObjectName("pushButton_replace_replace")
        self.gridLayout_replace.addWidget(self.pushButton_replace_replace,1,2)
        #self.verticalLayout_2.addWidget(self.pushButton_replace_replace)
        self.pushButton_replace_all = QtWidgets.QPushButton(self.tab_replace)
        self.pushButton_replace_all.setObjectName("pushButton_replace_all")
        self.gridLayout_replace.addWidget(self.pushButton_replace_all,2,2)
        #self.verticalLayout_2.addWidget(self.pushButton_replace_all)
        self.pushButton_replace_cancel = QtWidgets.QPushButton(self.tab_replace)
        self.pushButton_replace_cancel.setObjectName("pushButton_replace_cancel")
        self.gridLayout_replace.addWidget(self.pushButton_replace_cancel,3,2)
        #self.verticalLayout_2.addWidget(self.pushButton_replace_cancel)
        self.tabWidget_replace_find.addTab(self.tab_replace, "")


        """--------------tab_mark----------------"""
        self.tab_mark = QtWidgets.QWidget()
        self.tab_mark.setObjectName("tab_mark")
        self.gridLayout_mark = QtWidgets.QGridLayout(self.tab_mark)
        self.label_mark_target = QtWidgets.QLabel(self.tab_mark)
        #self.label_mark_target.setGeometry(QtCore.QRect(30, 60, 111, 18))
        self.label_mark_target.setObjectName("label_mark_target")
        self.gridLayout_mark.addWidget(self.label_mark_target,0,0)

        self.lineEdit_mark_target = QtWidgets.QLineEdit(self.tab_mark)
        #self.lineEdit_mark_target.setGeometry(QtCore.QRect(140, 60, 221, 25))
        self.lineEdit_mark_target.setObjectName("lineEdit_mark_target")
        self.gridLayout_mark.addWidget(self.lineEdit_mark_target,0,1)
        self.textBrowser_mark = QtWidgets.QTextBrowser(self.tab_mark)
        self.gridLayout_mark.addWidget(self.textBrowser_mark,1,0,2,2)

        #self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.tab_mark)
        #self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(420, 30, 160, 211))
        #self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        #self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        #self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_mark_all = QtWidgets.QPushButton(self.tab_mark)
        self.pushButton_mark_all.setObjectName("pushButton_mark_all")
        self.gridLayout_mark.addWidget(self.pushButton_mark_all,0,2)
        #self.verticalLayout_3.addWidget(self.pushButton_mark_all)
        self.pushButton_mark_clear = QtWidgets.QPushButton(self.tab_mark)
        self.pushButton_mark_clear.setObjectName("pushButton_mark_clear")
        self.gridLayout_mark.addWidget(self.pushButton_mark_clear,1,2)
        #self.verticalLayout_3.addWidget(self.pushButton_mark_clear)
        self.pushButton_mark_cancel = QtWidgets.QPushButton(self.tab_mark)
        self.pushButton_mark_cancel.setObjectName("pushButton_mark_cancel")
        self.gridLayout_mark.addWidget(self.pushButton_mark_cancel,2,2)
        #self.verticalLayout_3.addWidget(self.pushButton_mark_cancel)
        self.tabWidget_replace_find.addTab(self.tab_mark, "")


        self.gridLayout.addWidget(self.tabWidget_replace_find, 0, 1, 1, 1)

        self.retranslateUi(Find)
        self.tabWidget_replace_find.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Find)

    def retranslateUi(self, Find):
        _translate = QtCore.QCoreApplication.translate
        Find.setWindowTitle(_translate("Find", "Form"))
        self.label_find_target.setText(_translate("Find", "find target"))
        self.pushButton_find_next.setText(_translate("Find", "find next"))
        self.pushButton_find_count.setText(_translate("Find", "count"))
        self.pushButton_find_cancel.setText(_translate("Find", "cancel"))
        self.tabWidget_replace_find.setTabText(self.tabWidget_replace_find.indexOf(self.tab_find), _translate("Find", "find"))
        self.label_replace_target.setText(_translate("Find", "find target"))
        self.label_replace_with.setText(_translate("Find", "replace with"))
        self.pushButton_replace_next.setText(_translate("Find", "find next"))
        self.pushButton_replace_replace.setText(_translate("Find", "replace"))
        self.pushButton_replace_all.setText(_translate("Find", "replace all"))
        self.pushButton_replace_cancel.setText(_translate("Find", "cancel"))
        self.tabWidget_replace_find.setTabText(self.tabWidget_replace_find.indexOf(self.tab_replace), _translate("Find", "replace"))
        self.label_mark_target.setText(_translate("Find", "find target"))
        self.pushButton_mark_all.setText(_translate("Find", "mark all"))
        self.pushButton_mark_clear.setText(_translate("Find", "clear"))
        self.pushButton_mark_cancel.setText(_translate("Find", "cancel"))
        self.tabWidget_replace_find.setTabText(self.tabWidget_replace_find.indexOf(self.tab_mark), _translate("Find", "mark"))

