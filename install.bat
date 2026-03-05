@echo off
REM Utwórz środowisko wirtualne i zainstaluj wymagane biblioteki Pythona

REM sprawdź, czy polecenie python działa
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python nie jest dostępny w zmiennej PATH. Zainstaluj Pythona 3.11+ i spróbuj ponownie.
    exit /b 1
)

REM utwórz katalog venv, jeśli nie istnieje
if not exist venv (
    python -m venv venv
)

REM aktywuj środowisko
call venv\Scripts\activate

echo Aktualizuję pip...
python -m pip install --upgrade pip

echo Instaluję zależności z requirements.txt...
pip install -r requirements.txt

echo Wszystkie biblioteki zainstalowane. Aby aktywować środowisko użyj:
echo    call venv\Scripts\activate

pause