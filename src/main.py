import sys
import os

import PySide6.QtCore

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import QCoreApplication

from gui.mainwindow import MainWindow
from core.logger import logger


def setQtPluginPath():
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        base_path = sys._MEIPASS
        plugin_path = os.path.join(base_path, 'PySide6', 'plugins')
        QCoreApplication.addLibraryPath(plugin_path)

def main():

    setQtPluginPath()

    if PySide6.QtCore.__version_info__ >= (6, 0, 0):
        os.environ["QT_SCALE_FACTOR"] = "1"

    logger.info("Initialized Log")

    app = QApplication(sys.argv)

    # 设置全局字体
    fontId = QFontDatabase.addApplicationFont("resource\\font\\PINGFANG MEDIUM.TTF")
    if fontId != -1:
        fontFamily = QFontDatabase.applicationFontFamilies(fontId)[0]
        QApplication.setFont(QFont(fontFamily))
    else:
        logger.error("Failed to load font")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()