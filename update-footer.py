#!/usr/bin/env python3
"""
update-footer.py
- Fix GitHub links: https://github.com/ → https://github.com/cyork95/the-prompt-kitchen
- Add "Developed with ♥ by York.Dev" credit to footer-bottom on every page
"""

import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))

GITHUB_OLD = 'href="https://github.com/"'
GITHUB_NEW = 'href="https://github.com/cyork95/the-prompt-kitchen"'

# Also fix the challenges workflow deep-link
WORKFLOW_OLD = 'href="https://github.com/" rel="noopener" target="_blank">.github/workflows/new-challenge.yml'
WORKFLOW_NEW = 'href="https://github.com/cyork95/the-prompt-kitchen/blob/main/.github/workflows/new-challenge.yml" rel="noopener" target="_blank">.github/workflows/new-challenge.yml'

COPYRIGHT_OLD = '<span>© 2026 The Prompt Kitchen · <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener" style="color:inherit">CC BY 4.0</a></span>'
COPYRIGHT_NEW = '<span>© 2026 The Prompt Kitchen · <a href="https://creativecommons.org/licenses/by/4.0/" rel="noopener" style="color:inherit">CC BY 4.0</a></span>\n      <span>Developed with ♥ by <a href="https://yorkdevelops.com" rel="noopener" style="color:inherit">York.Dev</a></span>'

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # Fix GitHub links
    content = content.replace(GITHUB_OLD, GITHUB_NEW)

    # Fix challenges workflow link
    content = content.replace(WORKFLOW_OLD, WORKFLOW_NEW)

    # Add York.Dev credit (only if not already present)
    if 'yorkdevelops.com' not in content and COPYRIGHT_OLD in content:
        content = content.replace(COPYRIGHT_OLD, COPYRIGHT_NEW)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated: {os.path.relpath(path, ROOT)}")
    else:
        print(f"  Skipped: {os.path.relpath(path, ROOT)}")

def main():
    html_files = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # skip node_modules, .git, etc.
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in ('node_modules',)]
        for fn in filenames:
            if fn.endswith('.html'):
                html_files.append(os.path.join(dirpath, fn))

    html_files.sort()
    print(f"Processing {len(html_files)} HTML files...\n")
    for path in html_files:
        process_file(path)
    print("\nDone.")

if __name__ == '__main__':
    main()
