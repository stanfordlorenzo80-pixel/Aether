#!/bin/bash

# ANSI color codes
CYAN='\033[0;36m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'

echo -e "${CYAN}==============================================================================${NC}"
echo -e ""
echo -e "${CYAN}      .---.  .----. .---. .-..-. .----. .----. ${NC}"
echo -e "${CYAN}     / {_. \ } |__} {_   _}| || | } |__} } |__} ${NC}"
echo -e "${CYAN}     \  '_  / } '__}  | |  | \/ | } '__} } '__} ${NC}"
echo -e "${CYAN}      \`---'  \`----'  \`-'   \`----' \`----' \`----' ${NC}"
echo -e ""
echo -e "${CYAN}      COGNITIVE ARCHITECTURE | DESKTOP ENGINE${NC}"
echo -e ""
echo -e "${CYAN}==============================================================================${NC}"
echo ""

# 1. Python Environment
echo -e "${GREEN}[1/3] Initializing Aether Engine (Python)...${NC}"
cd engine
if [ ! -d "venv" ]; then
    echo "      [-] Creating isolated virtual environment..."
    python3 -m venv venv
fi
echo "      [-] Activating and verifying dependencies..."
source venv/bin/activate
pip install -q fastapi uvicorn anthropic networkx aiohttp
cd ..

# 2. Node Environment
echo ""
echo -e "${GREEN}[2/3] Initializing Desktop UI (Node.js)...${NC}"
if [ ! -d "node_modules" ]; then
    echo "      [-] Installing React/Tauri dependencies..."
    npm install --silent
fi

# 3. Launch
echo ""
echo -e "${GREEN}[3/3] Igniting Cortex Graph and launching App...${NC}"
echo "      [-] Starting Python Backend on Port 8420..."

# Start python server in background
(cd engine && source venv/bin/activate && python -m aether.server) &
BACKEND_PID=$!

echo "      [-] Launching Tauri Desktop interface..."
npm run tauri dev

# 4. Cleanup
echo ""
echo "Shutting down Aether..."
kill $BACKEND_PID
wait $BACKEND_PID 2>/dev/null
echo "Goodbye!"
