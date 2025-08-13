# Documentation - Thales CDSP CSM Akeyless Vault MCP Server

This directory contains focused documentation for the MCP server.

## 📚 **Available Documentation**

### **Root README.md**
- **Project overview** and quick start
- **Installation** (uv/pip, virtual/non-virtual environments)
- **Deployment** (stdio and HTTP transport modes)
- **Available tools** summary
- **Getting started** guide

### **TRANSPORT_MODES.md**
- **Transport mode configuration** (stdio vs HTTP)
- **Command examples** for each mode
- **Virtual environment notes** for uv and pip users
- **Security considerations**

### **TESTING.md**
- **Manual testing** procedures and examples
- **Automated testing** setup and execution
- **Test scenarios** and validation
- **Troubleshooting** common issues

## 🎯 **Quick Reference**

### **Installation**
```bash
# Using uv (recommended)
uv sync

# Using pip
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **Start Server**
```bash
# stdio mode (MCP clients)
python main.py --transport stdio

# HTTP mode (web/API access)
python main.py --transport streamable-http --host 0.0.0.0 --port 8000
```

### **Available Tools**
- **Secret Management**: `create_static_secret`, `create_dfc_key`, `get_secret`
- **Item Management**: `list_items`, `update_item`, `set_item_state`
- **Deletion**: `delete_item`, `delete_items`

## 🔗 **Navigation**

- **Getting Started** → See root `README.md`
- **Transport Configuration** → See `TRANSPORT_MODES.md`
- **Testing & Validation** → See `TESTING.md`
- **Tool Details** → See root `README.md` tools section

## 📖 **Documentation Philosophy**

This documentation is designed to be:
- **Focused** - Each file has a single, clear purpose
- **Navigable** - Easy to find what you need
- **Practical** - Contains working examples and commands
- **Maintainable** - Simple structure, easy to update 