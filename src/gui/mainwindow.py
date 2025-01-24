import os
import subprocess
import threading

from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy, QApplication
from PySide6.QtCore import Qt, QUrl, QEvent
from PySide6.QtGui import QIcon, QColor, QDesktopServices
from qfluentwidgets import (FluentWindow, MSFluentWindow, PushButton, FluentTitleBar, FluentIcon as FIF, NavigationItemPosition, MessageBox, CardWidget,
                            IconWidget, BodyLabel, CaptionLabel, TransparentToolButton, ComboBox, SingleDirectionScrollArea)
from qframelesswindow.webengine import FramelessWebEngineView

from core.logger import logger
from mumu.mumu_api import mumuApi


class AppCard(CardWidget):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        # self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton(self.tr('启动'), self)
        self.closeButton = PushButton(self.tr('关闭'), self)
        # self.moreButton = TransparentToolButton(FIF.MORE, self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        # self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(60)
        self.closeButton.setFixedWidth(60)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        # self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeButton, 0, Qt.AlignRight)
        # self.hBoxLayout.addWidget(self.moreButton, 0, Qt.AlignRight)

        # self.moreButton.setFixedSize(32, 32)


class HomeInterface(QWidget):
    def __init__(self, parent = None):
        super(HomeInterface, self).__init__(parent)
        self.setObjectName("homeInterface")

        self.initUI()

    def initUI(self) -> None:
        mumuIconPath = os.path.dirname(mumuApi.getMumuManagerPath()) + "/MuMuPlayer.ico"
        card = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )
        card.setBorderRadius(8)

        card2 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        card3 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        card4 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        card5 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        card6 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        card7 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        card8 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )
        card9 = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )

        contentWidget = QWidget()
        scrollArea = SingleDirectionScrollArea(orient = Qt.Vertical)
        scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scrollArea.setWidget(contentWidget)

        self.layout = QVBoxLayout(contentWidget)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(card)
        self.layout.addWidget(card2)
        self.layout.addWidget(card3)
        self.layout.addWidget(card4)
        self.layout.addWidget(card5)
        self.layout.addWidget(card6)
        self.layout.addWidget(card7)
        self.layout.addWidget(card8)
        self.layout.addWidget(card9)
        contentWidget.setLayout(self.layout)
        # self.setLayout(self.layout)

        card.openButton.clicked.connect(lambda: mumuApi.startMumu())
        card.closeButton.clicked.connect(lambda: mumuApi.closeMumu())
        

class MainWindow(FluentWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self) -> None:
        self.setWindowTitle(self.tr("Launcher"))
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon('resource/images/app_icon.png'))
        self.navigationInterface.setExpandWidth(100)

        # TitleBar
        self.titleBar.maxBtn.hide()
        self.titleBar.setDoubleClickEnabled(False)

        # Navigation
        self.navigationInterface
        self.navigationInterface.setReturnButtonVisible(False)

        homeInterface = HomeInterface()
        self.addSubInterface(homeInterface, FIF.HOME, '主页')

        testInterface = QWidget()
        testInterface.setObjectName("testInterface")
        self.addSubInterface(testInterface, FIF.CHAT, 'Test')

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

