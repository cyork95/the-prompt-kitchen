# -*- coding: utf-8 -*-
"""
add-cookbooks-nav.py
Adds Cookbooks to the More dropdown (after Pantry) and footer
Learn section on all existing top-level pages.
Skips any page already under /cookbooks/.
"""
import glob, re

pages = [f for f in glob.glob('**/*.html', recursive=True)
         if 'cookbooks' not in f.replace('\\', '/')]

# Dropdown: insert after Pantry
DROP_OLD_SUB  = '          <li><a href="../pantry/">&#129311; The Pantry</a></li>'
DROP_NEW_SUB  = ('          <li><a href="../pantry/">&#129311; The Pantry</a></li>\n'
                 '          <li><a href="../cookbooks/">&#128218; Cookbooks</a></li>')

DROP_OLD_ROOT = '          <li><a href="pantry/">&#129311; The Pantry</a></li>'
DROP_NEW_ROOT = ('          <li><a href="pantry/">&#129311; The Pantry</a></li>\n'
                 '          <li><a href="cookbooks/">&#128218; Cookbooks</a></li>')

# Footer: insert Cookbooks after Pantry in Learn section
FOOT_OLD_SUB  = '          <li><a href="../pantry/">The Pantry</a></li>'
FOOT_NEW_SUB  = ('          <li><a href="../pantry/">The Pantry</a></li>\n'
                 '          <li><a href="../cookbooks/">Cookbooks</a></li>')

FOOT_OLD_ROOT = '          <li><a href="pantry/">The Pantry</a></li>'
FOOT_NEW_ROOT = ('          <li><a href="pantry/">The Pantry</a></li>\n'
                 '          <li><a href="cookbooks/">Cookbooks</a></li>')

print(f'Processing {len(pages)} pages...')
updated = 0

for path in pages:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'cookbooks' in html:
        print(f'  SKIP (already has cookbooks): {path}')
        continue

    is_root = path.replace('\\', '/') in ('index.html', 'support.html')
    orig = html

    if is_root:
        html = html.replace(DROP_OLD_ROOT, DROP_NEW_ROOT, 1)
        html = html.replace(FOOT_OLD_ROOT, FOOT_NEW_ROOT, 1)
    else:
        html = html.replace(DROP_OLD_SUB, DROP_NEW_SUB, 1)
        html = html.replace(FOOT_OLD_SUB, FOOT_NEW_SUB, 1)

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Updated: {path}')
        updated += 1
    else:
        print(f'  No change: {path}')

print(f'\nDone. {updated} files updated.')
