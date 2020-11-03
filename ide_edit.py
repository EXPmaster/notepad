# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox, QPlainTextEdit, QWidget
from PyQt5.QtCore import Qt
import os
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerCPP, QsciLexerMarkdown, QsciLexerCustom
from PyQt5.QtGui import QFont, QFontMetrics, QColor


class IDEeditor(QsciScintilla):
    r"""
        文本框类
    """
    ARROW_MARKER_NUM = 8

    def __init__(self, name, parent=None, parent_tabWidget=None, language='txt',
                 font_content=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(name)
        # self.document().setModified(False)
        # self.setWindowModified(False)
        self.setModified(False)
        self.setText('')
        self.filepath = None
        self.language = language
        self.parent_tabw = parent_tabWidget
        self.font_content = font_content if font_content else {'font': 'Andale Mono', 'size': 12}
        self.setFontSize(font_content)
        #self.SendScintilla()
        #self.replaceSelectedText()


        

        # IDE settings
        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))


    def keyPressEvent(self, e):
        r"""
            监测文件内容是否修改，若修改则在tab中文件名末尾
            添加一个 '*'
        :param e:
        :return:
        """
        super().keyPressEvent(e)
        index = self.parent_tabw.currentIndex()
        tabtext = self.parent_tabw.tabText(index)
        if not tabtext.endswith('*') and self.isModified():
            self.parent_tabw.setTabText(index, tabtext + '*')
        if not self.isModified() and tabtext.endswith('*'):
            self.parent_tabw.setTabText(index, tabtext[:-1])

    def setlanguage(self, language):
        r"""
            改变语言
        :param language:
        :return:
        """
        self.set_lexer(language)
        self.language = language

    def set_lexer(self, language):
        r"""
            多语法代码高亮
        :param language:
        :return:
        """
        font = self.font_content['font']
        size = self.font_content['size']
        lexer_font = QFont(font, size)
        if language == 'py':
            lexer = QsciLexerPython()
            lexer.setFont(lexer_font)
            self.setLexer(lexer)
        elif language == 'c':
            lexer = QsciLexerCPP()
            lexer.setFont(lexer_font)
            self.setLexer(lexer)
        elif language == 'md':
            lexer = QsciLexerMarkdown()
            lexer.setFont(lexer_font)
            self.setLexer(lexer)
        else:
            self.setLexer(None)
            self.setText(self.text())

    def setFontSize(self, font_content):
        r"""
            修改字体大小和样式
        :param fontSize:
        :return:
        """
        # self.setStyleSheet(f"font: {fontSize}pt'.AppleSystemUIFont';")
        self.font_content = font_content
        font = font_content['font']
        size = font_content['size']
        qfont = QFont(font, size)

        self.setFont(qfont)
        self.set_lexer(self.language)
        self.codeRow()

    def codeRow(self):
        r"""
            显示代码行数
        :return:
        """
        font_categoty = self.font_content['font']
        size = self.font_content['size']
        font = QFont(font_categoty, size)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))
        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)

        self.markerDefine(QsciScintilla.RightArrow,
                          self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),
                                      self.ARROW_MARKER_NUM)
        # 取消显示横向bar
        # self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

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
            # self.setPlainText(text)
            self.setText(text)
            # 设置当前文件名
            _, tmpfilename = os.path.split(file_path)
            self.setObjectName(tmpfilename)
            # 设置语言
            _, prefix = os.path.splitext(tmpfilename)
            self.setlanguage(prefix[1:])
            # 清除改变
            self.setModified(False)
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
                text = self.text()
                f.writelines(text)
            # self.document().setModified(False)
            # 把 '*' 去掉
            index = self.parent_tabw.currentIndex()
            tabtext = self.parent_tabw.tabText(index)
            if tabtext.endswith('*'):
                self.parent_tabw.setTabText(index, tabtext[:-1])
            self.setModified(False)
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
                text = self.text()
                f.writelines(text)
            # self.document().setModified(False)
            # 路径
            self.filepath = file_path
            # 设置当前文件名
            _, tmpfilename = os.path.split(file_path)
            self.setObjectName(tmpfilename)
            # 设置语言
            _, prefix = os.path.splitext(tmpfilename)
            self.setlanguage(prefix[1:])
            self.setModified(False)
            return tmpfilename
        else:
            # QMessageBox.warning(self, 'Warning', 'File name should not be empty')
            return False

    def closeText(self):
        self.close()