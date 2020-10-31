# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
import os


class TextEditorS(QTextEdit):
    r"""
        文本框类
    """
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(name)
        self.document().setModified(False)
        self.setPlainText('')
        self.filepath = None
        self.language = 'txt'

    def isModified(self):
        return self.document().isModified()

    def language(self):
        return self.language

    def setlanguage(self, language):
        self.language = language

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
        except FileNotFoundError:
            ...

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

            # 设置当前文件名
            _, tmpfilename = os.path.split(file_path)
            self.setObjectName(tmpfilename)
            return tmpfilename
        else:
            # QMessageBox.warning(self, 'Warning', 'File name should not be empty')
            return False

    def closeText(self):
        self.close()