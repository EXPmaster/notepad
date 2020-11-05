from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, QProcess, pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor


class RunBrowser(QTextEdit):
    startSignal = pyqtSignal()
    exitSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.start = False
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.show_output)
        self.process.readyReadStandardError.connect(self.show_error)
        self.process.finished.connect(self.run_exit)
        self.cur = self.textCursor()  # 标记文本位置的游标
        self.in_cur = QTextCursor()   # 输入光标的映射游标
        self.last_pos = 0             # 上一次打印的最后位置
        self.cursorPositionChanged.connect(self.in_cur_change)

    def in_cur_change(self):
        """由输入/鼠标点击引起的输入光标的位置变化，将光标全局位置映射到文本框内相对位置"""
        p = self.mapFromGlobal(self.cursor().pos())
        self.in_cur = self.cursorForPosition(p)
        print('change in_cur pos to', self.in_cur.position())

    def start_process(self, cmd):
        r"""开始进程
            :param: cmd 指令
            :return:
        """
        self.clear()
        self.last_pos = 0
        self.append(cmd)
        print(self.cur.position())
        self.last_pos = self.cur.position()
        self.process.start(cmd)
        self.startSignal.emit()
        self.start = True

    def show_output(self):
        r"""收到标准输出数据并显示
            :return:
        """
        out = self.process.readAllStandardOutput()
        print(out)
        out = str(out, 'gbk')
        """从cur的位置追加文本"""
        print(out.strip())
        self.append(out.strip())
        """更新文末位置"""
        self.last_pos = self.cur.position()

    def show_error(self):
        """收到标准错误数据并标红显示"""
        err = self.process.readAllStandardError()
        err = str(err, 'gbk')
        self.setTextColor(QColor('red'))
        self.append(err.strip())
        self.setTextColor(QColor('black'))

    def run_exit(self, exitcode):
        """进程退出返回退出码，发射退出信号"""
        self.append('\nProcess finished with exit code ' + str(exitcode))
        self.start = False
        self.exitSignal.emit()
        self.last_pos = 0

    def keyPressEvent(self, e):
        """重写键盘事件"""
        print('last pos', self.last_pos)
        print('cur pos', self.cur.position())
        print('in_cur pos', self.in_cur.position())
        if not self.start:
            # 程序未启动禁止用户键入
            return
        elif e.key() == Qt.Key_Backspace and self.in_cur.position() == self.last_pos:
            # 当输入光标在已打印信息文末禁止退格
            return
        elif self.in_cur.position() < self.last_pos:
            # 当输入光标在已打印信息文内禁止用户键入
            return
        elif e.key() == Qt.Key_Return:
            """在准许键入时检测到回车视为提交键入字符至标准输入"""
            print('enter')
            self.cur.setPosition(self.last_pos)  # 定位至用户开始键入位置
            self.cur.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)  # 定位至行末-即回车位置

            print(self.process.write(self.cur.selectedText().encode('gbk')))  # 写标准输入
            self.cur.movePosition(QTextCursor.EndOfLine)
            # self.process.waitForBytesWritten()  # 等待写入完成
            self.setTextCursor(self.cur)  # 重新设置光标
            self.process.closeWriteChannel()  # 关闭写通道

            return

        super().keyPressEvent(e)
        e.accept()