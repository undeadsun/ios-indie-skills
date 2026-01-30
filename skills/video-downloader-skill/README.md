# Skill Template

> 🇨🇳 [简体中文](README_CN.md) | 🇺🇸 English

> This is an improved Skill template, designed based on best practices.

## 🚀 Quick Start

```bash
# 1. Install dependencies
chmod +x install.sh && ./install.sh

# 2. Check status
python cli.py status

# 3. Execute task
python cli.py run "parameters"
```

## 📁 Directory Structure

```
skill-template/
├── SKILL.md              # Main Skill description file (Read by Claude)
├── cli.py                # CLI entry script
├── core/                 # Core modules
│   ├── __init__.py       # Module exports
│   ├── base.py           # Abstract base class
│   ├── config.py         # Configuration management
│   ├── exceptions.py     # Exception definitions
│   └── utils.py          # Utility functions
├── requirements.txt      # Python dependencies
├── install.sh            # Installation script
├── .env.example          # Environment variable example
└── README.md             # This file
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧩 Modular Design | Separation of core logic and CLI |
| 🔒 Type Safety | Complete type hinting |
| 🎨 Beautiful Output | Supports rich progress bars |
| ⚠️ Error Handling | Custom exception hierarchy |
| 📝 Config Management | Supports .env files |
| 🌍 Internationalization | Bilingual support (En/Cn) |

## 🛠️ Customize Your Skill

### 1. Modify SKILL.md

Update `name` and `description` in the frontmatter:

```yaml
---
name: your-skill-name
description: |
  Your Skill description
---
```

### 2. Implement Your Handler

Edit `ExampleHandler` in `cli.py`:

```python
class MyHandler(BaseHandler):
    @property
    def name(self) -> str:
        return "my-handler"
    
    def execute(self, **kwargs) -> dict:
        # Your logic here
        return {"success": True}
```

### 3. Add Configuration Requirements

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

## 📖 API Reference

### BaseHandler

Base class for all handlers, using the Template Method pattern:

```python
handler = MyHandler()
result = handler.run(param1="value1")  # Automatically calls pre_execute -> execute -> post_execute
```

### Config

Configuration management:

```python
config = Config.load()
api_key = config.get("MY_API_KEY", required=True)
config.set("KEY", "value", persist=True)  # Persist to .env
```

### Progress Bar

```python
with get_progress_bar(100, "Processing") as update:
    for i in range(100):
        # Working...
        update(1)
```

## 📄 License

MIT License
