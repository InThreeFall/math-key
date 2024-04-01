from core.mathkey import MathKeyController
from core.service import ServerManager, Server
from core.gui import Tray, MainGUI

def main():
    #托盘
    tray = Tray('static/icon.png','MathKey','MathKey')
    startGUI = MainGUI()
    # 服务管理
    ServerManager.add_servers(
        [Server("MathKeyListener", MathKeyController.listenerStart, MathKeyController.listenerStop),
         Server("MathKeyGlobalHot", MathKeyController.globalStart, MathKeyController.globalStop),
         Server("MathKeyTray",tray.run,tray.stop),
         Server("MathKeyGUI", startGUI.run, startGUI.stop)])
    ServerManager.onSystemStart()
    
if __name__ == '__main__':
    main()

