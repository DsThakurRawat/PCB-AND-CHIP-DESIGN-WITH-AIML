# AI PCB Design Toolchain — Complete Installation & Setup Guide

This guide describes how to replicate our exact **AI-Assisted PCB Design Environment** on any new computer (Ubuntu/Debian, Fedora, Arch Linux, or macOS).

---

## ⚡ Quick One-Line Setup (Any PC)

To set up the complete environment automatically, download and run the setup script:

```bash
# Clone or download the setup script
chmod +x setup_ai_pcb_environment.sh

# Run the installer
./setup_ai_pcb_environment.sh
```

---

## 🛠️ What the Setup Script Installs

The installer provisions the full hardware engineering stack used by our autonomous AI agents:

### 1. Electronic Design Automation (EDA) Core
* **KiCad 9.0+**: Complete EDA suite (`kicad`, `eeschema`, `pcbnew`, `gerbview`, `kicad-cli`).
* **Official KiCad Libraries**:
  * Complete schematic symbols (`kicad-symbols`)
  * Standard footprints (`kicad-footprints`)
  * 3D STEP & VRML raytracing component models (`kicad-packages3d`)
* **KiCad Python C++ API (`pcbnew`)**: Native bindings enabling deep programmatic PCB manipulation, zone filling, track routing, and DRC validation.

### 2. Model Context Protocol (MCP) AI Servers
The Model Context Protocol (MCP) lets LLMs (Claude, Gemini, Cursor, Antigravity) directly read, modify, route, and verify your board:

| MCP Server | PyPI Package | Primary AI Capabilities |
| :--- | :--- | :--- |
| **KiCad MCP** | `mcp-server-kicad` | Byte-preserving schematic capture, netlist syncing, track routing, zone generation, ERC/DRC execution, fabrication exports. |
| **KiCad MCP Pro** | `kicad-mcp-pro` | Professional engineering quality gates: Signal Integrity (SI), Power Integrity (PDN/IR drop), high-speed differential pairs, DFM rule verification, placement scoring. |

### 3. Programmatic Circuit Synthesis
* **`kicad-sch-api`**: Direct Pythonic generation and editing of `.kicad_sch` S-expressions.
* **`atopile`**: Compiler transforming code-based circuit definitions into physical KiCad layouts.
* **`skidl`**: Python library for programmatic schematic design and electrical rule validation.

### 4. Manufacturing & Assembly Utilities
* **`InteractiveHtmlBom`**: Generates interactive browser-based assembly documentation (`ibom.html`) with interactive component highlighting and BoM sorting.
* **FreeRouting**: Automated multi-layer topological router via Specctra DSN interface.
* **Excellon & RS-274X Pipeline**: Headless CLI generation of Gerbers, drill files, centroid pick-and-place files, and high-resolution 3D raytraced renders.

---

## 🤖 Connecting Your AI Agent

Once the installer finishes, it generates a master configuration file at:
`~/.ai-pcb-env/configs/mcp_servers.json`

### 1. Claude Desktop
Add the following to your Claude Desktop configuration file:
* **Linux**: `~/.config/Claude/claude_desktop_config.json`
* **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kicad": {
      "command": "/home/<username>/.ai-pcb-env/venv/bin/mcp-server-kicad",
      "args": []
    },
    "kicad-mcp-pro": {
      "command": "/home/<username>/.ai-pcb-env/venv/bin/kicad-mcp-pro",
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
```

### 2. Cursor IDE
In Cursor, open **Settings > Features > MCP**, or create `~/.cursor/mcp.json` (or `.cursor/mcp.json` in your project root):

```json
{
  "mcpServers": {
    "kicad": {
      "command": "/home/<username>/.ai-pcb-env/venv/bin/mcp-server-kicad"
    },
    "kicad-mcp-pro": {
      "command": "/home/<username>/.ai-pcb-env/venv/bin/kicad-mcp-pro",
      "args": ["serve", "--mode", "write", "--profile", "full"]
    }
  }
}
```

### 3. Antigravity / Gemini CLI
Add to `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "kicad": {
      "command": "/home/<username>/.ai-pcb-env/venv/bin/mcp-server-kicad",
      "args": []
    },
    "kicad-mcp-pro": {
      "command": "/home/<username>/.ai-pcb-env/venv/bin/kicad-mcp-pro",
      "args": ["serve", "--mode", "write", "--profile", "full"]
    }
  }
}
```

---

## 🧪 Verifying the Installation

To verify that all components are operating correctly:

```bash
# Activate the virtual environment
source ~/.ai-pcb-env/venv/bin/activate

# 1. Verify KiCad CLI
kicad-cli --version

# 2. Verify Python pcbnew bindings
python3 -c "import pcbnew; print('pcbnew build:', pcbnew.GetBuildVersion())"

# 3. Verify KiCad MCP Pro Server diagnostics
kicad-mcp-pro doctor
```

All checks should report **PASS** / **healthy**.
