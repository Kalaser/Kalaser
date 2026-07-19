#!/bin/bash
# Kalaser - One-Click Setup Script
# Usage: curl -fsSL https://raw.githubusercontent.com/anthropics/kalaser/main/setup.sh | bash

set -e

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                   Kalaser Setup                            ║"
echo "║         Terminal-native AI coding assistant                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Node.js
echo -e "${YELLOW}Checking Node.js...${NC}"
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js is not installed.${NC}"
    echo "Please install Node.js 22+ from https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 22 ]; then
    echo -e "${RED}Node.js version $NODE_VERSION is too old. Version 22+ required.${NC}"
    exit 1
fi
echo -e "${GREEN}Node.js $(node -v) found${NC}"

# Check npm
echo -e "${YELLOW}Checking npm...${NC}"
if ! command -v npm &> /dev/null; then
    echo -e "${RED}npm is not installed.${NC}"
    exit 1
fi
echo -e "${GREEN}npm $(npm -v) found${NC}"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
npm install

# Build
echo -e "${YELLOW}Building project...${NC}"
npm run build

# Link globally
echo -e "${YELLOW}Linking kalaser command globally...${NC}"
npm link

# Create config directory
echo -e "${YELLOW}Creating config directory...${NC}"
mkdir -p ~/.kalaser

# Create default settings if not exists
if [ ! -f ~/.kalaser/settings.json ]; then
    cat > ~/.kalaser/settings.json << 'EOF'
{
  "models": {
    "default": {
      "protocol": "openai-chat",
      "model": "gpt-4o",
      "baseURL": "https://api.openai.com/v1",
      "apiKey": "${OPENAI_API_KEY}"
    }
  },
  "defaultModel": "default"
}
EOF
    echo -e "${YELLOW}Created default config at ~/.kalaser/settings.json${NC}"
    echo -e "${YELLOW}Please edit it with your API key and model settings.${NC}"
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                   Setup Complete!                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Run 'kalaser' to start using Kalaser."
echo ""
echo "Quick start:"
echo "  kalaser                    # Interactive mode"
echo "  echo 'hello' | kalaser --print  # Headless mode"
echo "  kalaser --help             # Show all options"
echo ""
echo "Configuration: ~/.kalaser/settings.json"
echo ""
