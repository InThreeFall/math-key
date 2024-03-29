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

class Tray:
    def __init__(self,icon,name,tip):
        self.image = Image.open(icon)
        self.icon = pystray.Icon(name, self.image, tip)
        #读取map.json
        with open(STATIC.MAP_PATH, 'r',encoding='utf-8') as f:
            self.list = list(json.load(f).keys())
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

class StateGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_attributes("-alpha",1)        # 透明度(0.0~1.0)
        self.root.wm_attributes("-toolwindow", True)  # 置为工具窗口(没有最大最小按钮)
        self.root.wm_attributes("-topmost", True)     # 永远处于顶层
        #隐藏窗口
        self.root.withdraw()
        #　导入DragWindow类
        self.root = DragWindow()
        self.root.set_window_size(100, 60)
        self.root.set_display_postion(1100, 600)
        # 还可以调用如下方法去除窗口边框
        self.root.overrideredirect(True)
        self.label = tk.Label(self.root, text=MathKeyController.state)
        self.label.pack()
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(side=tk.BOTTOM)
        self.updateState()

    def updateState(self):
        #开启定时器 1s更新一次
        self.label['text'] = MathKeyController.state
        self.root.after(1000, self.updateState)

    def run(self):
        self.root.mainloop()
    def stop(self):
        self.root.quit()




