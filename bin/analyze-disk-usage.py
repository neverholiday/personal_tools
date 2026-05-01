#!/usr/bin/env python3
import os
import subprocess
import shutil
from typing import List, Tuple

"""
Tool: analyze-disk-usage.py
Responsibility: Analyzes disk usage in the home directory, identifies common developer caches, 
                and lists the top 5 largest items for potential manual cleanup.
"""

def get_size(path: str) -> int:
    """Returns the size of a file or directory in bytes."""
    if not os.path.exists(path):
        return 0
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        
        # Use du for directory size to be efficient
        output = subprocess.check_output(['du', '-sk', path], stderr=subprocess.DEVNULL)
        return int(output.split()[0]) * 1024
    except (subprocess.CalledProcessError, ValueError, IndexError):
        return 0

def format_size(size: int) -> str:
    """Formats bytes into human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def check_caches():
    """Checks sizes of common developer caches."""
    home = os.path.expanduser("~")
    caches = {
        "Node.js (npm cache)": os.path.join(home, ".npm"),
        "Go (pkg cache)": os.path.join(home, "go", "pkg"),
        "Docker (images/volumes - approx)": os.path.join(home, ".docker"),
        "Cargo (Rust cache)": os.path.join(home, ".cargo", "registry"),
        "Yarn cache": os.path.join(home, ".yarn", "berry", "cache"),
        "Python (pip cache)": os.path.join(home, ".cache", "pip")
    }

    print("\n--- Developer Cache Usage ---")
    for name, path in caches.items():
        size = get_size(path)
        if size > 0:
            print(f"{name}: {format_size(size)} ({path})")
        else:
            print(f"{name}: Not found or empty")

def list_top_items(limit=5):
    """Lists top N largest items in the home directory (non-hidden)."""
    home = os.path.expanduser("~")
    print(f"\n--- Top {limit} Largest Items in {home} ---")
    
    items = []
    try:
        # We list directories and files, skipping hidden ones to keep it relevant to user data
        for entry in os.scandir(home):
            if not entry.name.startswith('.'):
                size = get_size(entry.path)
                items.append((entry.name, size))
    except PermissionError:
        pass

    items.sort(key=lambda x: x[1], reverse=True)
    
    for name, size in items[:limit]:
        print(f"{format_size(size)}: {name}")

def main():
    print("Disk Usage Analysis Tool")
    print("=========================")
    
    check_caches()
    list_top_items()
    
    print("\nNote: Please review the items above and delete them manually if they are no longer needed.")

if __name__ == "__main__":
    main()
