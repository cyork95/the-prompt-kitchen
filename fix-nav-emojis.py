# -*- coding: utf-8 -*-
"""
fix-nav-emojis.py
Fixes the desktop nav-links on every page:
  1. Removes stray Spice Rack entries (they belong only in the More dropdown)
  2. Restores missing emojis on Recipe Book, Tasting Menu, Appliance Guide, Test Kitchen
"""
import glob, re

def find_nav_links_end(html, start):
    """Depth-count </ul> to find the closing tag of <ul class="nav-links">."""
    depth = 0
    i = start
    while i < len(html):
        if html[i:i+3] == '<ul' and (i + 3 >= len(html) or html[i+3] in ' \t\n\r>'):
            depth += 1
            i += 3
        elif html[i:i+5] == '</ul>':
            depth -= 1
            if depth == 0:
                return i + 5
            i += 5
        else:
            i += 1
    return -1

pages = glob.glob('**/*.html', recursive=True)
print(f'Processing {len(pages)} pages...')
updated = 0

for path in pages:
    with open(path, encoding='utf-8') as f:
        html = f.read()

    orig = html
    is_root = path.replace('\\', '/') in ('index.html', 'support.html')
    p = '' if is_root else '../'   # path prefix

    nav_start = html.find('<ul class="nav-links"')
    if nav_start == -1:
        print(f'  SKIP (no nav-links): {path}')
        continue

    nav_end = find_nav_links_end(html, nav_start)
    if nav_end == -1:
        print(f'  SKIP (could not close nav-links): {path}')
        continue

    block = html[nav_start:nav_end]

    # 1. Remove ALL Spice Rack <li> entries from nav-links (any text, with or without emoji)
    block = re.sub(
        r'\s*<li><a href="' + re.escape(p) + r'spice-rack/">[^<]*</a></li>',
        '', block
    )

    # 2. Restore missing emojis (only affects entries that don't already have them)
    replacements = [
        (f'href="{p}prompts/">Recipe Book<',      f'href="{p}prompts/">\U0001f4d6 Recipe Book<'),
        (f'href="{p}context/">Kitchen Prep<',      f'href="{p}context/">\U0001f9d1‍\U0001f373 Kitchen Prep<'),
        (f'href="{p}examples/">Tasting Menu<',     f'href="{p}examples/">\U0001f37d️ Tasting Menu<'),
        (f'href="{p}models/">Appliance Guide<',    f'href="{p}models/">\U0001f373 Appliance Guide<'),
        (f'href="{p}model-tester/">Test Kitchen<', f'href="{p}model-tester/">\U0001f9ea Test Kitchen<'),
    ]
    for old, new in replacements:
        block = block.replace(old, new)

    html = html[:nav_start] + block + html[nav_end:]

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Updated: {path}')
        updated += 1
    else:
        print(f'  No change: {path}')

print(f'\nDone. {updated} files updated.')
