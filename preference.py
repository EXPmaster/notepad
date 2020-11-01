from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, \
    QStackedWidget, QHBoxLayout, QFormLayout, QLineEdit, QFontComboBox, \
    QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator


class Preference(QWidget):
    r"""
        偏好设置组件
    """
    def __init__(self, par=None):
        super().__init__()
        # self.setGeometry(300, 50, 10, 10)
        self.par = par
        self.resize(500, 400)
        self.setWindowTitle('Preferences')
        self.mainWidget = QWidget()
        self.buttonsWidget = QWidget()
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Font')
        self.leftlist.insertItem(1, 'Environment')
        self.fontsize = par.fontsize if par is not None else 12
        self.fontpage = QWidget()
        self.environpage = QWidget()
        self.lineEdit = QLineEdit()

        self.fontUI()
        self.buttonUI()

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.fontpage)
        self.stack.addWidget(self.environpage)

        mHbox = QHBoxLayout()
        mHbox.addWidget(self.leftlist)
        mHbox.addWidget(self.stack)
        self.mainWidget.setLayout(mHbox)

        Vbox = QVBoxLayout()
        Vbox.addWidget(self.mainWidget)
        Vbox.addWidget(self.buttonsWidget)
        Vbox.setStretchFactor(self.mainWidget, 10)
        Vbox.setStretchFactor(self.buttonsWidget, 1)
        self.setLayout(Vbox)
        self.leftlist.currentRowChanged.connect(self.display)

    def fontUI(self):
        font_layout = QFormLayout()
        line_edit = self.lineEdit
        line_edit.setText(str(self.fontsize))
        line_edit.setClearButtonEnabled(True)
        line_edit.setValidator(QIntValidator(12, 20))
        line_edit.setMaximumWidth(50)
        fontbox = QFontComboBox()
        fontbox.setMaximumWidth(200)
        font_layout.addRow('Font', fontbox)
        font_layout.addRow('Size', line_edit)
        self.fontpage.setLayout(font_layout)

    def buttonUI(self):
        layout = QHBoxLayout()
        ack_btn = QPushButton()
        layout.addWidget(QLabel())
        layout.addWidget(QLabel())
        ack_btn.setText('Apply')
        cancel_btn = QPushButton()
        cancel_btn.setText('Cancel')
        layout.addWidget(cancel_btn)
        layout.addWidget(ack_btn)

        cancel_btn.clicked.connect(self.close)
        ack_btn.clicked.connect(self.__ack_btn_event)
        self.buttonsWidget.setLayout(layout)

    def __ack_btn_event(self):
        fontsize = int(self.lineEdit.text())
        if fontsize in range(12, 31):
            self.fontsize = fontsize
            self.par.fontsize = fontsize
            self.par.setFontSizeEvent()
            self.close()
        else:
            QMessageBox.warning(self, 'Warning', 'Font size must be in range 12-30!')

    def display(self, index):
        r"""
            设置当前选项卡
        :param index:
        :return:
        """
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    demo = Preference()
    demo.show()
    sys.exit(app.exec_())