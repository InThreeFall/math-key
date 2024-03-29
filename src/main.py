from core.mathkey import MathKeyController
from core.service import ServerManager, Server
from core.gui import Tray, StateGUI
icon = None
if __name__ == '__main__':
    tray = Tray('static/icon.png','MathKey','MathKey')
    stateFlow = StateGUI()
    serverManager = ServerManager()
    serverManager.add_servers(
        [Server("MathKeyListener", MathKeyController.listenerStart, MathKeyController.listenerStop),
         Server("MathKeyGlobalHot", MathKeyController.globalStart, MathKeyController.globalStop),
         Server("MathKeyTray",tray.run,tray.stop),
         Server("MathKeyStateGUI",stateFlow.run,stateFlow.stop)])
    serverManager.onSystemStart()
    serverManager.onSystemFinish()

