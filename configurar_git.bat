@echo off
chcp 65001 >nul
echo ========================================
echo Configuração do Git para Sincronização
echo ========================================
echo.

cd /d "%~dp0"

echo Verificando se já é um repositório Git...
git status >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Repositório Git já inicializado!
    echo.
    echo Verificando remote...
    git remote get-url origin >nul 2>&1
    if %errorlevel% == 0 (
        echo ✅ Remote já configurado!
        git remote get-url origin
    ) else (
        echo Configurando remote...
        git remote add origin https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git
        echo ✅ Remote configurado!
    )
) else (
    echo Inicializando repositório Git...
    git init
    echo ✅ Repositório inicializado!
    echo.
    echo Configurando remote...
    git remote add origin https://github.com/BarbaNegraBR/atualiza-o-mec-nica.git
    echo ✅ Remote configurado!
    echo.
    echo Criando .gitignore...
    (
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo *$py.class
        echo *.so
        echo .Python
        echo build/
        echo develop-eggs/
        echo dist/
        echo downloads/
        echo eggs/
        echo .eggs/
        echo lib/
        echo lib64/
        echo parts/
        echo sdist/
        echo var/
        echo wheels/
        echo *.egg-info/
        echo .installed.cfg
        echo *.egg
        echo.
        echo # PyInstaller
        echo *.manifest
        echo *.spec
        echo.
        echo # IDEs
        echo .vscode/
        echo .idea/
        echo *.swp
        echo *.swo
        echo.
        echo # OS
        echo .DS_Store
        echo Thumbs.db
        echo.
        echo # Temporários
        echo *.tmp
        echo *.log
        echo atualizar.bat
    ) > .gitignore
    echo ✅ .gitignore criado!
)

echo.
echo ========================================
echo Configuração concluída!
echo ========================================
echo.
echo Próximos passos:
echo.
echo 1. Abra o GitHub Desktop OU
echo 2. Use a extensão Git do Cursor/VS Code (Ctrl+Shift+G)
echo.
echo Para fazer o primeiro commit:
echo   git add .
echo   git commit -m "Configuração inicial"
echo   git branch -M main
echo   git push -u origin main
echo.
pause

