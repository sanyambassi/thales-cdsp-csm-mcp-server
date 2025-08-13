# Thales CDSP CSM Akeyless Vault MCP Server

A Model Context Protocol (MCP) server for managing secrets in Thales CDSP CSM Akeyless Vault. This server provides tools for creating, managing, and deleting static secrets, DFC keys, and other vault resources through the MCP protocol.

## 📋 Table of Contents

- [🎥 Demo](#-demo)
- [🚀 Quick Start](#-quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [🪟 Windows-Specific Instructions](#-windows-specific-instructions)
  - [Prerequisites for Windows](#prerequisites-for-windows)
  - [Windows Installation Steps](#windows-installation-steps)
  - [Windows Virtual Environment Activation](#windows-virtual-environment-activation)
  - [Windows File Operations](#windows-file-operations)
  - [Running on Windows](#running-on-windows)
  - [Windows Troubleshooting](#windows-troubleshooting)
- [🛠️ Available Tools](#️-available-tools)
  - [Secret Management](#secret-management)
  - [Item Management](#item-management)
  - [Deletion Tools](#deletion-tools)
  - [Tool Features](#tool-features)
- [📋 Secret Formats](#-secret-formats)
  - [Text Format](#text-format)
  - [JSON Format](#json-format)
  - [Key-Value Format](#key-value-format)
- [🔐 DFC Key Support](#-dfc-key-support)
- [🗂️ Enhanced Deletion Strategy](#️-enhanced-deletion-strategy)
- [📚 Documentation](#-documentation)
- [⚙️ MCP Configuration Files](#️-mcp-configuration-files)
  - [Configuration Options](#configuration-options)
  - [Usage Instructions](#usage-instructions)
  - [Example Setup](#example-setup)
- [🧪 Testing](#-testing)
  - [Manual Testing](#manual-testing)
  - [Automated Testing](#automated-testing)
  - [Test Scenarios](#test-scenarios)
- [🔧 Development](#-development)
  - [Project Structure](#project-structure)
  - [Key Features](#key-features)
- [📄 License](#-license)
- [🤝 Contributing](#-contributing)
  - [Before Contributing](#before-contributing)
  - [How to Contribute](#how-to-contribute)
  - [Code Standards](#code-standards)
  - [Questions or Issues](#questions-or-issues)

---

## 🎥 Demo

📹 **[Watch the Demo Video - Coming Soon]()**

See the Thales CSM Akeyless Vault MCP Server in action, demonstrating:
- Protect hard coded secrets in repositories
- Secret creation and management
- DFC key operations  
- Both transport modes (stdio and HTTP)
- Real-world usage examples

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Thales CSM Akeyless Vault account
- API Key for Akeyless

### Installation

#### Using uv (Recommended)
```bash
# Clone the repository
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server

# Install dependencies and create virtual environment
uv sync

# Set up environment variables
cp env.example .env  # Linux/macOS
# or
copy env.example .env  # Windows
# Edit .env with your Thales CSM credentials
```

#### Using pip (Alternative)
```bash
# Clone the repository
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server

# Create virtual environment
python -m venv venv

# Activate virtual environment

# Linux/macOS:
source venv/bin/activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env  # Linux/macOS
# or
copy env.example .env  # Windows
# Edit .env with your Thales CSM credentials
```

### Environment Variables
```bash
AKEYLESS_API_URL=https://api.akeyless.io
AKEYLESS_ACCESS_ID=your_access_id
AKEYLESS_ACCESS_KEY=your_access_key
```

### Running the Server

The server supports two transport modes:

#### stdio Transport (Default)
```bash
# Start MCP server with stdio transport
python main.py --transport stdio

# Or using uv
uv run python main.py --transport stdio
```

**Use Case**: MCP client integration (Claude Desktop, Cursor, etc.)
**Features**: Direct communication, no network exposure, automatic tool discovery

#### HTTP Transport
```bash
# Start HTTP server for web/API access
python main.py --transport streamable-http --host 0.0.0.0 --port 8000

# Or using uv
uv run python main.py --transport streamable-http --host 0.0.0.0 --port 8000
```

**Use Case**: Web applications, API testing, remote access
**Features**: RESTful HTTP endpoints, network accessible, tool for testing

#### Transport Options
```bash
# Custom host and port
python main.py --transport streamable-http --host 127.0.0.1 --port 9000

# Help
python main.py --help
```

## 🪟 Windows-Specific Instructions

### Prerequisites for Windows
- **Python**: Download from [python.org](https://python.org) or use [Microsoft Store](https://apps.microsoft.com/detail/python-3-11/9NRWMJP3717K)
- **Git**: Download from [git-scm.com](https://git-scm.com) or use [Git for Windows](https://gitforwindows.org/)
- **PowerShell**: Use PowerShell 7+ for best experience (available via Microsoft Store)

### Windows Installation Steps

#### Using uv (Recommended for Windows)
```powershell
# Open PowerShell as Administrator (recommended)
# Install uv if not already installed
winget install --id=astral-sh.uv
# or
pip install uv

# Clone and setup
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server
uv sync
copy env.example .env
notepad .env  # Edit with your credentials
```

#### Using pip on Windows
```cmd
# Open Command Prompt or PowerShell
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server

# Create virtual environment
python -m venv venv

# Activate (choose based on your shell)
venv\Scripts\activate.bat     # Command Prompt
# or
venv\Scripts\Activate.ps1     # PowerShell

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy env.example .env
notepad .env  # Edit with your credentials
```

### Windows Virtual Environment Activation
- **Command Prompt**: `venv\Scripts\activate.bat`
- **PowerShell**: `venv\Scripts\Activate.ps1`
- **Git Bash**: `source venv/Scripts/activate`

### Windows File Operations
- **Copy files**: Use `copy` instead of `cp`
- **Edit files**: Use `notepad`, `code` (VS Code), or your preferred editor
- **Path separators**: Use backslashes `\` or forward slashes `/` (both work in modern Windows)

### Running on Windows
```cmd
# Command Prompt
venv\Scripts\activate.bat
python main.py --transport stdio

# PowerShell
venv\Scripts\Activate.ps1
python main.py --transport stdio

# With uv (no activation needed)
uv run python main.py --transport stdio
```

### Windows Troubleshooting
- **PowerShell Execution Policy**: If you get execution policy errors, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- **Path Issues**: Ensure Python and pip are in your system PATH
- **Virtual Environment**: If activation fails, try running as Administrator
- **Firewall**: Windows Defender may block HTTP transport mode - allow the application when prompted

## 🛠️ Available Tools

### Secret Management
- **`create_static_secret`** - Create static secrets with format validation
  - Supports text, JSON, and key-value formats
  - Automatic path normalization and validation
  - Tag-based organization and descriptions
- **`create_dfc_key`** - Create Distributed Fragment Cryptography keys
  - AES (128GCM, 256GCM, 128SIV, 256SIV, 128CBC, 256CBC)
  - RSA (1024, 2048, 3072, 4096)
  - Auto-rotation support for AES keys
- **`get_secret`** - Retrieve secret values with path resolution
- **`update_secret_value`** - Update existing secret values
- **`update_item`** - Update item metadata and properties

### Item Management
- **`list_items`** - List items with advanced filtering and pagination
  - Path-based filtering and item type filtering
  - Auto-pagination for large collections
  - Minimal view options for performance
- **`set_item_state`** - Enable/disable items
- **`update_rotation_settings`** - Configure automatic key rotation

### Deletion Tools
- **`delete_item`** - Delete single items with DFC key handling
- **`delete_items`** - Bulk delete with enhanced proactive strategy
  - Automatic DFC key discovery and handling
  - Recursive directory deletion
  - Scheduled deletion for security-sensitive items

### Tool Features
- **Path Normalization**: Automatic conversion to absolute paths
- **Format Validation**: Strict validation for all secret formats
- **Error Handling**: Comprehensive error messages and validation
- **Security**: DFC key protection and scheduled deletion

## 📋 Secret Formats

### Text Format
- Plain text secrets (default)
- Supports multiline content, Unicode, special characters
- Most flexible format

### JSON Format
- Valid JSON content
- Supports nested structures, arrays, mixed types
- Ideal for configuration data

### Key-Value Format
- Flat JSON objects with string values only
- No nested structures or arrays
- Perfect for simple key-value pairs

## 🔐 DFC Key Support

- **AES Keys**: AES128GCM, AES256GCM, AES128SIV, AES256SIV, AES128CBC, AES256CBC
- **RSA Keys**: RSA1024, RSA2048, RSA3072, RSA4096
- **Auto-rotation**: Supported for AES keys (7-365 day intervals)
- **Security**: Cannot be deleted immediately (scheduled deletion)

## 🗂️ Enhanced Deletion Strategy

The `delete_items` tool automatically:
1. Discovers all DFC keys in directories
2. Handles DFC keys according to security requirements
3. Bulk deletes remaining items efficiently
4. Supports both path-based and item-based deletion

## 📚 Documentation

- **`docs/README.md`** - Documentation overview and navigation
- **`docs/TRANSPORT_MODES.md`** - Transport mode configuration
- **`docs/TESTING.md`** - Manual and automated testing guide

## ⚙️ MCP Configuration Files

The repository includes multiple MCP configuration files in the `config/` directory for different environments:

### **Configuration Options:**

- **`config/mcp-config.json`** - Cross-platform standard Python (recommended for most users)
- **`config/mcp-config-uv.json`** - UV environment with `uv run python`
- **`config/mcp-config-venv.json`** - Windows virtual environment with explicit paths
- **`config/mcp-config-venv-unix.json`** - Unix/Linux virtual environment with explicit paths

### **Usage Instructions:**

1. **Choose the appropriate config file** based on your environment
2. **Copy the config file** to your MCP client's configuration directory
3. **Update the environment variables** with your actual Akeyless credentials
4. **Ensure you're in the repository directory** when running the server (paths are relative)

### **Example Setup:**
```bash
# Clone and navigate to repository
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server

# Copy your chosen config file to MCP client config directory
# (location varies by MCP client - check your client's documentation)

# Update credentials in the config file or use .env file
cp env.example .env
# Edit .env with your actual credentials
```

## 🧪 Testing

### Manual Testing
- **stdio Transport**: Test with MCP clients (Claude Desktop, Cursor)
- **HTTP Transport**: Test with HTTP requests (curl, Postman)
- **Tool Validation**: Test all available tools and error conditions
- **Path Resolution**: Verify path normalization and resolution

### Automated Testing
```bash
# Run test suite
uv run python -m pytest tests/

# Run with coverage
uv run python -m pytest tests/ --cov=src/ --cov-report=html
```

#### Windows Testing Commands
```cmd
# Command Prompt
venv\Scripts\activate.bat
python -m pytest tests/

# PowerShell
venv\Scripts\Activate.ps1
python -m pytest tests/

# With uv (no activation needed)
uv run python -m pytest tests/
```

### Test Scenarios
- Basic functionality and tool registration
- Secret creation, retrieval, and deletion
- Error handling and validation
- Performance and pagination
- Transport mode compatibility

**📖 See [docs/TESTING.md](docs/TESTING.md) for complete testing guide**

## 🔧 Development

### Project Structure
```
src/thales_cdsp_csm_mcp_server/
├── client.py          # Thales API client
├── server.py          # MCP server implementation
└── tools/
    ├── base_tools.py  # Base tool classes
    └── secret_tools.py # Secret management tools

config/                 # MCP configuration files
├── mcp-config.json    # Standard Python (cross-platform)
├── mcp-config-uv.json # UV environment
├── mcp-config-venv.json # Windows virtual environment
└── mcp-config-venv-unix.json # Unix/Linux virtual environment
```

### Key Features
- **FastMCP Integration**: Built-in type coercion and validation
- **Comprehensive Validation**: Format-specific validation for all secret types
- **Error Handling**: Robust error handling with user-friendly messages
- **Logging**: Detailed logging for debugging and monitoring

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### **Before Contributing**
- Check existing issues and pull requests
- Ensure your changes align with the project's scope
- Test your changes thoroughly

### **How to Contribute**
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** your changes (`uv run python -m pytest tests/`)
5. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### **Code Standards**
- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass before submitting

### **Questions or Issues?**
- Open an issue for bugs or feature requests
- Provide clear reproduction steps for bugs
- Include relevant system information 