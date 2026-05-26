# -*- coding: utf-8 -*-
"""
update-spicerack-nav.py
Adds Spice Rack to the More dropdown nav and footer LEARN section
on all existing pages (not spice-rack/index.html which already has it).
"""
import os, glob

pages = [f for f in glob.glob('**/*.html', recursive=True)
         if 'spice-rack' not in f.replace('\\','/')]

# ── Nav: insert Spice Rack as first item in More dropdown ──
NAV_OLD = '''          <li><a href="../audio/">'''
NAV_NEW = '''          <li><a href="../spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n          <li><a href="../audio/">'''

# For index.html (root), paths are different
NAV_OLD_ROOT = '          <li><a href="audio/">'
NAV_NEW_ROOT = '          <li><a href="spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n          <li><a href="audio/">'

# Mobile nav: insert after Recipe Book
MOB_OLD = '    <li><a href="../prompts/">&#128218; Recipe Book</a></li>'
MOB_NEW = '    <li><a href="../prompts/">&#128218; Recipe Book</a></li>\n    <li><a href="../spice-rack/">&#127798;&#65039; Spice Rack</a></li>'

MOB_OLD_ROOT = '    <li><a href="prompts/">'
MOB_NEW_ROOT = '    <li><a href="spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n    <li><a href="prompts/">'

# Footer LEARN section: insert Spice Rack after Recipe Book link
FOOT_OLD = '''<li><a href="../prompts/">Recipe Book</a></li>'''
FOOT_NEW = '''<li><a href="../prompts/">Recipe Book</a></li>\n        <li><a href="../spice-rack/">Spice Rack</a></li>'''

FOOT_OLD_ROOT = '<li><a href="prompts/">Recipe Book</a></li>'
FOOT_NEW_ROOT = '<li><a href="prompts/">Recipe Book</a></li>\n          <li><a href="spice-rack/">Spice Rack</a></li>'

print(f'Processing {len(pages)} pages...')
updated = 0
for path in pages:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    # Skip if already has spice-rack
    if 'spice-rack' in html:
        print(f'  SKIP (already has spice-rack): {path}')
        continue

    is_root = path == 'index.html' or path == 'support.html'

    orig = html

    if is_root:
        html = html.replace(NAV_OLD_ROOT, NAV_NEW_ROOT, 1)
        html = html.replace(MOB_OLD_ROOT, MOB_NEW_ROOT, 1)
        html = html.replace(FOOT_OLD_ROOT, FOOT_NEW_ROOT, 1)
    else:
        html = html.replace(NAV_OLD, NAV_NEW, 1)
        html = html.replace(MOB_OLD, MOB_NEW, 1)
        html = html.replace(FOOT_OLD, FOOT_NEW, 1)

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Updated: {path}')
        updated += 1
    else:
        print(f'  No change: {path}')

print(f'\nDone. {updated} files updated.')
