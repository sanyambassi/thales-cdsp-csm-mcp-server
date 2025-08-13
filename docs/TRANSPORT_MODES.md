# Transport Modes - Thales CDSP CSM Akeyless Vault MCP Server

This document explains the transport modes supported by the server.

## Overview

The server supports two transport modes:
1. **stdio Transport** - For MCP client integration
2. **HTTP Transport** - For web applications and API access

## stdio Transport (Default)

**Use Case**: MCP client integration (Claude Desktop, Cursor, etc.)

**Command**: `python main.py --transport stdio`

**Features**: 
- Direct communication with MCP clients
- No network exposure
- Automatic tool discovery
- Ideal for local development and production use

## HTTP Transport

**Use Case**: Web applications, API testing, remote access

**Command**: `python main.py --transport streamable-http --host 0.0.0.0 --port 8000`

**Features**:
- RESTful HTTP endpoints at `/mcp` and `/mcp/message`
- Network accessible
- Tool for testing and integration
- Supports both local and remote clients

## Examples

```bash
# stdio mode (default)
python main.py --transport stdio

# HTTP mode
python main.py --transport streamable-http --host 0.0.0.0 --port 8000

# Custom port
python main.py --transport streamable-http --port 9000
```

## Virtual Environment Notes

### uv Users
- Virtual environment is automatically created in `.venv/` directory
- Use `uv run` to automatically use the virtual environment
- Or activate manually: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)

### pip Users
- Virtual environment is typically created in `venv/` directory
- Activate manually: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)

## Security

- **stdio**: No network exposure, most secure
- **HTTP**: Network accessible, implement proper security measures 