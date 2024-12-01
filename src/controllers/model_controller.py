import os
import json
import asyncio
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal
from utils.logger import get_logger
from utils.config import get_config
from views.loading_window import LoadingWindow


class ModelController(QObject):
    """模型控制器，负责模型的检查、下载和加载"""

    # 定义信号
    model_load_complete = pyqtSignal()  # 模型加载完成信号
    progress_updated = pyqtSignal(int)  # 进度更新信号

    def __init__(self, parent_window=None):
        super().__init__()
        self.logger = get_logger()
        self.config = get_config()
        self.parent_window = parent_window
        self.loading_window = None

        # 模型信息
        self.model_dir = self.config.get("Model", "model_dir", "models")
        self.version_file = "version.json"  # 固定的版本文件名
        self.current_model = None  # 当前模型信息，从版本文件中读取
        
        # 确保模型目录存在
        os.makedirs(self.model_dir, exist_ok=True)

        # 连接进度信号到槽
        self.progress_updated.connect(self._update_progress)
        
    def _get_version_file_path(self):
        """获取版本文件的完整路径"""
        return os.path.join(self.model_dir, self.version_file)
    
    def _get_model_file_path(self):
        """获取模型文件的完整路径"""
        if not self.current_model:
            return None
        return os.path.join(self.model_dir, self.current_model.get("model_name"))
    
    def _read_local_version(self):
        """读取本地版本信息
        返回: (bool, dict) - (是否成功, 版本信息)
        """
        version_file = self._get_version_file_path()
        try:
            if not os.path.exists(version_file):
                self.logger.info("版本文件不存在")
                return False, None
            
            with open(version_file, 'r', encoding='utf-8') as f:
                version_info = json.load(f)
                
            # 验证版本信息格式
            required_fields = ['version', 'model_name', 'timestamp']
            if not all(field in version_info for field in required_fields):
                self.logger.error("版本文件格式错误")
                return False, None
            
            # 更新当前模型信息
            self.current_model = version_info
            return True, version_info
            
        except (json.JSONDecodeError, IOError) as e:
            self.logger.error(f"读取版本文件错误: {str(e)}")
            return False, None
    
    def _save_version_info(self, version_info):
        """保存版本信息到文件"""
        try:
            with open(self._get_version_file_path(), 'w', encoding='utf-8') as f:
                json.dump(version_info, f, indent=4)
            # 更新当前模型信息
            self.current_model = version_info
            return True
        except IOError as e:
            self.logger.error(f"保存版本文件错误: {str(e)}")
            return False

    def start_model_loading(self):
        """开始模型加载流程"""
        self.logger.info("开始加载模型流程")

        # 创建加载窗口（在主线程中）
        self.loading_window = LoadingWindow()
        if self.parent_window:
            self.loading_window.center_on_parent(self.parent_window)
        self.loading_window.show()

        # 在新线程中启动模型加载
        self.load_thread = Thread(target=self._run_model_loading)
        self.load_thread.daemon = True
        self.load_thread.start()

    def _update_progress(self, value):
        """在主线程中更新进度"""
        if self.loading_window:
            self.loading_window.update_progress(value)
            if value >= 100:
                self.loading_window.close()
                self.loading_window = None

    def _run_model_loading(self):
        """在单独的线程中运行模型加载"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._load_models())
        except Exception as e:
            self.logger.error(f"模型加载错误: {str(e)}")
            # 发送错误进度
            self.progress_updated.emit(-1)

    async def _check_model_version(self):
        """检查模型版本
        返回: (bool, dict) - (是否需要更新, 最新版本信息)
        """
        self.logger.info("正在检查模型版本...")
        
        # 读取本地版本信息
        local_success, local_version = self._read_local_version()
        
        # TODO: 实现实际的版本检查逻辑
        # 1. 向服务器发送请求，获取最新版本信息
        await asyncio.sleep(1)  # 模拟网络请求
        
        # 模拟服务器返回的新版本信息
        server_version = {
            "version": "1.0.0",
            "model_name": "model_1201.pt",
            "timestamp": "2023-12-01T12:00:00Z"
        }
        
        # 如果本地版本读取失败，需要更新
        if not local_success:
            return True, server_version
            
        # 比较版本
        return server_version["version"] != local_version["version"], server_version

    async def _download_model(self, version_info):
        """下载模型"""
        self.logger.info("开始下载模型...")
        
        # TODO: 实现实际的模型下载逻辑
        # 1. 下载模型文件
        # 2. 验证文件完整性
        # 3. 保存到指定位置
        model_path = os.path.join(self.model_dir, version_info["model_name"])
        
        # 模拟下载进度
        for i in range(0, 101, 10):
            await asyncio.sleep(1)
            self.progress_updated.emit(i)
            self.logger.info(f"下载进度：{i}%")
        
        # 保存版本信息
        if self._save_version_info(version_info):
            self.logger.info(f"模型已保存到: {model_path}")
        else:
            raise Exception("保存版本信息失败")

    async def _load_models(self):
        """检查并加载模型"""
        try:
            need_update, latest_version = await self._check_model_version()

            if need_update:
                self.logger.info("模型需要更新")
                await self._download_model(latest_version)
            else:
                self.logger.info("模型已是最新版本")
                self.progress_updated.emit(100)

            self.logger.info("模型加载完成")
            # 发出加载完成信号
            self.model_load_complete.emit()

        except Exception as e:
            self.logger.error(f"模型加载错误: {str(e)}")
            raise e
