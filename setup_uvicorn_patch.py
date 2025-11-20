#!/usr/bin/env python3
"""
Setup script to patch uvicorn for nest_asyncio compatibility with Python 3.12+.

This script applies a compatibility patch to uvicorn's _compat.py file to work
around an issue where nest_asyncio's patched version of asyncio.run() doesn't
support the loop_factory parameter.

Run this script after installing dependencies with: pip install -r requirements.txt
"""

import sys
import os
from pathlib import Path
import re

def find_uvicorn_compat_file():
    """Find the uvicorn _compat.py file in the virtual environment."""
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment
        venv_path = Path(sys.prefix)
    else:
        # Try to find venv in current directory
        venv_path = Path.cwd() / 'venv'
        if not venv_path.exists():
            print("⚠️  Warning: Could not find virtual environment.")
            print("   Please activate your virtual environment first, or run this from the project root.")
            return None
    
    # Try multiple possible paths
    possible_paths = [
        # Windows
        venv_path / 'Lib' / 'site-packages' / 'uvicorn' / '_compat.py',
        # Unix/Mac
        venv_path / 'lib' / f'python{sys.version_info.major}.{sys.version_info.minor}' / 'site-packages' / 'uvicorn' / '_compat.py',
        venv_path / 'lib' / 'site-packages' / 'uvicorn' / '_compat.py',
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return None

def patch_uvicorn_compat(compat_file):
    """Apply the compatibility patch to uvicorn's _compat.py file."""
    print(f"📝 Reading {compat_file}...")
    
    with open(compat_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already patched
    if 'Workaround for nest_asyncio compatibility' in content:
        print("✅ Uvicorn is already patched!")
        return True
    
    original_content = content
    
    # Python 3.13+ replacement
    python_313_replacement = '''if sys.version_info >= (3, 13):
    # Workaround for nest_asyncio compatibility: nest_asyncio patches asyncio.run()
    # and the patched version doesn't support loop_factory parameter.
    # This wrapper accepts loop_factory for compatibility but ignores it when calling
    # the potentially-patched asyncio.run().
    def asyncio_run(
        main: Coroutine[Any, Any, _T],
        *,
        debug: bool = False,
        loop_factory: Callable[[], asyncio.AbstractEventLoop] | None = None,
    ) -> _T:
        # Call asyncio.run() without loop_factory to work with nest_asyncio's patched version
        # Python 3.13+ still supports loop_factory, but nest_asyncio's patch doesn't
        return asyncio.run(main, debug=debug)'''
    
    # Python 3.12+ replacement
    python_312_replacement = '''elif sys.version_info >= (3, 12):
    # For Python 3.12, nest_asyncio may also patch asyncio.run(), so we need
    # a wrapper that handles loop_factory compatibility
    def asyncio_run(
        main: Coroutine[Any, Any, _T],
        *,
        debug: bool = False,
        loop_factory: Callable[[], asyncio.AbstractEventLoop] | None = None,
    ) -> _T:
        # Try to use loop_factory if nest_asyncio hasn't patched asyncio.run()
        try:
            return asyncio.run(main, debug=debug, loop_factory=loop_factory)
        except TypeError:
            # nest_asyncio's patched version doesn't support loop_factory
            return asyncio.run(main, debug=debug)'''
    
    # Try various patterns that might exist in different uvicorn versions
    patterns_to_replace = [
        # Pattern 1: Python 3.13 with simple assignment
        (r'if sys\.version_info >= \(3, 13\):\s*\n\s*asyncio_run = asyncio\.run', 
         python_313_replacement),
        # Pattern 2: Python 3.12 with simple assignment (elif)
        (r'elif sys\.version_info >= \(3, 12\):\s*\n\s*asyncio_run = asyncio\.run', 
         python_312_replacement),
        # Pattern 3: Python 3.12 with simple assignment (if - handles case where 3.13 doesn't exist)
        (r'if sys\.version_info >= \(3, 12\):\s*\n\s*asyncio_run = asyncio\.run', 
         python_312_replacement.replace('elif', 'if')),
    ]
    
    # Try regex replacements
    for pattern, replacement in patterns_to_replace:
        if re.search(pattern, content, re.MULTILINE):
            print(f"🔍 Found pattern to patch: {pattern[:50]}...")
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            break
    
    # If regex didn't work, try simple string replacements
    if content == original_content:
        # Try exact string matches with different whitespace variations
        replacements = [
            ('if sys.version_info >= (3, 13):\n    asyncio_run = asyncio.run', python_313_replacement),
            ('elif sys.version_info >= (3, 12):\n    asyncio_run = asyncio.run', python_312_replacement),
            ('if sys.version_info >= (3, 12):\n    asyncio_run = asyncio.run', python_312_replacement.replace('elif', 'if')),
            # Handle tabs
            ('if sys.version_info >= (3, 13):\n\tasyncio_run = asyncio.run', python_313_replacement.replace('    ', '\t')),
            ('elif sys.version_info >= (3, 12):\n\tasyncio_run = asyncio.run', python_312_replacement.replace('    ', '\t').replace('elif', 'elif')),
        ]
        
        for old, new in replacements:
            if old in content:
                print(f"🔍 Found exact match to patch...")
                content = content.replace(old, new)
                break
    
    # Only write if content changed
    if content != original_content:
        print(f"✏️  Applying patch to {compat_file}...")
        with open(compat_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully patched uvicorn for nest_asyncio compatibility!")
        return True
    else:
        # Diagnostic: show what we found
        print("⚠️  Warning: Could not find the expected section to patch.")
        print()
        print("Let's check what's actually in the file around the Python version checks:")
        print()
        
        lines = content.split('\n')
        found_sections = []
        for i, line in enumerate(lines):
            if 'sys.version_info' in line and ('3, 12' in line or '3, 13' in line):
                # Show context
                start = max(0, i - 1)
                end = min(len(lines), i + 3)
                section = '\n'.join(lines[start:end])
                found_sections.append((i, section))
        
        if found_sections:
            print("Found these sections:")
            for line_num, section in found_sections:
                print(f"  Line {line_num + 1}:")
                for line in section.split('\n'):
                    print(f"    {line}")
                print()
        else:
            print("  No Python 3.12+ version checks found in the file.")
            print("  This might be an older version of uvicorn that doesn't need patching.")
        
        print()
        print("The file structure might be different than expected.")
        print("You may need to manually apply the patch or check the uvicorn version.")
        return False

def main():
    """Main function to run the setup."""
    print("🔧 Setting up uvicorn patch for nest_asyncio compatibility...")
    print()
    
    compat_file = find_uvicorn_compat_file()
    if not compat_file:
        print("❌ Could not find uvicorn _compat.py file.")
        print()
        print("Please ensure:")
        print("1. You have activated your virtual environment")
        print("2. You have installed dependencies: pip install -r requirements.txt")
        print("3. You are running this script from the project root directory")
        sys.exit(1)
    
    if patch_uvicorn_compat(compat_file):
        print()
        print("🎉 Setup complete! You can now run your Gradio application.")
    else:
        print()
        print("❌ Failed to apply patch. Please check the error messages above.")
        print()
        print("Troubleshooting steps:")
        print("1. Check uvicorn version: pip show uvicorn")
        print("2. Try upgrading uvicorn: pip install --upgrade uvicorn")
        print("3. Check Python version: python --version")
        print("4. If you're on Python < 3.12, you may not need this patch")
        sys.exit(1)

if __name__ == '__main__':
    main()
