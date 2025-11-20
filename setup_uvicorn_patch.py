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
    
    # Patch for Python 3.13+
    python_313_pattern = r'(if sys\.version_info >= \(3, 13\):.*?)(?=elif sys\.version_info >= \(3, 12\):|$)'
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
        return asyncio.run(main, debug=debug)
'''
    
    # Try regex replacement first
    if re.search(python_313_pattern, content, re.DOTALL):
        content = re.sub(python_313_pattern, python_313_replacement, content, flags=re.DOTALL)
    
    # If that didn't work, try simple string replacement
    if 'asyncio_run = asyncio.run' in content and 'elif sys.version_info >= (3, 12):' in content:
        # Replace the simple assignment for Python 3.12
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
            return asyncio.run(main, debug=debug)
'''
        content = content.replace(
            'elif sys.version_info >= (3, 12):\n    asyncio_run = asyncio.run',
            python_312_replacement
        )
    
    # Manual replacement for Python 3.13+ if regex didn't work
    if 'if sys.version_info >= (3, 13):' in content and 'Workaround for nest_asyncio' not in content:
        # Find and replace the Python 3.13 section manually
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            if lines[i].strip() == 'if sys.version_info >= (3, 13):':
                # Add our replacement
                new_lines.extend(python_313_replacement.strip().split('\n'))
                # Skip the old section until we hit the next elif/else
                i += 1
                indent_level = len(lines[i]) - len(lines[i].lstrip()) if i < len(lines) else 0
                while i < len(lines):
                    line_stripped = lines[i].strip()
                    if not line_stripped or line_stripped.startswith('#'):
                        i += 1
                        continue
                    if line_stripped.startswith('elif ') or line_stripped.startswith('else:'):
                        break
                    if line_stripped.startswith('def ') or line_stripped.startswith('return '):
                        # Skip function definition lines
                        i += 1
                        while i < len(lines) and (not lines[i].strip() or 
                                                  lines[i].startswith(' ') or 
                                                  lines[i].startswith('\t')):
                            i += 1
                        continue
                    if len(lines[i]) - len(lines[i].lstrip()) <= indent_level and line_stripped:
                        break
                    i += 1
                continue
            new_lines.append(lines[i])
            i += 1
        content = '\n'.join(new_lines)
    
    # Only write if content changed
    if content != original_content:
        print(f"✏️  Applying patch to {compat_file}...")
        with open(compat_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Successfully patched uvicorn for nest_asyncio compatibility!")
        return True
    else:
        print("⚠️  Warning: Could not find the section to patch.")
        print("   The uvicorn version may have a different structure.")
        print("   You may need to manually apply the patch.")
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
        sys.exit(1)

if __name__ == '__main__':
    main()
