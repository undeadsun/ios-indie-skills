# 🎬 Smart Media Downloader

> Automatically search and download images and video clips based on your description, with support for automatic video trimming.

[🇨🇳 简体中文](./README_CN.md)

---

## 🚀 What can I do for you?

| If you say... | I will... |
|---------------|-----------|
| "Download some cute cat pictures" | Search and download 5 cat images |
| "Find a video of ocean waves, about 15 seconds" | Download a 15-second video of waves |
| "Download a cooking video, 30 seconds" | Download and trim a cooking video |
| "Download this YouTube video from 1:30 to 2:00" | Download and automatically trim the specified clip |

---

## ✨ Features

- 🖼️ **Image Download** - Search high-quality images from professional stock libraries
- 🎬 **Video Footage** - Get free-to-use commercial video clips
- 📺 **YouTube Download** - Support downloading and trimming
- ✂️ **Smart Trimming** - Automatically crop to your desired length
- 🌍 **Bilingual** - Supports both English and Chinese commands

---

## ⚡ Quick Install

Tell Claude in Claude Code:

> **"Help me install https://github.com/yizhiyanhua-ai/media-downloader.git skill and all its dependencies, and configure yt-dlp to use browser cookies"**

Claude will automatically:
- Download the skill to the correct location
- Install dependencies like yt-dlp, ffmpeg
- Configure browser cookies (to solve YouTube "Confirm you're not a robot" issues)
- Check installation status

You just need to click "Allow" when Claude asks!

---

## 🔑 About API Keys

> 💡 **Configure as needed**: No API Keys are required during installation!
>
> - **Downloading YouTube videos**: No API Key required, ready to use after installation
> - **Downloading images**: On first use, Claude will guide you to configure the Pexels API Key

### What happens when downloading images for the first time?

When you first say "Download some cat pictures", Claude will:

1. Detect that you haven't configured a stock library API Key
2. Guide you to **https://www.pexels.com** to register (supports one-click sign-up with Google/Apple)
3. Help you get the API Key and automatically save it to system environment variables
4. Continue with the image download

The whole process takes just a few minutes and only needs to be done once!

---

## 📋 More Libraries (Optional)

Pexels covers most needs. If you want more image sources, tell Claude:

> **"Help me configure Pixabay API Key"** or **"Help me configure Unsplash API Key"**

Claude will guide you through registration and configuration.

---

## 💬 Usage Examples

> ⚠️ **Important**: Before using, tell Claude **"Check media-downloader status"** to ensure all dependencies are installed!

### Download Images

```
"Help me download 5 pictures of starry sky"
"Download 10 photos of coffee shops"
"Find some landscape images suitable for wallpapers"
```

### Download Video Footage

> 💡 **Recommendation**: If you need video, **prioritize YouTube**! YouTube content is rich, high quality, and requires no extra API Key.

```
"Download this video: https://youtube.com/watch?v=xxx"
"Download this YouTube video from minute 2 to minute 3"
"Download only the audio of this video"
```

If you need short clips from stock libraries:

```
"Download a video of city night view, under 30 seconds"
"Find a 15-second video of ocean waves"
"Find some nature scenery videos suitable for background"
```

---

## 📁 Download Location

All files are saved by default in:

```
~/.claude/skills/media-downloader/downloads/
```

### Custom Download Directory

You can use `-o` or `--output` arguments to specify download location:

```bash
# Download images to a specific folder
media_cli.py image "cat" -o ~/Pictures/cats

# Download video to desktop
media_cli.py video "sunset" -o ~/Desktop

# Download YouTube video to current directory
media_cli.py youtube "URL" -o .
```

Or just tell me where you want to save it:

```
"Download 5 cat pictures to the desktop"
"Save video to ~/Videos/project folder"
```

---

## ❓ FAQ

### Q: YouTube says "Sign in required" or "Confirm you're not a robot"?

This is YouTube's anti-crawler mechanism. The solution is to let yt-dlp use your browser's login state:

**Method 1: Tell Claude (Recommended)**

> **"Help me configure yt-dlp to use browser cookies"**

Claude will set it up for you.

**Method 2: Manual Configuration**

1. Ensure you are logged into YouTube in your browser (Chrome/Firefox/Edge)
2. Add `--cookies-from-browser chrome` when downloading:

```bash
yt-dlp --cookies-from-browser chrome "YouTube_URL"
```

> 💡 **Tip**: Replace `chrome` with your browser: `firefox`, `edge`, `safari`, `brave`, etc.

### Q: Why are there no results when searching for images?
A: Please check if the API Key is configured. Run `status` command to check configuration status.

### Q: YouTube video download failed?
A: YouTube download doesn't need an API Key, but requires yt-dlp installed. Run `pip install yt-dlp` to install.

### Q: Video trimming not working?
A: Requires ffmpeg installed. macOS users run `brew install ffmpeg`.

### Q: Can these images/videos be used commercially?
A: Assets from Pexels, Pixabay, Unsplash are free for commercial use without attribution (though attribution is appreciated).

---

## 🛠️ CLI Command Reference

For advanced users to use directly in the command line:

```bash
# Check configuration status
media_cli.py status

# Download images
media_cli.py image "keyword" -n count -o output_dir

# Download video footage
media_cli.py video "keyword" -d max_duration -n count

# Download YouTube video
media_cli.py youtube "URL" --start start_seconds --end end_seconds

# Search media (no download)
media_cli.py search "keyword" --type image/video/all

# Trim local video
media_cli.py trim input_file --start start --end end
```

---

## 📦 Supported Sources

| Source | Type | Features |
|--------|------|----------|
| Pexels | Image + Video | High quality, fast updates |
| Pixabay | Image + Video | Large quantity, wide variety |
| Unsplash | Image | Artistic, great for wallpapers |
| YouTube | Video | Rich content, supports trimming |

---

## 📄 License

MIT License
