@echo off
chcp 65001 >nul
cd /d %~dp0
echo [1/4] 吉祥物設定圖
python tools\gen_card.py --mascot || goto :err
echo [2/4] NIHSS
python tools\gen_card.py html\01_NIHSS.html || goto :err
echo [3/4] Grad-CAM
python tools\gen_card.py html\02_GradCAM.html || goto :err
echo [4/4] SHAP
python tools\gen_card.py html\03_SHAP.html || goto :err
echo 全部完成，請看 output\ 與 logs\
pause
exit /b 0
:err
echo 發生錯誤，請截圖上面訊息
pause
exit /b 1
