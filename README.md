# iOS Indie Skills

A collection of Claude Code / Antigravity skills for iOS indie developers.

## Available Skills

| Skill | Description |
|-------|-------------|
| [appicon-export](skills/appicon-export/) | Generate all iOS App Icon sizes from a 1024x1024 source image |
| [video-generator-skill](skills/video-generator-skill/) | Smart media downloader & Video Generator. Search/download assets and scaffold Remotion videos. |

## Installation

### Option 1: Install All Skills

```bash
git clone https://github.com/undeadsun/ios-indie-skills.git
cp -r ios-indie-skills/skills/* /path/to/your/project/.agent/skills/
```

### Option 2: Install Single Skill

```bash
# Download specific skill
curl -L https://github.com/undeadsun/ios-indie-skills/archive/main.zip -o skills.zip
unzip skills.zip
cp -r ios-indie-skills-main/skills/appicon-export /path/to/your/project/.agent/skills/
```

## Usage

In Claude Code / Antigravity, use natural language:

**For App Icon Export:**
```
Use appicon-export skill to process my icon: ~/my-icon-1024.png
```

**For Media Downloader:**
```
Find a video of ocean waves, about 15s
```

## Contributing

Feel free to submit PRs for new skills!

## License

MIT
