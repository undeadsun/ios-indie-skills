#!/usr/bin/env python3
import os
import sys
import argparse
import shutil
import subprocess
from pathlib import Path

# Import core handlers
sys.path.insert(0, str(Path(__file__).parent))
from core import Config, ImageHandler, VideoHandler, setup_logging

def init_project(target_dir: Path):
    """Initialize a new Remotion project from template"""
    template_src = Path(__file__).parent / "templates/default"
    
    if not template_src.exists():
        print(f"❌ Template not found at {template_src}")
        return False
        
    print(f"📦 Initializing project in {target_dir.absolute()}...")
    
    # Copy template files
    try:
        shutil.copytree(template_src, target_dir, dirs_exist_ok=True)
        print("✅ Template files copied")
        
        # Create assets directory
        (target_dir / "public/assets").mkdir(parents=True, exist_ok=True)
        
        # Install dependencies
        print("📦 Installing dependencies (may take a minute)...")
        subprocess.run(["npm", "install", "--legacy-peer-deps"], cwd=target_dir, check=True)
        
        print(f"\n✨ Project initialized! To generate a video:\n  cd {target_dir}\n  python3 {Path(__file__).absolute()} generate \"Your Topic\"")
        return True
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

def download_media(prompt: str, count: int, output_dir: Path):
    """Download images using ImageHandler"""
    config = Config.load()
    handler = ImageHandler(config)
    
    print(f"📷 Downloading {count} images for: {prompt}")
    result = handler.execute(
        query=prompt,
        count=count,
        output_dir=output_dir
    )
    
    if not result.get("success"):
        print(f"❌ Image download failed: {result.get('error')}")
        return []
        
    return result.get("files", [])

def download_music(prompt: str, output_path: Path):
    """Download background music"""
    config = Config.load()
    handler = VideoHandler(config)
    
    music_prompt = f"{prompt} lofi hip hop relaxed music"
    print(f"🎵 Searching music for: {music_prompt}")
    
    # Try downloading a short video to extract audio
    temp_dir = output_path.parent / "temp_music"
    temp_dir.mkdir(exist_ok=True)
    
    # Try YouTube first
    result = handler.execute(
        query=music_prompt,
        count=1,
        duration=180, # Max 3 mins
        output_dir=temp_dir,
        youtube_search=True
    )
    
    if result.get("success") and result.get("files"):
        src_file = Path(result["files"][0])
        shutil.move(src_file, output_path)
        shutil.rmtree(temp_dir)
        print(f"✅ Music downloaded")
        return True
    
    print("⚠️ Music download failed, using fallback.")
    fallback_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    try:
        subprocess.run(["curl", "-L", "-o", str(output_path), fallback_url], check=True)
        print("✅ Fallback music downloaded")
        return True
    except Exception as e:
        print(f"❌ Fallback failed: {e}")
        return False

def generate_manifest(images: list, music_path: Path, phrases: list, project_dir: Path):
    """Generate manifest.ts for Remotion"""
    
    manifest_content = """
import { staticFile } from "remotion";

export const manifest = {
    images: [
"""
    for img in images:
        filename = Path(img).name
        manifest_content += f'        staticFile("assets/{filename}"),\n'

    manifest_content += """    ],
"""

    if music_path and music_path.exists():
        manifest_content += f'    music: staticFile("assets/{music_path.name}"),\n'
    else:
        print(f"⚠️ Warning: Music file not found at {music_path}. Video will be silent.")
        manifest_content += '    music: null,\n'

    manifest_content += """    phrases: [
"""
    for p in phrases:
        manifest_content += f'        "{p}",\n'
    manifest_content += """    ],
    durationPerSlide: 90,
    fps: 30
};
"""
    
    manifest_path = project_dir / "src/manifest.ts"
    with open(manifest_path, "w") as f:
        f.write(manifest_content)
    print(f"📝 Manifest generated at {manifest_path}")

def generate_video(prompt: str, count: int, output_file: str, project_dir: Path):
    """Orchestrate video generation"""
    
    # Validation
    if not (project_dir / "package.json").exists():
        print(f"❌ Error: {project_dir} does not appear to be a Remotion project.")
        print("Run 'init' first to create a project.")
        return 1

    public_assets_dir = project_dir / "public/assets"
    
    # Ensure assets dir exists
    public_assets_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Download Images
    images = download_media(prompt, count, public_assets_dir)
    if not images:
        print("❌ No images found. Aborting.")
        return 1
        
    # 2. Download Music
    music_path = public_assets_dir / "music.mp3"
    # Remove old music
    if music_path.exists():
        music_path.unlink()
    download_music(prompt, music_path)
    
    # 3. Generate Phrases (Mock)
    phrases = [
        f"Explore {prompt}", "Discover Beauty", "Inspiration Awaits", "Dream Big", "Start Now"
    ]
    
    # 4. Generate Manifest
    generate_manifest(images, music_path, phrases, project_dir)
    
    # 5. Render Video
    print("🎬 Rendering video...")
    
    if not output_file:
        output_file = f"{prompt.replace(' ', '_')}.mp4"
    if not output_file.endswith(".mp4"):
        output_file += ".mp4"
        
    # Output to project root/out by default, or absolute path
    if Path(output_file).is_absolute():
        final_output_path = Path(output_file)
    else:
        # If relative, save to Downloads for easy access
        final_output_path = Path.home() / "Downloads" / output_file
    
    render_cmd = [
        "npx", "remotion", "render",
        "src/index.tsx", "Video",
        str(final_output_path),
        "--overwrite"
    ]
    
    try:
        subprocess.run(render_cmd, cwd=project_dir, check=True)
        print(f"\n✅ Video generated successfully!")
        print(f"📁 {final_output_path}")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Rendering failed: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="AI Video Generator Skill")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new project")
    init_parser.add_argument("path", nargs="?", default=".", help="Directory to initialize")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a video")
    gen_parser.add_argument("prompt", help="Video topic")
    gen_parser.add_argument("--count", "-n", type=int, default=5, help="Number of slides")
    gen_parser.add_argument("--output", "-o", help="Output filename")
    gen_parser.add_argument("--project-dir", "-d", default=".", help="Project directory")
    
    # Shortcut: if first arg is not a command, assume it's a prompt for 'generate'
    if len(sys.argv) > 1 and sys.argv[1] not in ["init", "generate", "-h", "--help"]:
        # Mock args for shortcut
        sys.argv.insert(1, "generate")
        
    args = parser.parse_args()
    
    if args.command == "init":
        return 0 if init_project(Path(args.path)) else 1
    elif args.command == "generate":
        return generate_video(args.prompt, args.count, args.output, Path(args.project_dir))
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    setup_logging()
    sys.exit(main())
