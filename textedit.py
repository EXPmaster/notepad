# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox, QPlainTextEdit, QWidget
from PyQt5.QtCore import Qt,QProcess,pyqtSignal
from PyQt5.QtGui import  QTextCursor,QColor
import os
import time
from PyQt5.Qsci import QsciScintilla
import  sys


class TextEditorS(QTextEdit):
    r"""
        文本框类
    """
    def __init__(self, name, parent=None, parent_tabWidget=None, language='txt',
                 font_size=12):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(name)
        self.document().setModified(False)
        self.setPlainText('')
        self.filepath = None
        self.language = language
        self.parent_tabw = parent_tabWidget
        self.setFontSize(font_size)

    def isModified(self):
        return self.document().isModified()

    # def keyPressEvent(self, e):
    #     r"""
    #         监测文件内容是否修改，若修改则在tab中文件名末尾
    #         添加一个 '*'
    #     :param e:
    #     :return:
    #     """
    #     super().keyPressEvent(e)
    #     index = self.parent_tabw.currentIndex()
    #     tabtext = self.parent_tabw.tabText(index)
    #     if not tabtext.endswith('*') and self.isModified():
    #         self.parent_tabw.setTabText(index, tabtext + '*')

    def setlanguage(self, language):
        self.language = language

    def setFontSize(self, fontSize=12):
        r"""
            修改字体大小
        :param fontSize:
        :return:
        """
        self.setStyleSheet(f"font: {fontSize}pt'.AppleSystemUIFont';")

    def load(self, file_path):
        r"""
        读取文件
        :param file_path: 文件路径
        :return: None
        """
        text = ''
        try:
            """读文件"""
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    text += line
                self.filepath = file_path
            self.setPlainText(text)
            # 设置当前文件名
            _, tmpfilename = os.path.split(file_path)
            self.setObjectName(tmpfilename)
            # 设置语言
            _, prefix = os.path.splitext(tmpfilename)
            self.setlanguage(prefix[1:])
        except FileNotFoundError:
            """弹出窗口，提示文件不存在"""
            QMessageBox.warning(self, 'Warning', 'Text does not exist!')

    def save(self):
        r"""
        保存
        :return:
        """
        if self.filepath is not None:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                text = self.toPlainText()
                f.writelines(text)
            self.document().setModified(False)
            # 把 '*' 去掉
            index = self.parent_tabw.currentIndex()
            tabtext = self.parent_tabw.tabText(index)
            if tabtext.endswith('*'):
                self.parent_tabw.setTabText(index, tabtext[:-1])

        else:
            self.saveas()

    def saveas(self):
        r"""
        另存为
        :return:
        """
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save As')
        if len(file_path):
            """如果路径不为空，则保存"""
            self.filepath = file_path
            with open(file_path, 'w', encoding='utf-8') as f:
                text = self.toPlainText()
                f.writelines(text)
            self.document().setModified(False)
            # 路径
            self.filepath = file_path
            # 设置当前文件名
            _, tmpfilename = os.path.split(file_path)
            self.setObjectName(tmpfilename)
            # 设置语言
            _, prefix = os.path.splitext(tmpfilename)
            self.setlanguage(prefix[1:])
            return tmpfilename
        else:
            # QMessageBox.warning(self, 'Warning', 'File name should not be empty')
            return False

    def closeText(self):
        self.close()


class RunBrowser(QTextEdit):
    exitSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.start = False
        self.process = QProcess()
        self.cur = self.textCursor()  # 标记文本位置的游标
        self.in_cur = QTextCursor()   # 输入光标的映射游标
        self.last_pos = 0             # 上一次打印的最后位置
        self.cursorPositionChanged.connect(self.in_cur_change)

    def in_cur_change(self):
        """由输入/鼠标点击引起的输入光标的位置变化，将光标全局位置映射到文本框内相对位置"""
        p = self.mapFromGlobal(self.cursor().pos())
        self.in_cur = self.cursorForPosition(p)
        print('change in_cur pos to', self.in_cur.position())

    def start_process(self, path):
        r"""开始进程
            :param: path 绝对路径
            :return:
        """
        self.clear()
        self.last_pos = 0
        cmd = 'python ' + path
        self.append(cmd)
        print(self.cur.position())
        self.last_pos = self.cur.position()
        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.show_output)
        self.process.readyReadStandardError.connect(self.show_error)
        self.process.finished.connect(self.run_exit)
        self.process.start(cmd)
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

            print(self.process.write(('\r\n'+self.cur.selectedText() + '\r\n' +'sdc').encode('gbk')))  # 写标准输入
            self.cur.movePosition(QTextCursor.EndOfLine)
            # self.process.waitForBytesWritten()  # 等待写入完成
            self.setTextCursor(self.cur)  # 重新设置光标
            self.process.closeWriteChannel()  # 关闭写通道

            return



        super().keyPressEvent(e)
        e.accept()


