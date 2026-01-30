"""
Utility Functions

Common utility functions and tools
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Callable, Iterator
from contextlib import contextmanager


# Try to import optional dependencies
try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    use_rich: bool = True
) -> logging.Logger:
    """
    Configure logging system
    
    Args:
        level: Logging level
        log_file: Log file path (optional)
        use_rich: Use rich for better output
        
    Returns:
        Root logger
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    if use_rich and RICH_AVAILABLE:
        console_handler = RichHandler(
            rich_tracebacks=True,
            show_time=True,
            show_path=False
        )
        console_handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
    
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(file_handler)
    
    return logger


@contextmanager
def get_progress_bar(
    total: int,
    description: str = "Processing",
    unit: str = "items"
) -> Iterator:
    """
    Get progress bar context manager
    
    Uses rich > tqdm > print fallback
    
    Args:
        total: Total count
        description: Description text
        unit: Unit string
        
    Yields:
        Update function
        
    Example:
        with get_progress_bar(100, "Downloading") as update:
            for i in range(100):
                # Do work
                update(1)
    """
    if RICH_AVAILABLE:
        # Use rich progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("[bold green]{task.completed}/{task.total} {task.fields[unit]}"),
        ) as progress:
            task = progress.add_task(description, total=total, unit=unit)
            
            def update(advance: int = 1):
                progress.update(task, advance=advance)
            
            yield update
            
    elif TQDM_AVAILABLE:
        # Use tqdm progress bar
        pbar = tqdm(total=total, desc=description, unit=unit)
        
        def update(advance: int = 1):
            pbar.update(advance)
        
        try:
            yield update
        finally:
            pbar.close()
    else:
        # Simple fallback: print percentage
        current = [0]  # Use list to bypass closure limitations
        
        def update(advance: int = 1):
            current[0] += advance
            percent = (current[0] / total) * 100
            print(f"\r{description}: {percent:.1f}% ({current[0]}/{total} {unit})", end="", flush=True)
            if current[0] >= total:
                print()  # New line on completion
        
        yield update


def print_status_box(title: str, items: dict, width: int = 60):
    """
    Print status box
    
    Args:
        title: Title
        items: Status items dict {name: status}
        width: Box width
    """
    if RICH_AVAILABLE:
        from rich.panel import Panel
        from rich.table import Table
        from rich.console import Console
        
        console = Console()
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column("Item", style="cyan")
        table.add_column("Status")
        
        for name, status in items.items():
            if isinstance(status, bool):
                status_str = "✅ Available" if status else "❌ Not Configured"
                style = "green" if status else "red"
            else:
                status_str = str(status)
                style = "white"
            table.add_row(name, f"[{style}]{status_str}[/{style}]")
        
        console.print(Panel(table, title=f"[bold]{title}[/bold]", width=width))
    else:
        # Simple text output
        print("╔" + "═" * (width - 2) + "╗")
        print(f"║ {title:^{width-4}} ║")
        print("╠" + "═" * (width - 2) + "╣")
        
        for name, status in items.items():
            if isinstance(status, bool):
                status_str = "✅" if status else "❌"
            else:
                status_str = str(status)[:width-len(name)-8]
            line = f"  {name}: {status_str}"
            print(f"║ {line:<{width-4}} ║")
        
        print("╚" + "═" * (width - 2) + "╝")


def ensure_dir(path: Path) -> Path:
    """
    Ensure directory exists
    
    Args:
        path: Directory path
        
    Returns:
        Directory path
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_size(size_bytes: int) -> str:
    """
    Format file size
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """
    Format duration
    
    Args:
        seconds: Seconds
        
    Returns:
        Formatted duration string
    """
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"
