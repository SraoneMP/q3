# GitHub Repository Creation and Push Script
# ============================================

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  GitHub Actions Implementation - Push to GitHub" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Display what we have
Write-Host "âœ… Local Repository Status:" -ForegroundColor Green
Write-Host ""
git log --oneline -3
Write-Host ""

# Check if repo exists
Write-Host "ðŸ" Checking if GitHub repository exists..." -ForegroundColor Yellow
Write-Host ""

$response = try {
    Invoke-WebRequest -Uri "https://github.com/SraoneMP/TDS-GAA3" -Method Head -ErrorAction SilentlyContinue
    $true
} catch {
    $false
}

if (-not $response) {
    Write-Host "âš ï¸  Repository not found on GitHub" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "OPTION 1: Create via Web (Recommended)" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "1. Open: https://github.com/new" -ForegroundColor White
    Write-Host "2. Repository name: TDS-GAA3" -ForegroundColor White
    Write-Host "3. Visibility: Public" -ForegroundColor White
    Write-Host "4. Do NOT initialize with README" -ForegroundColor White
    Write-Host "5. Click 'Create repository'" -ForegroundColor White
    Write-Host ""
    
    Write-Host "OPTION 2: Create via CLI" -ForegroundColor Cyan
    Write-Host "=========================" -ForegroundColor Cyan
    Write-Host "gh repo create TDS-GAA3 --public --source=. --remote=origin" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Press any key after creating the repository..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    Write-Host ""
}

# Push to GitHub
Write-Host "ðŸš€ Pushing to GitHub..." -ForegroundColor Green
Write-Host ""

try {
    git push -u origin main 2>&1 | Write-Host
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "================================================" -ForegroundColor Green
        Write-Host "  âœ… Successfully Pushed to GitHub!" -ForegroundColor Green
        Write-Host "================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your repository:" -ForegroundColor Cyan
        Write-Host "https://github.com/SraoneMP/TDS-GAA3" -ForegroundColor White
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Go to: https://github.com/SraoneMP/TDS-GAA3/actions" -ForegroundColor White
        Write-Host "2. Click 'Daily Automated Commit - DevSync'" -ForegroundColor White
        Write-Host "3. Click 'Run workflow' button" -ForegroundColor White
        Write-Host "4. Wait ~30 seconds for completion" -ForegroundColor White
        Write-Host "5. Verify green checkmark âœ…" -ForegroundColor White
        Write-Host ""
        Write-Host "Submit this URL:" -ForegroundColor Yellow
        Write-Host "https://github.com/SraoneMP/TDS-GAA3" -ForegroundColor Green
        Write-Host ""
    } else {
        throw "Push failed"
    }
} catch {
    Write-Host ""
    Write-Host "âš ï¸  Push failed. Common solutions:" -ForegroundColor Red
    Write-Host ""
    Write-Host "1. Repository doesn't exist - Create it first" -ForegroundColor Yellow
    Write-Host "2. Authentication failed - Use Personal Access Token" -ForegroundColor Yellow
    Write-Host "   Generate at: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "3. Permission denied - Check repository permissions" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
