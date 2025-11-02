# AR Galgame Assistant

一个可以嵌入AR眼镜的应用程序，用于识别身边人的语音对话，并通过大模型生成三个高情商的回复选项，以Galgame风格展示。

## 功能特性

- 🎤 **语音识别**：使用浏览器内置的语音识别API识别中文语音
- 🤖 **AI生成回复**：集成Qwen大模型，生成三个日常、简洁、高情商的回复选项
- 🎮 **Galgame风格UI**：美观的选项框界面，支持鼠标点击和键盘快捷键
- 📱 **响应式设计**：适配不同屏幕尺寸，便于嵌入AR眼镜
- ⚙️ **参数化配置**：所有API参数可通过环境变量或请求参数配置
- 🔧 **Blueprint架构**：使用Flask Blueprint实现模块化设计

## 项目结构

```
earthonline_liveGalgame/
├── backend/
│   ├── app.py                    # Flask主应用（使用Blueprint）
│   ├── config.py                 # 配置管理
│   ├── requirements.txt          # Python依赖
│   ├── .env.example              # 环境变量示例
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # API路由Blueprint
│   │   └── qwen_service.py        # Qwen API服务
│   └── routes/
│       ├── __init__.py
│       └── static_routes.py       # 静态文件路由Blueprint
├── frontend/
│   ├── index.html                # 主页面
│   ├── style.css                 # Galgame风格样式
│   └── app.js                    # 前端逻辑（支持参数传递）
└── README.md                      # 项目说明
```

## 安装和运行

### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

或者直接设置环境变量：

```bash
# Windows PowerShell
$env:QWEN_API_KEY="your-api-key"
$env:QWEN_MODEL="qwen-turbo"

# Linux/Mac
export QWEN_API_KEY="your-api-key"
export QWEN_MODEL="qwen-turbo"
```

### 3. 运行后端服务

```bash
python app.py
```

后端服务将在 `http://localhost:5000` 启动

### 4. 打开前端页面

在浏览器中访问 `http://localhost:5000`

**注意**：语音识别功能需要在HTTPS环境下运行，或者在localhost下使用Chrome浏览器。

## 使用方法

1. 点击"开始识别"按钮或按下空格键开始语音识别
2. 对着麦克风说话，系统会自动识别并转换为文本
3. 系统将文本发送给Qwen API，生成三个回复选项
4. 在Galgame风格的选项框中，点击选项或按键盘1/2/3键选择回复

## API使用

### 生成回复选项

**端点**: `POST /api/generate-responses`

**请求体**:
```json
{
  "message": "用户输入的文本",
  "model": "qwen-turbo",           // 可选，覆盖默认模型
  "temperature": 0.7,              // 可选，覆盖默认温度
  "max_tokens": 200,               // 可选，覆盖默认最大token数
  "top_p": 0.8,                    // 可选，覆盖默认top_p
  "api_key": "your-api-key",       // 可选，覆盖默认API Key
  "api_url": "custom-api-url",     // 可选，覆盖默认API URL
  "custom_prompt": "自定义提示词"   // 可选，自定义提示词模板
}
```

**响应**:
```json
{
  "success": true,
  "options": ["选项1", "选项2", "选项3"],
  "message": "用户输入的文本"
}
```

### 获取配置

**端点**: `GET /api/config`

**响应**:
```json
{
  "api_url": "...",
  "model": "qwen-turbo",
  "temperature": 0.7,
  "max_tokens": 200,
  "top_p": 0.8,
  "timeout": 15
}
```

### 健康检查

**端点**: `GET /api/health`

**响应**:
```json
{
  "status": "healthy",
  "service": "AR Galgame Assistant API"
}
```

## 配置参数

所有配置参数可以通过环境变量设置：

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `FLASK_DEBUG` | `True` | Flask调试模式 |
| `FLASK_HOST` | `0.0.0.0` | Flask服务器主机 |
| `FLASK_PORT` | `5000` | Flask服务器端口 |
| `QWEN_API_KEY` | `sk-1ff3a1c15f884e31b3a7492748e37a97` | Qwen API密钥 |
| `QWEN_API_URL` | `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` | Qwen API URL |
| `QWEN_MODEL` | `qwen-turbo` | Qwen模型名称 |
| `QWEN_TEMPERATURE` | `0.7` | 生成温度参数 |
| `QWEN_MAX_TOKENS` | `200` | 最大token数 |
| `QWEN_TOP_P` | `0.8` | Top-p参数 |
| `QWEN_TIMEOUT` | `15` | API请求超时时间（秒） |

## 前端参数传递

前端支持通过JavaScript动态更新API配置：

```javascript
// 更新API配置
updateAPIConfig({
    model: 'qwen-turbo',
    temperature: 0.8,
    max_tokens: 300
});

// 调用时传递自定义参数
generateResponses(message, {
    temperature: 0.9,
    custom_prompt: "自定义提示词模板"
});
```

## 技术栈

- **后端**：Flask + Flask-CORS + Flask Blueprint
- **前端**：HTML5 + CSS3 + JavaScript
- **语音识别**：Web Speech API
- **AI模型**：Qwen (通过阿里云API)
- **架构**：Blueprint模块化设计

## 浏览器兼容性

- Chrome/Edge（推荐）：完整支持语音识别
- Firefox：部分支持
- Safari：不支持Web Speech API

## 注意事项

- 需要授予浏览器麦克风权限
- 语音识别需要在HTTPS环境或localhost下运行
- 如果API调用失败，系统会显示默认的回复选项
- 所有参数都可以通过环境变量或请求参数配置，无需修改代码
