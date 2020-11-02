
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class embterminal(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.process = QProcess()
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)


        self.process.start('start cmd')

        print(self.winId())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embterminal()
    main.show()
    sys.exit(app.exec_())


