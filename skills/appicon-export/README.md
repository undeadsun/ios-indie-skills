# iOS AppIcon Export Skill

A Claude Code / Antigravity skill that generates all iOS App Icon sizes from a single 1024x1024 source image.

## Features

- ✅ Validates source image (1024x1024)
- ✅ Auto-converts JPG to PNG
- ✅ Generates all 11 required iOS icon sizes
- ✅ Creates proper `Contents.json` for Xcode
- ✅ Backups existing AppIcon before overwriting

## Installation

Copy the `appicon-export` folder to your project's `.agent/skills/` directory:

```bash
cp -r appicon-export /path/to/your/project/.agent/skills/
```

## Usage

In Claude Code / Antigravity, simply say:

```
Use appicon-export skill to process my icon: /path/to/icon-1024.png
```

Or run the script directly:

```bash
bash .agent/skills/appicon-export/scripts/generate.sh <source-image> <output-dir>
```

Example:
```bash
bash .agent/skills/appicon-export/scripts/generate.sh ~/my-icon.png MyApp/Assets.xcassets/AppIcon.appiconset
```

## Output

```
✅ Source verified: 1024x1024
⚠️  Existing AppIcon found, backing up to: AppIcon_bak_1048.appiconset
📦 Generating icon sizes...
✅ Done! Generated 11 icons
```

## Generated Sizes

| Purpose | Size | Filename |
|---------|------|----------|
| App Store | 1024x1024 | appicon-1024.png |
| iPhone App (3x) | 180x180 | appicon-60@3x.png |
| iPhone App (2x) | 120x120 | appicon-60@2x.png |
| iPad App (2x) | 152x152 | appicon-76@2x.png |
| iPad Pro (2x) | 167x167 | appicon-83.5@2x.png |
| iPhone Settings | 87x87, 58x58 | appicon-29@3x/2x.png |
| iPhone Spotlight | 120x120, 80x80 | appicon-40@3x/2x.png |
| iPhone Notification | 60x60, 40x40 | appicon-20@3x/2x.png |

## Requirements

- macOS (uses built-in `sips` command)
- Claude Code / Antigravity (for AI-driven usage)

## License

MIT
