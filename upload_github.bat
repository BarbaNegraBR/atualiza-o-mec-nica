@echo off
chcp 65001 >nul
echo ========================================
echo Upload Automático para GitHub
echo ========================================
echo.

python upload_github.py

if errorlevel 1 (
    echo.
    echo Erro ao executar o script!
    pause
)

