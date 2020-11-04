from PyQt5.QtWidgets import QFrame, QFileDialog, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QPixmap
from PyQt5.QtCore import Qt, QSize
import pickle
import time


import torch
import os
from time import time
from PIL import Image
from torchvision import transforms
import torch.nn.functional as F
from .nets import SOAT
from collections import OrderedDict 

transform = transforms.Compose([
                                    transforms.Grayscale(1),
                                    transforms.Resize([96, 96]),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.86693], [0.216285])
                                    ])


class PaintBoard(QFrame):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.root = parent
        self.size = QSize(330,330)
        self.board = QPixmap(self.size)
        self.pixPainter=QPainter(self.board)
        self.board.fill(Qt.white)
        self.setFixedSize(self.size)
        self.setMouseTracking(False)
        self.EraserMode = False
        self.points=[[[-1,-1]]]
        self.point_temp =[]
        self.color = Qt.black
        self.line = 8
        self.path=("temp.png",'*.png')

    def paintEvent(self, QPaintEvent):
        painter = QPainter(self.board)
        painter.begin(self)
        if self.EraserMode == False:
            pen = QPen(self.color, self.line, Qt.SolidLine)
        else:
            pen = QPen(Qt.white, self.line, Qt.SolidLine)
        painter.setPen(pen)
        self.draw(painter)
        painter.end()


    def draw(self,painter):
        # self.pixPainter.begin(self)
        # self.pixPainter.drawPixmap(0,0,self.board)
        # self.pixPainter.end()
        p1=[-1,-1]
        for point in self.point_temp:
            if point==[-1,-1]:
                p1=[-1,-1]
                continue
            else:
                if p1==[-1,-1]:
                    p1=point
                    continue
                else:
                    p2=point
                    painter.drawLine(p1[0],p1[1],p2[0],p2[1])
                    self.point_temp=[]
                    #self.save()
                    p1=p2
        self.pixPainter.begin(self)
        self.pixPainter.drawPixmap(0,0,self.board)
        self.pixPainter.end()

    def mousePressEvent(self, QMouseEvent):
        self.__painting=True
        self.points.append([])
        self.point_temp = []
        self.update()

    def mouseMoveEvent(self, QMouseEvent):
        if self.__painting:
            print ("move")
            x = QMouseEvent.pos().x()
            y = QMouseEvent.pos().y()
            self.points[-1].append([x, y])
            self.point_temp=self.points[-1]
            self.update()
    
    def mouseReleaseEvent(self, QMouseEvent):
        #self.point_temp=self.points[-1]
        self.update()
        print('1')
        # 每松一次鼠标就暂存一下画板内容
        self.save()

    def save(self):
        self.board.scaled(QSize(64,64),Qt.KeepAspectRatio,Qt.SmoothTransformation).save(self.path[0])
        self.predict()

    
    def predict(self):
        image_dir = 'temp.png'
        img = Image.open(image_dir)
        img = transform(img)
        img=img.unsqueeze(0)
        self.root.model.eval()
        logits,v1,v2 = self.root.model(img)
        output = F.log_softmax(logits,dim=1)
        print(output.data.topk(k=3,dim=-1, largest=True).indices)
        pred=output.data.topk(k=3,dim=-1, largest=True).indices
        temp = ['','','']
        temp[0]=self.root.char_dict[pred.numpy()[0][0]]
        temp[1]=self.root.char_dict[pred.numpy()[0][1]]
        temp[2]=self.root.char_dict[pred.numpy()[0][2]]
        self.root.add_words(temp)


    def Clear(self):
        #清空画板
        self.points=[[[-1,-1]]]
        self.point_temp=[]
        self.board.fill(Qt.white)
        self.update()
        self.IsEmpty = True
        self.save()

    

    
    