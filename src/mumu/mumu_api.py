import subprocess
import threading

from typing import Dict, List
from core.logger import logger
from .auto_task import getMumuManagerPath, autoDetectMumu

class MumuApi:

    def __init__(self):\
        self.mumuManagerPath = self.getMumuManagerPath()

    def getMumuManagerPath(self) -> str:
        """
        获取mumu manager路径
        """
        return getMumuManagerPath()

    def startMumu(self):
        """
        启动mumu
        """
        cmd = [self.mumuManagerPath, "api", "-v", "0", "launch_player"]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()  


    def closeMumu(self):
        """
        关闭mumu
        """   
        cmd = [self.mumuManagerPath, "api", "-v", "0", "shutdown_player"]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()  


    def getStateInfo(self):
        """
        获取mumu状态信息
        """
        cmd = [self.mumuManagerPath, "api", "-v", "0", "player_state"]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()    
        

    def startApp(self, packageName):
        """
        启动应用
        """
        cmd = [self.mumuManagerPath, "api", "-v", "0", "launch_app", packageName]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()


    def stopApp(self, packageName):
        """
        关闭应用
        """
        cmd = [self.mumuManagerPath, "api", "-v", "0", "close_app", packageName]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()


    def detectAdbAddr(self):
        """
        检测adb地址
        """
        # subprocess.run("adb start-server", shell=True, capture_output=True)
        threading.Thread(target=autoDetectMumu, args=()).start()


    def runCmd(self, cmd):
        result = subprocess.run(cmd, capture_output = True, text = True)
        logger.info(result.stdout)


mumuApi = MumuApi()