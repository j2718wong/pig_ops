#!/usr/bin/env python3
"""
add_file_header.py - Add filename comment to Python and JavaScript files

Usage:
    python add_file_header.py <directory>
    python add_file_header.py /path/to/project

This script recursively scans all .py and .js files in the given directory
and adds a filename comment at the top if not already present.
"""

import os
import sys
import re
from pathlib import Path


# File type configurations
FILE_CONFIGS = {
    '.py': {
        'comment_start': '# ',
        'comment_end': '',
        'pattern': r'^# [a-zA-Z0-9_\-\.]+\.py$'  # More specific: must end with .py
    },
    '.js': {
        'comment_start': '// ',
        'comment_end': '',
        'pattern': r'^// [a-zA-Z0-9_\-\.]+\.js$'  # More specific: must end with .js
    }
}


def get_filename_comment(file_path, file_ext):
    """Generate the filename comment for a given file."""
    filename = os.path.basename(file_path)
    config = FILE_CONFIGS[file_ext]
    
    return f"{config['comment_start']}{filename}{config['comment_end']}"


def has_filename_comment(content, file_ext, filename):
    """Check if the file already has a filename comment at the top."""
    if not content:
        return False
    
    config = FILE_CONFIGS[file_ext]
    lines = content.split('\n')
    
    # Check first few lines (skip empty lines, shebang, encoding)
    for line in lines[:10]:  # Check first 10 lines max
        stripped = line.strip()
        if not stripped:
            continue
        
        # Skip shebang for Python
        if file_ext == '.py' and stripped.startswith('#!'):
            continue
        
        # Skip encoding declaration
        if file_ext == '.py' and '# -*- coding:' in stripped:
            continue
        
        # Check if line exactly matches the filename comment pattern
        if re.match(config['pattern'], stripped):
            return True
        
        # Also check if line contains the exact filename
        if stripped.startswith(config['comment_start']):
            comment_content = stripped[len(config['comment_start']):].strip()
            if comment_content == filename:
                return True
        
        # If we find a comment that's not a filename comment, stop checking
        # (This prevents false positives with date comments)
        if stripped.startswith(config['comment_start']):
            # This is a comment but not a filename comment
            # Continue checking next lines for filename comment
            continue
        
        # If we hit non-comment code, stop checking
        break
    
    return False


def add_filename_comment(file_path, dry_run=False):
    """Add filename comment to the file if not already present."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext not in FILE_CONFIGS:
        return False, f"Skipped (unsupported extension)"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(file_path)
        
        if has_filename_comment(content, file_ext, filename):
            return False, "Already has filename comment"
        
        # Generate the filename comment
        filename_comment = get_filename_comment(file_path, file_ext)
        
        # Add comment at the top (preserve shebang if present)
        lines = content.split('\n')
        
        # Check for shebang (#!/usr/bin/env python3) - only for .py files
        shebang_line = None
        start_index = 0
        
        if file_ext == '.py' and lines and lines[0].startswith('#!'):
            shebang_line = lines[0]
            start_index = 1
        
        # Check for encoding declaration (Python)
        encoding_line = None
        if file_ext == '.py' and start_index < len(lines):
            # Look for encoding line in first few lines
            for i in range(start_index, min(start_index + 2, len(lines))):
                if lines[i].strip().startswith('# -*- coding:'):
                    encoding_line = lines[i]
                    start_index = i + 1
                    break
        
        # Build new content
        new_lines = []
        
        # Add shebang if present
        if shebang_line:
            new_lines.append(shebang_line)
        
        # Add encoding if present
        if encoding_line:
            new_lines.append(encoding_line)
        
        # Add blank line after shebang/encoding if needed
        if (shebang_line or encoding_line) and new_lines:
            new_lines.append('')
        
        # Add filename comment
        new_lines.append(filename_comment)
        new_lines.append('')  # Blank line after comment
        
        # Add original content from start_index
        new_lines.extend(lines[start_index:])
        
        new_content = '\n'.join(new_lines)
        
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        
        return True, "Added filename comment"
        
    except Exception as e:
        return False, f"Error: {str(e)}"


def scan_directory(directory, dry_run=False, verbose=False):
    """Recursively scan directory and process all .py and .js files."""
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return
    
    # Find all .py and .js files
    patterns = ['**/*.py', '**/*.js']
    files = []
    for pattern in patterns:
        files.extend(directory.glob(pattern))
    
    # Filter out node_modules, .venv, __pycache__, etc.
    exclude_dirs = {'node_modules', '.venv', 'venv', '__pycache__', '.git', 'dist', 'build'}
    files = [f for f in files if not any(excluded in f.parts for excluded in exclude_dirs)]
    
    if not files:
        print(f"No .py or .js files found in '{directory}'")
        return
    
    print(f"{'DRY RUN - ' if dry_run else ''}Processing {len(files)} files...")
    print("-" * 60)
    
    stats = {
        'processed': 0,
        'skipped': 0,
        'errors': 0,
        'modified': 0
    }
    
    for file_path in sorted(files):
        rel_path = file_path.relative_to(directory)
        success, message = add_filename_comment(str(file_path), dry_run)
        
        if success:
            stats['modified'] += 1
            status = "✅ ADDED"
        elif "Already has" in message:
            stats['skipped'] += 1
            status = "⏭️ SKIP"
        else:
            stats['errors'] += 1
            status = "❌ ERROR"
        
        stats['processed'] += 1
        
        if verbose or not success:
            print(f"{status} {rel_path} - {message}")
        elif success:
            print(f"{status} {rel_path}")
    
    print("-" * 60)
    print(f"\n📊 Summary:")
    print(f"   Total files found: {len(files)}")
    print(f"   ✅ Modified: {stats['modified']}")
    print(f"   ⏭️  Already had comment: {stats['skipped']}")
    print(f"   ❌ Errors: {stats['errors']}")
    
    if dry_run and stats['modified'] > 0:
        print(f"\n💡 This was a DRY RUN. To apply changes, run without --dry-run flag.")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Add filename comments to .py and .js files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s /path/to/project           # Add comments to all .py and .js files
    %(prog)s . --dry-run                # Preview changes without modifying
    %(prog)s ./src --verbose            # Show detailed output
        """
    )
    
    parser.add_argument(
        'directory',
        help='Root directory to scan'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output for all files'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📝 File Header Adder - Add Filename Comments")
    print("=" * 60)
    print(f"Directory: {args.directory}")
    print(f"Mode: {'DRY RUN (preview only)' if args.dry_run else 'LIVE (will modify files)'}")
    print("=" * 60)
    print()
    
    scan_directory(args.directory, dry_run=args.dry_run, verbose=args.verbose)


if __name__ == "__main__":
    main()
