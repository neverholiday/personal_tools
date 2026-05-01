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

def clean_path(path: str, name: str):
    """Interactively deletes a path after user confirmation."""
    if not os.path.exists(path):
        return

    response = input(f"Do you want to clean up {name} at {path}? (y/N): ").lower()
    if response == 'y':
        try:
            if name.startswith("Docker"):
                print(f"Running 'docker system prune -f'...")
                subprocess.run(['docker', 'system', 'prune', '-f'], check=True)
            elif os.path.isfile(path):
                os.remove(path)
                print(f"Removed file: {path}")
            else:
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
        except Exception as e:
            print(f"Error cleaning {path}: {e}")

def check_and_clean_caches():
    """Checks sizes of common developer caches and offers cleanup."""
    home = os.path.expanduser("~")
    caches = [
        ("Node.js (npm cache)", os.path.join(home, ".npm")),
        ("Go (pkg cache)", os.path.join(home, "go", "pkg")),
        ("Docker (system prune)", os.path.join(home, ".docker")),
        ("Cargo (Rust cache)", os.path.join(home, ".cargo", "registry")),
        ("Yarn cache", os.path.join(home, ".yarn", "berry", "cache")),
        ("Python (pip cache)", os.path.join(home, ".cache", "pip"))
    ]

    print("\n--- Developer Cache Usage ---")
    found_caches = []
    for name, path in caches:
        size = get_size(path)
        if size > 0:
            print(f"{name}: {format_size(size)} ({path})")
            found_caches.append((name, path))
        else:
            print(f"{name}: Not found or empty")

    if found_caches:
        print("\n--- Cache Cleanup ---")
        for name, path in found_caches:
            clean_path(path, name)

def main():
    print("Disk Usage Analysis & Cleanup Tool")
    print("===================================")
    
    check_and_clean_caches()
    list_top_items()
    
    print("\nNote: Please review the top items above and handle them manually if needed.")

if __name__ == "__main__":
    main()
