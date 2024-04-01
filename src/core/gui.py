import pystray
from PIL import Image
from pystray import MenuItem
from core.mathkey import MathKeyController
import json
import threading
import subprocess
import config.STATIC as STATIC
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout,QPushButton
from PyQt5.QtCore import QTimer
import sys
import core.loader as loader
from core.service import ServerManager
"""
@description: 系统托盘,使用pystray库,实现系统托盘功能
@create: 2024/03/28
@lastUpdate: 2024/04/01
@problems: 点击退出后，程序只是将托盘退出，但是程序并没有退出
"""
class Tray:
    def __init__(self,icon,name,tip):
        self.image = Image.open(icon)
        self.icon = pystray.Icon(name, self.image, tip)
        #创建映射列表
        self.mappinglist = loader.load_mappingNameList()
        #加前缀 映射:
        self.mappinglist = list(map(lambda x:"映射:"+x,self.mappinglist))
        #创建配置列表
        self.configlist = loader.load_configNameList()
        self.configlist = list(map(lambda x:"配置:"+x,self.configlist))
        #创建语料库列表
        self.corpusNamelist = loader.load_corpusNameList()
        self.corpusNamelist = list(map(lambda x:"输入法:"+x,self.corpusNamelist))
        self.__updateMenu()

    def __openConfig(self):
        subprocess.Popen(["start", "", STATIC.CONFIG_PATH], shell=True)

    def __openMap(self):
        subprocess.Popen(["start", "", STATIC.MAP_PATH], shell=True)

    def __update(self,item):
        if item == None:
            MathKeyController.on_change_state(None)
        else:
            MathKeyController.on_change_state(item.text)
        self.__updateMenu()
        

    def __updateMenu(self):
        menu = []
        text = "状态："+str(MathKeyController.state)
        menu.append(MenuItem(text,action=None))   
        menu.append(MenuItem('----映射功能---\n', None))
        for state in self.mappinglist:
            menu.append(MenuItem(state, lambda icon,item:self.__update(item)))
        menu.append(MenuItem('----语料库---\n', None))
        for state in self.corpusNamelist:
            menu.append(MenuItem(state, lambda icon,item:self.__update(item)))
        menu.append(MenuItem('----系统设置---\n', None))
        menu.append(MenuItem('打开映射文件', self.__openMap))
        menu.append(MenuItem('打开配置文件', self.__openConfig))
        menu.append(MenuItem('----配置功能---\n', None))
        for state in self.configlist:
            menu.append(MenuItem(state, lambda icon,item:self.__update(item)))
        menu.append(MenuItem('退出', ServerManager.onSystemFinish))
        self.icon.menu = pystray.Menu(*menu)

    def stop(self):
        self.icon.stop()
        
    def run(self):
        #子线程中运行
        threading.Thread(target=self.icon.run).start()

"""
@description: 主GUI,使用PyQt5库,实现状态栏功能
@create: 2024/03/28
@lastUpdate: 2024/04/01
@problems: 丑陋的界面，需要美化
"""
class MainGUI:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.status_bar = StatusBarWin()
        self.input_win = InputWin()
        
    def run(self):
        self.app.exec_()

    def stop(self):
        self.app.quit()

"""
@description: 状态栏窗口,使用PyQt5库,实现状态栏功能
@create: 2024/03/28
@lastUpdate: 2024/04/01
@problems: 丑陋的界面，需要美化,状态文字背景应与窗口背景一致
"""
class StatusBarWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.m_flag = False

    def initUI(self):
        #设置窗口属性
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint) #窗口置顶，无边框
        screen_geometry = QApplication.desktop().screenGeometry()#获取屏幕大小
        status_width = 120  #设置窗口大小
        status_height = 50
        self.setGeometry(screen_geometry.width() - status_width - 10,  
                         screen_geometry.height() - status_height - 10,
                           status_width, status_height)
        self.setStyleSheet("background-color: rgba(135,206,250, 50%);")# 设置窗口浅蓝色背景，透明度为50%

        #状态提示
        text_label = QLabel('状态提示', self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setGeometry(10, 10, 100, 30)
        text_label.setStyleSheet("QLabel { color : white; }")#设置字体颜色为白色不透明

        #设置定时器，每隔一段时间更新状态，连接插槽
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__updateState)
        self.timer.start(300)
        self.show()
    
    def __updateState(self):
        text = MathKeyController.state
        self.findChild(QLabel).setText(text)

    #重写鼠标事件实现窗口拖动
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))

    #退出程序
    def exit(self):
        ServerManager.onSystemFinish()

"""
@description: 输入窗口,使用PyQt5库,实现输入窗口功能
@create: 2024/03/28
@lastUpdate: 2024/04/01
@problems: 丑陋的界面，需要美化
"""
class InputWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口属性
        self.setFixedSize(1000, 100)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)

        #输入提示
        layout = QVBoxLayout()
        text_label = QLabel('候选区', self)
        text_label.setGeometry(10, 10, 980, 80)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("QLabel { color : black; }")  # 根据背景颜色调整字体颜色
        layout.addWidget(text_label)

        # 设置定时器，每隔一段时间更新状态
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.__updateState)
        self.timer.start(100)

    #随鼠标移动
    def __followMouse(self, pos):
        self.move(pos.x(), pos.y() + 20)  # 位置稍微往下偏移，避免阻碍视线
        self.show()

    #更新状态
    def __updateState(self):
        state = MathKeyController.state.split(":")[0]
        if state == '输入法':
            if len(MathKeyController.inputKey) > 0:
                self.show()
                text = str(MathKeyController.showCandidate)
                if len(MathKeyController.candidate) != 0:
                    selectedCand = MathKeyController.candidate[MathKeyController.selected]
                else:
                    selectedCand = "无"
                text = "候选词："+text +"\n"+"第"+str(MathKeyController.showCandidatePage)+"页" + "\n" + "已选词："+selectedCand
                self.findChild(QLabel).setText(text)
                self.__followMouse(QCursor.pos())
            else:
                self.hide()
        else:
            self.hide()




