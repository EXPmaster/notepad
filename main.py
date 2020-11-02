# -*- coding: utf-8 -*-

import sys
from UI_forms import Ui_CodePlus
from all_windows import Find_Win
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget, QGridLayout, QTextEdit, QDirModel
from PyQt5 import QtWidgets
from reward_handler import Reward
from PyQt5.QtCore import Qt
from textedit import TextEditorS
import os
from preference import Preference
from ide_edit import IDEeditor


class TabItem:
    r"""
        用于存放新建的Tab、layout、textEditor
    """
    __slots__ = ['tab', 'layout', 'text']

    def __init__(self, tab, layout, texteditor):
        self.tab = tab
        self.layout = layout
        self.text = texteditor


class Notebook(QMainWindow, Ui_CodePlus):
    r"""
        Notebook 类
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        """-------- Code ---------"""
        self.actionAbout_us.triggered.connect(self.aboutusEvent)  # 关于我们
        self.actionExit.triggered.connect(self.closeEvent)  # 退出
        self.actionPreference.triggered.connect(self.showpreferenceEvent)# 偏好设置
        """-------- File ---------"""
        self.actionNew.triggered.connect(self.newfileEvent)  # 新建
        self.actionOpen_File.triggered.connect(self.openfileEvent)  # 打开文件
        self.actionOpen_Folder.triggered.connect(self.openfolderEvent)# 打开文件夹
        self.actionSave.triggered.connect(self.savefileEvent)  # 保存文件
        # self.actionSave.setShortcut('Ctrl + S')
        self.actionSave_All.triggered.connect(self.saveallEvent)  # 全部保存
        self.actionSave_As.triggered.connect(self.saveasEvent)  # 另存为
        self.actionClose.triggered.connect(self.closefileEvent)  # 关闭
        self.tabWidget.tabCloseRequested.connect(self.closefileEvent)  # 关闭tab
        """-------- Edit ---------"""
        self.actionUndo.triggered.connect(self.text_undo)  # 撤销
        self.actionRedo.triggered.connect(self.text_redo)  # 重做
        self.actionCut.triggered.connect(self.text_cut)  # 剪切
        self.actionCopy.triggered.connect(self.text_copy)  # 复制
        self.actionPast.triggered.connect(self.text_paste)  # 粘贴
        self.actionFind.triggered.connect(self.text_find)  # 查找
        self.win_find_is_show = False
        self.actionSelect_All.triggered.connect(self.text_selectAll)  # 全选
        """-------- Language ---------"""
        self.actionPlain_Text.triggered.connect(self.selectLanguage)
        self.actionC.triggered.connect(self.selectLanguage)
        self.actionMarkdown.triggered.connect(self.selectLanguage)
        self.actionPython.triggered.connect(self.selectLanguage)
        """-------- Whatever... ---------"""
        self.actionQR_Code.triggered.connect(self.rewardEvent)  # 打赏
        """-------- Status bar ---------"""
        self.lb_margin = QtWidgets.QLabel()
        self.lb_lang = QtWidgets.QLabel()
        self.statusbar.addWidget(self.lb_margin, 4)
        self.statusbar.addWidget(self.lb_lang, 1)
        """-------- Dir Tree ---------"""
        self.dirtree = QtWidgets.QTreeView()
        self.dirtree.setObjectName('dirtree')
        self.gridLayout_1.addWidget(self.dirtree, 0, 0)
        self.gridLayout_1.setColumnStretch(0, 2)
        self.gridLayout_1.setColumnStretch(1, 5)
        """-------- Basic Configs ---------"""
        self.tabWidget.setAttribute(Qt.WA_DeleteOnClose, False)
        self.tabidx = 0
        self.font_content = {'font': 'Andale Mono', 'size': 12}
        self.tab_dict = {}  # 存放tab
        self.file_save_path = None  # 保存文件的路径
        self.language = 'txt'  # 当前语言
        """所有语言类型为：
            txt -> 文本文件
            md -> Markdown文件
            c -> C文件
            py -> Python文件
            """

        """-------- 初始执行的操作 ---------"""
        self.__create_tab()  # 初始创建一个tab
        self.tabWidget.currentChanged.connect(self.changeTab)  # 切换tab触发
        self.lb_lang.setText(self.language)

    #查找
    def text_find(self):
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        if not self.win_find_is_show:
            self.win_find_is_show = True
            self.find_win = Find_Win(self,textedit)
            self.find_win.show()


    def text_undo(self):
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        textedit.undo()

    def text_redo(self):
        
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        textedit.redo()

    def text_copy(self):
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        textedit.copy()

    def text_paste(self):
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        textedit.paste()

    def text_cut(self):
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        textedit.cut()

    def text_selectAll(self):
        textedit = self.__get_textEditor()
        # if isinstance(textedit, QTextEdit):
        textedit.selectAll()

    def selectLanguage(self):
        r"""
            选择语言
        :return:
        """
        language_support = {
            'Plain Text': 'txt',
            'C': 'c',
            'Markdown': 'md',
            'Python': 'py'
        }
        textedit = self.__get_textEditor()
        signal_src = self.sender().text()
        language = language_support[signal_src]
        textedit.setlanguage(language)
        self.language = language
        self.lb_lang.setText(self.language)


    def changeTab(self):
        # super().tabWidget.changeEvent()
        self.language = self.cur_language()
        self.lb_lang.setText(self.language)

    def cur_language(self):
        if self.tabWidget.count() == 0:
            return ''
        language = self.__get_textEditor().language
        return language

    def __find_tab_by_index(self, index):
        r"""
            通过currentIndex获取字典中的
        :param index: CurrentIndex
        :return: (str, object) 当前Tab名，TabItem 对象
        """
        cur_tab_name = self.tabWidget.widget(index).objectName()
        return cur_tab_name, self.tab_dict[cur_tab_name]

    def __get_textEditor(self, index=None):
        r"""
            获取当前tab的textEditor
        :return: (object) textEditor
        """
        if index is None:
            index = self.tabWidget.currentIndex()
        _, tabitem = self.__find_tab_by_index(index)
        return tabitem.text

    def newfileEvent(self):
        r"""
            新建文件事件函数
        :return: None
        """
        self.__create_tab()

    def __create_tab(self, name=None):
        r"""
            新建tab
        :return: None
        """

        self.tabidx += 1
        newfile_name = f'New File {self.tabidx}' if name is None else name
        if name:
            _, language = os.path.splitext(name)
            language = language[1:]
        else:
            language = 'txt'
        new_tabname = 'tab_' + str(self.tabidx)
        tab_new = QWidget()
        tab_new.setObjectName(new_tabname)
        layout = QGridLayout(tab_new)
        layout.setObjectName(f'layout_of_{new_tabname}')
        # text_editor = TextEditorS(name=newfile_name, parent_tabWidget=self.tabWidget,
        #                           language=language, font_size=self.fontsize)
        # text_editor = Editor()
        text_editor = IDEeditor(name=newfile_name, parent_tabWidget=self.tabWidget,
                                language=language, font_content=self.font_content)
        # text_editor.textChange.connect(self.__handle_textChange)
        layout.addWidget(text_editor, 0, 0, 1, 1)
        tabitem = TabItem(tab_new, layout, text_editor)
        self.tab_dict[new_tabname] = tabitem
        self.tabWidget.addTab(tab_new, newfile_name)
        # 跳转到新页面
        index = self.tabWidget.count() - 1
        self.tabWidget.setCurrentIndex(index)

    def openfileEvent(self, file_path=None):
        r"""
            打开文件事件函数
        :return: None
        """
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(self, 'Choose a file', '/',
                                                                'All Files (*);;'
                                                                'Text Files (*.txt);;'
                                                                'Markdown Files (*.md);;'
                                                                'C Sources (*.c);;'
                                                                'Python Scripts (*.py)')
        # 判断文件是否可读取
        if not os.path.splitext(file_path)[-1] in ['.py', '.c', '.txt', '.md']:
            QMessageBox.warning(self, u'警告', u'文件类型不支持！')
            return
        if len(file_path):
            _, file_fullname = os.path.split(file_path)

            for tabitem in self.tab_dict.values():
                tmp_edititem = tabitem.text
                if file_fullname == tmp_edititem.objectName():
                    index = self.tabWidget.indexOf(tabitem.tab)
                    self.tabWidget.setCurrentIndex(index)
                    return
            self.__create_tab(name=file_fullname)
            index = self.tabWidget.count() - 1
            textedit = self.__get_textEditor(index=index)
            textedit.load(file_path)

    def openfolderEvent(self):
        folder_path = QFileDialog.getExistingDirectory(self, '请选择打开的文件夹')
        if folder_path:
            self.model = QDirModel()
            self.dirtree.setModel(self.model)
            self.dirtree.setRootIndex(self.model.index(folder_path))
            self.dirtree.setAnimated(False)
            self.dirtree.setIndentation(20)
            self.dirtree.setSortingEnabled(True)
            self.dirtree.doubleClicked.connect(self.__choose_file)
            self.dirtree.setWindowTitle("Dir View")
            self.dirtree.setHeaderHidden(True)

    def __choose_file(self, index):
        file_path = self.model.filePath(index)
        # print(file_path)
        self.openfileEvent(file_path)

    def saveasEvent(self):
        r"""
            另存为事件函数
        :return: None
        """
        textedit = self.__get_textEditor()
        status = textedit.saveas()
        if status:
            """保存成功，设置tab名"""
            index = self.tabWidget.currentIndex()
            self.tabWidget.setTabText(index, status)

    def savefileEvent(self):
        r"""
            保存文件事件函数
        :return:
        """
        textedit = self.__get_textEditor()
        textedit.save()

    def saveallEvent(self):
        r"""
            全部保存
        :return:
        """
        for tabitem in self.tab_dict.values():
            textedit = tabitem.text
            textedit.save()

    def closefileEvent(self, index):
        r"""
            关闭文件事件函数
        :return: None
        """
        if self.tabWidget.count() == 0:
            self.close()
            return
        cur_tab_name, tabitem = self.__find_tab_by_index(index)
        textedit = tabitem.text
        # print(cur_tab_name)
        if textedit.isModified():
            """已修改文件，需要保存"""
            ret_code = QMessageBox.information(self, '提示', '文件尚未保存，确定退出？',
                                               QMessageBox.Yes | QMessageBox.No)
            # ret_code: Yes -- 16384
            #           No -- 65536
            if ret_code == QMessageBox.Yes:
                textedit.closeText()
                self.tabWidget.removeTab(index)
                del self.tab_dict[cur_tab_name]
        else:
            textedit.closeText()
            self.tabWidget.removeTab(index)
            del self.tab_dict[cur_tab_name]

    def setFontSizeEvent(self):
        r"""
            改变所有textedit的字体大小和样式
        :return:
        """
        for tabitem in self.tab_dict.values():
            textedit = tabitem.text
            textedit.setFontSize(self.font_content)

    def rewardEvent(self):
        r"""
            打赏事件函数
        :return:
        """
        self.qrcode_window = Reward()
        self.qrcode_window.show()
        # TODO: 修改字体

    def showpreferenceEvent(self):
        r"""
            调出偏好设置
        :return:
        """
        self.preference = Preference(par=self)
        self.preference.show()

    def aboutusEvent(self):
        r"""
            关于我们事件函数
        :return:
        """
        QMessageBox.information(self, 'About us', 'This editor was designed by xxx, \n'
                                                  'with hand-writing board inside')

    def closeEvent(self, event):
        r"""
            关闭notebook事件函数
        :param event:
        :return: None
        """
        check_quit = True
        for tabitem in self.tab_dict.values():
            textedit = tabitem.text
            if textedit.isModified():
                check_quit = False
                break
        if not check_quit:
            ret_code = QMessageBox.information(self, '提示', '存在文件未保存，确定退出？',
                                                   QMessageBox.Yes | QMessageBox.No)
            if ret_code == QMessageBox.Yes:
                self.close()
            else:
                event.ignore()
        else:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Notebook()
    MainWindow.show()
    sys.exit(app.exec_())
