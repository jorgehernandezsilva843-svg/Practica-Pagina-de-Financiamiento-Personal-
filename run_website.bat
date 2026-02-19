@echo off
:: ═══════════════════════════════════════════════════════
::  run_website.bat — Lanzador de FinanceOS
::  Doble clic para instalar dependencias y abrir el server
:: ═══════════════════════════════════════════════════════

title FinanceOS — Servidor Web
color 0A

echo.
echo  ██████╗ ██╗███╗   ██╗ █████╗ ███╗   ██╗ ██████╗███████ ╗ ██████╗ ███████╗
echo  ██╔══  ╗██║████╗  ██║██╔══██╗████╗  ██║██╔════╝██╔════╝ ██╔═══██╗██╔════╝
echo  ██████ ║██║██╔██╗ ██║███████║██╔██╗ ██║██║     █████╗   ██║   ██║███████╗
echo  ██╔══  ╗██║██║╚██╗██║██╔══██║██║╚██╗██║██║     ██╔══╝   ██║   ██║╚════██║
echo  ██║     ██║██║ ╚████║██║  ██║██║ ╚████║╚██████╗███████╗╚ ██████╔╝███████║
echo  ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝╚══════╝ ╚═════╝ ╚══════╝
echo.
echo  Gestion Financiera Personal — Sistema de Metas Conectado
echo  ──────────────────────────────────────────────────────────
echo.

:: ── Verificar Python ──────────────────────────────────
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python no esta instalado o no esta en el PATH.
    echo  Descargalo desde: https://www.python.org/downloads/
    echo  Asegurate de marcar "Add Python to PATH" al instalar.
    echo.
    pause
    exit /b 1
)

:: ── Verificar / instalar Flask ────────────────────────
echo  [1/3] Verificando dependencias...
py -c "import flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo  [2/3] Flask no encontrado. Instalando...
    py -m pip install flask
    if %errorlevel% neq 0 (
        echo  [ERROR] No se pudo instalar Flask. Revisa tu conexion a internet.
        pause
        exit /b 1
    )
    echo  Flask instalado correctamente.
) else (
    echo  [2/3] Flask ya esta instalado. OK.
)

:: ── Moverse al directorio del script ─────────────────
cd /d "%~dp0"

:: ── Iniciar servidor ──────────────────────────────────
echo  [3/3] Iniciando servidor Flask...
echo.
echo  ┌─────────────────────────────────────────────┐
echo  │  Servidor corriendo en:                     │
echo  │  http://127.0.0.1:5000                      │
echo  │                                             │
echo  │  Abre esa URL en tu navegador.              │
echo  │  Presiona Ctrl+C en esta ventana para       │
echo  │  detener el servidor cuando termines.       │
echo  └─────────────────────────────────────────────┘
echo.

:: Abrir navegador automaticamente (esperar 1.5 seg a que Flask arranque)
start "" timeout /t 2 >nul
start "" "http://127.0.0.1:5000"

:: Lanzar Flask
py app.py

echo.
echo  Servidor detenido.
pause
