from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, \
    QStackedWidget, QHBoxLayout, QFormLayout, QLineEdit, QFontComboBox, \
    QPushButton, QVBoxLayout, QLabel, QMessageBox, QFileDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QIntValidator, QFont
import configparser


class Preference(QWidget):
    r"""
        偏好设置组件
    """
    def __init__(self, par=None):
        super().__init__()
        # self.setGeometry(300, 50, 10, 10)
        self.par = par
        self.resize(500, 400)
        self.setWindowTitle('Preferences')
        self.mainWidget = QWidget()
        self.buttonsWidget = QWidget()
        self.interpWidget = QWidget()  # 配环境Widget
        self.leftlist = QListWidget()
        self.leftlist.insertItem(0, 'Font')
        self.leftlist.insertItem(1, 'Environment')
        self.font_content = {'font': 'Andale Mono', 'size': '12'}
        self.cfg_path = 'config.ini'
        self.interpreter = ''
        self.load_cfg()
        self.fontpage = QWidget()
        self.environpage = QWidget()
        self.lineEdit = QLineEdit()  # 设置字体大小的文本框
        self.fontbox = QFontComboBox()  # 设置字体样式的下拉框
        self.interpEdit = QLineEdit()  # 设置解释器的文本框

        self.fontUI()
        self.buttonUI()
        self.environUI()

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.fontpage)
        self.stack.addWidget(self.environpage)
        # Widget handler
        mHbox = QHBoxLayout()
        mHbox.addWidget(self.leftlist)
        mHbox.addWidget(self.stack)
        mHbox.setStretchFactor(self.leftlist, 1)
        mHbox.setStretchFactor(self.stack, 5)
        self.mainWidget.setLayout(mHbox)

        Vbox = QVBoxLayout()
        Vbox.addWidget(self.mainWidget)
        Vbox.addWidget(self.buttonsWidget)
        Vbox.setStretchFactor(self.mainWidget, 10)
        Vbox.setStretchFactor(self.buttonsWidget, 1)
        self.setLayout(Vbox)
        self.leftlist.currentRowChanged.connect(self.display)

    def load_cfg(self):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(self.cfg_path)
        # secs = cfg_parser.sections()
        try:
            self.font_content = dict(cfg_parser.items('font_family'))
            self.interpreter = cfg_parser.get('environment', 'interpreter')
        except Exception as e:
            self.save_cfg()
        self.par.font_content = self.font_content

    def save_cfg(self):
        cfg_parser = configparser.ConfigParser()
        cfg_parser.read(self.cfg_path)
        if 'font_family' not in cfg_parser.sections():
            cfg_parser.add_section('font_family')
        if 'environment' not in cfg_parser.sections():
            cfg_parser.add_section('environment')
        cfg_parser.set('font_family', 'font', self.font_content['font'])
        cfg_parser.set('font_family', 'size', self.font_content['size'])
        cfg_parser.set('environment', 'interpreter', self.interpreter)
        with open(self.cfg_path, 'w') as f:
            cfg_parser.write(f)

    def fontUI(self):
        r"""
        字体设置栏目的UI界面
        :return:
        """
        font_layout = QFormLayout()
        line_edit = self.lineEdit
        line_edit.setText(str(self.font_content['size']))
        line_edit.setClearButtonEnabled(True)
        line_edit.setValidator(QIntValidator(12, 20))
        line_edit.setMaximumWidth(50)
        self.fontbox.setFontFilters(self.fontbox.MonospacedFonts)
        self.fontbox.setMaximumWidth(200)
        self.fontbox.setCurrentFont(QFont(self.font_content['font']))
        font_layout.addRow('Font', self.fontbox)
        font_layout.addRow('Size', line_edit)
        self.fontpage.setLayout(font_layout)

    def buttonUI(self):
        r"""
        确认、取消按键的UI
        :return:
        """
        layout = QHBoxLayout()
        ok_btn = QPushButton()
        layout.addWidget(QLabel())
        layout.addWidget(QLabel())
        layout.addWidget(QLabel())
        ok_btn.setText('OK')
        apply_btn = QPushButton()
        apply_btn.setText('Apply')
        cancel_btn = QPushButton()
        cancel_btn.setText('Cancel')
        layout.addWidget(cancel_btn)
        layout.addWidget(apply_btn)
        layout.addWidget(ok_btn)

        cancel_btn.clicked.connect(self.close)
        apply_btn.clicked.connect(self.__apply_btn_event)
        ok_btn.clicked.connect(self.__ok_btn_event)
        self.buttonsWidget.setLayout(layout)

    def environUI(self):
        r"""
        环境设置栏目的UI界面
        :return:
        """
        environ_layout = QFormLayout()
        interp_layout = QHBoxLayout()
        env_btn = QPushButton()
        env_btn.setText('browse')
        env_btn.clicked.connect(self.environHandler)

        self.interpEdit.setText(self.interpreter)
        interp_layout.addWidget(self.interpEdit)
        interp_layout.addWidget(env_btn)
        self.interpWidget.setLayout(interp_layout)
        environ_layout.addRow('Interpreter', self.interpWidget)

        self.environpage.setLayout(environ_layout)

    def environHandler(self):
        r"""
        环境设置打开文件夹
        :return:
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Choose a interpreter')
        self.interpEdit.setText(file_path)

    def __apply_btn_event(self):
        fontsize = int(self.lineEdit.text())
        font = self.fontbox.currentFont().toString().split(',')[0]
        font_family = {'font': font, 'size': str(fontsize)}
        self.interpreter = self.interpEdit.text()
        if fontsize in range(12, 31):
            self.font_content = font_family
            self.par.font_content = font_family
            self.par.setFontSizeEvent()
            self.save_cfg()
        else:
            QMessageBox.warning(self, 'Warning', 'Font size must be in range 12-30!')

    def __ok_btn_event(self):
        fontsize = int(self.lineEdit.text())
        font = self.fontbox.currentFont().toString().split(',')[0]
        font_family = {'font': font, 'size': str(fontsize)}
        self.interpreter = self.interpEdit.text()
        if fontsize in range(12, 31):
            self.font_content = font_family
            self.par.font_content = font_family
            self.par.setFontSizeEvent()
            self.save_cfg()
            self.close()
        else:
            QMessageBox.warning(self, 'Warning', 'Font size must be in range 12-30!')

    def display(self, index):
        r"""
            设置当前选项卡
        :param index:
        :return:
        """
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    demo = Preference()
    demo.show()
    sys.exit(app.exec_())