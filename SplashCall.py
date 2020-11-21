import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QBasicTimer , pyqtSignal
#from ui_Splash import Ui_Form
from UI_forms import Ui_Form

# 主窗口
class Splash(QWidget):
    splashClose = pyqtSignal()                               #自定义信号
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.ui = Ui_Form()                                 #命名ui 为form的对象
        self.ui.setupUi(self)                               #导入QWidget基本窗体到ui
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)  # 设置无边框并置顶 '''注意：ui是Ui_from的对象，不是窗体基类，所以不能使用ui.setWindowFlags'''
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)      # 设置背景为透明色
        self.timeRun() #计时开始

#进度条逻辑
    def timeRun(self):
        self.timer = QBasicTimer()
        self.step = 0
        self.timer.start(10,self) #设置10超时时间 并开始计时

    def timerEvent(self, evet):
        if self.step >= 100:
            self.timer.stop()
            self.splashClose.emit() #发出信号，可打开其它界面
            self.close()  #关闭开机画面
            return
        else:
            self.step = self.step + 0.5
            self.ui.prg.setValue(self.step)
            self.ui.lab1.setText('正在加载...{}%'.format(self.step))
            return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = Splash()
    myWin.show()
    sys.exit(app.exec_())