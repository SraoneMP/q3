@echo off
echo ================================================
echo   GitHub Repository Setup and Push
echo ================================================
echo.

echo Step 1: Create GitHub Repository
echo ---------------------------------
echo Please do ONE of the following:
echo.
echo Option A: Using GitHub Web UI (Easiest)
echo   1. Go to https://github.com/new
echo   2. Repository name: TDS-GAA3
echo   3. Make it PUBLIC
echo   4. Do NOT initialize with README
echo   5. Click "Create repository"
echo.
echo Option B: Using GitHub CLI (if installed)
echo   gh repo create TDS-GAA3 --public --source=. --remote=origin
echo.
pause
echo.

echo Step 2: Add GitHub Remote
echo ---------------------------------
set /p GITHUB_USERNAME="Enter your GitHub username: "
echo.

echo Adding remote origin...
git remote add origin https://github.com/%GITHUB_USERNAME%/TDS-GAA3.git

echo Renaming branch to main...
git branch -M main

echo.
echo Step 3: Push to GitHub
echo ---------------------------------
echo Now pushing your code to GitHub...
echo You may be prompted for credentials.
echo.

git push -u origin main

echo.
echo ================================================
echo   ✅ Repository Pushed Successfully!
echo ================================================
echo.
echo Your repository is now live at:
echo https://github.com/%GITHUB_USERNAME%/TDS-GAA3
echo.
echo Next Steps:
echo 1. Go to: https://github.com/%GITHUB_USERNAME%/TDS-GAA3/actions
echo 2. Click on "Daily Automated Commit - DevSync"
echo 3. Click "Run workflow" button
echo 4. Wait for it to complete (~30 seconds)
echo 5. Verify a new commit was created
echo.
echo Submit this URL in your assignment:
echo https://github.com/%GITHUB_USERNAME%/TDS-GAA3
echo.
pause
