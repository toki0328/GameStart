from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from qfluentwidgets import (FluentWindow, PushButton, FluentTitleBar, FluentIcon as FIF, NavigationItemPosition, MessageBox, CardWidget,
                            IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, ComboBox, ScrollArea, ExpandLayout, SingleDirectionScrollArea)
from qframelesswindow.webengine import FramelessWebEngineView

from .home_fragment import HomeFragment
from .app_fragment import AppFragment
from .settings_fragment import SettingsFragment

from core.logger import logger


class MainWindow(FluentWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.tr("鸽子小助手"))
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon('resource/images/app_icon_circle.png'))
        self.navigationInterface.setExpandWidth(100)

        # TitleBar
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)

        # Navigation
        self.navigationInterface.setReturnButtonVisible(False)

        homeFragment = HomeFragment(self)
        self.addSubInterface(homeFragment, FIF.HOME, '主页')
        
        appFragment = AppFragment(self)
        self.addSubInterface(appFragment, FIF.APPLICATION, '应用')
        
        testInterface = QWidget()
        testInterface.setObjectName("testInterface")
        self.addSubInterface(testInterface, FIF.CHAT, 'Test')

        settingsFragment = SettingsFragment()
        self.addSubInterface(settingsFragment, FIF.SETTING, '设置')

        self.navigationInterface.addItem(
            routeKey = 'Help',
            icon = FIF.HELP,
            text = self.tr('关于'),
            onClick = self.showMessageBox,
            selectable = False,
            position = NavigationItemPosition.BOTTOM,
        )

    def mouseReleaseEvent(self, event):
        # 获取窗口的几何信息
        rect = self.frameGeometry()
        # 获取屏幕的几何信息
        screen = QApplication.primaryScreen().availableGeometry()
        
        # 获取左上角和右下角的坐标
        top_left = rect.topLeft()
        bottom_right = rect.bottomRight()
        
        # 检查窗口是否在屏幕边缘
        if top_left.x() <= screen.left() or top_left.y() <= screen.top() or \
           bottom_right.x() >= screen.right() or bottom_right.y() >= screen.bottom():
            # 禁止窗口自动放大
            event.ignore()
        else:
            # 处理其他鼠标释放事件
            super().mouseReleaseEvent(event)

    def showMessageBox(self):
        w = MessageBox(
            self.tr('关于本项目'),
            self.tr('本项目为开源项目，仅供学习交流使用，请勿用于商业用途。'),
            self
        )
        w.yesButton.setText(self.tr('项目详情'))
        w.cancelButton.setText(self.tr('取消'))

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click"))
