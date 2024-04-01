from core.mathkey import MathKeyController
from core.service import ServerManager, Server
from core.gui import Tray, StateGUI, InputWin, StatusBarWin
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import sys
# from core.gui import Tray, StateGUI, InputWin, StatusBarWin
import sys

def main():
    #托盘
    tray = Tray('static/icon.png','MathKey','MathKey')
    startGUI = StateGUI()
    # 服务管理
    serverManager = ServerManager()
    serverManager.add_servers(
        [Server("MathKeyListener", MathKeyController.listenerStart, MathKeyController.listenerStop),
         Server("MathKeyGlobalHot", MathKeyController.globalStart, MathKeyController.globalStop),
         Server("MathKeyTray",tray.run,tray.stop),
         Server("MathKeyGUI", startGUI.run, startGUI.stop)])
    serverManager.onSystemStart()
    
if __name__ == '__main__':
    main()

