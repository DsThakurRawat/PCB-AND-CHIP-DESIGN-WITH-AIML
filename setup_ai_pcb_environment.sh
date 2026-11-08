#!/usr/bin/env bash
# ==============================================================================
#  AI-Assisted PCB Design Environment - Turnkey Bootstrap Installer
# ==============================================================================
#  This script installs and configures the exact AI PCB design toolchain:
#   1. KiCad 9 EDA Suite & Official Symbol/Footprint/3D Libraries
#   2. KiCad Python C++ Bindings (pcbnew)
#   3. KiCad Model Context Protocol (MCP) Servers (mcp-server-kicad, kicad-mcp-pro)
#   4. Programmatic EDA synthesis frameworks (kicad-sch-api, atopile, skidl)
#   5. Manufacturing & inspection utilities (InteractiveHtmlBom, FreeRouting)
#   6. Ready-to-use AI Agent Client Configurations (Antigravity, Claude, Cursor, VS Code)
# ==============================================================================

set -euo pipefail

# ANSI Color codes for clean output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

INSTALL_DIR="${AI_PCB_DIR:-$HOME/.ai-pcb-env}"
BIN_DIR="$HOME/.local/bin"
TOOLS_DIR="$INSTALL_DIR/tools"
CONFIG_DIR="$INSTALL_DIR/configs"

echo -e "${PURPLE}${BOLD}"
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          AI PCB DESIGN TOOLCHAIN - BOOTSTRAP INSTALLER             ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}[*] Target Environment Directory: ${BOLD}${INSTALL_DIR}${NC}"
echo -e "${CYAN}[*] Target Executable Directory:  ${BOLD}${BIN_DIR}${NC}"
echo ""

# ------------------------------------------------------------------------------
# 1. OS & Distribution Detection
# ------------------------------------------------------------------------------
detect_os() {
    OS_TYPE="$(uname -s)"
    case "$OS_TYPE" in
        Linux*)
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                DISTRO=$ID
                DISTRO_LIKE=${ID_LIKE:-""}
            else
                DISTRO="unknown"
                DISTRO_LIKE=""
            fi
            ;;
        Darwin*)
            DISTRO="macos"
            DISTRO_LIKE=""
            ;;
        *)
            DISTRO="unsupported"
            DISTRO_LIKE=""
            ;;
    esac
}

detect_os
echo -e "${BLUE}[+] Detected Operating System: ${BOLD}${OS_TYPE} (${DISTRO})${NC}"

# Helper for elevated commands
SUDO=""
if [ "$(id -u)" -ne 0 ]; then
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        echo -e "${RED}[!] 'sudo' is required for system package installations. Please run as root or install sudo.${NC}"
        exit 1
    fi
fi

# ------------------------------------------------------------------------------
# 2. Install KiCad 9 & System Packages
# ------------------------------------------------------------------------------
install_system_dependencies() {
    echo -e "\n${YELLOW}=== Step 1: Installing System Dependencies & KiCad 9 EDA ===${NC}"
    
    mkdir -p "$BIN_DIR" "$TOOLS_DIR" "$CONFIG_DIR"
    export PATH="$BIN_DIR:$PATH"

    case "$DISTRO" in
        ubuntu|debian|pop|linuxmint)
            echo -e "${BLUE}[-] Updating package lists and installing software-properties-common...${NC}"
            $SUDO apt-get update -y
            $SUDO apt-get install -y --no-install-recommends \
                curl wget git software-properties-common ca-certificates build-essential \
                python3 python3-pip python3-venv python3-dev \
                default-jre-headless imagemagick ffmpeg jq

            # Check if KiCad 9 is already installed
            if command -v kicad-cli >/dev/null 2>&1 && kicad-cli --version 2>&1 | grep -q "9\."; then
                echo -e "${GREEN}[✓] KiCad 9 is already installed: $(kicad-cli --version)${NC}"
            else
                echo -e "${BLUE}[-] Adding official KiCad 9 PPA repository...${NC}"
                $SUDO add-apt-repository -y ppa:kicad/kicad-9.0-releases || true
                $SUDO apt-get update -y
                echo -e "${BLUE}[-] Installing KiCad 9 and complete symbol/footprint/3D libraries...${NC}"
                $SUDO apt-get install -y \
                    kicad \
                    kicad-libraries \
                    kicad-symbols \
                    kicad-footprints \
                    kicad-packages3d \
                    python3-kicad || true
            fi
            ;;
        fedora|rhel)
            echo -e "${BLUE}[-] Installing KiCad 9 and build tools via DNF...${NC}"
            $SUDO dnf install -y \
                kicad kicad-packages3d \
                python3 python3-pip python3-devel \
                git curl wget java-latest-openjdk-headless gcc
            ;;
        arch|manjaro)
            echo -e "${BLUE}[-] Installing KiCad and build tools via Pacman...${NC}"
            $SUDO pacman -Syu --noconfirm --needed \
                kicad kicad-library kicad-library-3d \
                python python-pip \
                git curl wget jre-headless base-devel
            ;;
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                echo -e "${RED}[!] Homebrew is required on macOS. Install from https://brew.sh/${NC}"
                exit 1
            fi
            echo -e "${BLUE}[-] Installing KiCad & dependencies via Homebrew...${NC}"
            brew install --cask kicad || true
            brew install python git curl wget openjdk imagemagick jq
            ;;
        *)
            echo -e "${YELLOW}[!] Warning: Unrecognized distribution ($DISTRO). Proceeding with generic tool setup...${NC}"
            ;;
    esac
}

# ------------------------------------------------------------------------------
# 3. Create Dedicated Python AI Virtual Environment
# ------------------------------------------------------------------------------
setup_python_environment() {
    echo -e "\n${YELLOW}=== Step 2: Setting up Python AI Virtual Environment ===${NC}"
    
    # We use --system-site-packages so that the system pcbnew (KiCad Python API) is importable
    if [ ! -d "$INSTALL_DIR/venv" ]; then
        echo -e "${BLUE}[-] Creating Python virtual environment at $INSTALL_DIR/venv...${NC}"
        python3 -m venv --system-site-packages "$INSTALL_DIR/venv"
    else
        echo -e "${GREEN}[✓] Virtual environment exists at $INSTALL_DIR/venv${NC}"
    fi

    VENV_PIP="$INSTALL_DIR/venv/bin/pip"
    VENV_PY="$INSTALL_DIR/venv/bin/python3"

    echo -e "${BLUE}[-] Upgrading pip, setuptools, and wheel...${NC}"
    "$VENV_PIP" install --upgrade pip setuptools wheel

    echo -e "\n${YELLOW}=== Step 3: Installing AI PCB MCP Servers & Core EDA Toolchain ===${NC}"
    echo -e "${BLUE}[-] Installing: mcp-server-kicad, kicad-mcp-pro, kicad-sch-api, atopile, InteractiveHtmlBom...${NC}"
    
    "$VENV_PIP" install \
        "mcp-server-kicad>=0.21.0" \
        "kicad-mcp-pro>=4.9.0" \
        "kicad-sch-api>=0.2.0" \
        "kicad-python>=0.5.0" \
        "InteractiveHtmlBom>=2.9.0" \
        "atopile>=0.15.0" \
        "skidl>=3.0.0" \
        "fastmcp>=0.1.0" \
        "mcp>=1.0.0" \
        "sexpdata>=1.0.0" \
        "matplotlib" \
        "numpy" \
        "pandas" \
        "rich" \
        "typer" \
        "pydantic"

    echo -e "${GREEN}[✓] Python AI PCB toolchain successfully installed!${NC}"
}

# ------------------------------------------------------------------------------
# 4. Install FreeRouting Auto-Router Utility
# ------------------------------------------------------------------------------
setup_freerouting() {
    echo -e "\n${YELLOW}=== Step 4: Installing FreeRouting Auto-Router ===${NC}"
    FREEROUTING_JAR="$TOOLS_DIR/freerouting.jar"
    if [ ! -f "$FREEROUTING_JAR" ]; then
        echo -e "${BLUE}[-] Downloading FreeRouting standalone release jar...${NC}"
        FREEROUTING_URL="https://github.com/freerouting/freerouting/releases/download/v2.5.0/freerouting-2.5.0.jar"
        wget -q -O "$FREEROUTING_JAR" "$FREEROUTING_URL" || \
        curl -fsSL -o "$FREEROUTING_JAR" "$FREEROUTING_URL" || {
            echo -e "${YELLOW}[!] Note: Could not download freerouting jar automatically. You can manually place freerouting.jar in $TOOLS_DIR${NC}"
        }
    fi

    # Create wrapper executable in ~/.local/bin
    cat << 'EOF' > "$BIN_DIR/freerouting"
#!/usr/bin/env bash
JAR_PATH="$HOME/.ai-pcb-env/tools/freerouting.jar"
if [ ! -f "$JAR_PATH" ]; then
    echo "Error: FreeRouting JAR not found at $JAR_PATH" >&2
    exit 1
fi
exec java -jar "$JAR_PATH" "$@"
EOF
    chmod +x "$BIN_DIR/freerouting"
    echo -e "${GREEN}[✓] FreeRouting command created at $BIN_DIR/freerouting${NC}"
}

# ------------------------------------------------------------------------------
# 5. Generate AI MCP Client Configurations
# ------------------------------------------------------------------------------
generate_mcp_configs() {
    echo -e "\n${YELLOW}=== Step 5: Generating AI Agent MCP Client Configurations ===${NC}"

    KICAD_MCP_BIN="$INSTALL_DIR/venv/bin/mcp-server-kicad"
    KICAD_PRO_BIN="$INSTALL_DIR/venv/bin/kicad-mcp-pro"

    # 1. Standard MCP JSON configuration snippet
    CONFIG_JSON="$CONFIG_DIR/mcp_servers.json"
    cat << EOF > "$CONFIG_JSON"
{
  "mcpServers": {
    "kicad": {
      "command": "${KICAD_MCP_BIN}",
      "args": []
    },
    "kicad-mcp-pro": {
      "command": "${KICAD_PRO_BIN}",
      "args": [
        "serve",
        "--mode",
        "write",
        "--profile",
        "full"
      ]
    }
  }
}
EOF
    echo -e "${GREEN}[✓] Master MCP configuration created at: ${BOLD}${CONFIG_JSON}${NC}"

    # 2. Auto-configure Claude Desktop if directory exists
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
    [ "$DISTRO" = "macos" ] && CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
    if [ -d "$CLAUDE_CONFIG_DIR" ] || [ -f "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" ]; then
        echo -e "${BLUE}[-] Auto-detecting Claude Desktop installation...${NC}"
        mkdir -p "$CLAUDE_CONFIG_DIR"
        # If config doesn't exist, write it directly
        if [ ! -f "$CLAUDE_CONFIG_DIR/claude_desktop_config.json" ]; then
            cp "$CONFIG_JSON" "$CLAUDE_CONFIG_DIR/claude_desktop_config.json"
            echo -e "${GREEN}[✓] Installed MCP configuration into Claude Desktop!${NC}"
        else
            echo -e "${CYAN}[i] Claude config already exists. You can merge the snippet from: $CONFIG_JSON${NC}"
        fi
    fi

    # 3. Auto-configure Antigravity / Gemini CLI if ~/.gemini/config exists
    GEMINI_CONFIG_DIR="$HOME/.gemini/config"
    if [ -d "$GEMINI_CONFIG_DIR" ]; then
        echo -e "${BLUE}[-] Configuring Antigravity / Gemini CLI MCP server registry...${NC}"
        # Merge or update
        if [ -f "$GEMINI_CONFIG_DIR/mcp_config.json" ]; then
            python3 -c "
import json
try:
    with open('$GEMINI_CONFIG_DIR/mcp_config.json') as f:
        d = json.load(f)
    servers = d.setdefault('mcpServers', {})
    servers['kicad'] = {'command': '$KICAD_MCP_BIN', 'args': []}
    servers['kicad-mcp-pro'] = {'command': '$KICAD_PRO_BIN', 'args': ['serve', '--mode', 'write', '--profile', 'full']}
    with open('$GEMINI_CONFIG_DIR/mcp_config.json', 'w') as f:
        json.dump(d, f, indent=2)
    print('[✓] Updated $GEMINI_CONFIG_DIR/mcp_config.json successfully!')
except Exception as e:
    print('Failed to merge into gemini config:', e)
" || true
        fi
    fi

    # 4. Cursor IDE global or project config template
    CURSOR_CONFIG_DIR="$HOME/.cursor"
    mkdir -p "$CURSOR_CONFIG_DIR"
    cp "$CONFIG_JSON" "$CURSOR_CONFIG_DIR/mcp.json"
    echo -e "${GREEN}[✓] Cursor configuration template generated at: $CURSOR_CONFIG_DIR/mcp.json${NC}"
}

# ------------------------------------------------------------------------------
# 6. Verification and Health Check
# ------------------------------------------------------------------------------
verify_installation() {
    echo -e "\n${YELLOW}=== Step 6: Verifying Toolchain & Diagnostics ===${NC}"
    
    VENV_PY="$INSTALL_DIR/venv/bin/python3"
    
    # Check 1: KiCad CLI
    echo -n "Checking kicad-cli: "
    if command -v kicad-cli >/dev/null 2>&1; then
        KICAD_VER=$(kicad-cli --version 2>&1 || true)
        echo -e "${GREEN}${KICAD_VER}${NC}"
    else
        echo -e "${RED}FAILED (kicad-cli not found in PATH)${NC}"
    fi

    # Check 2: Python pcbnew binding
    echo -n "Checking KiCad Python API (pcbnew): "
    if "$VENV_PY" -c "import pcbnew; print('pcbnew ' + pcbnew.GetBuildVersion())" >/dev/null 2>&1; then
        PCBNEW_VER=$("$VENV_PY" -c "import pcbnew; print(pcbnew.GetBuildVersion())")
        echo -e "${GREEN}PASS (${PCBNEW_VER})${NC}"
    else
        echo -e "${YELLOW}WARNING (pcbnew C++ API not bound in venv - check python3-kicad)${NC}"
    fi

    # Check 3: KiCad MCP Servers
    echo -n "Checking mcp-server-kicad: "
    if [ -f "$INSTALL_DIR/venv/bin/mcp-server-kicad" ]; then
        echo -e "${GREEN}PASS${NC}"
    else
        echo -e "${RED}FAILED${NC}"
    fi

    echo -n "Checking kicad-mcp-pro: "
    if [ -f "$INSTALL_DIR/venv/bin/kicad-mcp-pro" ]; then
        MCP_PRO_VER=$("$INSTALL_DIR/venv/bin/kicad-mcp-pro" --help | head -n 3 | tr '\n' ' ' || true)
        echo -e "${GREEN}PASS${NC}"
    else
        echo -e "${RED}FAILED${NC}"
    fi

    # Check 4: InteractiveHtmlBom
    echo -n "Checking InteractiveHtmlBom: "
    if [ -f "$INSTALL_DIR/venv/bin/generate_interactive_bom.py" ]; then
        echo -e "${GREEN}PASS${NC}"
    else
        echo -e "${YELLOW}OPTIONAL${NC}"
    fi

    # Check 5: Atopile
    echo -n "Checking atopile: "
    if [ -f "$INSTALL_DIR/venv/bin/ato" ]; then
        echo -e "${GREEN}PASS${NC}"
    else
        echo -e "${YELLOW}OPTIONAL${NC}"
    fi
}

# ------------------------------------------------------------------------------
# Main Execution Flow
# ------------------------------------------------------------------------------
main() {
    install_system_dependencies
    setup_python_environment
    setup_freerouting
    generate_mcp_configs
    verify_installation

    echo -e "\n${GREEN}${BOLD}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}${BOLD} 🎉 SETUP COMPLETE! AI PCB DESIGN ENVIRONMENT IS READY TO USE!      ${NC}"
    echo -e "${GREEN}${BOLD}════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "To activate the environment in your shell:"
    echo -e "  ${BOLD}source $INSTALL_DIR/venv/bin/activate${NC}"
    echo ""
    echo -e "To configure any AI Agent (Claude Code, Cursor, Windsurf, Roo Code, etc.):"
    echo -e "  Point your agent's MCP settings to: ${BOLD}$CONFIG_DIR/mcp_servers.json${NC}"
    echo ""
    echo -e "The MCP configuration contents are:"
    cat "$CONFIG_DIR/mcp_servers.json"
    echo ""
    echo -e "${CYAN}Happy AI PCB Designing! 🚀${NC}"
}

main "$@"
