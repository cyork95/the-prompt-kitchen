#!/usr/bin/env python3
"""Update nav across all HTML pages:
  - Add Kitchen Prep as 2nd item in desktop nav
  - Remove Kitchen Prep from More dropdown
  - Rename Gallery -> The Table Spread
  - Add favicon link to all heads
"""
import os, re

BASE = r'C:\Users\coyof\Documents\Claude\Claude Code\ThePromptKitchen'

SUBPAGES = [
    'prompts/index.html','examples/index.html','models/index.html',
    'model-tester/index.html','context/index.html','daily/index.html',
    'image-video/index.html','gallery/index.html','fails/index.html',
    'quiz/index.html','challenges/index.html','audio/index.html','video/index.html'
]
ROOT_PAGES = ['index.html','support.html']


def process(path, prefix):
    """prefix is '../' for subpages, '' for root pages."""
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        print(f'SKIP (missing): {path}')
        return
    with open(full, encoding='utf-8') as f:
        c = f.read()
    orig = c

    p = prefix  # '../' or ''

    # 1. Insert Kitchen Prep between Recipe Book and Tasting Menu in desktop nav
    old = f'<li><a href="{p}prompts/">Recipe Book</a></li>'
    after = f'<li><a href="{p}examples/">Tasting Menu</a></li>'
    insert = f'<li><a href="{p}context/">Kitchen Prep</a></li>'
    # Only add if not already there
    if insert not in c:
        # Find the Recipe Book entry and insert Kitchen Prep after it, before Tasting Menu
        pattern = re.compile(
            r'(<li><a href="' + re.escape(p) + r'prompts/">Recipe Book</a></li>)([ \t]*\r?\n)([ \t]*)(<li><a href="' + re.escape(p) + r'examples/">Tasting Menu</a></li>)'
        )
        c = pattern.sub(
            r'\1\2\3' + insert + r'\2\3\4',
            c
        )

    # 2. Remove Kitchen Prep from dropdown (the full <li> line with emoji)
    c = re.sub(
        r'\n[ \t]*<li><a href="' + re.escape(p) + r'context/">[^<]*Kitchen Prep</a></li>',
        '',
        c
    )

    # 3. Rename Gallery in dropdown and everywhere in nav
    c = c.replace(
        f'<li><a href="{p}gallery/">\U0001f5bc️ Gallery</a></li>',
        f'<li><a href="{p}gallery/">\U0001f37d️ The Table Spread</a></li>'
    )
    # Also handle without variation selector
    c = c.replace(
        f'<li><a href="{p}gallery/">\U0001f5bc Gallery</a></li>',
        f'<li><a href="{p}gallery/">\U0001f37d️ The Table Spread</a></li>'
    )

    # 4. Mobile nav: Insert Kitchen Prep after Recipe Book (position 2)
    mob_insert = f'    <li><a href="{p}context/">\U0001f9d1‍\U0001f373 Kitchen Prep</a></li>'
    if mob_insert not in c:
        mob_pattern = re.compile(
            r'(<li><a href="' + re.escape(p) + r'prompts/">[^<]*Recipe Book</a></li>)([ \t]*\r?\n)([ \t]*)(<li><a href="' + re.escape(p) + r'examples/">)'
        )
        c = mob_pattern.sub(
            r'\1\2    ' + f'<li><a href="{p}context/">\U0001f9d1‍\U0001f373 Kitchen Prep</a></li>' + r'\2\3\4',
            c
        )

    # 5. Remove old mobile Kitchen Prep (it's now duplicated from step 4 removing dropdown)
    # (The dropdown removal in step 2 already handles the emoji variant;
    #  the mobile list has a slightly different emoji combo)
    # Remove any remaining context/ li that isn't the one we just inserted at position 2
    # Count occurrences - if more than 1, remove extras
    lines = c.split('\n')
    ctx_lines = [(i, l) for i, l in enumerate(lines)
                 if f'href="{p}context/"' in l and 'Kitchen Prep' in l]
    if len(ctx_lines) > 1:
        # Keep only the first one (position 2), remove all others
        for idx, (lineno, _) in enumerate(ctx_lines):
            if idx > 0:  # remove all but first
                lines[lineno] = None
        c = '\n'.join(l for l in lines if l is not None)

    # 6. Add favicon to <head> (only if not already present)
    favicon_sub = f'../favicon.svg' if p == '../' else 'favicon.svg'
    if 'rel="icon"' not in c:
        stylesheet_pattern = f'  <link rel="stylesheet" href="{p}css/style.css"'
        favicon_tag = f'  <link rel="icon" href="{favicon_sub}" type="image/svg+xml" />\n'
        c = c.replace(stylesheet_pattern, favicon_tag + stylesheet_pattern, 1)

    if c != orig:
        with open(full, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f'Updated: {path}')
    else:
        print(f'No change: {path}')


for p in SUBPAGES:
    process(p, '../')
for p in ROOT_PAGES:
    process(p, '')

print('Done!')
