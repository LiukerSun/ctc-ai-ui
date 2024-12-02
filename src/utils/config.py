import os
import configparser
from typing import Any, Optional


class Config:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not Config._initialized:
            Config._initialized = True
            self._config = configparser.ConfigParser(interpolation=None)
            self._load_config()

    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "config",
            "config.ini",
        )

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"配置文件未找到: {config_path}")

        self._config.read(config_path, encoding="utf-8")

    def get(self, section: str, key: str, fallback: Any = None) -> Optional[str]:
        """获取配置值"""
        return self._config.get(section, key, fallback=fallback)

    def getint(self, section: str, key: str, fallback: int = None) -> Optional[int]:
        """获取整数配置值"""
        return self._config.getint(section, key, fallback=fallback)

    def getfloat(
        self, section: str, key: str, fallback: float = None
    ) -> Optional[float]:
        """获取浮点数配置值"""
        return self._config.getfloat(section, key, fallback=fallback)

    def getboolean(
        self, section: str, key: str, fallback: bool = None
    ) -> Optional[bool]:
        """获取布尔配置值"""
        return self._config.getboolean(section, key, fallback=fallback)


# 全局函数获取配置实例
def get_config() -> Config:
    """获取全局配置实例"""
    return Config()
