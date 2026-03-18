#!/usr/bin/env python3
# /root/projects/jsys/pig_ops/webroot/scripts/restore_templates.py
"""
Restore original templates from backup
Run this if you need to debug with unminified files
"""

import sys
from pathlib import Path

# Add script directory to path so we can import minify_templates
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.append(str(SCRIPT_DIR))

from minify_templates import restore_from_backup, TEMPLATES_DIR

if __name__ == "__main__":
    print("🔄 Restoring templates from backup...")
    if restore_from_backup():
        print(f"✅ Templates restored in {TEMPLATES_DIR}")
        print("   Run 'sudo systemctl restart superpig' to apply changes")
    else:
        print("❌ Restore failed - no backup found")
