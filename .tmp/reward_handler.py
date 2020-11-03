# -*- coding: utf-8 -*-

from UI_forms import Ui_Form_reward
from PyQt5 import QtWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap


class Reward(QtWidgets.QWidget, Ui_Form_reward):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButton_close.clicked.connect(self.close)
        self.addPicture()

    def addPicture(self):
        img_path = './imgs/qrcode.PNG'
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x, y = img.shape[1], img.shape[0]
        self.zoomscale = 0.5  # 图片放缩尺度
        frame = QImage(img, x, y, x*3, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QtWidgets.QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setScale(self.zoomscale)
        self.scene = QtWidgets.QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)


