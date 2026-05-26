# -*- coding: utf-8 -*-
"""
add-pantry-nav.py
Adds The Pantry to the More dropdown and footer LEARN section
on all existing pages (not pantry/index.html which already has it).
"""
import os, glob

pages = [f for f in glob.glob('**/*.html', recursive=True)
         if 'pantry' not in f.replace('\\', '/')]

# ── More dropdown: insert Pantry right after Spice Rack ──
# Sub-pages
DROP_OLD = '          <li><a href="../spice-rack/">&#127798;&#65039; Spice Rack</a></li>'
DROP_NEW = '          <li><a href="../spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n          <li><a href="../pantry/">&#129311; The Pantry</a></li>'

# Root pages
DROP_OLD_ROOT = '          <li><a href="spice-rack/">&#127798;&#65039; Spice Rack</a></li>'
DROP_NEW_ROOT = '          <li><a href="spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n          <li><a href="pantry/">&#129311; The Pantry</a></li>'

# ── Footer LEARN section: insert Pantry after Recipe Book ──
FOOT_OLD = '          <li><a href="../prompts/">Recipe Book</a></li>'
FOOT_NEW = '          <li><a href="../prompts/">Recipe Book</a></li>\n          <li><a href="../pantry/">The Pantry</a></li>'

FOOT_OLD_ROOT = '          <li><a href="prompts/">Recipe Book</a></li>'
FOOT_NEW_ROOT = '          <li><a href="prompts/">Recipe Book</a></li>\n          <li><a href="pantry/">The Pantry</a></li>'

print(f'Processing {len(pages)} pages...')
updated = 0

for path in pages:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Skip if already has pantry link
    if 'pantry' in html:
        print(f'  SKIP (already has pantry): {path}')
        continue

    is_root = path.replace('\\', '/') in ('index.html', 'support.html')
    orig = html

    if is_root:
        html = html.replace(DROP_OLD_ROOT, DROP_NEW_ROOT, 1)
        html = html.replace(FOOT_OLD_ROOT, FOOT_NEW_ROOT, 1)
    else:
        html = html.replace(DROP_OLD, DROP_NEW, 1)
        html = html.replace(FOOT_OLD, FOOT_NEW, 1)

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Updated: {path}')
        updated += 1
    else:
        print(f'  No change: {path}')

print(f'\nDone. {updated} files updated.')
