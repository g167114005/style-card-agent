@echo off
chcp 65001 >nul
cd /d "%~dp0"
REM 先在 GitHub 建立空的 repo：g167114005/style-card-agent（不要勾 README）
if not exist .git git init -b main
git add -A
git commit -m "Week 12: update (%DATE% %TIME%)"
git remote remove origin 2>nul
git remote add origin https://github.com/g167114005/style-card-agent.git
git push -u origin main
if errorlevel 1 goto fail
echo DONE.
pause
exit /b 0
:fail
echo FAILED. Please copy the messages above and send them to Claude.
pause
