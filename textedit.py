# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox, QPlainTextEdit, QWidget
from PyQt5.QtCore import Qt,QProcess,pyqtSignal
from PyQt5.QtGui import  QTextCursor
import os
from PyQt5.Qsci import QsciScintilla


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
        self.process = ...
        self.cur = self.textCursor()
        self.in_cur = QTextCursor()
        self.last_pos = 0
        self.cursorPositionChanged.connect(self.test)


    def test(self):
        p = self.mapFromGlobal(self.cursor().pos())
        self.in_cur = self.cursorForPosition(p)
        print('change in_cur pos to', self.in_cur.position())


    def start_process(self, path):
        print(self.cur.position())
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
        out = self.process.readAllStandardOutput()
        print(out)
        out = str(out, 'gbk')
        self.append(out[:-2])
        self.last_pos = self.cur.position()
        self.append('')

    def show_error(self):
        err = self.process.readAllStandardError()
        err = str(err, 'gbk')
        self.append('<font color = red>' + err)

    def run_exit(self, exitcode):
        self.append('\nProcess finished with exit code ' + str(exitcode))
        self.start = False
        self.exitSignal.emit()
        self.last_pos = 0

    def keyPressEvent(self, e):
        print('last pos', self.last_pos)
        print('cur pos', self.cur.position())
        print('in_cur pos', self.in_cur.position())
        if not self.start:
            # 程序未启动禁止键入
            return
        elif e.key() == Qt.Key_Backspace and self.cur.position() == self.last_pos + 1:
            # 已打印信息的下一行行首禁止退格
            return
        elif self.in_cur.position() <= self.last_pos:
            return


        super().keyPressEvent(e)
        e.accept()