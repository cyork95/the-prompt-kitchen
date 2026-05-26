# -*- coding: utf-8 -*-
"""
fix-dropdown-indent.py
Cleans up extra whitespace on <li> items inside .nav-dropdown
that got introduced by the strip-and-reinject approach.
"""
import glob, re

pages = glob.glob('**/*.html', recursive=True)
fixed = 0

for path in pages:
    with open(path, encoding='utf-8') as f:
        html = f.read()
    orig = html

    # Replace any run of >6 spaces before a <li> inside nav-dropdown with exactly 10 spaces
    # We target lines that have more than 10 leading spaces before <li>
    html = re.sub(r'^ {11,}(<li)', r'          \1', html, flags=re.MULTILINE)

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Fixed: {path}')
        fixed += 1

print(f'Done. {fixed} files fixed.')
