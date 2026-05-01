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

def clean_path(path: str, name: str, command: List[str] = None):
    """Cleans up a cache using a specific command or interactive deletion."""
    if not os.path.exists(path) and not command:
        return

    msg = f"Do you want to clean up {name}?"
    if command:
        msg += f" (Runs: {' '.join(command)})"
    else:
        msg += f" (Path: {path})"
    
    response = input(f"{msg} (y/N): ").lower()
    if response == 'y':
        try:
            if command:
                print(f"Running '{' '.join(command)}'...")
                subprocess.run(command, check=True)
            elif os.path.isfile(path):
                os.remove(path)
                print(f"Removed file: {path}")
            else:
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
        except Exception as e:
            print(f"Error cleaning {name}: {e}")

def check_and_clean_caches():
    """Checks sizes of common developer caches and offers cleanup."""
    home = os.path.expanduser("~")
    # Format: (DisplayName, Path, CleanupCommand)
    caches = [
        ("Node.js (npm cache)", os.path.join(home, ".npm"), ["npm", "cache", "clean", "--force"]),
        ("Go (pkg cache)", os.path.join(home, "go", "pkg"), ["go", "clean", "-modcache"]),
        ("Docker (system prune)", os.path.join(home, ".docker"), ["docker", "system", "prune", "-f"]),
        ("Cargo (Rust cache)", os.path.join(home, ".cargo", "registry"), None),
        ("Yarn cache", os.path.join(home, ".yarn", "berry", "cache"), ["yarn", "cache", "clean"]),
        ("Python (pip cache)", os.path.join(home, ".cache", "pip"), ["pip", "cache", "purge"]),
        ("Bun cache", os.path.join(home, ".bun", "install", "cache"), None)
    ]

    print("\n--- Developer Cache Usage ---")
    found_caches = []
    for name, path, cmd in caches:
        size = get_size(path)
        if size > 0:
            print(f"{name}: {format_size(size)} ({path})")
            found_caches.append((name, path, cmd))
        else:
            print(f"{name}: Not found or empty")

    if found_caches:
        print("\n--- Cache Cleanup ---")
        for name, path, cmd in found_caches:
            clean_path(path, name, cmd)

def list_top_items():
    """Lists the top 5 largest items in the home directory."""
    home = os.path.expanduser("~")
    print(f"\n--- Top 5 Largest Items in {home} ---")
    try:
        # -k for kilobytes, -d 1 for max-depth 1
        # We use check=False because du may return non-zero if some directories are inaccessible
        result = subprocess.run(
            ['du', '-k', '-d', '1', home], 
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding='utf-8',
            check=False
        )
        
        output = result.stdout
        lines = output.strip().split('\n')
        items = []
        for line in lines:
            parts = line.split('\t')
            if len(parts) == 2:
                try:
                    size_kb = int(parts[0])
                    items.append((size_kb * 1024, parts[1]))
                except ValueError:
                    continue
        
        # Sort by size descending
        items.sort(key=lambda x: x[0], reverse=True)
        
        count = 0
        for size, path in items:
            # Skip the home directory itself which is usually the largest
            if os.path.abspath(path) == os.path.abspath(home):
                continue
            print(f"{format_size(size)}: {path}")
            count += 1
            if count >= 5:
                break
    except Exception as e:
        print(f"Error listing top items: {e}")

def main():
    print("Disk Usage Analysis & Cleanup Tool")
    print("===================================")
    
    check_and_clean_caches()
    list_top_items()
    
    print("\nNote: Please review the top items above and handle them manually if needed.")

if __name__ == "__main__":
    main()
