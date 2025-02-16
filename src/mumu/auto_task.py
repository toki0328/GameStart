import subprocess
import platform
import os
import re

from core.config import config

# 自动检测相关
# 自动查找mumu manager路径
def autoFindMumuManagerPath():
    if os.name == 'nt':
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MuMuPlayer-12.0")
        # _ 忽略值的类型
        iconPath, _ = winreg.QueryValueEx(key, "DisplayIcon")
        iconPath = iconPath.replace('"', '')
        iconDirPath = os.path.dirname(iconPath)
        mumuManagerPath = os.path.join(iconDirPath, "MuMuManager.exe")
        return mumuManagerPath
    

def getMumuManagerPath() -> str:
    """
    获取mumu manager路径
    """
    # if config['mumuManagerPath'] == "": 
    #     config['mumuManagerPath'] = autoFindMumuManagerPath()
    #     json.dump(config, open(m_ConfigPath, "w", encoding="utf-8"), indent=4)
    #     return autoFindMumuManagerPath()
    # else:
    #     if os.path.exists(config['mumuManagerPath']):
    #         return config['mumuManagerPath']
    #     else:
    #         config['mumuManagerPath'] = autoFindMumuManagerPath()
    #         json.dump(config, open(m_ConfigPath, "w", encoding="utf-8"), indent=4)
    #         return autoFindMumuManagerPath()

    if config.get('mumuManagerPath') == "":
        config.set('mumuManagerPath', autoFindMumuManagerPath())
        return autoFindMumuManagerPath()
    else:
        if os.path.exists(config.get('mumuManagerPath')):
            return config.get('mumuManagerPath')
        else:
            config.set('mumuManagerPath', autoFindMumuManagerPath())
            return autoFindMumuManagerPath()


# ADB 检测
def findMumuAdbPorts():
    """通过进程检测或网络端口扫描获取 MuMu 模拟器的 ADB 端口"""
    """Mumu12 主进程名为 MuMuVMMHeadless.exe, Mumu11 主进程名为 NemuHeadless.exe"""
    system = platform.system()
    adb_ports = []

    # Windows 系统（MuMu 主要在 Windows 运行）
    if system == "Windows":
        try:
            # 方法1: 检测 MuMu 进程的端口（依赖 netstat 和 tasklist）
            # 获取所有 NemuHeadless.exe 进程（MuMu 模拟器主进程）
            tasklist = subprocess.check_output(
                "tasklist /FI \"IMAGENAME eq MuMuVMMHeadless.exe\"", 
                shell=True, 
                text=True
            )
            if "MuMuVMMHeadless.exe" in tasklist:                  
                lines = tasklist.strip().split('\n')
                if len(lines) > 2:
                    pid = int(lines[2].split()[1])

                # 使用 netstat 查找 MuMuVMMHeadless.exe 占用的端口
                if pid is not None:
                    netstat = subprocess.check_output(
                        "netstat -ano | findstr LISTENING | findstr " + str(pid),
                        shell=True,
                        text=True
                    )
                    # 提取端口号（示例输出行：TCP    0.0.0.0:7555           0.0.0.0:0              LISTENING       1234）
                    for line in netstat.splitlines():
                        match = re.search(r":(\d+)\s+0\.0\.0\.0:0\s+LIS", line)
                        if match:
                            adb_ports.append(int(match.group(1)))

            # 方法2: 若方法1失败，尝试默认端口（MuMu 默认端口范围：7555, 7556, 7557...）
            # if not adb_ports:
            #     for port in range(7555, 7560):  # 假设最多检测5个实例
            #         adb_ports.append(port)

        except subprocess.CalledProcessError:
            pass

    # Mac/Linux 暂不支持（MuMu 无官方 Mac/Linux 版本）
    else:
        print("暂不支持非 Windows 系统")

    return adb_ports


def connectMumuAdb(port):
    """尝试连接指定 ADB 端口"""
    adbPath = os.path.dirname(getMumuManagerPath()) + "\\adb.exe"
    cmd = adbPath + f" connect 127.0.0.1:{port}"
    result = subprocess.run(
        cmd,
        capture_output = True,
        text = True
    )


    if result.stdout is not None and "connected" in result.stdout:
        return True, port
    else:
        print(f"连接失败: {result.stderr}")
        return False, port


def autoDetectMumu():
    """自动检测并连接 MuMu 模拟器"""
    ports = findMumuAdbPorts()
    if not ports:
        print("未检测到 MuMu 模拟器")
        return

    # 尝试连接所有检测到的端口
    success_ports = []
    for port in ports:
        success, port = connectMumuAdb(port)
        if success:
            success_ports.append(port)

    # 验证最终连接设备
    if success_ports:
        print("\n连接成功的设备:")

        adbPath = os.path.dirname(getMumuManagerPath()) + "\\adb.exe"
        devices = subprocess.run(adbPath + " devices", capture_output = True, text=True)
        print(devices.stdout)
    else:
        print("连接失败，请确保：\n1. MuMu 已启动\n2. ADB 服务已开启\n3. 防火墙未阻止端口")