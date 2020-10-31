# -*- coding: utf-8 -*-

import sys
from UI_forms import Ui_CodePlus
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QWidget, QGridLayout, QTextEdit
from reward_handler import Reward
from PyQt5.QtCore import Qt
from textedit import TextEditorS
import os


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
        """-------- File ---------"""
        self.actionNew.triggered.connect(self.newfileEvent)  # 新建
        self.actionOpen_File.triggered.connect(self.openfileEvent)  # 打开文件
        # TODO: Open Folder
        self.actionSave.triggered.connect(self.savefileEvent)  # 保存文件
        self.actionSave_As.triggered.connect(self.saveasEvent)  # 另存为
        self.actionClose.triggered.connect(self.closefileEvent)  # 关闭
        self.tabWidget.tabCloseRequested.connect(self.closefileEvent)  # 关闭tab
        """-------- Edit ---------"""
        self.actionUndo.triggered.connect(self.text_undo)  # 撤销
        self.actionRedo.triggered.connect(self.text_redo)  # 重做
        self.actionCut.triggered.connect(self.text_cut)  # 剪切
        self.actionCopy.triggered.connect(self.text_copy)  # 复制
        self.actionPast.triggered.connect(self.text_paste)  # 粘贴
        # # TODO: Find
        self.actionSelect_All.triggered.connect(self.text_selectAll)  # 全选
        """-------- Whatever... ---------"""
        self.actionQR_Code.triggered.connect(self.rewardEvent)  # 打赏
        """-------- Basic Configs ---------"""
        self.tabWidget.setAttribute(Qt.WA_DeleteOnClose, False)
        self.tabidx = 0
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

    def text_undo(self):
        textedit = self.__get_textEditor()
        if isinstance(textedit, QTextEdit):
            textedit.undo()

    def text_redo(self):
        textedit = self.__get_textEditor()
        if isinstance(textedit, QTextEdit):
            textedit.redo()

    def text_copy(self):
        textedit = self.__get_textEditor()
        if isinstance(textedit, QTextEdit):
            textedit.copy()

    def text_paste(self):
        textedit = self.__get_textEditor()
        if isinstance(textedit, QTextEdit):
            textedit.paste()

    def text_cut(self):
        textedit = self.__get_textEditor()
        if isinstance(textedit, QTextEdit):
            textedit.cut()

    def text_selectAll(self):
        textedit = self.__get_textEditor()
        if isinstance(textedit, QTextEdit):
            textedit.selectAll()

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
        index = self.tabWidget.count() - 1
        self.tabWidget.setCurrentIndex(index)

    def __create_tab(self, name=None):
        r"""
            新建tab
        :return: None
        """

        self.tabidx += 1
        newfile_name = f'New File {self.tabidx}' if name is None else name
        new_tabname = 'tab_' + str(self.tabidx)
        tab_new = QWidget()
        tab_new.setObjectName(new_tabname)

        self.tabWidget.addTab(tab_new, newfile_name)
        layout = QGridLayout(tab_new)
        layout.setObjectName(f'layout_of_{new_tabname}')
        text_editor = TextEditorS(name=newfile_name)
        # text_editor.textChange.connect(self.__handle_textChange)
        layout.addWidget(text_editor, 0, 0, 1, 1)
        tabitem = TabItem(tab_new, layout, text_editor)
        self.tab_dict[new_tabname] = tabitem

    # TODO: 文件改变则在tab中文件名末尾加上'*'
    # def __handle_textChange(self):
    #     index = self.tabWidget.currentIndex()
    #     if not self.tabWidget.tabText(index).endswith('*'):
    #         pass

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
        if len(file_path):
            _, file_fullname = os.path.split(file_path)

            for tabitem in self.tab_dict.values():
                tmp_edititem = tabitem.text
                # print(tmp_edititem.objectName())
                if file_fullname == tmp_edititem.objectName():
                    return
            self.__create_tab(name=file_fullname)
            index = self.tabWidget.count() - 1
            textedit = self.__get_textEditor(index=index)
            file_type = file_path.split('.')[-1]
            self.language = file_type
            # print('file path: {}, file type: {}'.format(file_path, file_type))
            text = ''
            try:
                """读文件"""
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        text += line
                    self.file_save_path = file_path
                textedit.setPlainText(text)
                self.tabWidget.setCurrentIndex(index)
            except FileNotFoundError:
                """弹出窗口，提示文件不存在"""
                QMessageBox.warning(self, 'Warning', 'Text does not exist!')

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
        ...

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
        # print(self.tab_dict)

    def rewardEvent(self):
        r"""
            打赏事件函数
        :return:
        """
        self.qrcode_window = Reward()
        self.qrcode_window.show()
        
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
