import pystray
from PIL import Image
from pystray import MenuItem
from core.mathkey import MathKeyController
import json
import tkinter as tk
import threading
from utils.tk_utils import DragWindow
import subprocess
import config.STATIC as STATIC
from tkinter.messagebox import showinfo, showwarning, showerror
from PyQt5.QtCore import Qt, QPoint, QEvent, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
import sys
class Tray:#依赖于pystray,与tk无关
    def __init__(self,icon,name,tip):
        self.image = Image.open(icon)
        self.icon = pystray.Icon(name, self.image, tip)
        #读取map.json
        with open(STATIC.MAP_PATH, 'r',encoding='utf-8') as f:
            self.list = list(json.load(f).keys())
        self.list.append("pinyin")
        self.updateMenu()

    def openConfig(self):
        subprocess.Popen(["start", "", STATIC.CONFIG_PATH], shell=True)

    def openMap(self):
        subprocess.Popen(["start", "", STATIC.MAP_PATH], shell=True)

    def update(self,item):
        if item == None:
            MathKeyController.on_change_state(None)
        else:
            MathKeyController.on_change_state(item.text)
        self.updateMenu()
        

    def updateMenu(self):
        menu = []
        text = "状态："+str(MathKeyController.state)
        menu.append(MenuItem(text,action=None))   
        menu.append(MenuItem('----更改输入法---\n', None))
        for state in self.list:
            menu.append(MenuItem(state, lambda icon,item:self.update(item)))
        menu.append(MenuItem('----系统设置---\n', None))
        menu.append(MenuItem('打开映射文件', self.openMap))
        menu.append(MenuItem('打开配置文件', self.openConfig))
        menu.append(MenuItem('退出', self.stop))
        self.icon.menu = pystray.Menu(*menu)

    def stop(self):
        self.icon.stop()

    def run(self):
        #子线程中运行
        threading.Thread(target=self.icon.run).start()


# 桌面底部的状态提示窗口
class StatusBarWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        print('StatusBarWin')

    def initUI(self):
        #在所有窗口的最上层显示
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        screen_geometry = QApplication.desktop().screenGeometry()
        # 宽度可以根据需要设置，这里举例使用100px的宽度
        status_width = 100
        # 高度可以根据需要设置，这里举例使用30px的高度
        status_height = 30
        
        # 靠右对齐，离底部一定高度(例如离底部10px)
        self.setGeometry(screen_geometry.width() - status_width - 10, screen_geometry.height() - status_height - 10, status_width, status_height)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)

        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")

        # 添加一些内容到窗体
        text_label = QLabel('状态提示', self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("QLabel { color : white; }")  # 根据背景颜色调整字体颜色

        #设置定时器，每隔一段时间更新状态，连接插槽
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateState)
        self.timer.start(500)
        self.show()
    
    def updateState(self):
        text = MathKeyController.state
        self.findChild(QLabel).setText(text)


# 跟随鼠标移动的输入法窗口
class InputWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口的大小
        self.setFixedSize(1000, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)

        # 添加一些内容到窗体,文字垂直和水平都居中
        layout = QVBoxLayout()
        text_label = QLabel('状态提示', self)
        #靠底部对齐，离上方一定高度(例如离上方10px)
        #离左边一定距离(例如离左边10px)
        text_label.setGeometry(10, 10, 980, 80)

        text_label.setAlignment(Qt.AlignCenter)

        text_label.setStyleSheet("QLabel { color : black; }")  # 根据背景颜色调整字体颜色
        layout.addWidget(text_label)

        # 设置定时器，每隔一段时间更新状态，连接插槽
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateState)
        self.timer.start(100)

    def followMouse(self, pos):
        # 移动窗口到鼠标位置
        self.move(pos.x(), pos.y() + 20)  # 位置稍微往下偏移，避免阻碍视线
        self.show()

    def updateState(self):
        if MathKeyController.state == "pinyin":
            if len(MathKeyController.inputKey) > 0:
                self.show()
                text = str(MathKeyController.showCandidate)
                if len(MathKeyController.candidate) != 0:
                    selectedCand = MathKeyController.candidate[MathKeyController.selected]
                else:
                    selectedCand = "无"
                text = "候选词："+text +"\n"+"第"+str(MathKeyController.showCandidatePage)+"页" + "\n" + "已选词："+selectedCand
                self.findChild(QLabel).setText(text)
                self.followMouse(QCursor.pos())
            else:
                self.hide()
        else:
            self.hide()


class StateGUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.status_bar = StatusBarWin()
        self.input_win = InputWin()

    def updateState(self):
        if(MathKeyController.state != "pinyin"):
            self.input_win.hide()
        elif MathKeyController.state == "pinyin":
            self.input_win.show()
            pos = QCursor.pos()
            self.input_win.followMouse(pos)
        
    def run(self):
        self.app.exec_()

    def stop(self):
        self.app.quit()
