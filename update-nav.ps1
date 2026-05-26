$base = 'C:\Users\coyof\Documents\Claude\Claude Code\ThePromptKitchen'

$subpages = @(
  'prompts\index.html','examples\index.html','models\index.html','model-tester\index.html',
  'context\index.html','daily\index.html','image-video\index.html','gallery\index.html',
  'fails\index.html','quiz\index.html','challenges\index.html','audio\index.html','video\index.html'
)

foreach ($f in $subpages) {
  $path = Join-Path $base $f
  if (-not (Test-Path $path)) { Write-Host "SKIP: $f"; continue }
  $c = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
  $orig = $c

  # 1. Add Kitchen Prep as 2nd item in desktop nav
  $c = [regex]::Replace($c,
    '(<li><a href="\.\./prompts/">Recipe Book</a></li>)\s*\r?\n(\s*)(<li><a href="\.\./examples/">)',
    '$1' + "`n" + '      <li><a href="../context/">Kitchen Prep</a></li>' + "`n" + '$2$3')

  # 2. Remove Kitchen Prep from dropdown (with leading whitespace/newline)
  $c = [regex]::Replace($c, '\r?\n\s*<li><a href="\.\./context/">🧑‍🍳 Kitchen Prep</a></li>', '')

  # 3. Rename Gallery in dropdown
  $c = $c.Replace('<li><a href="../gallery/">🖼️ Gallery</a></li>', '<li><a href="../gallery/">🍽️ The Table Spread</a></li>')

  # 4. Add Kitchen Prep to mobile nav (position 2, after Recipe Book)
  $c = [regex]::Replace($c,
    '(<li><a href="\.\./prompts/">📖 Recipe Book</a></li>)\s*\r?\n(\s*)(<li><a href="\.\./examples/">)',
    '$1' + "`n" + '    <li><a href="../context/">🧑‍🍳 Kitchen Prep</a></li>' + "`n" + '$2$3')

  # 5. Remove old mobile Kitchen Prep (was after Disasters or other items)
  $c = [regex]::Replace($c, '\r?\n\s*<li><a href="\.\./context/">🧑‍🍳 Kitchen Prep</a></li>', '')

  # 6. Rename Gallery in mobile nav
  $c = $c.Replace('<li><a href="../gallery/">🖼️ Gallery</a></li>', '<li><a href="../gallery/">🍽️ The Table Spread</a></li>')

  # 7. Add favicon before stylesheet
  if ($c -notmatch 'rel="icon"') {
    $c = $c.Replace('  <link rel="stylesheet" href="../css/style.css" />', '  <link rel="icon" href="../favicon.svg" type="image/svg+xml" />' + "`n  " + '<link rel="stylesheet" href="../css/style.css" />')
  }

  if ($c -ne $orig) {
    [System.IO.File]::WriteAllText($path, $c, [System.Text.Encoding]::UTF8)
    Write-Host "Updated: $f"
  } else {
    Write-Host "No change: $f"
  }
}

# Root-level pages
$rootPages = @('index.html','support.html')
foreach ($f in $rootPages) {
  $path = Join-Path $base $f
  if (-not (Test-Path $path)) { Write-Host "SKIP: $f"; continue }
  $c = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
  $orig = $c

  # 1. Add Kitchen Prep as 2nd item in desktop nav
  $c = [regex]::Replace($c,
    '(<li><a href="prompts/">Recipe Book</a></li>)\s*\r?\n(\s*)(<li><a href="examples/">)',
    '$1' + "`n" + '      <li><a href="context/">Kitchen Prep</a></li>' + "`n" + '$2$3')

  # 2. Remove Kitchen Prep from dropdown
  $c = [regex]::Replace($c, '\r?\n\s*<li><a href="context/">🧑‍🍳 Kitchen Prep</a></li>', '')

  # 3. Rename Gallery in dropdown
  $c = $c.Replace('<li><a href="gallery/">🖼️ Gallery</a></li>', '<li><a href="gallery/">🍽️ The Table Spread</a></li>')

  # 4. Mobile nav: add Kitchen Prep at position 2
  $c = [regex]::Replace($c,
    '(<li><a href="prompts/">📖 Recipe Book</a></li>)\s*\r?\n(\s*)(<li><a href="examples/">)',
    '$1' + "`n" + '    <li><a href="context/">🧑‍🍳 Kitchen Prep</a></li>' + "`n" + '$2$3')

  # 5. Remove old mobile Kitchen Prep
  $c = [regex]::Replace($c, '\r?\n\s*<li><a href="context/">🧑‍🍳 Kitchen Prep</a></li>', '')

  # 6. Rename Gallery in mobile nav
  $c = $c.Replace('<li><a href="gallery/">🖼️ Gallery</a></li>', '<li><a href="gallery/">🍽️ The Table Spread</a></li>')

  # 7. Add favicon
  if ($c -notmatch 'rel="icon"') {
    $c = $c.Replace('  <link rel="stylesheet" href="css/style.css" />', '  <link rel="icon" href="favicon.svg" type="image/svg+xml" />' + "`n  " + '<link rel="stylesheet" href="css/style.css" />')
  }

  if ($c -ne $orig) {
    [System.IO.File]::WriteAllText($path, $c, [System.Text.Encoding]::UTF8)
    Write-Host "Updated: $f"
  } else {
    Write-Host "No change: $f"
  }
}

Write-Host "All done!"
