#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  WiFiSlayerTool v3.0 — Auto Installer
#  Developer: waheeb Al-Humaeri
# ═══════════════════════════════════════════════════════════════

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════╗"
echo "║    WiFiSlayerTool v3.0 — Installer       ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${NC}"

# Check root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}[!] Please run as root: sudo bash install.sh${NC}"
    exit 1
fi

echo -e "${YELLOW}[*] Updating package lists...${NC}"
apt update -y

echo -e "${YELLOW}[*] Installing system packages...${NC}"
apt install -y aircrack-ng bettercap iw crunch python3-pip macchanger reaver pixiewps hcxdumptool hcxtools mdk4 hostapd dnsmasq

echo -e "${YELLOW}[*] Installing Python packages...${NC}"
pip3 install -r requirements.txt --break-system-packages

echo ""
echo -e "${GREEN}[✓] Installation complete!${NC}"
echo -e "${CYAN}[*] Run the tool with: sudo python3 main.py${NC}"
echo ""
