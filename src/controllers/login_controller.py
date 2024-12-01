import asyncio
import websockets
import json
import socket
import webbrowser
from threading import Thread, Lock
from PyQt5.QtCore import QObject, pyqtSignal
from utils.logger import get_logger
from utils.config import get_config
from views.login_window import LoginWindow
from views.user_window import UserWindow
from controllers.model_controller import ModelController


class LoginController(QObject):
    """登录控制器，负责创建和控制登录视图"""
    
    # 添加登录成功信号
    login_success = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.logger = get_logger()
        self.config = get_config()
        self.websocket_server = None
        self.server_thread = None
        self.event_loop = None
        self.is_login_in_progress = False
        self.state_lock = Lock()
        
        # 保存当前用户的token
        self.current_utoken = None
        
        # 窗口实例
        self.login_window = None
        self.user_window = None
        
        # 连接信号到槽
        self.login_success.connect(self._on_login_success)
        
        # 创建并配置登录窗口
        self.setup_login_window()
    
    def setup_login_window(self):
        """创建并配置登录窗口"""
        window_config = {
            'title': self.config.get('Window', 'login_title', 'CTC-AI'),
            'size': (
                self.config.getint('Window', 'login_width', 280),
                self.config.getint('Window', 'login_height', 400)
            ),
            'window_background': self.config.get('LoginStyle', 'window_background', 'white'),
            'login_button_background': self.config.get('LoginStyle', 'login_button_background', '#07C160'),
            'login_button_hover': self.config.get('LoginStyle', 'login_button_hover', '#06B057'),
            'login_button_pressed': self.config.get('LoginStyle', 'login_button_pressed', '#059A4C'),
            'title_label_color': self.config.get('LoginStyle', 'title_label_color', '#353535'),
            'status_label_color': self.config.get('LoginStyle', 'status_label_color', '#888888'),
            'login_button_text': self.config.get('UI', 'login_button_text', '登录')
        }
        
        self.login_window = LoginWindow(window_config)
        self.login_window.login_clicked.connect(self.start_login)
    
    def show_login_window(self):
        """显示登录窗口"""
        self.login_window.show_window()
    
    def find_free_port(self):
        """查找可用的端口"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
            self.logger.debug(f"找到空闲端口: {port}")
            return port

    def reset_login_state(self):
        """重置登录状态"""
        with self.state_lock:
            self.is_login_in_progress = False
            self.login_window.set_status_text("")
            self.login_window.set_login_button_enabled(True)
            self.logger.info("登录状态已重置")
    
    def start_login(self):
        """开始登录流程"""
        with self.state_lock:
            if self.is_login_in_progress:
                self.logger.info("登录已在进行中，重置状态")
                self.cleanup_server()
                self.reset_login_state()
                return
            
            self.is_login_in_progress = True
            self.login_window.set_login_button_enabled(False)
            
        self.logger.info("开始登录流程")
        self.login_window.set_status_text("正在启动登录流程...")
        
        # TODO: 实现实际的登录流程
        # 1. 检查本地是否有保存的登录状态（token）
        # 2. 如果有，验证token是否有效
        # 3. 如果token有效，直接进入已登录状态
        # 4. 如果无效，再启动WebSocket服务器进行扫码登录
        # 示例 API:
        # GET /api/auth/check_token
        # Headers: {
        #     "Authorization": "Bearer {token}"
        # }
        
        # 在单独的线程中启动WebSocket服务器
        self.server_thread = Thread(target=self.run_websocket_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.logger.debug("WebSocket服务器线程已启动")
    
    def run_websocket_server(self):
        """在单独的线程中运行WebSocket服务器"""
        async def connection_timeout():
            """等待连接超时"""
            timeout = self.config.getint('WebSocket', 'connection_timeout', 30)
            try:
                await asyncio.sleep(timeout)
                if self.is_login_in_progress:
                    self.logger.info("登录超时 - 未收到连接")
                    self.login_window.set_status_text("登录超时，请重试")
                    self.reset_login_state()
            except Exception as e:
                self.logger.error(f"超时处理器错误: {str(e)}")

        async def websocket_handler(websocket, path):
            self.logger.debug(f"收到新的WebSocket连接，来自 {websocket.remote_address}")
            try:
                async for message in websocket:
                    self.logger.debug(f"收到消息: {message}")
                    try:
                        data = json.loads(message)
                        if 'utoken' in data:
                            # TODO: 实现token验证和用户信息获取
                            # 1. 验证token的合法性
                            # 2. 获取用户基本信息
                            # 3. 保存必要的用户数据
                            # 4. 如果验证失败，通知用户重新登录
                            # 示例 API:
                            # POST /api/auth/verify_token
                            # {
                            #     "token": data['utoken']
                            # }
                            # GET /api/user/info
                            # Headers: {
                            #     "Authorization": "Bearer {token}"
                            # }
                            
                            self.logger.info("收到有效的utoken")
                            self.handle_login_success(data['utoken'])
                            return
                    except json.JSONDecodeError as e:
                        self.logger.error(f"收到无效的JSON: {message}")
                        continue
            except websockets.exceptions.ConnectionClosed:
                self.logger.debug("WebSocket连接已关闭")
                if self.is_login_in_progress:
                    self.logger.info("浏览器在登录完成前关闭")
                    self.login_window.set_status_text("浏览器已关闭，请重试")
                    self.reset_login_state()
            except Exception as e:
                self.logger.error(f"WebSocket处理器错误: {str(e)}")
                self.login_window.set_status_text(f"错误: {str(e)}")
                self.reset_login_state()
        
        async def start_server():
            port = self.find_free_port()
            try:
                self.websocket_server = await websockets.serve(
                    websocket_handler, 'localhost', port
                )
                self.logger.info(f"WebSocket服务器已在端口 {port} 上启动")
                
                # 启动超时计时器
                asyncio.create_task(connection_timeout())
                
                # TODO: 实现实际的登录URL生成和处理
                # 1. 生成包含必要参数的登录URL
                # 2. 可能需要包含：
                #    - 应用标识（client_id）
                #    - 随机状态码（state）防止CSRF攻击
                #    - 回调地址（redirect_uri）
                #    - 权限范围（scope）
                # 3. 考虑添加本地状态存储，用于验证回调
                auth_server_url = self.config.get('WebSocket', 'auth_server_url', 'http://localhost:8000')
                login_url = f"{auth_server_url}/login?ws_port={port}"
                self.logger.debug(f"正在打开浏览器，URL: {login_url}")
                webbrowser.open(login_url)
                self.login_window.set_status_text("请在浏览器中完成登录...")
                await self.websocket_server.wait_closed()
            except Exception as e:
                error_msg = f"服务器错误: {str(e)}"
                self.logger.error(error_msg)
                self.login_window.set_status_text(error_msg)
                self.reset_login_state()
        
        try:
            self.logger.debug("创建新的事件循环")
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            self.event_loop.run_until_complete(start_server())
        except Exception as e:
            error_msg = f"启动服务器错误: {str(e)}"
            self.logger.error(error_msg)
            self.login_window.set_status_text(error_msg)
            self.reset_login_state()
        finally:
            self.cleanup_server()
    
    def handle_login_success(self, utoken):
        """处理登录成功"""
        self.logger.info("登录成功，发出创建用户窗口信号")
        self.login_success.emit(utoken)
    
    def _on_login_success(self, utoken):
        """登录成功后的处理"""
        self.logger.info("登录成功，开始加载模型")
        self.login_window.set_status_text("登录成功！")
        self.is_login_in_progress = False
        
        # 保存token
        self.current_utoken = utoken
        
        # 创建模型控制器并开始加载
        self.model_controller = ModelController(self.login_window)
        self.model_controller.model_load_complete.connect(self._on_model_load_complete)
        self.model_controller.start_model_loading()
    
    def _on_model_load_complete(self):
        """模型加载完成后的处理"""
        self.logger.info("模型加载完成，创建用户窗口")
        
        # 创建并显示用户窗口
        self.user_window = UserWindow(self.current_utoken)
        self.user_window.show()
        self.login_window.hide_window()
    
    def cleanup_server(self):
        """清理服务器资源"""
        self.logger.info("正在清理服务器资源")
        
        # 关闭WebSocket服务器
        if self.websocket_server:
            self.websocket_server.close()
            self.websocket_server = None
            self.logger.debug("WebSocket服务器已关闭")
        
        # 关闭事件循环
        if self.event_loop:
            try:
                if not self.event_loop.is_closed():
                    pending = asyncio.all_tasks(self.event_loop)
                    if pending:
                        self.event_loop.run_until_complete(asyncio.gather(*pending))
                    self.event_loop.close()
            except Exception as e:
                self.logger.error(f"关闭事件循环错误: {str(e)}")
            finally:
                self.event_loop = None
                self.logger.debug("事件循环已关闭")
        
        # 结束服务器线程
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=1)
            self.server_thread = None
            self.logger.debug("服务器线程已结束")
