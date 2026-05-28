# Fix all articles to have proper navigation matching the CSS

$articlesFolder = "C:\Openclaw\agents\longevity-journal\articles"
$rootFolder = "C:\Openclaw\agents\longevity-journal"

# Navigation HTML for articles in the ROOT folder (new articles)
$rootNavTemplate = @'
    <header class="masthead">
        <div class="container">
            <div class="masthead-inner">
                <div class="masthead-left">
                    <span class="masthead-date">May 29, 2026</span>
                    <span class="masthead-issue">Issue No. 001</span>
                </div>
                <div class="masthead-center">
                    <div class="masthead-logo">TLJ</div>
                    <h1 class="masthead-title">The Longevity Journal</h1>
                    <div class="masthead-tagline">AI-Curated Research &middot; Human-Tested</div>
                </div>
                <div class="masthead-right">
                    <a href="index.html#newsletter" class="btn-subscribe">Subscribe Free &rarr;</a>
                </div>
            </div>
        </div>
    </header>

    <nav class="site-nav">
        <div class="container">
            <div class="site-nav-inner">
                <a href="index.html">Home</a>
                <a href="index.html#articles">Articles</a>
                <a href="index.html#about">About</a>
                <a href="index.html#newsletter">Subscribe</a>
            </div>
        </div>
    </nav>

    <div class="article-page container">
        <a href="index.html" class="back-link">&larr; Back to Latest Issue</a>
'@

# Navigation HTML for articles in the ARTICLES folder (old articles)
$articleNavTemplate = @'
    <header class="masthead">
        <div class="container">
            <div class="masthead-inner">
                <div class="masthead-left">
                    <span class="masthead-date">May 13, 2026</span>
                    <span class="masthead-issue">Issue No. 001</span>
                </div>
                <div class="masthead-center">
                    <div class="masthead-logo">TLJ</div>
                    <h1 class="masthead-title">The Longevity Journal</h1>
                    <div class="masthead-tagline">AI-Curated Research &middot; Human-Tested</div>
                </div>
                <div class="masthead-right">
                    <a href="../index.html#newsletter" class="btn-subscribe">Subscribe Free &rarr;</a>
                </div>
            </div>
        </div>
    </header>

    <nav class="site-nav">
        <div class="container">
            <div class="site-nav-inner">
                <a href="../index.html">Home</a>
                <a href="../index.html#articles">Articles</a>
                <a href="../index.html#about">About</a>
                <a href="../index.html#newsletter">Subscribe</a>
            </div>
        </div>
    </nav>

    <div class="article-page container">
        <a href="../index.html" class="back-link">&larr; Back to Latest Issue</a>
'@

Write-Host "Fixing old articles in articles/ folder..." -ForegroundColor Yellow
Get-ChildItem -Path $articlesFolder -Filter "*.html" | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw
    
    # Check if it already has proper masthead
    if ($content -match 'class="masthead"') {
        Write-Host "  $($_.Name) already has masthead" -ForegroundColor Gray
        return
    }
    
    # Remove old header/nav if present
    $content = $content -replace '<header class="header"[\s\S]*?</header>', ''
    $content = $content -replace '<nav class="nav"[\s\S]*?</nav>', ''
    
    # Remove old back-link if present (we'll add it in the template)
    $content = $content -replace '<a href="\.\./index\.html" class="back-link"[^>]*>.*?</a>', ''
    $content = $content -replace '<a href="index\.html" class="back-link"[^>]*>.*?</a>', ''
    
    # Find the body tag and insert navigation after it
    $content = $content -replace '(<body[^>]*>)', "`$1`n`n    <!-- Noise Texture Overlay -->`n    <div class=""noise-overlay""></div>`n`n$articleNavTemplate"
    
    Set-Content $file $content -Encoding UTF8
    Write-Host "  Fixed $($_.Name)" -ForegroundColor Green
}

Write-Host "`nFixing new articles in root folder..." -ForegroundColor Yellow
Get-ChildItem -Path $rootFolder -Filter "*20260529.html" | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw
    
    # Check if it already has proper masthead
    if ($content -match 'class="masthead"') {
        Write-Host "  $($_.Name) already has masthead" -ForegroundColor Gray
        return
    }
    
    # Find the body tag and insert navigation after it
    $content = $content -replace '(<body[^>]*>)', "`$1`n`n    <!-- Noise Texture Overlay -->`n    <div class=""noise-overlay""></div>`n`n$rootNavTemplate"
    
    Set-Content $file $content -Encoding UTF8
    Write-Host "  Fixed $($_.Name)" -ForegroundColor Green
}

Write-Host "`nDone!" -ForegroundColor Green
