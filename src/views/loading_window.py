from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class LoadingWindow(QWidget):
    """加载窗口，显示模型下载进度"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        # 设置窗口属性
        self.setWindowTitle('加载模型')
        self.setFixedSize(300, 150)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 状态标签
        self.status_label = QLabel('正在检查模型...')
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)
        
    def update_progress(self, value):
        """更新进度条"""
        self.progress_bar.setValue(value)
        if value < 100:
            self.status_label.setText(f'正在下载模型... {value}%')
        else:
            self.status_label.setText('下载完成！')
            
    def center_on_parent(self, parent):
        """将窗口居中显示在父窗口上"""
        parent_pos = parent.pos()
        parent_size = parent.size()
        self_size = self.size()
        
        x = parent_pos.x() + (parent_size.width() - self_size.width()) // 2
        y = parent_pos.y() + (parent_size.height() - self_size.height()) // 2
        
        self.move(x, y)
