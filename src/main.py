import sys
from PyQt5.QtWidgets import QApplication
from controllers.login_controller import LoginController


def main():
    """程序入口点"""
    app = QApplication(sys.argv)
    
    # 创建登录控制器并显示登录窗口
    login_controller = LoginController()
    login_controller.show_login_window()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
