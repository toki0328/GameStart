import json
import subprocess
import threading
import os

from core.logger import logger

class MumuApi:

    m_ConfigPath = "config/config.json"

    def __init__(self):
        pass

    def getMumuManagerPath(self) -> str:
        config = json.load(open(self.m_ConfigPath, "r", encoding="utf-8"))

        if config['mumuManagerPath'] == "": 
            config['mumuManagerPath'] = self.autoFindMumuManagerPath()
            json.dump(config, open(self.m_ConfigPath, "w", encoding="utf-8"), indent=4)
            return self.autoFindMumuManagerPath()
        else:
            if os.path.exists(config['mumuManagerPath']):
                return config['mumuManagerPath']
            else:
                config['mumuManagerPath'] = self.autoFindMumuManagerPath()
                json.dump(config, open(self.m_ConfigPath, "w", encoding="utf-8"), indent=4)
                return self.autoFindMumuManagerPath()


    def startMumu(self):
        """
        启动mumu
        """
        cmd = [self.getMumuManagerPath(), "api", "-v", "0", "launch_player"]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()  


    def closeMumu(self):
        """
        关闭mumu
        """   
        cmd = [self.getMumuManagerPath(), "api", "-v", "0", "shutdown_player"]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()  


    def getStateInfo(self):
        """
        获取mumu状态信息
        """
        cmd = [self.getMumuManagerPath(), "api", "-v", "0", "player_state"]
        threading.Thread(target = self.runCmd, args = (cmd, )).start()    
        
    def runCmd(self, cmd):
        result = subprocess.run(cmd, capture_output = True, text = True)
        logger.info(result.stdout)


    # 自动查找mumu manager路径
    def autoFindMumuManagerPath(self):
        if os.name == 'nt':
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MuMuPlayer-12.0")
            # _ 忽略值的类型
            iconPath, _ = winreg.QueryValueEx(key, "DisplayIcon")
            iconPath = iconPath.replace('"', '')
            iconDirPath = os.path.dirname(iconPath)
            mumuManagerPath = os.path.join(iconDirPath, "MuMuManager.exe")
            return mumuManagerPath
        


mumuApi = MumuApi()