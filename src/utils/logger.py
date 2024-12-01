import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from .config import get_config


class Logger:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            Logger._initialized = True
            self._setup_logger()

    def _setup_logger(self):
        """设置logger，包括文件和控制台处理器。"""
        config = get_config()
        
        # 创建日志目录
        logs_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            config.get('Logging', 'log_dir', 'logs')
        )
        os.makedirs(logs_dir, exist_ok=True)

        # 创建logger
        app_name = config.get('App', 'name', 'CTC-AI-UI')
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(config.get('Logging', 'level', 'DEBUG'))

        # 如果logger已经有处理器，先清除
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 创建格式化器
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # 文件处理器（带有日志文件轮转）
        log_file_prefix = config.get('Logging', 'log_file_prefix', 'app')
        date_format = config.get('Logging', 'date_format', '%Y%m%d')
        log_file = os.path.join(
            logs_dir,
            f'{log_file_prefix}_{datetime.now().strftime(date_format)}.log'
        )
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=config.getint('Logging', 'max_file_size', 10*1024*1024),
            backupCount=config.getint('Logging', 'backup_count', 5),
            encoding='utf-8'
        )
        file_handler.setLevel(config.get('Logging', 'file_level', 'DEBUG'))
        file_handler.setFormatter(file_formatter)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.get('Logging', 'console_level', 'INFO'))
        console_handler.setFormatter(console_formatter)

        # 添加处理器到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # 输出日志系统初始化信息
        self.logger.info("日志系统初始化完成")
        self.logger.debug(f"日志文件路径: {log_file}")

    def get_logger(self):
        """获取logger实例。"""
        return self.logger


# 全局函数获取logger实例
def get_logger():
    """获取全局logger实例。"""
    return Logger().get_logger()
