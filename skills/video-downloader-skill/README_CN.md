# Skill Template

> 这是一个改进版的 Skill 模板，基于最佳实践设计。

## 🚀 快速开始

```bash
# 1. 安装依赖
chmod +x install.sh && ./install.sh

# 2. 检查状态
python cli.py status

# 3. 执行任务
python cli.py run "参数"
```

## 📁 目录结构

```
skill-template/
├── SKILL.md              # Skill 主说明文件（Claude 读取）
├── cli.py                # CLI 入口脚本
├── core/                 # 核心模块
│   ├── __init__.py       # 模块导出
│   ├── base.py           # 抽象基类
│   ├── config.py         # 配置管理
│   ├── exceptions.py     # 异常定义
│   └── utils.py          # 工具函数
├── requirements.txt      # Python 依赖
├── install.sh            # 安装脚本
├── .env.example          # 环境变量示例
└── README.md             # 本文件
```

## ✨ 特点

| 特点 | 说明 |
|------|------|
| 🧩 模块化设计 | 核心逻辑与 CLI 分离 |
| 🔒 类型安全 | 完整的类型提示 |
| 🎨 美化输出 | 支持 rich 进度条 |
| ⚠️ 错误处理 | 自定义异常层级 |
| 📝 配置管理 | 支持 .env 文件 |
| 🌍 国际化 | 中英双语支持 |

## 🛠️ 自定义你的 Skill

### 1. 修改 SKILL.md

更新 frontmatter 中的 `name` 和 `description`：

```yaml
---
name: your-skill-name
description: |
  你的 Skill 描述
---
```

### 2. 实现你的处理器

编辑 `cli.py` 中的 `ExampleHandler`：

```python
class MyHandler(BaseHandler):
    @property
    def name(self) -> str:
        return "my-handler"
    
    def execute(self, **kwargs) -> dict:
        # 你的逻辑
        return {"success": True}
```

### 3. 添加配置需求

```python
@property
def required_config_keys(self) -> list:
    return ["MY_API_KEY"]

@property
def required_dependencies(self) -> list:
    return [
        {"name": "ffmpeg", "check_cmd": "ffmpeg -version", "install_cmd": "brew install ffmpeg"}
    ]
```

## 📖 API 参考

### BaseHandler

所有处理器的基类，使用模板方法模式：

```python
handler = MyHandler()
result = handler.run(param1="value1")  # 自动调用 pre_execute -> execute -> post_execute
```

### Config

配置管理：

```python
config = Config.load()
api_key = config.get("MY_API_KEY", required=True)
config.set("KEY", "value", persist=True)  # 持久化到 .env
```

### 进度条

```python
with get_progress_bar(100, "处理中") as update:
    for i in range(100):
        # 工作...
        update(1)
```

## 📄 许可证

MIT License
