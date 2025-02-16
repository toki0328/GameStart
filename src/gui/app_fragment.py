import os
import subprocess

from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout
from qfluentwidgets import CardWidget, IconWidget, BodyLabel, PushButton, ScrollArea
from PySide6.QtCore import Qt

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

class AppFragment(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("appFragment")

        self.initUI()

    def initUI(self) -> None:

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        mumuIconPath = os.path.dirname(mumuApi.getMumuManagerPath()) + "/MuMuPlayer.ico"
        maaIconPath = 'resource/images/maa_logo.png'
        maaExePath = "C:\Dev\Scripts\MAA-v5.12.3-win-x64\MAA.exe"
        
        # 滚动区域
        contentWidget = QWidget()
        contentWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contentLayout = QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(0, 0, 0, 0)

        # mumu模拟器
        mumuCard = AppCard(
            icon = mumuIconPath,
            title = self.tr('Mumu模拟器'),
            content = self.tr('点击启动模拟器'),
        )
        mumuCard.setBorderRadius(8)
        mumuCard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mumuCard.setFixedWidth(700)

        # maa
        maaCard = AppCard(
            icon = maaIconPath,
            title = self.tr('MAA'),
            content = self.tr('点击启动MAA'),
        )

        arknightsCard = AppCard(
            icon = 'resource/images/arknights_logo.png',
            title = self.tr('明日方舟'),
            content = self.tr('点击启动明日方舟'),
        )

        contentLayout.addWidget(mumuCard)
        contentLayout.addWidget(maaCard)
        contentLayout.addWidget(arknightsCard)
        
        scrollArea = ScrollArea(self)
        scrollArea.setStyleSheet("background-color: transparent; border: none;")
        scrollArea.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scrollArea.setWidget(contentWidget)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(scrollArea)
        self.setLayout(mainLayout)
        
        mumuCard.openButton.clicked.connect(lambda: mumuApi.startMumu())
        mumuCard.closeButton.clicked.connect(lambda: mumuApi.closeMumu())

        maaCard.openButton.clicked.connect(lambda: 
            subprocess.Popen(maaExePath, shell = True, creationflags = subprocess.CREATE_NEW_CONSOLE))
        maaCard.closeButton.clicked.connect(lambda:
            subprocess.Popen('taskkill /f /im MAA.exe', shell = True, creationflags = subprocess.CREATE_NEW_CONSOLE))
        
        arknightsCard.openButton.clicked.connect(lambda: mumuApi.startApp('com.hypergryph.arknights.bilibili'))
        arknightsCard.closeButton.clicked.connect(lambda: mumuApi.stopApp('com.hypergryph.arknights.bilibili'))