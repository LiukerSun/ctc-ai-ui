from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QDesktopWidget,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class LoginWindow(QMainWindow):
    """登录窗口，纯视图类"""

    # 用户操作的信号
    login_clicked = pyqtSignal()  # 用户点击登录按钮时发出

    def __init__(self, window_config):
        """
        初始化登录窗口

        Args:
            window_config: 窗口配置字典，包含：
                - title: 窗口标题
                - size: (width, height) 窗口大小
                - styles: 样式表
                - login_button_text: 登录按钮文本
        """
        super().__init__()
        self.login_button = None
        self.status_label = None
        self.setup_ui(window_config)

    def setup_ui(self, config):
        """根据配置设置UI"""
        # 设置窗口基本属性
        self.setWindowTitle(config.get("title", "Login"))
        width, height = config.get("size", (280, 400))
        self.setGeometry(100, 100, width, height)

        # 构建样式表
        styles = f"""
            QMainWindow {{
                background-color: {config.get('window_background', 'white')};
            }}
            QPushButton#loginButton {{
                background-color: {config.get('login_button_background', '#07C160')};
                border: none;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 16px;
            }}
            QPushButton#loginButton:hover {{
                background-color: {config.get('login_button_hover', '#06B057')};
            }}
            QPushButton#loginButton:pressed {{
                background-color: {config.get('login_button_pressed', '#059A4C')};
            }}
            QLabel#titleLabel {{
                color: {config.get('title_label_color', '#353535')};
                font-size: 24px;
                font-weight: bold;
            }}
            QLabel#statusLabel {{
                color: {config.get('status_label_color', '#888888')};
                font-size: 14px;
            }}
        """
        self.setStyleSheet(styles)

        # 创建中央部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 40, 20, 40)
        layout.setSpacing(20)

        # 添加顶部空白
        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # 添加标题
        title_label = QLabel(config.get("title", ""))
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 添加中间空白
        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # 登录按钮
        self.login_button = QPushButton(config.get("login_button_text", "Login"))
        self.login_button.setObjectName("loginButton")
        self.login_button.setFixedHeight(45)
        self.login_button.clicked.connect(self.login_clicked.emit)
        layout.addWidget(self.login_button)

        # 状态标签
        self.status_label = QLabel("")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # 添加底部空白
        layout.addSpacerItem(
            QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # 将窗口居中显示
        self.center_window()

    def center_window(self):
        """将窗口居中显示"""
        frame_geometry = self.frameGeometry()
        desktop = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(desktop)
        self.move(frame_geometry.topLeft())

    def set_login_button_enabled(self, enabled):
        """设置登录按钮状态"""
        self.login_button.setEnabled(enabled)

    def set_status_text(self, text):
        """设置状态文本"""
        self.status_label.setText(text)

    def show_window(self):
        """显示窗口"""
        self.show()

    def hide_window(self):
        """隐藏窗口"""
        self.hide()
