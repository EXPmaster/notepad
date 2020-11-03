from PyQt5.QtWidgets import *
from UI_forms import Ui_Find
from PyQt5.QtGui import *


class Find_Win(QMainWindow, Ui_Find):
    def __init__(self, parent_win, textedit):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Find")
        self.parent_win = parent_win
        self.textedit = textedit
        self.text_target = ''
        self.text_rep_with = ''
        self.start = 0
        self.is_mark = False
        self.text_content = self.textedit.text()
        self.current_count = 1
        self.lineEdit_find_find.textChanged.connect(self.target_changed)
        self.lineEdit_mark_target.textChanged.connect(self.target_changed)
        self.lineEdit_replace_target.textChanged.connect(self.target_changed)
        self.textedit.textChanged.connect(self.content_changed)
        self.pushButton_find_cancel.clicked.connect(self.win_close)
        self.pushButton_replace_cancel.clicked.connect(self.win_close)
        self.pushButton_mark_cancel.clicked.connect(self.win_close)
        self.pushButton_find_next.clicked.connect(self.find_find)
        self.pushButton_find_count.clicked.connect(self.count)
        self.pushButton_replace_next.clicked.connect(self.replace_find)
        self.pushButton_replace_replace.clicked.connect(self.replace_one)
        self.pushButton_replace_all.clicked.connect(self.replace_all)
        #self.pushButton_mark_all.clicked.connect(self.mark_all)
        #self.pushButton_mark_clear.clicked.connect(self.clear_all)

    """-----目标搜索框文本改变--------"""

    def target_changed(self):
        # print("目标框文本改变")
        self.text_target = self.sender().text()
        self.current_count = 1
        self.start = 0
        self.total_count = self.text_content.count(self.text_target)
        self.text_syn()
        self.is_mark = False

    """文本编辑框文本改变--------"""

    def content_changed(self):
        # print("文本编辑框文本改变")
        self.text_content = self.textedit.text()
        self.current_count = 1
        self.start = 0
        self.total_count = self.text_content.count(self.text_target)
        self.is_mark = False

    """----三个搜索框文本同步-----"""

    def text_syn(self):
        self.lineEdit_find_find.setText(self.text_target)
        self.lineEdit_mark_target.setText(self.text_target)
        self.lineEdit_replace_target.setText(self.text_target)

    """----find tab页 find next操作----"""

    def find_find(self):
        self.find(self.textBrowser_find)

    """----replace tap页 find next操作----"""

    def replace_find(self):
        self.find(self.textBrowser_replace)

    """----字符串查找返回索引到代码编辑器编辑器坐标的转化----"""
    def index2coor(self,index):
        count=0
        row_num=0
        col_num=0
        while count < index:
            if self.text_content[count] == '\n':
                row_num += 1
                col_num = 0
            else:
                col_num += 1
            count+=1
        return (row_num,col_num)

    """----find操作----"""

    def find(self, parent_Browser):
        if self.total_count == 0:
            parent_Browser.setText("find:Unable to find text {}".format(self.text_target))
        elif self.current_count <= self.total_count:
            self.start = self.text_content.find(self.text_target, self.start)
            #print(self.start)
            row_num1,col_num1 = self.index2coor(self.start)
            row_num2,col_num2 = self.index2coor(self.start + len(self.text_target))
            #print(row_num1,col_num1,row_num2,col_num2)
            self.select(len(self.text_target))
            parent_Browser.setText("find:{}/{} match".format(str(self.current_count), str(self.total_count)))
            self.current_count += 1
            self.start += len(self.text_target)
        else:
            parent_Browser.setText("find: We have found to the bottom!")

    """----replace tap页replace操作----"""
    """替换后，从当前光标处往后移动寻找target并且选中"""

    def replace_one(self):
        # tc.selectedText()
        """如果没有选中，第一个replace先执行find选中"""
        if self.textedit.selectedText() == '':
            self.start = self.text_content.find(self.text_target, 0)
            row_num1,col_num1 = self.index2coor(self.start)
            row_num2,col_num2 = self.index2coor(self.start + len(self.text_target))
        else:
            self.replace()
        self.curse_move()

    """替换光标选中的字符串"""

    def replace(self):
        self.text_rep_with = self.lineEdit_replace_with.text()
        self.textedit.replaceSelectedText(self.text_rep_with)
        self.start = self.text_content.find(self.text_target, self.start + len(self.text_rep_with))

    """标记光标选中的字符串"""

    def mark(self):
        self.textedit.setSelectionForegroundColor(QColor('red'))
        self.start = self.text_content.find(self.text_target, self.start+len(self.text_target))

    """取消标记光标选中的字符串"""

    def clear(self):
        self.textedit.resetSelectionForegroundColor()
        self.start = self.text_content.find(self.text_target, self.start+len(self.text_target))

    """----curse移动选中指定位置start目标文本----"""

    def curse_move(self):
        if self.start == -1:
            self.textBrowser_replace.setText("Remove to the bottom or there are no matches")
        else:
            self.select(len(self.text_target))

    def select(self,length):
        row_num1,col_num1 = self.index2coor(self.start)
        row_num2,col_num2 = self.index2coor(self.start + length)
        self.textedit.setSelection(row_num1,col_num1,row_num2,col_num2)

    """----find tap页count操作----"""

    def count(self):
        self.textBrowser_find.setText('count:There are {} matches'.format(str(self.total_count)))

    """----replace tap页replace all操作----"""

    def replace_all(self):
        current_count = 1
        start = 0
        total_count = self.total_count
        while current_count <= total_count:
            print("start" + str(start))
            print("current_count" + str(current_count))
            self.start = self.text_content.find(self.text_target, start)
            start = self.start + len(self.text_rep_with)
            print("self.start" + str(self.start))
            self.select(len(self.text_target))
            self.replace()
            current_count += 1
        self.textBrowser_replace.setText('replace all: {} matches has been replaced'.format(str(current_count - 1)))

    """----mark tap页mark all操作----"""

    def mark_all(self):
        if not self.is_mark:
            current_count = 1
            start = 0
            total_count = self.total_count
            while current_count <= total_count:
                self.start = self.text_content.find(self.text_target, start)
                start = self.start + len(self.text_target)
                self.select(len(self.text_target))
                self.mark()
                current_count += 1
            self.is_mark = True
            self.textBrowser_mark.setText('mark: {} markes'.format(str(current_count - 1)))

    """----mark tab页clear all操作----"""

    def clear_all(self):
        if self.is_mark:
            current_count = 1
            start = 0
            total_count = self.total_count
            print(total_count)
            while current_count <= total_count:
                print("start" + str(start))
                print("current_count" + str(current_count))
                self.start = self.text_content.find(self.text_target, start)
                start = self.start + len(self.text_target)
                print("self.start" + str(self.start))
                self.select(len(self.text_target))
                self.clear()
                current_count += 1
            self.is_mark = False
            self.textBrowser_mark.setText('clear: {} cleares'.format(str(current_count - 1)))

    """----界面关闭界面函数(母界面find打开使能)----"""

    def closeEvent(self, event):
        self.parent_win.win_find_is_show = False

    def win_close(self):
        self.close()



