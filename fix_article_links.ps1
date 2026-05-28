Get-ChildItem -Path "C:\Openclaw\agents\longevity-journal\articles" -Filter "*.html" | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw
    
    # Fix links to point to parent directory for index.html
    $content = $content -replace 'href="index.html"', 'href="../index.html"'
    $content = $content -replace 'href="index.html#articles"', 'href="../index.html#articles"'
    $content = $content -replace 'href="index.html#about"', 'href="../index.html#about"'
    $content = $content -replace 'href="index.html#newsletter"', 'href="../index.html#newsletter"'
    
    Set-Content $file $content -Encoding UTF8
    Write-Host "Fixed: $file"
}

Write-Host "All articles in /articles/ folder have been updated!"
