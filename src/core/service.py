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
    def __init__(self):
        self.servers = []

    def add_server(self, server:Server):
        self.servers.append(server)
    
    def add_servers(self, servers):
        for server in servers:
            self.servers.append(server)

    def remove_server(self, serverName):
        for server in self.servers:
            if server.servername == serverName:
                self.servers.remove(server)
                break

    def get_servers(self):
        return self.servers
    
    def onSystemStart(self):
        try:
            for server in self.servers:
                server.start()
        except Exception as e:
            print(e)
            #弹出系统提示 错误
            pywin.showMessageBox('错误',e,pywin.MB_ICONERROR)


            
        
    def onSystemFinish(self):
        try:
            for server in self.servers:
                server.finish()
        except Exception as e:
            #弹出系统提示 错误
            pywin.showMessageBox('错误',e,pywin.MB_ICONERROR)

