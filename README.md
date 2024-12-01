# CTC-AI-UI

基于 PyQt5 的现代化桌面应用程序，采用 WebSocket 登录机制和模块化架构。

## 项目特点

- **模块化设计**: 采用 MVC 架构，实现关注点分离
- **WebSocket 登录**: 安全可靠的身份验证机制
- **配置驱动**: 所有设置都可通过配置文件管理
- **完整日志**: 集成了可配置的日志系统
- **主题定制**: 支持通过配置文件自定义界面样式
- **模型管理**: 支持模型版本检查和自动更新

## 项目结构

```
project/
├── config/
│   └── config.ini        # 集中配置文件
├── models/              # 模型存储目录
├── src/
│   ├── main.py           # 应用入口点
│   ├── controllers/      # 控制器
│   │   ├── login_controller.py  # 登录逻辑控制
│   │   └── model_controller.py  # 模型管理控制
│   ├── views/           # 视图
│   │   ├── login_window.py      # 登录界面
│   │   ├── loading_window.py    # 加载进度界面
│   │   └── user_window.py       # 用户界面
│   └── utils/          # 工具类
│       ├── logger.py    # 日志工具
│       └── config.py    # 配置管理
└── pyproject.toml      # Poetry 项目配置
```

## 配置系统

配置文件 (`config.ini`) 采用分模块管理：

### 基础配置
```ini
[App]
name = CTC-AI-UI
version = 0.1.0
```

### 窗口配置
```ini
[Window]
login_title = CTC-AI
login_width = 280
login_height = 400
user_width = 800
user_height = 600
```

### 样式配置
登录窗口样式：
```ini
[LoginStyle]
window_background = white
login_button_background = #07C160
login_button_hover = #06B057
login_button_pressed = #059A4C
title_label_color = #353535
status_label_color = #888888
```

### 模型配置
```ini
[Model]
model_dir = models       # 模型文件存储目录
```

模型的版本信息存储在模型目录下的 `version.json` 文件中：
```json
{
    "version": "1.0.0",
    "model_name": "model_1201.pt",
    "timestamp": "2023-12-01T12:00:00Z"
}
```

用户窗口样式：
```ini
[UserStyle]
window_background = white
welcome_label_color = #353535
```

### WebSocket 配置
```ini
[WebSocket]
auth_server_url = http://localhost:8000
connection_timeout = 30
```

### 日志配置
```ini
[Logging]
level = DEBUG
console_level = INFO
file_level = DEBUG
max_file_size = 10485760  # 10MB
backup_count = 5
log_dir = logs
log_file_prefix = app
date_format = %Y%m%d
```

### 界面文本
```ini
[UI]
login_button_text = 登录
loading_text = 正在加载...
welcome_text = 欢迎回来！
```

## 开发环境

- Python 3.8+
- Poetry 依赖管理
- PyQt5 界面框架

## 主要依赖

- PyQt5: UI 框架
- websockets: WebSocket 通信
- configparser: 配置管理
- logging: 日志系统

## 开始使用

### 方式一：使用 Poetry（推荐）

1. 安装依赖：
```bash
poetry install
```

2. 运行应用：
```bash
poetry run python src/main.py
```

### 方式二：使用 pip + 虚拟环境

1. 创建并激活虚拟环境：

Windows:
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

Linux/macOS:
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 运行应用：
```bash
python src/main.py
```

4. 退出虚拟环境（完成后）：
```bash
deactivate
```

注意：首次使用 pip 安装时，需要先从 Poetry 导出依赖：
```bash
poetry export -f requirements.txt --output requirements.txt
```

## 自定义主题

要自定义应用外观，只需修改 `config.ini` 中的样式配置：

1. `LoginStyle` 部分控制登录窗口的外观
2. `UserStyle` 部分控制用户主界面的外观

所有颜色值支持 CSS 颜色格式（如 `#RGB`、`#RRGGBB`）。

## 日志系统

应用使用分级日志系统：

- 控制台日志：显示重要信息
- 文件日志：记录详细调试信息
- 自动日志轮转：防止日志文件过大

## 模型管理

应用集成了智能模型管理系统：

### 功能特点

- **自动版本检查**: 登录后自动检查模型版本
- **增量更新**: 仅在需要时下载新模型
- **进度显示**: 直观的下载进度界面
- **错误处理**: 完整的错误处理和日志记录

### 工作流程

1. **版本检查**：
   - 检查模型目录下的 version.json 文件
   - 读取本地版本信息并与服务器比对
   - 如果版本文件不存在或格式错误，触发更新

2. **更新流程**：
   - 从服务器获取最新版本信息
   - 下载对应的模型文件
   - 验证文件完整性
   - 更新本地版本信息文件
   - 显示实时下载进度

3. **错误处理**：
   - 版本文件读取错误自动触发更新
   - 下载失败自动重试
   - 文件完整性校验
   - 详细的错误日志记录

## 许可证

MIT License
