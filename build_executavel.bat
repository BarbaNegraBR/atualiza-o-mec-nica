@echo off
echo Instalando dependencias...
pip install -r requirements.txt
REM Garante Pillow para converter PNG->ICO
pip install pillow

echo.
echo Preparando icone...
IF EXIST "Pngtre.png" IF NOT EXIST "Pngtre.ico" (
  python -c "from PIL import Image; im=Image.open('Pngtre.png'); im.save('Pngtre.ico', sizes=[(256,256),(128,128),(64,64),(48,48),(32,32),(16,16)])"
)


echo Criando executavel...
pyinstaller --onefile --windowed --icon "Pngtre.ico" --name "Calculadora_Death_Row_Garage" calculadora_reparos_gui.py

echo.
echo Executavel criado em: dist\Calculadora_Death_Row_Garage.exe
echo.
pause
