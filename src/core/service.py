#导入系统弹窗
import pywin

class Server:
    def __init__(self, servername,startfun,finishfun):
        self.servername = servername
        self.startfun = startfun
        self.finishfun = finishfun

    def start(self):
        self.startfun()

    def finish(self):
        self.finishfun()

class ServerManager:
    servers = []

    def add_server(server:Server):
        ServerManager.servers.append(server)
    
    def add_servers(servers):
        for server in servers:
            ServerManager.servers.append(server)

    def remove_server(serverName):
        for server in ServerManager.servers:
            if server.servername == serverName:
                ServerManager.servers.remove(server)
                break

    def get_servers():
        return ServerManager.servers
    
    def onSystemStart():
        try:
            for server in ServerManager.servers:
                server.start()
        except Exception as e:
            print(e)
        
    def onSystemFinish():
        try:
            for server in ServerManager.servers:
                server.finish()

        except Exception as e:
            print(e)

