"""
Media Download Handlers

Core functionality for downloading images and videos
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.parse import quote_plus

from .base import BaseHandler
from .config import Config
from .exceptions import NetworkError, DependencyError, ConfigError


# Try to import requests
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class ImageHandler(BaseHandler):
    """Image Download Handler"""
    
    @property
    def name(self) -> str:
        return "image-handler"
    
    @property
    def required_config_keys(self) -> list:
        return []  # Pexels API Key is optional, configure as needed
    
    @property
    def required_dependencies(self) -> list:
        return []
    
    def __init__(self, config: Config = None):
        super().__init__(config)
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
        else:
            self.session = None
    
    def search_pexels(self, query: str, count: int = 5) -> List[Dict]:
        """Search images from Pexels"""
        api_key = self.config.get("PEXELS_API_KEY")
        if not api_key:
            return []
        
        url = f"https://api.pexels.com/v1/search?query={quote_plus(query)}&per_page={count}"
        headers = {"Authorization": api_key}
        
        try:
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "url": photo["src"]["large"],
                        "original": photo["src"]["original"],
                        "photographer": photo["photographer"],
                        "source": "pexels",
                        "id": photo["id"],
                    }
                    for photo in data.get("photos", [])
                ]
        except Exception as e:
            self.logger.warning(f"Pexels search failed: {e}")
        return []
    
    def download(self, url: str, filename: str, output_dir: Path = None) -> Optional[Path]:
        """Download image"""
        if not REQUESTS_AVAILABLE:
            raise DependencyError("requests", "pip install requests")
        
        output_dir = output_dir or self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        
        try:
            resp = self.session.get(url, timeout=30, stream=True)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return filepath
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
        return None
    
    def execute(self, query: str, count: int = 5, output_dir: str = None, **kwargs) -> Dict[str, Any]:
        """Execute image download"""
        if not REQUESTS_AVAILABLE:
            raise DependencyError("requests", "pip install requests")
        
        self.logger.info(f"🔍 Searching images: {query}")
        results = self.search_pexels(query, count * 2)
        
        if not results:
            api_key = self.config.get("PEXELS_API_KEY")
            if not api_key:
                return {
                    "success": False,
                    "error": "PEXELS_API_KEY required",
                    "help": "Please run: export PEXELS_API_KEY=your_key"
                }
            return {"success": False, "error": "No images found"}
        
        output_path = Path(output_dir) if output_dir else self.config.output_dir
        downloaded = []
        
        for i, img in enumerate(results[:count]):
            ext = img["url"].split(".")[-1].split("?")[0][:4]
            if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                ext = "jpg"
            filename = f"{query.replace(' ', '_')}_{i+1}_{img['source']}.{ext}"
            
            self.logger.info(f"  ⬇️ Downloading {i+1}/{count}: {filename}")
            path = self.download(img["url"], filename, output_path)
            if path:
                downloaded.append(str(path))
        
        return {
            "success": True,
            "count": len(downloaded),
            "files": downloaded,
            "output_dir": str(output_path)
        }


class VideoHandler(BaseHandler):
    """Video Download Handler"""
    
    @property
    def name(self) -> str:
        return "video-handler"
    
    @property
    def required_dependencies(self) -> list:
        return [
            {"name": "yt-dlp", "check_cmd": "yt-dlp --version", "install_cmd": "pip install yt-dlp"},
            {"name": "ffmpeg", "check_cmd": "ffmpeg -version", "install_cmd": "brew install ffmpeg"}
        ]
    
    def __init__(self, config: Config = None):
        super().__init__(config)
        if REQUESTS_AVAILABLE:
            self.session = requests.Session()
        else:
            self.session = None
        self.ytdlp_available = self._check_tool("yt-dlp")
        self.ffmpeg_available = self._check_tool("ffmpeg")
    
    def _check_tool(self, tool: str) -> bool:
        """Check if tool is available"""
        try:
            result = subprocess.run([tool, "--version"], capture_output=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def search_pexels_videos(self, query: str, count: int = 5) -> List[Dict]:
        """Search videos from Pexels"""
        api_key = self.config.get("PEXELS_API_KEY")
        if not api_key or not REQUESTS_AVAILABLE:
            return []
        
        url = f"https://api.pexels.com/videos/search?query={quote_plus(query)}&per_page={count}"
        headers = {"Authorization": api_key}
        
        try:
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                results = []
                for video in data.get("videos", []):
                    files = video.get("video_files", [])
                    best = max(files, key=lambda x: x.get("width", 0)) if files else None
                    if best:
                        results.append({
                            "url": best["link"],
                            "duration": video.get("duration", 0),
                            "width": best.get("width", 0),
                            "height": best.get("height", 0),
                            "source": "pexels",
                            "id": video["id"],
                        })
                return results
        except Exception as e:
            self.logger.warning(f"Pexels Videos search failed: {e}")
        return []
    
    def download_video(self, url: str, filename: str, output_dir: Path = None) -> Optional[Path]:
        """Download video file"""
        if not REQUESTS_AVAILABLE:
            return None
        
        output_dir = output_dir or self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        filepath = output_dir / filename
        
        try:
            resp = self.session.get(url, timeout=60, stream=True)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                return filepath
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
        return None
    
    def search_youtube(self, query: str, count: int = 1, max_duration: int = None) -> List[Dict]:
        """
        Search YouTube videos
        
        Args:
            query: Search keyword
            count: Number of results
            max_duration: Max duration (seconds), for filtering short videos
        """
        if not self.ytdlp_available:
            return []
        
        # Search more if duration filtering is needed
        search_count = count * 5 if max_duration else count
        
        try:
            cmd = [
                'yt-dlp',
                '--cookies-from-browser', 'chrome',
                f'ytsearch{search_count}:{query}',
                '--dump-json',
                '--no-download',
                '--flat-playlist',
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if result.returncode == 0:
                results = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            data = json.loads(line)
                            video_duration = data.get("duration", 0) or 0
                            
                            # Filter by duration
                            if max_duration and video_duration > max_duration:
                                continue
                            
                            results.append({
                                "url": f"https://www.youtube.com/watch?v={data.get('id', '')}",
                                "title": data.get("title", ""),
                                "duration": video_duration,
                                "channel": data.get("channel", ""),
                                "source": "youtube",
                                "id": data.get("id", ""),
                            })
                            
                            # Break if count reached
                            if len(results) >= count:
                                break
                        except json.JSONDecodeError:
                            pass
                return results
        except subprocess.TimeoutExpired:
            self.logger.error("YouTube search timed out")
        except Exception as e:
            self.logger.error(f"YouTube search failed: {e}")
        return []

    def download_youtube(self, url: str = None, query: str = None, output_dir: Path = None, 
                         start: float = None, end: float = None, duration: float = None,
                         audio_only: bool = False, use_cookies: bool = True) -> Optional[Path]:
        """
        Download video from YouTube
        
        Args:
            url: YouTube URL (optional)
            query: Search keyword (optional, used if url is None)
            output_dir: Output directory
            start: Start time (seconds)
            end: End time (seconds)
            duration: Duration (seconds), trim from start
            audio_only: Download audio only
            use_cookies: Use browser cookies
        """
        if not self.ytdlp_available:
            raise DependencyError("yt-dlp", "pip install yt-dlp")
        
        # Search if no URL
        if not url and query:
            self.logger.info(f"🔍 Searching YouTube: {query}")
            # Filter short videos (max 5 mins, download then trim)
            results = self.search_youtube(query, 1, max_duration=300)
            if results:
                url = results[0]["url"]
                video_dur = results[0].get('duration', 0)
                self.logger.info(f"✅ Found: {results[0].get('title', '')[:40]} ({video_dur}s)")
            else:
                self.logger.error("No suitable short video found")
                return None
        
        if not url:
            self.logger.error("Please provide URL or search query")
            return None
        
        output_dir = output_dir or self.config.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_template = str(output_dir / f"yt_{timestamp}_%(title).30s.%(ext)s")
        
        # Check if trimming is needed
        need_trim = duration or start or end
        trim_start = start or 0
        trim_duration = duration or (end - trim_start if end else None)
        
        # Build command
        cmd = ['yt-dlp']
        
        # Use browser cookies
        if use_cookies:
            cmd.extend(['--cookies-from-browser', 'chrome'])
        
        cmd.extend(['-o', output_template])
        
        if audio_only:
            cmd.extend(['--extract-audio', '--audio-format', 'mp3'])
        else:
            # Use best format (avoid 403 on format 18)
            # Limit height to avoid large files
            cmd.extend(['-f', 'best[height<=480]/best'])
        
        # Note: Avoid --download-sections (prone to failure)
        # Instead download full video and trim locally
        
        # Add progress display options
        cmd.extend(['--progress', '--newline'])
        cmd.append(url)
        
        self.logger.info(f"⬇️ Starting download...")
        
        try:
            # Use Popen for real-time progress
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            # Output progress in real-time
            for line in process.stdout:
                line = line.strip()
                if line:
                    # Only show download progress lines
                    if '%' in line or 'Destination' in line or 'download' in line.lower():
                        print(f"   {line[:80]}")
            
            process.wait(timeout=300)
            
            if process.returncode == 0:
                # Find downloaded file
                for f in output_dir.iterdir():
                    if f.name.startswith(f"yt_{timestamp}_"):
                        self.logger.info(f"✅ Download complete: {f.name}")
                        
                        # Trim if needed
                        if need_trim and self.ffmpeg_available:
                            self.logger.info(f"✂️ Trimming video (Start: {trim_start}s, Duration: {trim_duration}s)")
                            trimmed = self.trim_video(f, trim_start, trim_start + trim_duration if trim_duration else None)
                            if trimmed:
                                return trimmed
                        return f
            else:
                self.logger.error(f"Download failed: {result.stderr[-300:] if result.stderr else 'unknown error'}")
        except subprocess.TimeoutExpired:
            self.logger.error("Download timed out")
        except Exception as e:
            self.logger.error(f"Download failed: {e}")
        return None
    
    def trim_video(self, input_path: Path, start: float = None, end: float = None) -> Optional[Path]:
        """Trim video"""
        if not self.ffmpeg_available:
            self.logger.warning("ffmpeg not installed, skipping trim")
            return input_path
        
        output_path = input_path.parent / f"{input_path.stem}_trimmed{input_path.suffix}"
        
        cmd = ['ffmpeg', '-y']
        
        if start and start > 0:
            cmd.extend(['-ss', str(start)])
        
        cmd.extend(['-i', str(input_path)])
        
        if end:
            duration = end - (start or 0)
            cmd.extend(['-t', str(duration)])
        
        cmd.extend(['-c:v', 'libx264', '-preset', 'fast', '-c:a', 'aac', str(output_path)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            if result.returncode == 0:
                input_path.unlink()  # Delete original file
                return output_path
        except Exception as e:
            self.logger.error(f"Trim failed: {e}")
        
        return input_path
    
    def execute(self, query: str = None, url: str = None, count: int = 3, 
                duration: int = None, output_dir: str = None,
                start: float = None, end: float = None, 
                youtube_search: bool = True, **kwargs) -> Dict[str, Any]:
        """
        Execute video download
        
        Args:
            query: Search keyword
            url: YouTube URL (optional)
            count: Download count
            duration: Video duration (seconds)
            output_dir: Output directory
            start: Start time (seconds)
            end: End time (seconds)
            youtube_search: Prefer YouTube search (default True)
        """
        output_path = Path(output_dir) if output_dir else self.config.output_dir
        
        # YouTube URL Download
        if url:
            self.logger.info(f"⬇️ Downloading YouTube video: {url}")
            path = self.download_youtube(
                url=url, 
                output_dir=output_path, 
                start=start, 
                end=end,
                duration=duration
            )
            if path:
                return {
                    "success": True,
                    "count": 1,
                    "files": [str(path)],
                    "output_dir": str(output_path)
                }
            return {"success": False, "error": "YouTube download failed"}
        
        # Search by keyword
        if query:
            # Prefer YouTube (No API Key required)
            if youtube_search and self.ytdlp_available:
                self.logger.info(f"🔍 Searching YouTube: {query}")
                path = self.download_youtube(
                    query=query,
                    output_dir=output_path,
                    duration=duration,
                    start=start,
                    end=end
                )
                if path:
                    return {
                        "success": True,
                        "count": 1,
                        "files": [str(path)],
                        "output_dir": str(output_path)
                    }
                # YouTube failed, try Pexels
                self.logger.warning("YouTube failed, trying Pexels...")
            
            # Search Pexels
            self.logger.info(f"🔍 Searching Pexels: {query}")
            results = self.search_pexels_videos(query, count)
            
            # Filter duration
            if duration:
                results = [v for v in results if v.get("duration", 0) <= duration * 1.5]
            
            if not results:
                api_key = self.config.get("PEXELS_API_KEY")
                if not api_key:
                    return {
                        "success": False,
                        "error": "Download failed. YouTube network issue and PEXELS_API_KEY not configured",
                        "help": "Please retry or configure PEXELS_API_KEY"
                    }
                return {"success": False, "error": "No videos found"}
            
            downloaded = []
            for i, video in enumerate(results[:count]):
                filename = f"{query.replace(' ', '_')}_{i+1}_{video['source']}.mp4"
                self.logger.info(f"  ⬇️ Downloading {i+1}/{count}: {filename} ({video.get('duration', '?')}s)")
                
                path = self.download_video(video["url"], filename, output_path)
                if path:
                    downloaded.append(str(path))
            
            return {
                "success": True,
                "count": len(downloaded),
                "files": downloaded,
                "output_dir": str(output_path)
            }
        
        return {"success": False, "error": "Please provide search keyword or YouTube URL"}
