# /root/projects/jsys/pig_ops/webroot/scripts/minify_templates.py
#!/usr/bin/env python3
"""
Minify HTML templates before FastAPI serves them
Run this after git pull and before restarting the app
"""

import os
import re
import shutil
from pathlib import Path

# Paths - now relative to script location
SCRIPT_DIR = Path(__file__).parent.absolute()
WEBROOT_DIR = SCRIPT_DIR.parent
TEMPLATES_DIR = WEBROOT_DIR / "templates"
BACKUP_DIR = WEBROOT_DIR / "templates_backup"
REPO_ROOT = WEBROOT_DIR.parent.parent  # Goes up to /root/projects/jsys/

def minify_html(content):
    """Minify HTML content"""
    # Remove HTML comments (except IE conditionals)
    content = re.sub(r'<!--(?!\[if).*?-->', '', content, flags=re.DOTALL)
    
    # Remove whitespace between tags
    content = re.sub(r'>\s+<', '><', content)
    
    # Remove multiple newlines
    content = re.sub(r'\n\s*\n', '\n', content)
    
    # Trim lines
    lines = [line.strip() for line in content.split('\n')]
    content = '\n'.join(lines)
    
    return content.strip()

def minify_file(file_path):
    """Minify a single HTML file"""
    original_size = file_path.stat().st_size
    
    # Read original
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Minify
    minified = minify_html(content)
    
    # Write back (overwrite original)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    
    new_size = file_path.stat().st_size
    saved = original_size - new_size
    
    print(f"  ✅ {file_path.name}: {original_size:,} → {new_size:,} bytes (saved {saved:,})")
    return saved

def backup_originals():
    """Create backup of original templates"""
    if BACKUP_DIR.exists():
        shutil.rmtree(BACKUP_DIR)
    
    shutil.copytree(TEMPLATES_DIR, BACKUP_DIR)
    print(f"📦 Backup created at {BACKUP_DIR}")

def restore_from_backup():
    """Restore originals from backup"""
    if not BACKUP_DIR.exists():
        print("❌ No backup found!")
        return False
    
    # Clear templates directory
    for f in TEMPLATES_DIR.glob("*.html"):
        f.unlink()
    
    # Copy back from backup
    for f in BACKUP_DIR.glob("*.html"):
        shutil.copy2(f, TEMPLATES_DIR)
    
    print(f"🔄 Restored from backup")
    return True

def main():
    print("🔧 Minifying HTML templates...")
    print(f"📁 Templates directory: {TEMPLATES_DIR}")
    print(f"📁 Script location: {SCRIPT_DIR}")
    
    # Create backup first
    backup_originals()
    
    total_saved = 0
    minified_count = 0
    
    # Minify all HTML files
    for html_file in TEMPLATES_DIR.glob("*.html"):
        saved = minify_file(html_file)
        total_saved += saved
        minified_count += 1
    
    print(f"\n📊 Summary: {minified_count} files minified")
    print(f"💰 Total bandwidth saved: {total_saved:,} bytes ({total_saved/1024:.1f} KB)")
    
    # Create a marker file to remember this was done
    marker = TEMPLATES_DIR / ".minified"
    marker.touch()
    print(f"✅ Minification complete. Marker: {marker}")

if __name__ == "__main__":
    main()
