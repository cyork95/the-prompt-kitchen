# -*- coding: utf-8 -*-
"""
fix-dropdown-nav.py
Ensures every page's More dropdown starts with:
  🌶️ Spice Rack
  🥫 The Pantry
...then the rest of the dropdown items.
Also ensures the footer LEARN section has both links.
Skips pantry/index.html (already has everything).
"""
import glob, re

pages = [f for f in glob.glob('**/*.html', recursive=True)
         if 'pantry' not in f.replace('\\', '/')]

# Spice Rack + Pantry block to inject at TOP of nav-dropdown
SUB_BLOCK = (
    '          <li><a href="../spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n'
    '          <li><a href="../pantry/">&#129311; The Pantry</a></li>\n'
    '          '
)
ROOT_BLOCK = (
    '          <li><a href="spice-rack/">&#127798;&#65039; Spice Rack</a></li>\n'
    '          <li><a href="pantry/">&#129311; The Pantry</a></li>\n'
    '          '
)

# Footer patterns — insert after Recipe Book if missing
FOOT_SUB_OLD  = '          <li><a href="../prompts/">Recipe Book</a></li>'
FOOT_SUB_NEW  = ('          <li><a href="../prompts/">Recipe Book</a></li>\n'
                 '          <li><a href="../pantry/">The Pantry</a></li>')

FOOT_ROOT_OLD = '          <li><a href="prompts/">Recipe Book</a></li>'
FOOT_ROOT_NEW = ('          <li><a href="prompts/">Recipe Book</a></li>\n'
                 '          <li><a href="pantry/">The Pantry</a></li>')

print(f'Processing {len(pages)} pages...')
updated = 0

for path in pages:
    with open(path, encoding='utf-8') as f:
        html = f.read()
    orig = html

    is_root = path.replace('\\', '/') in ('index.html', 'support.html')
    block = ROOT_BLOCK if is_root else SUB_BLOCK

    # ── Dropdown: find opening of <ul class="nav-dropdown"> and inject after it ──
    DROP_OPEN = '        <ul class="nav-dropdown" role="menu">\n'
    idx = html.find(DROP_OPEN)
    if idx != -1:
        insert_at = idx + len(DROP_OPEN)
        # Check what's already right after the opening tag
        existing_after = html[insert_at:insert_at + 60]
        has_spice  = '../spice-rack/' in existing_after or '"spice-rack/"' in existing_after
        has_pantry = '../pantry/'     in existing_after or '"pantry/"'     in existing_after

        if not has_spice or not has_pantry:
            # Remove any stray Spice Rack or Pantry that are already in the dropdown
            # so we can re-insert them cleanly at the top
            spice_pattern_sub  = r'\s*<li><a href="\.\./spice-rack/">[^<]*</a></li>'
            spice_pattern_root = r'\s*<li><a href="spice-rack/">[^<]*</a></li>'
            pantry_pattern_sub  = r'\s*<li><a href="\.\./pantry/">[^<]*</a></li>'
            pantry_pattern_root = r'\s*<li><a href="pantry/">[^<]*</a></li>'

            # Strip existing entries so we don't duplicate
            html = re.sub(spice_pattern_sub,  '', html)
            html = re.sub(spice_pattern_root, '', html)
            html = re.sub(pantry_pattern_sub,  '', html)
            html = re.sub(pantry_pattern_root, '', html)

            # Re-find the dropdown opening after stripping
            idx2 = html.find(DROP_OPEN)
            if idx2 != -1:
                insert_at2 = idx2 + len(DROP_OPEN)
                html = html[:insert_at2] + block + html[insert_at2:]
    else:
        print(f'  WARN (no dropdown found): {path}')

    # ── Footer: add Pantry after Recipe Book if missing ──
    if '../pantry/' not in html and '"pantry/"' not in html:
        if is_root:
            html = html.replace(FOOT_ROOT_OLD, FOOT_ROOT_NEW, 1)
        else:
            html = html.replace(FOOT_SUB_OLD, FOOT_SUB_NEW, 1)
    else:
        # Footer Pantry already there — make sure Spice Rack is also in footer Create section if desired
        pass

    if html != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'  Updated: {path}')
        updated += 1
    else:
        print(f'  No change: {path}')

print(f'\nDone. {updated} files updated.')
