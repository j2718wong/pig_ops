#!/usr/bin/env python3
"""
Log Management Script for SuperPig
Controls log size by date-based retention
Run daily via cron or after deployment
"""

import os
import shutil
import gzip
import time
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
LOGS_DIR = Path("/root/projects/jsys/pig_ops/webroot/data/logs")
DAYS_TO_KEEP = 14              # Keep logs for 2 weeks
MAX_LOG_SIZE_MB = 10            # Max size per log file before compression
COMPRESS_AFTER_DAYS = 3         # Compress logs older than 3 days

def get_log_directories():
    """Get all dated log directories"""
    if not LOGS_DIR.exists():
        print(f"📁 Creating logs directory: {LOGS_DIR}")
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        return []
    
    # Get all directories matching YYYY-MM-DD pattern
    log_dirs = []
    for item in LOGS_DIR.iterdir():
        if item.is_dir():
            # Check if name matches date pattern (YYYY-MM-DD)
            try:
                datetime.strptime(item.name, "%Y-%m-%d")
                log_dirs.append(item)
            except ValueError:
                # Not a date directory, skip
                pass
    
    return sorted(log_dirs, reverse=True)  # Newest first

def get_log_files(log_dir):
    """Get all log files in a directory with better pattern matching"""
    files = []
    # Match common log file patterns used by your app
    patterns = ['*.log', '*.log.gz', '*_web.log', 'app_*.log', '*.txt']
    for pattern in patterns:
        files.extend(log_dir.glob(pattern))
    return files

def get_directory_size_mb(directory):
    """Calculate directory size in MB"""
    total_bytes = 0
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            total_bytes += file_path.stat().st_size
    return total_bytes / (1024 * 1024)

def compress_file(file_path):
    """Compress a log file with gzip - with error handling"""
    # Check if file exists before trying to compress
    if not file_path.exists():
        print(f"  ⚠️  File not found, skipping: {file_path.name}")
        return False
    
    compressed_path = file_path.with_suffix('.log.gz')
    
    # Skip if already compressed
    if compressed_path.exists():
        print(f"  ⏭️  Already compressed: {file_path.name}")
        return False
    
    try:
        print(f"  🗜️  Compressing: {file_path.name}")
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        # Get sizes after compression
        original_size = file_path.stat().st_size / 1024
        compressed_size = compressed_path.stat().st_size / 1024
        
        # Remove original after successful compression
        file_path.unlink()
        
        print(f"     {original_size:.1f}KB → {compressed_size:.1f}KB (saved {original_size - compressed_size:.1f}KB)")
        return True
        
    except Exception as e:
        print(f"  ❌ Error compressing {file_path.name}: {e}")
        # Clean up partial compressed file if it exists
        if compressed_path.exists():
            compressed_path.unlink()
        return False

def delete_old_directories():
    """Delete entire log directories older than DAYS_TO_KEEP"""
    log_dirs = get_log_directories()
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP)
    
    deleted_count = 0
    for log_dir in log_dirs:
        try:
            dir_date = datetime.strptime(log_dir.name, "%Y-%m-%d")
            if dir_date < cutoff_date:
                size = get_directory_size_mb(log_dir)
                print(f"🗑️  Deleting old directory: {log_dir.name} ({size:.1f}MB)")
                shutil.rmtree(log_dir)
                deleted_count += 1
        except ValueError:
            continue
    
    return deleted_count

def compress_old_logs():
    """Compress logs older than COMPRESS_AFTER_DAYS - with better error handling"""
    log_dirs = get_log_directories()
    cutoff_date = datetime.now() - timedelta(days=COMPRESS_AFTER_DAYS)
    
    compressed_count = 0
    for log_dir in log_dirs:
        try:
            dir_date = datetime.strptime(log_dir.name, "%Y-%m-%d")
            if dir_date < cutoff_date:
                # Get all log files using our improved pattern matching
                log_files = get_log_files(log_dir)
                
                # Filter for uncompressed logs only
                uncompressed = [f for f in log_files if f.suffix != '.gz']
                
                for log_file in uncompressed:
                    if compress_file(log_file):
                        compressed_count += 1
        except ValueError:
            continue
    
    return compressed_count

def check_current_log_size():
    """Check size of today's log and warn if too large"""
    today_dir = LOGS_DIR / datetime.now().strftime("%Y-%m-%d")
    
    if not today_dir.exists():
        return
    
    size_mb = get_directory_size_mb(today_dir)
    print(f"📊 Today's log size: {size_mb:.1f}MB")
    
    if size_mb > MAX_LOG_SIZE_MB:
        print(f"⚠️  WARNING: Today's log exceeds {MAX_LOG_SIZE_MB}MB!")
        print(f"   Consider reducing log verbosity in setup_logging()")
    
    return size_mb

def get_total_log_size():
    """Get total size of all logs"""
    total_mb = 0
    for log_dir in get_log_directories():
        total_mb += get_directory_size_mb(log_dir)
    return total_mb

def main():
    print("🔧 SuperPig Log Manager")
    print("========================")
    print(f"Logs directory: {LOGS_DIR}")
    print(f"Keeping logs for: {DAYS_TO_KEEP} days")
    print(f"Compressing after: {COMPRESS_AFTER_DAYS} days")
    print()
    
    # Get initial stats
    total_before = get_total_log_size()
    dir_count = len(get_log_directories())
    print(f"📁 Found {dir_count} log directories")
    print(f"📊 Total log size before: {total_before:.1f}MB")
    print()
    
    # Delete old directories
    deleted = delete_old_directories()
    if deleted > 0:
        print(f"✅ Deleted {deleted} old log directories")
    else:
        print("✅ No old directories to delete")
    
    # Compress old logs
    compressed = compress_old_logs()
    if compressed > 0:
        print(f"✅ Compressed {compressed} log files")
    else:
        print("✅ No logs needed compression")
    
    # Check current log size
    check_current_log_size()
    print()
    
    # Get final stats
    total_after = get_total_log_size()
    saved = total_before - total_after
    print(f"📊 Total log size after: {total_after:.1f}MB")
    print(f"💰 Saved: {saved:.1f}MB")
    
    # Summary
    print()
    print("✅ Log management complete!")
    print(f"   Current logs: {len(get_log_directories())} days")
    print(f"   Total size: {total_after:.1f}MB")

if __name__ == "__main__":
    main()
