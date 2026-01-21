#!/bin/bash
# AppIcon Export Script
# Usage: ./generate.sh <source-image> <output-dir>

set -e

SOURCE="$1"
OUTPUT_DIR="$2"

if [ -z "$SOURCE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: ./generate.sh <source-1024.png> <output-dir>"
    exit 1
fi

# Verify source exists
if [ ! -f "$SOURCE" ]; then
    echo "❌ Source file not found: $SOURCE"
    exit 1
fi

# Check dimensions
WIDTH=$(sips -g pixelWidth "$SOURCE" | tail -1 | awk '{print $2}')
HEIGHT=$(sips -g pixelHeight "$SOURCE" | tail -1 | awk '{print $2}')

if [ "$WIDTH" != "1024" ] || [ "$HEIGHT" != "1024" ]; then
    echo "❌ Source must be 1024x1024, got ${WIDTH}x${HEIGHT}"
    exit 1
fi

echo "✅ Source verified: 1024x1024"

# Backup existing directory if it exists
if [ -d "$OUTPUT_DIR" ]; then
    # Get directory name without .appiconset extension
    DIR_NAME=$(dirname "$OUTPUT_DIR")
    BASE_NAME=$(basename "$OUTPUT_DIR" .appiconset)
    BACKUP_DIR="${DIR_NAME}/${BASE_NAME}_bak_$(date +%H%M).appiconset"
    echo "⚠️  Existing AppIcon found, backing up to: $(basename "$BACKUP_DIR")"
    mv "$OUTPUT_DIR" "$BACKUP_DIR"
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Convert to PNG if needed (handles JPG input)
sips -s format png "$SOURCE" --out "$OUTPUT_DIR/appicon-1024.png" > /dev/null

# Generate all sizes
echo "📦 Generating icon sizes..."
sips -z 180 180 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-60@3x.png" > /dev/null
sips -z 120 120 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-60@2x.png" > /dev/null
sips -z 152 152 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-76@2x.png" > /dev/null
sips -z 167 167 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-83.5@2x.png" > /dev/null
sips -z 87 87 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-29@3x.png" > /dev/null
sips -z 58 58 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-29@2x.png" > /dev/null
sips -z 120 120 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-40@3x.png" > /dev/null
sips -z 80 80 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-40@2x.png" > /dev/null
sips -z 60 60 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-20@3x.png" > /dev/null
sips -z 40 40 "$OUTPUT_DIR/appicon-1024.png" --out "$OUTPUT_DIR/appicon-20@2x.png" > /dev/null

# Generate Contents.json
cat > "$OUTPUT_DIR/Contents.json" << 'EOF'
{
  "images" : [
    {"filename":"appicon-20@2x.png","idiom":"iphone","scale":"2x","size":"20x20"},
    {"filename":"appicon-20@3x.png","idiom":"iphone","scale":"3x","size":"20x20"},
    {"filename":"appicon-29@2x.png","idiom":"iphone","scale":"2x","size":"29x29"},
    {"filename":"appicon-29@3x.png","idiom":"iphone","scale":"3x","size":"29x29"},
    {"filename":"appicon-40@2x.png","idiom":"iphone","scale":"2x","size":"40x40"},
    {"filename":"appicon-40@3x.png","idiom":"iphone","scale":"3x","size":"40x40"},
    {"filename":"appicon-60@2x.png","idiom":"iphone","scale":"2x","size":"60x60"},
    {"filename":"appicon-60@3x.png","idiom":"iphone","scale":"3x","size":"60x60"},
    {"filename":"appicon-20@2x.png","idiom":"ipad","scale":"2x","size":"20x20"},
    {"filename":"appicon-29@2x.png","idiom":"ipad","scale":"2x","size":"29x29"},
    {"filename":"appicon-40@2x.png","idiom":"ipad","scale":"2x","size":"40x40"},
    {"filename":"appicon-76@2x.png","idiom":"ipad","scale":"2x","size":"76x76"},
    {"filename":"appicon-83.5@2x.png","idiom":"ipad","scale":"2x","size":"83.5x83.5"},
    {"filename":"appicon-1024.png","idiom":"ios-marketing","scale":"1x","size":"1024x1024"}
  ],
  "info" : {"author":"xcode","version":1}
}
EOF

echo ""
echo "✅ Done! Generated $(ls -1 "$OUTPUT_DIR"/*.png | wc -l | tr -d ' ') icons:"
ls -la "$OUTPUT_DIR"
