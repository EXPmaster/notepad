import sys
from .ui_paint import Ui_paint_window
from PyQt5.QtWidgets import QApplication,QMainWindow,QFrame,QWidget
from PyQt5.QtGui import QPainter,QColor,QFont,QPixmap
from PyQt5 import QtCore
from .PaintBoard import PaintBoard

import pyperclip

import torch
import os

from torchvision import transforms
from .nets import SOAT
from collections import OrderedDict

class PaintForm(QMainWindow,Ui_paint_window):
    def __init__(self,parent=None):
        super(PaintForm, self).__init__(parent)
        with open('./hd_board/new_char_dict.txt', 'r',encoding='UTF-8') as f:
            self.char_dict = {k: v.strip() for k,v in enumerate(f.readlines())}

        #img transform
        transform = transforms.Compose([
                                        transforms.Grayscale(1),
                                        transforms.Resize([96, 96]),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.86693], [0.216285])
                                        ])

        #训练模型读取，替换匹配
        model_dir = './hd_board/'
        self.model = SOAT(num_classes=3755)
        model_path = os.path.join(model_dir, 'model_best.pth.tar')
        print('Loading model params from %s' % model_path)
        checkpoint = torch.load(model_path,map_location=torch.device('cpu'))
        new_state_dict = OrderedDict()
        for k, v in checkpoint['state_dict'].items():
            name = k
            if k[:4] == "attn":
                name = k[:5] + ".0" + k[5:]
            new_state_dict[name] = v
        self.model.load_state_dict(new_state_dict)

        self.words=['汪','潇','翔']
        self.word=''
        self.setupUi(self)
        self.r.setFrameStyle(QFrame.Box|QFrame.Plain)
        self.r.setLineWidth(5)
        self.boardframe = PaintBoard(self)
        self.boardframe.setGeometry(QtCore.QRect(20, 20, 330, 330))
        self.Textplay1=Textplay(0,self)
        self.Textplay1.setGeometry(QtCore.QRect(385, 20, 70, 70))
        self.Textplay2=Textplay(1,self)
        self.Textplay2.setGeometry(QtCore.QRect(385, 120, 70, 70))
        self.Textplay3=Textplay(2,self)
        self.Textplay3.setGeometry(QtCore.QRect(385, 220, 70, 70))

        #清零按钮绑定
        self.pushButton_clear.pressed.connect(self.boardframe.Clear)
        #撤销事件绑定
        self.pushButton_back.pressed.connect(self.Back)#boardframe.Clear)
        self.pushButton_back.released.connect(self.Back_end)
        #橡皮擦事件绑定
        self.radioButton_Eraser.toggled.connect(self.Eraser_choose)
        #颜色改变
        self.comboBox_color.currentIndexChanged.connect(self.color_changed)
        #线宽改变
        self.comboBox_line.currentIndexChanged.connect(self.line_changed)

    def Eraser_choose(self):
        if self.radioButton_Eraser.isChecked():
            self.boardframe.EraserMode = True #进入橡皮擦模式
        else:
            self.boardframe.EraserMode = False #退出橡皮擦模式

    def Back(self):
        #撤销笔迹
        self.boardframe.EraserMode = True
        self.boardframe.point_temp = self.boardframe.points[-1]
        self.boardframe.update()
        #print (self.word)

    def Back_end(self):
        #删除列表
        self.boardframe.EraserMode = False
        if len(self.boardframe.points) == 1:
            pass
        else:
            self.boardframe.points.pop()
            self.boardframe.point_temp = []
            for point_temp in self.boardframe.points:
                self.boardframe.point_temp.extend(point_temp)
                self.boardframe.point_temp.extend([[-1,-1]])
            self.boardframe.update()
            self.boardframe.save()

    def color_changed(self):
        Ind=self.comboBox_color.currentIndex()
        if Ind == 0:
            self.boardframe.color=QtCore.Qt.black
        if Ind == 1:
            self.boardframe.color=QtCore.Qt.blue
    
    def line_changed(self):
        lin=int(self.comboBox_line.currentText())
        self.boardframe.line=lin

    #传入三个字
    def add_words(self,words):
        self.words = words
        self.Textplay1.update()
        self.Textplay2.update()
        self.Textplay3.update()

    #读取正确结果
    def get_res(self):
        return (self.word)

class Textplay(QWidget):
    def __init__(self,index,parent=None):
        super(Textplay, self).__init__(parent)
        self.root=parent
        self.resize(70,70)
        self.index=index

    def paintEvent(self,event):
        self.text=self.root.words[self.index]
        painter=QPainter()
        painter.begin(self)
        #自定义绘制方法
        self.drawText(event,painter)
        painter.end()

    def drawText(self,event,qp):
        #设置画笔的颜色
        qp.setPen(QColor(0,0,0))
        #设置字体
        qp.setFont(QFont('SimSun',50))
        #绘制文字
        qp.drawText(event.rect(),QtCore.Qt.AlignCenter,self.text)
    
    def mousePressEvent(self, QMouseEvent):
        self.root.word = self.text
        pyperclip.copy(self.root.get_res())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = PaintForm()
    MainWindow.show()
    sys.exit(app.exec_())