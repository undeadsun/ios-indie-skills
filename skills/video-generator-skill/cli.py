#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Downloader - Smart Media Downloader (Enhanced)

Usage:
    python cli.py status              # Check configuration status
    python cli.py image "keyword"     # Download images
    python cli.py video "keyword"     # Download video materials
    python cli.py youtube "URL"       # Download YouTube video
"""

import sys
import argparse
import logging
from pathlib import Path

#
sys.path.insert(0, str(Path(__file__).parent))

from core import Config, ImageHandler, VideoHandler
from core.utils import setup_logging, print_status_box
from core.exceptions import DependencyError


# ═══════════════════════════════════════════════════════════
# CLI 
# ═══════════════════════════════════════════════════════════

def cmd_status(args):
    """Check configuration status"""
    config = Config.load()
    image_handler = ImageHandler(config)
    video_handler = VideoHandler(config)
    
    # API Keys Status
    pexels = config.get("PEXELS_API_KEY")
    
    print_status_box("🔑 API Keys", {
        "PEXELS_API_KEY": bool(pexels),
    })
    
    print()
    
    # Tools Status
    print_status_box("🛠️ Tools", {
        "yt-dlp": video_handler.ytdlp_available,
        "ffmpeg": video_handler.ffmpeg_available,
        "requests": True,  # If here, requests is installed
    })
    
    print()
    
    # Features Status
    print_status_box("✨ Features", {
        "Image Download": bool(pexels),
        "Video Material": bool(pexels),
        "YouTube Download": video_handler.ytdlp_available,
        "Video Trimming": video_handler.ffmpeg_available,
    })
    
    print()
    print(f"📁 Download Dir: {config.output_dir}")
    
    if not pexels:
        print()
        print("💡 Tip: Configure Pexels API Key to enable image/video search:")
        print("   export PEXELS_API_KEY=your_key")
        print("   Get free key: https://www.pexels.com/api/")
    
    return 0


def cmd_image(args):
    """Download images"""
    config = Config.load()
    handler = ImageHandler(config)
    
    output_dir = args.output if args.output else None
    result = handler.execute(
        query=args.query,
        count=args.count,
        output_dir=output_dir
    )
    
    if result.get("success"):
        print(f"\n✅ Download complete: {result.get('count', 0)} images")
        print(f"📁 Saved to: {result.get('output_dir')}")
        return 0
    else:
        print(f"\n❌ Download failed: {result.get('error')}")
        if result.get('help'):
            print(f"💡 {result.get('help')}")
        return 1


def cmd_video(args):
    """Download video materials"""
    config = Config.load()
    handler = VideoHandler(config)
    
    output_dir = args.output if args.output else None
    result = handler.execute(
        query=args.query,
        count=args.count,
        duration=args.duration,
        output_dir=output_dir
    )
    
    if result.get("success"):
        print(f"\n✅ Download complete: {result.get('count', 0)} videos")
        print(f"📁 Saved to: {result.get('output_dir')}")
        return 0
    else:
        print(f"\n❌ Download failed: {result.get('error')}")
        if result.get('help'):
            print(f"💡 {result.get('help')}")
        return 1


def cmd_youtube(args):
    """Download YouTube video"""
    config = Config.load()
    handler = VideoHandler(config)
    
    if not handler.ytdlp_available:
        print("❌ yt-dlp required: pip install yt-dlp")
        return 1
    
    output_dir = args.output if args.output else None
    result = handler.execute(
        url=args.url,
        start=args.start,
        end=args.end,
        output_dir=output_dir
    )
    
    if result.get("success"):
        print(f"\n✅ Download complete!")
        for f in result.get("files", []):
            print(f"📁 {f}")
        return 0
    else:
        print(f"\n❌ Download failed: {result.get('error')}")
        return 1


def cmd_search(args):
    """Search media"""
    config = Config.load()
    
    print(f"🔍 Searching: {args.query}")
    print()
    
    if args.type in ["image", "all"]:
        handler = ImageHandler(config)
        images = handler.search_pexels(args.query, args.count)
        if images:
            print(f"📷 Images ({len(images)}):")
            for img in images[:5]:
                print(f"   • [{img['source']}] by {img['photographer']}")
        print()
    
    if args.type in ["video", "all"]:
        handler = VideoHandler(config)
        videos = handler.search_pexels_videos(args.query, args.count)
        if videos:
            print(f"🎬 Videos ({len(videos)}):")
            for vid in videos[:5]:
                print(f"   • [{vid['source']}] {vid.get('duration', '?')}s - {vid.get('width', '?')}x{vid.get('height', '?')}")
        print()
    
    return 0


# ═══════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════

def main():
    # Setup logging
    setup_logging(level=logging.INFO)
    
    # Create parser
    parser = argparse.ArgumentParser(
        description="Media Downloader - Smart Media Downloader (Enhanced)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py status                    # Check config
  python cli.py image "cute cats" -n 5    # Download images
  python cli.py video "sunset" -d 30      # Download videos
  python cli.py youtube "URL" -s 60 -e 90 # YouTube + trim
  python cli.py search "nature"           # Search
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # status command
    subparsers.add_parser("status", help="Check configuration status")
    
    # image command
    img_parser = subparsers.add_parser("image", help="Download images")
    img_parser.add_argument("query", help="Search keyword")
    img_parser.add_argument("--count", "-n", type=int, default=5, help="Download count")
    img_parser.add_argument("--output", "-o", help="Output directory")
    
    # video command
    vid_parser = subparsers.add_parser("video", help="Download video materials")
    vid_parser.add_argument("query", help="Search keyword")
    vid_parser.add_argument("--count", "-n", type=int, default=3, help="Download count")
    vid_parser.add_argument("--duration", "-d", type=int, default=60, help="Max duration (seconds)")
    vid_parser.add_argument("--output", "-o", help="Output directory")
    
    # youtube command
    yt_parser = subparsers.add_parser("youtube", help="Download YouTube video")
    yt_parser.add_argument("url", help="YouTube URL")
    yt_parser.add_argument("--start", "-s", type=float, help="Start time (seconds)")
    yt_parser.add_argument("--end", "-e", type=float, help="End time (seconds)")
    yt_parser.add_argument("--output", "-o", help="Output directory")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search media")
    search_parser.add_argument("query", help="Search keyword")
    search_parser.add_argument("--type", "-t", choices=["image", "video", "all"], default="all")
    search_parser.add_argument("--count", "-n", type=int, default=5)
    
    # Parse arguments
    args = parser.parse_args()
    
    # 
    if args.command == "status":
        return cmd_status(args)
    elif args.command == "image":
        return cmd_image(args)
    elif args.command == "video":
        return cmd_video(args)
    elif args.command == "youtube":
        return cmd_youtube(args)
    elif args.command == "search":
        return cmd_search(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
