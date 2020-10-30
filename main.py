import sys
from UI_forms import Ui_CodePlus
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from reward_handler import Reward


class Notebook(QMainWindow, Ui_CodePlus):
    r"""
        Notebook 类
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        """-------- Code ---------"""
        self.actionAbout_us.triggered.connect(self.aboutusEvent)  # 关于我们
        self.actionExit.triggered.connect(self.close)  # 退出
        """-------- File ---------"""
        self.actionNew.triggered.connect(self.newfileEvent)  # 新建
        self.actionOpen_File.triggered.connect(self.openfileEvent)  # 打开文件
        # TODO: Open Folder
        self.actionSave.triggered.connect(self.savefileEvent)  # 保存文件
        self.actionSave_As.triggered.connect(self.saveasEvent)  # 另存为
        self.actionClose.triggered.connect(self.closefileEvent)  # 关闭
        """-------- Edit ---------"""
        self.actionUndo.triggered.connect(self.textEditor.undo)  # 撤销
        self.actionRedo.triggered.connect(self.textEditor.redo)  # 重做
        self.actionCut.triggered.connect(self.textEditor.cut)  # 剪切
        self.actionCopy.triggered.connect(self.textEditor.copy)  # 复制
        self.actionPast.triggered.connect(self.textEditor.paste)  # 粘贴
        # TODO: Find
        self.actionSelect_All.triggered.connect(self.textEditor.selectAll)  # 全选
        """-------- Whatever... ---------"""
        self.actionQR_Code.triggered.connect(self.rewardEvent)  # 打赏
        """-------- Basic Configs ---------"""
        self.file_save_path = None  # 保存文件的路径
        self.tmpNone = 0  # 当前空文件的个数
        self.file_text_dict = {}  # 用于保存文件名和内容，切换文件时进行存、读
        self.language = 'txt'  # 当前语言
        """所有语言类型为：
            txt -> 文本文件
            md -> Markdown文件
            c -> C文件
            py -> Python文件
            """

    def newfileEvent(self):
        r"""
            新建文件事件函数
        :return:
        """
        if self.file_save_path is not None:
            self.file_text_dict[self.file_save_path] = self.textEditor.toPlainText()
        else:
            self.file_text_dict[self.tmpNone] = self.textEditor.toPlainText()
            self.tmpNone += 1
        text = ''
        self.file_save_path = None
        self.textEditor.setPlainText(text)
        # print(self.textEditor.isWindowModified())
        # print(self.file_text_dict)

    def openfileEvent(self):
        r"""
            打开文件事件函数
        :return:
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Choose a file', '/',
                                                        'All Files (*);;'
                                                        'Text Files (*.txt);;'
                                                        'Markdown Files (*.md);;'
                                                        'C Sources (*.c);;'
                                                        'Python Scripts (*.py)')
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
        except FileNotFoundError:
            """弹出窗口，提示文件不存在"""
            QMessageBox.warning(self, 'Warning', 'Text does not exist!')
        self.textEditor.setPlainText(text)

    def saveasEvent(self):
        r"""
            另存为事件函数
        :return:
        """
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save As')
        if len(file_path):
            """如果路径不为空，则保存"""
            self.file_save_path = file_path
            with open(file_path, 'w', encoding='utf-8') as f:
                text = self.textEditor.toPlainText()
                f.writelines(text)
        else:
            # QMessageBox.warning(self, 'Warning', 'File name should not be empty')
            ...

    def savefileEvent(self):
        r"""
            保存文件事件函数
        :return:
        """
        if self.file_save_path is not None:
            """如果文件路径存在，则保存文件"""
            with open(self.file_save_path, 'w', encoding='utf-8') as f:
                text = self.textEditor.toPlainText()
                f.writelines(text)
        else:
            """文件路径不存在则另存为"""
            self.saveasEvent()

    def closefileEvent(self):
        if self.textEditor.document().isModified():
            """以修改文件，需要保存"""
            ret_code = QMessageBox.information(self, '提示', '文件尚未保存，需要保存吗？',
                                               QMessageBox.Yes | QMessageBox.No)
            print(ret_code)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Notebook()
    MainWindow.show()
    sys.exit(app.exec_())