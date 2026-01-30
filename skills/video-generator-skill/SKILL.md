---
name: media-downloader-v2
description: |
  Smart media downloader & Video Generator. Automatically search and download images/videos, and generate full video compositions using Remotion.
  Triggers: "download media", "create video", "generate video", "make video"
---
// turbo-all

# 🎬 Video Generator Skill

> Smart Video Generator - Scaffolds and automates Remotion video projects.

---

## 🚀 Workflow

### 1. Initialize Project (One-time)
Create a new video project in your workspace (not inside the skill directory).

```bash
# Create and enter directory
mkdir my-video-project
cd my-video-project

# Initialize with template
python3 ~/.gemini/antigravity/skills/video-generator-skill/generator.py init .
```

### 2. Generate Video
Run the generator inside your project directory.

```bash
python3 ~/.gemini/antigravity/skills/video-generator-skill/generator.py "Cyberpunk City"
```

This will:
1. Download assets to `public/assets/`
2. Download music
3. Update `src/manifest.ts`
4. Render video to `~/Downloads/Cyberpunk_City.mp4`

---

## 🛠 Advanced Usage

### Dynamic Composition (Agent Mode)
When the user requests specific effects:
1. Agent reads `remotion-best-practices`
2. Agent modifies `src/Composition.tsx` in the **user's project directory**
3. Agent runs generator

### Commands

| Command | Usage | Description |
|---------|-------|-------------|
| **Init** | `generator.py init [path]` | Initialize new Remotion project |
| **Generate** | `generator.py "Topic"` | Generate video from current dir |
| **Download Image** | `cli.py image "Topic"` | Download images only |

---

## ⚙️ Configuration

API Key stored in `~/.gemini/antigravity/skills/video-generator-skill/.env`:
```bash
PEXELS_API_KEY="your_key_here"
```
