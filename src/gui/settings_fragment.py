import os
import subprocess

from PySide6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget, QHBoxLayout
from qfluentwidgets import CardWidget, IconWidget, BodyLabel, PushButton, ScrollArea, SwitchSettingCard, FluentIcon as FIF, SwitchButton
from PySide6.QtCore import Qt

from mumu.mumu_api import mumuApi
from core.config import config


class SwitchSettingsCard(CardWidget):

    def __init__(self, icon: str, title: str, parent: QWidget = None):
        super().__init__(parent)
        
        self.setFixedHeight(48)
        self.setBorderRadius(8)

        self.iconWidget = IconWidget(icon, self)
        self.iconWidget.setFixedSize(20, 20)

        self.titleLabel = BodyLabel(title, self)

        self.switchBtn = SwitchButton(self)
        self.switchBtn.setOnText(self.tr('开'))
        self.switchBtn.setOffText(self.tr('关'))

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 5, 10, 5)
        self.mainLayout.setSpacing(10)

        self.mainLayout.addWidget(self.iconWidget)
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.switchBtn, alignment=Qt.AlignRight)


class SettingsCard(CardWidget):

    def __init__(self, icon: str, title: str, buttonLabel: str, parent: QWidget = None):
        super().__init__(parent)
        
        self.setFixedHeight(48)
        self.setBorderRadius(8)

        self.iconWidget = IconWidget(icon, self)
        self.iconWidget.setFixedSize(20, 20)

        self.titleLabel = BodyLabel(title, self)

        self.button = PushButton(buttonLabel, self)

        self.mainLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(10, 5, 10, 5)
        self.mainLayout.setSpacing(10)

        self.mainLayout.addWidget(self.iconWidget)
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.button, alignment=Qt.AlignRight)


class SettingsFragment(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("settingsFragment")

        self.initUI()

    def initUI(self) -> None:

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(10, 10, 10, 5)
        mainLayout.setAlignment(Qt.AlignTop)

        withOpenScriptCard = SwitchSettingsCard(
            icon = FIF.TAG,
            title=self.tr("启动时自动打开脚本")
        )
        if config.get('withOpenScript') == "":
            config.set('withOpenScript', False)
        withOpenScriptCard.switchBtn.setChecked(config.get('withOpenScript'))

        detectAdbCard = SettingsCard(
            icon = FIF.TAG,
            title=self.tr("检测Adb地址"),
            buttonLabel=self.tr("连接Adb")
        )

        mainLayout.addWidget(withOpenScriptCard)
        mainLayout.addWidget(detectAdbCard)

        self.setLayout(mainLayout)

        withOpenScriptCard.switchBtn.checkedChanged.connect(lambda: config.set('withOpenScript', withOpenScriptCard.switchBtn.isChecked()))
        detectAdbCard.button.clicked.connect(lambda: mumuApi.detectAdbAddr())