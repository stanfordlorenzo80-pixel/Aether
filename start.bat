@echo off
setlocal EnableDelayedExpansion

:: Set console colors (Cyan on Black)
color 0B

echo ==============================================================================
echo.
echo       .---.  .----. .---. .-..-. .----. .----. 
echo      / {_. \ } ^|__} {_   _}^| ^|^| ^| } ^|__} } ^|__} 
echo      \  '_  / } '__}  ^| ^|  ^| \/ ^| } '__} } '__} 
echo       `---'  `----'  `-'   `----' `----' `----' 
echo.
echo       COGNITIVE ARCHITECTURE ^| DESKTOP ENGINE
echo.
echo ==============================================================================
echo.

:: 1. Python Environment Setup
echo [1/3] Initializing Aether Engine (Python)...
cd engine
if not exist "venv\" (
    echo       [-] Creating isolated virtual environment...
    python -m venv venv
)
echo       [-] Activating and verifying dependencies...
call venv\Scripts\activate.bat
pip install -q fastapi uvicorn anthropic networkx aiohttp
cd ..

:: 2. Node Environment Setup
echo.
echo [2/3] Initializing Desktop UI (Node.js)...
if not exist "node_modules\" (
    echo       [-] Installing React/Tauri dependencies...
    call npm install --silent
)

:: 3. Launch Sequence
echo.
echo [3/3] Igniting Cortex Graph and launching App...
echo       [-] Starting Python Backend on Port 8420...

:: Launch the python server in a minimized background window
start "Aether_Engine_Backend" /MIN cmd /c "cd engine && call venv\Scripts\activate.bat && python -m aether.server"

echo       [-] Launching Tauri Desktop interface...
call npm run tauri dev

:: 4. Cleanup
echo.
echo Shutting down Aether...
:: Find and kill the backend process we started
taskkill /FI "WINDOWTITLE eq Aether_Engine_Backend*" /T /F >nul 2>&1
echo Goodbye!
timeout /t 2 >nul
