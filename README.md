# Thales CipherTrust Secrets Management MCP Server, powered by Akeyless

A production-ready Model Context Protocol (MCP) server for enterprise secrets management in **Thales CipherTrust Secrets Management (CSM)**, powered by Akeyless Vault technology. This server delivers enterprise-grade secrets management through AI assistants and applications, with built-in security, compliance, and scalability features.

## 🎥 Demo

📹 **[Watch the Demo Video - Coming Soon]()**

See the Thales CipherTrust Secrets Management MCP Server in action, demonstrating:
- **Enterprise Deployment**: Seamless integration with CipherTrust Manager
- **AI Assistant Integration**: Using with Claude Desktop, Cursor AI, and other MCP clients
- **Real-World Scenarios**: Protecting hardcoded secrets in repositories and codebases
- **Advanced Operations**: DFC key management, rotation, and certificate generation
- **Security Features**: Delete protection, access control, and audit logging

## 🚀 Features

### **Core Capabilities**
- **Universal Secret Management**: Create, read, update, and delete static, dynamic, and rotated secrets
- **DFC Key Management**: Manage Data Fragmentation Keys with comprehensive encryption options
- **Smart Deletion**: Intelligent directory and bulk deletion with DFC key handling
- **Auto-Format Detection**: Automatically detects and converts key-value format to JSON

### **Enterprise Security**
- **Delete Protection**: Secure secrets with deletion protection and audit trails
- **Access Control**: Role-based access management through CipherTrust Manager
- **Compliance Ready**: Built for enterprise compliance requirements (SOC2, ISO27001, etc.)
- **Audit Logging**: Comprehensive logging for security and compliance audits

### **Infrastructure & Monitoring**
- **Multiple Transport Modes**: Support for stdio and HTTP transports
- **Health Monitoring**: Built-in health check endpoint for HTTP transport
- **MCP Protocol Support**: Latest (2025-06-18) and backward compatible (2025-03-26) with FastMCP 2.10.5
- **Scalable Architecture**: Designed for enterprise-scale deployments

### **Integration & Automation**
- **AI Assistant Ready**: Seamless integration with Claude, Cursor, and other MCP clients
- **API-First Design**: RESTful endpoints for automation and CI/CD integration
- **Multi-Platform Support**: Windows, Linux, and macOS compatibility

## 🏗️ Architecture

```
src/
├── core/           # Core client and configuration
├── server/         # MCP server implementation
├── tools/          # Tool implementations
│   ├── secrets/    # Secret management tools
│   ├── dfc_keys/   # DFC key management tools
│   ├── auth/       # Authentication management
│   ├── rotation/   # Secret rotation tools
│   └── customer_fragments/  # Customer fragment management
├── tests/          # Test suite and validation
├── docs/           # Documentation and guides
├── config/         # MCP configuration templates
├── uv.lock         # UV dependency lock file (for reproducible builds)
└── requirements.txt # Traditional pip requirements
```

## 📋 Prerequisites

### **System Requirements**
- **Python**: 3.8 or higher (3.9+ recommended for production)
- **Memory**: Minimum 512MB RAM, 2GB+ recommended
- **Storage**: 100MB+ available disk space
- **Network**: Access to CipherTrust Manager instance

### **Thales CipherTrust Access**
- **CipherTrust Manager**: Active instance with CSM enabled
- **API Access**: Valid Akeyless API credentials
- **Permissions**: Appropriate access levels for secrets management
- **Network**: Firewall access to CipherTrust Manager API endpoints

### **Development Environment**
- **Git**: For cloning and version control
- **Package Manager**: 
  - **uv** (recommended): Modern, fast Python package manager
  - **pip**: Traditional Python package manager
- **Virtual Environment**: Automatically managed by uv, or manual with pip

## 🛠️ Installation

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server
```

### **Step 2: Install Dependencies**

#### **Option A: Using uv (Recommended for Development)**
```bash
# Install uv if you don't have it
pip install uv

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

#### **Option B: Using pip (Alternative)**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### **Step 3: Configure Environment**
```bash
# Copy environment template
cp env.example .env

# Edit .env with your CipherTrust Manager credentials
# Required: AKEYLESS_ACCESS_ID, AKEYLESS_ACCESS_KEY, AKEYLESS_API_URL
# Optional: LOG_LEVEL, AKEYLESS_VERIFY_SSL
```

### **Step 4: Verify Installation**
```bash
# Test the server startup
python main.py --help

# Should display available transport options and help information
```

## 🚀 **UV Package Manager (Recommended)**

### **Quick Start with UV**
```bash
# 1. Install uv
# On Windows (recommended):
winget install --id=astral-sh.uv
# Or using pip:
pip install uv

# 2. Clone and setup
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server

# 3. Install dependencies (creates .venv automatically)
uv sync

# 4. Run the server
uv run python main.py
```

### **Why Use UV?**
- **Faster Installation**: 10-100x faster than pip
- **Dependency Resolution**: Intelligent conflict resolution
- **Lock File**: Reproducible builds with `uv.lock`
- **Modern Tooling**: Built-in virtual environment management

### **UV Commands Reference**
```bash
# Install uv
pip install uv

# Create project and install dependencies
uv sync

# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update dependencies
uv sync --upgrade

# Run commands in virtual environment
uv run python main.py

# Activate virtual environment manually
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### **UV vs Traditional pip**
| Feature | UV | pip + venv |
|---------|----|------------|
| **Speed** | ⚡ 10-100x faster | 🐌 Standard speed |
| **Lock File** | ✅ `uv.lock` | ❌ No lock file |
| **Virtual Env** | ✅ Auto-created | ⚠️ Manual creation |
| **Dependency Resolution** | ✅ Smart | ⚠️ Basic |
| **Cross-Platform** | ✅ Yes | ✅ Yes |

### **UV Troubleshooting**
```bash
# If uv sync fails, try:
uv sync --reinstall

# Clear uv cache if needed:
uv cache clean

# Check uv version:
uv --version

# Force recreate virtual environment:
rm -rf .venv
uv sync
```

## ⚙️ Configuration

### **Environment Variables**

Create a `.env` file with your CipherTrust Manager configuration:

```env
# Required: CipherTrust Manager API credentials
AKEYLESS_ACCESS_ID=your_access_id
AKEYLESS_ACCESS_KEY=your_access_key
AKEYLESS_API_URL=https://your-ciphertrust-manager/akeyless-api/v2/

# Optional: Logging and security settings
LOG_LEVEL=INFO                    # DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY
AKEYLESS_VERIFY_SSL=true          # SSL certificate verification (true/false)
```

### **Configuration Notes**

- **API URL Format**: Must end with `/akeyless-api/v2/`
- **SSL Verification**: Set to `false` only for self-signed certificates in development
- **Log Levels**: Use `DEBUG` for troubleshooting, `INFO` for production, `WARNING`/`ERROR` for critical operations
- **Access Credentials**: Store securely, never commit to version control

### **Security Best Practices**

- Use environment-specific credentials for different deployments
- Rotate access keys regularly
- Monitor API access logs for suspicious activity
- Use network segmentation to limit API access

## 🚀 Usage

### **Quick Start Example**

```bash
# 1. Start the server in stdio mode (for AI assistants)
python main.py

# 2. Or start in HTTP mode for API access
python main.py --transport streamable-http --port 8000

# 3. Test the health endpoint (HTTP mode only)
curl http://localhost:8000/health
```

### **Transport Modes**

- **stdio (default)**: Direct integration with MCP clients like Claude Desktop and Cursor
- **HTTP**: RESTful API access for automation, monitoring, and integration

### Health Monitoring

When running in HTTP mode, the server provides a health check endpoint:

```bash
# Check server health
curl http://localhost:8000/health

# Response includes:
# - Server status and version
# - MCP protocol versions
# - Available tools count
# - Configuration status
# - Connectivity information

# Test with curl
curl http://localhost:8000/health
```

### **Available Tools**

#### **Secrets Management** (`manage_secrets`)
- **Create secrets**: Static, dynamic, and rotated secrets with format validation
- **Update secrets**: Modify values and properties including delete protection
- **Delete secrets**: Smart deletion with directory support and DFC key handling
- **List secrets**: Browse and search secret collections with pagination

#### **DFC Key Management** (`manage_dfc_keys`)
- **Create DFC keys**: AES and RSA encryption keys with comprehensive options
- **Auto-rotation**: Automatic key rotation for AES keys (7-365 day intervals)
- **Certificate generation**: Self-signed X.509 certificates with configurable parameters
- **Key state management**: Enable/disable keys and manage lifecycle

#### **Authentication & Access** (`manage_auth`)
- **API key management**: Create and manage API keys for automation
- **Customer fragments**: Manage customer fragment access and permissions
- **Role-based access**: Integrate with CipherTrust Manager access controls

#### **Additional Tools**
- **Rotation Management**: Configure and monitor secret rotation schedules
- **Security Guidelines**: Access security best practices and compliance information

## 🔧 Development

### **Project Structure**
```
src/
├── core/           # Core client and configuration management
├── server/         # MCP server implementation and transport layers
├── tools/          # Tool implementations and business logic
│   ├── secrets/    # Secret management tools and validation
│   ├── dfc_keys/   # DFC key management and encryption
│   ├── auth/       # Authentication and access management
│   ├── rotation/   # Secret rotation and lifecycle
│   └── customer_fragments/  # Customer fragment management
└── tests/          # Test suite and validation
```

### **Technology Stack**
- **FastMCP**: Modern, production-ready MCP server framework
- **Async/await**: Full asynchronous support for high-performance operations
- **Type hints**: Comprehensive type annotations for maintainability
- **Error handling**: User-friendly error messages with actionable guidance
- **Configuration**: Pydantic-based config management with environment variable support
- **Logging**: Structured logging with rotation and multiple output formats

### Logging
The server provides comprehensive logging with both console and file output:
- **Log Levels**: DEBUG, INFO, NOTICE, WARNING, ERROR, CRITICAL, ALERT, EMERGENCY (configurable via `LOG_LEVEL` env var)
- **Log Files**: Stored in `logs/thales-csm-mcp.log` with automatic rotation
- **Rotation**: 10MB max per file, keeping 5 backup files
- **Format**: Timestamp, logger name, level, and message
- **MCP Compliance**: Full MCP protocol logging with level filtering and notifications

### Adding New Tools
1. Create tool class in `src/tools/`
2. Implement required methods
3. Register with MCP server
4. Add to documentation

## 🏢 Enterprise Features

### **Security & Compliance**
- **SOC2 Type II Ready**: Built with enterprise security standards
- **ISO27001 Compatible**: Follows information security best practices
- **Audit Trail**: Comprehensive logging for compliance and forensics
- **Access Control**: Role-based permissions through CipherTrust Manager

### **Scalability & Performance**
- **High Availability**: Designed for enterprise-scale deployments
- **Load Balancing**: HTTP transport supports multiple instances
- **Performance Monitoring**: Built-in health checks and metrics
- **Resource Optimization**: Efficient memory and CPU usage

### **Integration & Automation**
- **CI/CD Ready**: API endpoints for automation workflows
- **Monitoring Integration**: Health endpoints for monitoring systems
- **Multi-Environment**: Support for dev, staging, and production
- **Backup & Recovery**: Integrates with enterprise backup solutions

## 📚 Documentation

- [Tools Reference](docs/TOOLS.md) - Comprehensive tool documentation and examples
- [Transport Modes](docs/TRANSPORT_MODES.md) - Available transport configurations
- [Documentation Directory](docs/README.md) - Overview of all documentation files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### **Getting Help**

- **Documentation**: Start with the [Tools Reference](docs/TOOLS.md) and [Transport Modes](docs/TRANSPORT_MODES.md)
- **Issues**: Check existing [GitHub Issues](https://github.com/sanyambassi/thales-cdsp-csm-mcp-server/issues)
- **Discussions**: Use [GitHub Discussions](https://github.com/sanyambassi/thales-cdsp-csm-mcp-server/discussions) for questions

### **Reporting Issues**

When creating an issue, please include:
- **Environment**: OS, Python version, CipherTrust Manager version
- **Configuration**: Relevant environment variables (masked)
- **Error Details**: Full error messages and stack traces
- **Steps to Reproduce**: Clear sequence of actions
- **Expected vs Actual**: What you expected vs what happened

### **Enterprise Support**

For enterprise customers:
- **Thales Support**: Contact your Thales representative
- **Professional Services**: Available through Thales consulting
- **Training**: Custom training and implementation support

## 🔗 Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Thales CipherTrust](https://ciphertrust.com/)
- [Akeyless Vault](https://www.akeyless.io/)
- [FastMCP](https://github.com/jlowin/fastmcp) 