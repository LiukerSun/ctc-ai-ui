from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from utils.logger import get_logger
from utils.config import get_config


class UserWindow(QMainWindow):
    """用户登录后的主界面"""

    def __init__(self, utoken):
        super().__init__()
        self.utoken = utoken
        self.logger = get_logger()
        self.config = get_config()
        self.logger.info("初始化用户窗口")

        # 先创建基本UI
        self.init_basic_ui()

        # 使用定时器延迟加载其他组件
        QTimer.singleShot(100, self.init_components)

    def init_basic_ui(self):
        """初始化基本界面结构"""
        self.setWindowTitle("用户界面")
        self.setGeometry(
            100,
            100,
            self.config.getint("Window", "user_width", 800),
            self.config.getint("Window", "user_height", 600),
        )

        # 设置样式
        styles = f"""
            QMainWindow {{
                background-color: {self.config.get('UserStyle', 'window_background', 'white')};
            }}
            QLabel#welcomeLabel {{
                color: {self.config.get('UserStyle', 'welcome_label_color', '#353535')};
                font-size: 24px;
                font-weight: bold;
            }}
        """
        self.setStyleSheet(styles)

        # 创建中央部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 添加欢迎标签
        self.welcome_label = QLabel(
            self.config.get("UI", "loading_text", "正在加载...")
        )
        self.welcome_label.setObjectName("welcomeLabel")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

        self.logger.debug("用户窗口基本UI初始化完成")

    def init_components(self):
        """延迟初始化其他组件"""
        self.logger.info("开始初始化用户窗口组件")

        # 更新欢迎标签
        self.welcome_label.setText(self.config.get("UI", "welcome_text", "欢迎回来！"))

        # 在这里添加其他组件的初始化
        # TODO: 添加更多组件

        self.logger.debug("用户窗口组件初始化完成")

    def closeEvent(self, event):
        """处理窗口关闭事件"""
        self.logger.info("用户窗口正在关闭")
        event.accept()  # 关闭整个应用
