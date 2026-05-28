# Fix curl error 0xc0000012d
# This error occurs when curl.exe is corrupted or has DLL conflicts

Write-Host "Checking curl installations..." -ForegroundColor Yellow

# Check all curl installations
$curlPaths = @(
    "C:\Windows\System32\curl.exe",
    "C:\Program Files\Git\mingw64\bin\curl.exe",
    "C:\Users\Gomes\scoop\shims\curl.exe",
    "C:\ProgramData\scoop\shims\curl.exe"
)

foreach ($path in $curlPaths) {
    if (Test-Path $path) {
        Write-Host "Found: $path" -ForegroundColor Green
        try {
            $version = & $path --version 2>&1 | Select-Object -First 1
            Write-Host "  Version: $version" -ForegroundColor Cyan
        } catch {
            Write-Host "  ERROR: Could not run this curl!" -ForegroundColor Red
        }
    }
}

# The fix: Create a PowerShell profile that uses the correct curl
Write-Host "`nCreating PowerShell profile to fix curl alias..." -ForegroundColor Yellow

$profileDir = Split-Path $PROFILE -Parent
if (!(Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

# Add to profile to remove the curl alias and use proper curl
$profileContent = @'
# Fix curl - Remove PowerShell alias and use Windows curl
Remove-Item Alias:curl -ErrorAction SilentlyContinue

# Ensure we use Windows curl by default
$env:PATH = "C:\Windows\System32;" + $env:PATH
'@

# Check if profile exists and append or create
if (Test-Path $PROFILE) {
    $existingContent = Get-Content $PROFILE -Raw
    if ($existingContent -notcontains "Fix curl") {
        Add-Content $PROFILE "`n$profileContent"
        Write-Host "Updated PowerShell profile" -ForegroundColor Green
    }
} else {
    Set-Content $PROFILE $profileContent
    Write-Host "Created PowerShell profile" -ForegroundColor Green
}

Write-Host "`nFix applied! Please restart your terminal or run: . `$PROFILE" -ForegroundColor Green
Write-Host "The curl error should now be resolved." -ForegroundColor Green
