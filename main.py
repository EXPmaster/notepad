# -*- coding: utf-8 -*-

import platform
import sys
from UI_forms import Ui_CodePlus
from all_windows import Find_Win
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
     QFileDialog, QWidget, QGridLayout, QTextEdit, QDirModel, QTabWidget, QDockWidget
from PyQt5 import QtWidgets
from PyQt5.QtGui import QTextCursor,QIcon,QPixmap
from reward_handler import Reward
from PyQt5.QtCore import Qt, QProcess
from textedit import TextEditorS
import os
from preference import Preference
from ide_edit import IDEeditor
from PyQt5.QtGui import QPixmap, QIcon, QKeySequence
import pickle
import shutil
from RunWindow import RunBrowser
from hd_board import PaintForm
from hd_board import PaintForm
from SplashCall import Splash
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class TabItem:
    r"""
        用于存放新建的Tab、layout、textEditor
    """
    __slots__ = ['tab', 'layout', 'text', 'textview']

    def __init__(self, tab, layout, texteditor, textview=None):
        self.tab = tab
        self.layout = layout
        self.text = texteditor
        self.textview = textview


class Notebook(QMainWindow, Ui_CodePlus):
    r"""
        Notebook 类
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.icon = QIcon()
        self.icon.addPixmap(QPixmap("./tianhou.ico"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(self.icon)
        self.setupUi(self)
        """-------- System ---------"""
        self.local_system = platform.system()
        """-------- Short Cuts ---------"""
        self.actionSave.setShortcut(QKeySequence(QKeySequence.Save))
        self.actionUndo.setShortcut(QKeySequence(QKeySequence.Undo))
        self.actionRedo.setShortcut(QKeySequence(QKeySequence.Redo))
        self.actionNew.setShortcut(QKeySequence(QKeySequence.New))
        self.actionCopy.setShortcut(QKeySequence(QKeySequence.Copy))
        self.actionPaste.setShortcut(QKeySequence(QKeySequence.Paste))
        self.actionCut.setShortcut(QKeySequence(QKeySequence.Cut))
        self.actionFind.setShortcut(QKeySequence(QKeySequence.Find))
        self.actionSelect_All.setShortcut(QKeySequence(QKeySequence.SelectAll))
        """-------- Code ---------"""
        self.actionAbout_us.triggered.connect(self.aboutusEvent)  # 关于我们
        self.actionExit.triggered.connect(self.closeEvent)  # 退出
        self.actionPreference.triggered.connect(self.showpreferenceEvent)# 偏好设置
        """-------- File ---------"""
        self.actionNew.triggered.connect(self.newfileEvent)  # 新建
        self.actionOpen_File.triggered.connect(self.openfileEvent)  # 打开文件
        self.actionOpen_Folder.triggered.connect(self.openfolderEvent)# 打开文件夹
        self.actionSave.triggered.connect(self.savefileEvent)  # 保存文件
        self.actionSave_All.triggered.connect(self.saveallEvent)  # 全部保存
        self.actionSave_As.triggered.connect(self.saveasEvent)  # 另存为
        self.actionClose.triggered.connect(self.closefileEvent)  # 关闭
        self.tabWidget.tabCloseRequested.connect(self.closefileEvent)  # 关闭tab
        """-------- Edit ---------"""
        self.actionUndo.triggered.connect(self.text_undo)  # 撤销
        self.actionRedo.triggered.connect(self.text_redo)  # 重做
        self.actionCut.triggered.connect(self.text_cut)  # 剪切
        self.actionCopy.triggered.connect(self.text_copy)  # 复制
        self.actionPaste.triggered.connect(self.text_paste)  # 粘贴
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
        self.model = QDirModel()
        """ view from source"""
        """-------- Run Event ---------"""
        self.dock_win = QtWidgets.QDockWidget()
        self.dock_tab = QtWidgets.QTabWidget()
        self.dock_win.setWidget(self.dock_tab)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_win)
        self.dock_tab.setTabPosition(QTabWidget.South)
        self.teridx = 0
        self.dock_win.setFeatures(QDockWidget.DockWidgetVerticalTitleBar)
        self.dock_tab.setTabsClosable(True)
        self.dock_tab.tabCloseRequested.connect(self.run_close_event)
        self.run_event = False
        self.actionStop.setDisabled(True)
        """-------- Basic Configs ---------"""
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.tabWidget.setAttribute(Qt.WA_DeleteOnClose, True)
        self.tabidx = 0
        self.font_content = None  # 字体和大小
        self.interpreter = None  # 解释器
        self.preference = Preference(par=self)
        self.tab_dict = {}  # 存放tab
        self.file_save_path = None  # 保存文件的路径
        self.language = 'txt'  # 当前语言
        """-------- Terminal ---------"""
        self.actionNew_Terminal.triggered.connect(self.new_terminal_event)
        # self.actionClose_Terminal.triggered.connect(self.close_terminal_event)
        """-------- Run ---------"""
        self.run_browser = RunBrowser(self.font_content)
        self.run_browser.startSignal.connect(self.run_start_event)
        self.run_browser.exitSignal.connect(self.run_exit_event)
        self.gcc = None
        self.actionRun.triggered.connect(self.new_run_event)
        self.actionStop.triggered.connect(self.stop_run)
        self.actionCompile.triggered.connect(self.compile_event)
        """--------tool------------"""
        self.actionWrite_Board.triggered.connect(self.OpenBoard)

        self.enableClickFlag = True  # 改变tab enable的flag
        """所有语言类型为：
            txt -> 文本文件
            md -> Markdown文件
            c -> C文件
            py -> Python文件
            """

        """-------- 初始执行的操作 ---------"""
        self.openIDEevent()

    def OpenBoard(self):
        textedit = self.__get_textEditor()
        self.boardwindow = PaintForm(textedit)
        self.boardwindow.show()

    def openIDEevent(self):
        tmp_path = '.tmp'

        def listdir(path):
            for item in os.listdir(path):
                if not item.startswith('.') and not item.endswith('.pkl'):
                    yield item

        if not os.path.exists(tmp_path) or not os.path.exists(os.path.join(tmp_path, 'mapping.pkl')):
            self.__create_tab()  # 初始创建一个tab
            self.tabWidget.currentChanged.connect(self.changeTab)  # 切换tab触发
        else:
            """读取缓存的文件"""
            with open(os.path.join(tmp_path, 'mapping.pkl'), 'rb') as f:
                mapping = pickle.load(f)
            tmp_files = listdir(tmp_path)
            for i, file in enumerate(tmp_files):

                file_path = os.path.join(tmp_path, file)
                if file.startswith('*'):
                    file = file[1:]
                origin_path = mapping[file]
                self.openfileEvent(file_path, origin_path)
                if i == 0:
                    self.tabWidget.currentChanged.connect(self.changeTab)  # 切换tab触发

        self.lb_lang.setText(self.language)

    def stop_run(self):
        self.run_browser.process.close()

    def run_start_event(self):
        self.actionRun.setDisabled(True)
        self.actionStop.setDisabled(False)

    def run_exit_event(self):
        self.actionRun.setDisabled(False)
        self.actionStop.setDisabled(True)

    def new_run_event(self):
        if not self.run_event:
            pix = QPixmap('./imgs/run.jpg')
            icon = QIcon()
            icon.addPixmap(pix)
            self.dock_tab.addTab(self.run_browser, 'Run ')
            index = self.dock_tab.count() - 1
            self.dock_tab.setTabIcon(index, icon)
            self.dock_tab.setCurrentIndex(index)
            self.run_event = True
        cur_path = self.__get_textEditor().filepath
        if cur_path:
            if os.path.splitext(cur_path)[-1] == '.py':
                if not self.interpreter:
                    QMessageBox.warning(self, '提示', '未设置有效的python解释器\n' +
                                        '->\n'.join(['Code', 'Preference', 'Environment', 'interpreter']))
                    return
                cmd = ' '.join([self.interpreter, cur_path])
                self.run_browser.start_process(cmd)
            elif os.path.splitext(cur_path)[-1] == '.c':
                cmd = os.path.splitext(cur_path)[0] + '.exe'
                if os.path.exists(cmd):
                    self.run_browser.process.start(cmd)
                else:
                    compile_cmd = 'gcc ' + cur_path
                    self.run_browser.process.start(compile_cmd)
                    self.run_browser.process.waitForFinished()
                    if os.path.exists(cmd):
                        self.run_browser.process.start(cmd)

    def compile_event(self):
        if not self.run_event:
            pix = QPixmap('./imgs/run.jpg')
            icon = QIcon()
            icon.addPixmap(pix)
            self.dock_tab.addTab(self.run_browser, 'Run ')
            index = self.dock_tab.count() - 1
            self.dock_tab.setTabIcon(index, icon)
            self.dock_tab.setCurrentIndex(index)
            self.run_event = True
        cur_path = self.__get_textEditor().filepath
        if cur_path:
            if os.path.splitext(cur_path)[-1] == '.c':
                cmd = 'gcc ' + cur_path
                self.run_browser.start_process(cmd)

    def run_close_event(self):
        if not self.actionRun.isEnabled():
            ref = QMessageBox.information(self, '提示', '还有项目正在运行\n确定退出？', QMessageBox.Yes | QMessageBox.No)
            if ref == QMessageBox.Yes:
                self.stop_run()
            else:
                return
        self.run_event = False
        self.dock_tab.removeTab(0)

    def new_terminal_event(self):
        if self.local_system == 'Windows':
            os.system('start cmd')
        elif self.local_system == 'Linux':
            os.system('gnome-terminal')
        elif self.local_system == 'Darwin':
            os.system('open -a Terminal .')

    def close_terminal_event(self):
        if self.local_system == 'Darwin':
            import appscript
            appscript.app('Terminal').do_script('exit')
    # def new_terminal_event(self):
    #     from threading import Thread
    #     t = Thread(target=self.aaa)
    #     t.start()
    #
    #     self.teridx += 1
    #     self.temp = QTextEdit()
    #     time.sleep(1)
    #     calc_hwnd = win32gui.FindWindow(None, u'C:\WINDOWS\system32\cmd.exe')
    #     print(calc_hwnd)
    #
    #     self.win = QWindow.fromWinId(calc_hwnd)
    #
    #     self.new_tab = self.createWindowContainer(self.win, self.temp)
    #     self.new_tab.showMaximized()
    #     # self.win.setKeyboardGrabEnabled(True)
    #     # self.win.setMouseGrabEnabled(True)

    # 查找
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
        # if self.language == 'txt':
        #     self.actionPlain_Text.setDisabled(True)

        if signal_src == 'Markdown':
            self.markdown_handler()
        else:
            self.normalmode_handler()

    def changeTab(self):
        # super().tabWidget.changeEvent()
        self.language = self.cur_language()
        self.lb_lang.setText(self.language)
        cur_tabs = self.tabWidget.count()
        if cur_tabs == 0:
            self.actionCut.setDisabled(True)
            self.actionFind.setDisabled(True)
            self.actionSave.setDisabled(True)
            self.actionSave_All.setDisabled(True)
            self.actionSave_As.setDisabled(True)
            self.actionClose.setDisabled(True)
            self.actionUndo.setDisabled(True)
            self.actionRedo.setDisabled(True)
            self.actionCopy.setDisabled(True)
            self.actionPaste.setDisabled(True)
            self.actionSelect_All.setDisabled(True)
            self.actionC.setDisabled(True)
            self.actionPython.setDisabled(True)
            self.actionPlain_Text.setDisabled(True)
            self.actionMarkdown.setDisabled(True)
            self.actionRun.setDisabled(True)
            self.actionCompile.setDisabled(True)
            self.enableClickFlag = False
        else:
            if not self.enableClickFlag:
                self.enableClickFlag = True
                self.actionCut.setDisabled(False)
                self.actionFind.setDisabled(False)
                self.actionSave.setDisabled(False)
                self.actionSave_All.setDisabled(False)
                self.actionSave_As.setDisabled(False)
                self.actionClose.setDisabled(False)
                self.actionUndo.setDisabled(False)
                self.actionRedo.setDisabled(False)
                self.actionCopy.setDisabled(False)
                self.actionPaste.setDisabled(False)
                self.actionSelect_All.setDisabled(False)
                self.actionC.setDisabled(False)
                self.actionPython.setDisabled(False)
                self.actionPlain_Text.setDisabled(False)
                self.actionMarkdown.setDisabled(False)
                self.actionRun.setDisabled(False)
                self.actionCompile.setDisabled(False)

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

    def __get_tabitem(self, index=None):
        r"""
            获取当前tab
        :return: (object) tab
        """
        if index is None:
            index = self.tabWidget.currentIndex()
        _, tabitem = self.__find_tab_by_index(index)
        return tabitem

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
        text_editor.newFileSignal.connect(lambda: self.model.refresh())
        # text_editor.textChange.connect(self.__handle_textChange)

        layout.addWidget(text_editor, 0, 0, 1, 1)
        tabitem = TabItem(tab_new, layout, text_editor)
        self.tab_dict[new_tabname] = tabitem
        self.tabWidget.addTab(tab_new, newfile_name)
        # 跳转到新页面
        index = self.tabWidget.count() - 1
        self.tabWidget.setCurrentIndex(index)
        if language == 'md':
            self.markdown_handler()

    def openfileEvent(self, file_path=None, mapping=None):
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
            if not file_path:
                return
        # 判断文件是否可读取
        if os.path.isdir(file_path):  # 屏蔽文件夹
            return
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
            textedit.load(file_path, mapping)

    def openfolderEvent(self):
        folder_path = QFileDialog.getExistingDirectory(self, '请选择打开的文件夹')
        if folder_path:
            self.dirtree.setModel(self.model)
            self.dirtree.setRootIndex(self.model.index(folder_path))
            self.dirtree.setAnimated(False)
            self.dirtree.setIndentation(20)
            self.dirtree.setSortingEnabled(True)
            self.dirtree.doubleClicked.connect(self.__choose_file)
            self.dirtree.setWindowTitle("Dir View")
            # self.dirtree.setHeaderHidden(True)

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
            textedit = self.__get_textEditor(index)
            self.language = textedit.language
            self.lb_lang.setText(self.language)

    def savefileEvent(self):
        r"""
            保存文件事件函数
        :return:
        """
        textedit = self.__get_textEditor()
        text_saveas = textedit.save()
        if text_saveas:
            self.language = textedit.language
            self.lb_lang.setText(self.language)

    def saveallEvent(self):
        r"""
            全部保存
        :return:
        """
        for tabitem in self.tab_dict.values():
            textedit = tabitem.text
            text_saveas = textedit.save()
            if text_saveas:
                self.language = textedit.language
                self.lb_lang.setText(self.language)

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
        self.run_browser.set_font(self.font_content)

    def rewardEvent(self):
        r"""
            打赏事件函数
        :return:
        """
        self.qrcode_window = Reward()
        self.qrcode_window.show()

    def showpreferenceEvent(self):
        r"""
            调出偏好设置
        :return:
        """
        self.preference.show()

    def aboutusEvent(self):
        r"""
            关于我们事件函数
        :return:
        """
        QMessageBox.information(self, 'About us',
                                'Monkey Editor v0.1\n'
                                u'天猴工作室出品 \n'
                                u'制作人：吴栋、廖满文、汪潇翔、文一晴、吴雨暄、张维天')

    def closeEvent(self, event):
        r"""
            关闭notebook事件函数
        :param event:
        :return: None
        """
        # 缓存文件的文件夹
        tmp_path = '.tmp'
        if os.path.exists(tmp_path):
            # os.system(f'rm -r {tmp_path}')
            shutil.rmtree(tmp_path)

        if len(self.tab_dict):
            os.mkdir(tmp_path)
        # check_quit = True
        increment = 1
        mapping = {}  # 地址映射表
        for tabitem in self.tab_dict.values():
            # 缓存当前未关闭的页面
            textedit = tabitem.text
            if textedit.filepath is None:
                tmp_filename = f'Plain_{increment}.' + self.language
                mapping[tmp_filename] = None
                tmp_filepath = os.path.join(tmp_path, tmp_filename)
                increment += 1
            else:
                _, tmp_filename = os.path.split(textedit.filepath)
                mapping[tmp_filename] = textedit.filepath
                tmp_filepath = os.path.join(tmp_path, tmp_filename)

            if textedit.isModified():
                # check_quit = False
                tmp_filepath = os.path.join(tmp_path, '*' + tmp_filename)
            textedit.save(tmp_filepath)

        # 保存mapping
        try:
            with open(os.path.join(tmp_path, 'mapping.pkl'), 'wb') as f:
                pickle.dump(mapping, f)
        except:
            pass

        # if not check_quit:
        #     ret_code = QMessageBox.information(self, '提示', '存在文件未保存，确定退出？',
        #                                            QMessageBox.Yes | QMessageBox.No)
        #     if ret_code == QMessageBox.Yes:
        #         self.close()
        #     else:
        #         event.ignore()
        # else:
        # 保存preference
        self.preference.close()
        self.close()

    def markdown_handler(self):
        index = self.tabWidget.currentIndex()
        _, tabitem = self.__find_tab_by_index(index)
        current_tab = tabitem.tab
        current_layout = tabitem.layout
        current_text = tabitem.text
        # content = current_text.text()
        # content.replace(r'\r\n', r'  \n')
        # content = ''
        # for i in range(linenum - 1):
        #     current_content = current_text.document().findBlockByLineNumber(i).text()
        #     current_content += '  \n'
        #     content += current_content
        # for i in reversed(range(current_layout.count())):
        #     current_layout.takeAt(i).widget().deleteLater()
        # markdown_tab = QtWidgets.QTabWidget(current_tab)
        # markdown_tab.setTabPosition(3)
        # orin = QWidget()
        # md = QWidget()
        # orin.setObjectName("orin")
        # md.setObjectName("md")
        # layout_orin = QGridLayout(orin)
        # text_editor_orin = TextEditorS(name='orin', parent_tabWidget=self.tabWidget, language=language)
        # layout_orin.addWidget(text_editor_orin, 0, 0, 1, 1)
        # layout_md = QGridLayout(md)
        # text_editor_txt = TextEditorS(name='md_txt', parent_tabWidget=self.tabWidget,
        #                         language='txt', font_content=self.font_content)
        text_browser_md = TextEditorS(name='md_show', parent_tabWidget=self.tabWidget,
                                language='md')

        text_browser_md.setReadOnly(True)
        # text_editor_txt = TextEditorS(name='md_txt', parent_tabWidget=self.tabWidget, language='txt')
        # text_browser_md = TextEditorS(name='md_md', parent_tabWidget=self.tabWidget, language=self.language)
        # layout_md.addWidget(text_editor_txt, 0, 0, 1, 1)
        # layout_md.addWidget(text_browser_md, 0, 1, 1, 1)
        # markdown_tab.addTab(orin, 'orin')
        # markdown_tab.addTab(md, 'md')
        current_layout.addWidget(text_browser_md, 0, 1, 1, 1)
        # current_layout.addWidget(markdown_tab, 0, 0, 1, 1)
        tabitem = TabItem(current_tab, current_layout, current_text, text_browser_md)
        now_tabname = 'tab_' + str(self.tabidx)
        self.tab_dict[now_tabname] = tabitem
        current_text.linesChanged.connect(self.show_markdown)
        # text_editor_txt.document().blockCountChanged.connect(self.show_markdown)
        # text_editor_txt.setPlainText(content)
        # text_editor_txt.document().blockCountChanged.connect(self.show_markdown)

    def normalmode_handler(self):
        index = self.tabWidget.currentIndex()
        _, tabitem = self.__find_tab_by_index(index)
        current_tab = tabitem.tab
        current_layout = tabitem.layout
        current_text = tabitem.text
        if tabitem.textview != None:
            current_layout.itemAt(1).widget().close()
            tabitem = TabItem(current_tab, current_layout, current_text)
            now_tabname = 'tab_' + str(self.tabidx)
            self.tab_dict[now_tabname] = tabitem

    def show_markdown(self):
        current_tab = self.__get_tabitem()
        textedit = current_tab.text
        textview = current_tab.textview
        if textview != None:
            content = textedit.text()
            content = content.replace('\r\n', '  \n')
            textview.document().setMarkdown(content)
        # linenum = textedit.document().lineCount()
        # content = ''
        # for i in range(linenum - 1):
        #     current_content = textedit.document().findBlockByLineNumber(i).text()
        #     current_content += '  \n'
        #     content += current_content
    def windowShow(self):
        youWin.show()  #你的主页程序
#style_transfer


if __name__ == '__main__':
    # with open("style.qss") as f:
    #     qss = f.read()
    app = 0
    app = QApplication(sys.argv)
    #style_transfer()
    youWin = Notebook()
    # app.setStyleSheet(qss)
    #MainWindow = Notebook()
    #MainWindow.show()
    UiSplash = Splash()  ##开机界面
    UiSplash.show()
    UiSplash.splashClose.connect(youWin.windowShow) #开机界面关闭连接打开你的主页
    
    sys.exit(app.exec_())
