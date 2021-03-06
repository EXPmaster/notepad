# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit, QFileDialog, QMessageBox, QPlainTextEdit, QWidget,QFileSystemModel
from PyQt5.QtCore import Qt, pyqtSignal,QFileSystemWatcher, QTimer
import os
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerCPP,\
    QsciLexerMarkdown, QsciAPIs
from PyQt5.QtGui import QFont, QFontMetrics, QColor
import functools
from AST import goto_definition


class IDEeditor(QsciScintilla):
    r"""
        文本框类
    """
    ARROW_MARKER_NUM = 8
    newFileSignal = pyqtSignal()

    def __init__(self, name, parent=None, parent_tabWidget=None, language='txt',
                 font_content=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setObjectName(name)
        # self.document().setModified(False)
        # self.setWindowModified(False)
        self.setUtf8(True)
        self.setModified(False)
        self.setText('')
        self.filepath = None
        self.language = language
        self.parent_tabw = parent_tabWidget
        self.font_content = font_content if font_content else {'font': 'Andale Mono', 'size': '12'}
        self.lxr = None
        self.api = None



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
        # 自动缩进
        self.setAutoIndent(True)
        self.setTabWidth(4)

        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionSource(self.AcsAll)
        # self.cursorPositionChanged.connect(self.testEvent)
        # Hotspot
        # 5:关键词
        # 8：类名
        # 9：函数名
        # 10：标点符号
        # 11：变量名
        self.SendScintilla(self.SCI_STYLESETHOTSPOT, 8, True)
        self.SendScintilla(self.SCI_STYLESETHOTSPOT, 9, True)
        self.SendScintilla(self.SCI_STYLESETHOTSPOT, 11, True)
        self.SCN_HOTSPOTCLICK.connect(self.hotspot_clicked)

    def hotspot_clicked(self, position, modifiers):
        r"""
        点击hotspot触发事件
        :return:
        """
        print(position)
        QTimer.singleShot(100, functools.partial(
            self.hotspot_clicked_delayed, position, modifiers))

    def hotspot_clicked_delayed(self, position, modifiers):
        start = self.SendScintilla(self.SCI_WORDSTARTPOSITION, position)
        end = self.SendScintilla(self.SCI_WORDENDPOSITION, position)
        text = self.text(start, end)# [start:end]
        click_line = self.SendScintilla(self.SCI_LINEFROMPOSITION, position) + 1
        click_column = self.SendScintilla(self.SCI_GETCOLUMN, position) + 1
        new_row, new_col = goto_definition(text, click_line, click_column, contents=self.text())
        if new_row is not None and new_col is not None:
            self.setCursorPosition(new_row-1, new_col-1)
        print(text)

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
        if not tabtext.startswith('*') and self.isModified():
            self.parent_tabw.setTabText(index, '*' + tabtext)
        if not self.isModified() and tabtext.startswith('*'):
            self.parent_tabw.setTabText(index, tabtext[1:])

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
        size = int(self.font_content['size'])
        lexer_font = QFont(font, size)
        if language == 'py':
            self.lxr = QsciLexerPython()
            self.lxr.setFont(lexer_font)
            self.setLexer(self.lxr)
            self.__pythonCompletion()

        elif language == 'c':
            self.lxr = QsciLexerCPP()
            self.lxr.setFont(lexer_font)
            self.setLexer(self.lxr)
            self.__cCompletion()
        elif language == 'md':
            self.lxr = QsciLexerMarkdown()
            self.lxr.setFont(lexer_font)
            self.setLexer(self.lxr)
        else:
            self.setLexer(None)
            self.setText(self.text())

    def __pythonCompletion(self):
        r"""
            python 自动补全
        :return:
        """
        python_keywords = ["False", "None", "True", "and", "as", "assert", "break", "class", "continue", "def",
                           "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in",
                           "is", "isinstance", "print", "len", "range", "enumerate", "input", "int", "float", "bool",
                           "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with",
                           "yield", "next", "iter"]
        try:
            if isinstance(self.api, QsciAPIs):
                del self.api
        except:
            pass
        self.api = QsciAPIs(self.lxr)
        for kw in python_keywords:
            self.api.add(kw)
        self.api.prepare()
        # self.api.add('class')
        # import PyQt5
        # pyqt_path = os.path.dirname(PyQt5.__file__)
        # self.api.load(os.path.join(pyqt_path, "Qt/qsci/api/python/Python-3.6.api"))

        # self.api.prepare()
        # print('OK')

    def __cCompletion(self):
        r"""
            C自动补全
        :return:
        """
        c_keywords = ["char", "double", "enum", "float", "int", "long", "short", "signed", "struct",
                      "union", "unsigned", "void", "for", "do", "while", "break", "continue", "if",
                      "else", "goto", "switch", "case", "default", "return", "auto", "extern", "register",
                      "static", "const", "sizeof", "typedef", "volatile"]
        try:
            if isinstance(self.api, QsciAPIs):
                del self.api
        except:
            pass
        self.api = QsciAPIs(self.lxr)
        for kw in c_keywords:
            self.api.add(kw)
        self.api.prepare()

    def setFontSize(self, font_content):
        r"""
            修改字体大小和样式
        :param fontSize:
        :return:
        """
        # self.setStyleSheet(f"font: {fontSize}pt'.AppleSystemUIFont';")
        self.font_content = font_content
        font = font_content['font']
        size = int(font_content['size'])
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
        size = int(self.font_content['size'])
        font = QFont(font_categoty, size)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))
        # Clickable margin 1 for showing markers
        self.setMarginSensitivity(1, True)
        self.marginClicked.connect(self.on_margin_clicked)
        self.markerDefine(QsciScintilla.RightArrow,
                          self.ARROW_MARKER_NUM)
        self.setMarkerBackgroundColor(QColor("#ee1111"),
                                      self.ARROW_MARKER_NUM)
        # 取消显示横向bar
        # self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

    def on_margin_clicked(self, nmargin, nline, modifiers):
        # Toggle marker for the line the margin was clicked on
        if self.markersAtLine(nline) != 0:
            self.markerDelete(nline, self.ARROW_MARKER_NUM)
        else:
            self.markerAdd(nline, self.ARROW_MARKER_NUM)

    def load(self, file_path, mapping=None):
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
                if mapping is not None or file_path.startswith('.tmp'):
                    self.filepath = mapping
                else:
                    self.filepath = file_path
            # self.setPlainText(text)
            self.setText(text)
            # 设置当前文件名
            _, tmpfilename = os.path.split(file_path)
            self.setObjectName(tmpfilename)
            # 设置语言
            _, prefix = os.path.splitext(tmpfilename)
            self.setlanguage(prefix[1:])
            # 是否清除改变
            if tmpfilename.startswith('*'):
                self.setModified(True)
            else:
                self.setModified(False)
        except FileNotFoundError:
            """弹出窗口，提示文件不存在"""
            QMessageBox.warning(self, 'Warning', 'Text does not exist!')

    def save(self, file_path=None):
        r"""
        保存
        :return:
        """
        if self.filepath is not None or file_path:
            if file_path:
                save_path = file_path
            else:
                save_path = self.filepath
            with open(save_path, 'w', encoding='utf-8') as f:
                text = self.text()
                f.writelines(text)
            # self.document().setModified(False)
            # 把 '*' 去掉
            index = self.parent_tabw.currentIndex()
            tabtext = self.parent_tabw.tabText(index)
            if tabtext.startswith('*'):
                self.parent_tabw.setTabText(index, tabtext[1:])
            self.setModified(False)
            return False
        else:
            self.saveas()
            return True

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
            index = self.parent_tabw.currentIndex()
            self.parent_tabw.setTabText(index, tmpfilename)
            self.newFileSignal.emit()
            return True
        else:
            # QMessageBox.warning(self, 'Warning', 'File name should not be empty')
            return False

    def closeText(self):
        self.close()