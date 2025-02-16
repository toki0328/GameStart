from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class HomeFragment(QFrame):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setObjectName("HomeFragment")
        self.init_ui()

    def init_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # 应用logo
        logo = QLabel(self)
        logo_pixmap = QPixmap("resource/images/app_icon_circle.png")

        logo.setPixmap(logo_pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        # 欢迎文字
        welcome_label = QLabel("欢迎使用鸽子小助手", self)
        welcome_label.setStyleSheet("font: 24px 'PINGFANG MEDIUM'; color: #333;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # 功能按钮
        start_btn = QPushButton("开始使用", self)
        start_btn.setFixedSize(200, 40)
        start_btn.setStyleSheet(
            "QPushButton {"
            "   background-color: #4CAF50;"
            "   color: white;"
            "   border-radius: 5px;"
            "   font: 16px 'PINGFANG MEDIUM';"
            "}"
            "QPushButton:hover {"
            "   background-color: #45a049;"
            "}"
        )
        layout.addWidget(start_btn, 0, Qt.AlignCenter)
        
        self.setLayout(layout)
