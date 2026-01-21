---
name: appicon-export
description: |
  Generate iOS App Icon assets from a source image. Creates all required 
  sizes for iOS apps and generates the proper Contents.json for Xcode's 
  Assets.xcassets. Use when you have a 1024x1024 source icon and need 
  to prepare it for an iOS app release.
---

# AppIcon Assets Exporter

Generate all iOS App Icon sizes from a 1024x1024 source image and create the proper Assets.xcassets structure.

## Use Cases

- Preparing a new app release
- Updating the app icon
- Regenerating all icon sizes

## Workflow

### 1. Validate Source Image

First, verify the source image:
- Must be 1024x1024 pixels
- Must be PNG format (JPG will be converted)
- Should have no transparency (App Store requirement)

### 2. Generate Required Sizes

iOS requires the following App Icon sizes:

| Purpose | Size | Filename |
|---------|------|----------|
| App Store | 1024x1024 | appicon-1024.png |
| iPhone App (3x) | 180x180 | appicon-60@3x.png |
| iPhone App (2x) | 120x120 | appicon-60@2x.png |
| iPad App (2x) | 152x152 | appicon-76@2x.png |
| iPad Pro (2x) | 167x167 | appicon-83.5@2x.png |
| iPhone Settings (3x) | 87x87 | appicon-29@3x.png |
| iPhone Settings (2x) | 58x58 | appicon-29@2x.png |
| iPhone Spotlight (3x) | 120x120 | appicon-40@3x.png |
| iPhone Spotlight (2x) | 80x80 | appicon-40@2x.png |
| iPhone Notification (3x) | 60x60 | appicon-20@3x.png |
| iPhone Notification (2x) | 40x40 | appicon-20@2x.png |

### 3. Directory Structure

```
YourApp/Assets.xcassets/AppIcon.appiconset/
├── Contents.json
├── appicon-1024.png
├── appicon-60@3x.png
├── appicon-60@2x.png
├── appicon-76@2x.png
├── appicon-83.5@2x.png
├── appicon-29@3x.png
├── appicon-29@2x.png
├── appicon-40@3x.png
├── appicon-40@2x.png
├── appicon-20@3x.png
└── appicon-20@2x.png
```

### 4. Execution

Run the bundled script:

```bash
bash .agent/skills/appicon-export/scripts/generate.sh <source-image> <output-dir>
```

Example:
```bash
bash .agent/skills/appicon-export/scripts/generate.sh ~/icon-1024.png FretMaster/Assets.xcassets/AppIcon.appiconset
```

The script will:
1. Verify source image is 1024x1024
2. Backup existing AppIcon if present (e.g., `AppIcon_bak_1041.appiconset`)
3. Convert JPG to PNG if needed
4. Generate all 11 sizes using macOS `sips`
5. Create proper `Contents.json`

## Constraints

- ❌ Do not use PNGs with transparency (App Store will reject)
- ❌ Do not use alpha channel
- ✅ Use sRGB color space
- ✅ Source must be square 1024x1024

## Verification

After completion, verify:
1. All size files are generated
2. Contents.json format is correct
3. No warnings in Xcode AppIcon asset
