# Thales CSM MCP Server

Simple MCP server for Thales CipherTrust Secrets Management, powered by Akeyless.

## 🚀 **What It Does**

- **Secrets Management**: Create, read, update, delete secrets
- **Key Management**: DFC encryption keys (AES, RSA)
- **Authentication**: Access control and policies
- **Security**: Guidelines and best practices
- **MCP Protocol**: Model Context Protocol compliance

## ⚡ **Quick Start**

### **1. Install**
```bash
git clone https://github.com/sanyambassi/thales-cdsp-csm-mcp-server
cd thales-cdsp-csm-mcp-server
pip install -r requirements.txt
```

### **2. Configure**
Create `.env` file:
```env
AKEYLESS_ACCESS_ID=your_access_id
AKEYLESS_ACCESS_KEY=your_access_key
AKEYLESS_API_URL=https://your-ciphertrust-manager/akeyless-api/v2
LOG_LEVEL=INFO
```

### **3. Run**
```bash
# stdio mode
python main.py

# HTTP mode 
python main.py --transport streamable-http --host localhost --port 8000
```

## 🛠️ **Available Tools**

| Tool | Description |
|------|-------------|
| `manage_secrets` | Create, read, update, delete secrets |
| `manage_dfc_keys` | Manage encryption keys |
| `manage_auth` | Authentication and access control |
| `manage_rotation` | Secret rotation policies |
| `manage_customer_fragments` | Enhanced security features |
| `security_guidelines` | Security best practices |

## 🔍 **Test It**

```bash
# Run tests
python tests/run_tests.py

# Test health endpoint (HTTP mode)
curl http://localhost:8000/health
```

## 📚 **Documentation**

- **[TESTING.md](docs/TESTING.md)** - How to test
- **[TRANSPORT_MODES.md](docs/TRANSPORT_MODES.md)** - How to run
- **[TOOLS.md](docs/TOOLS.md)** - What tools do
- **[TESTING.md](docs/TESTING.md)** - Complete testing guide

## 🎯 **Use Cases**

- **AI Assistants**: Claude Desktop, Cursor AI
- **Web Applications**: REST API integration
- **Automation**: CI/CD, scripts, tools
- **Enterprise**: Secrets management, compliance

## 🤖 **AI Assistant Integration**

### **Claude Desktop**
```json
{
  "mcpServers": {
    "thales-csm": {
      "command": "python",
      "args": ["main.py", "--transport", "stdio"],
      "env": {
        "AKEYLESS_ACCESS_ID": "your_access_id_here",
        "AKEYLESS_ACCESS_KEY": "your_access_key_here",
        "AKEYLESS_API_URL": "https://your-ciphertrust-manager/akeyless-api/v2",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### **Cursor AI**
```json
{
  "mcpServers": {
    "thales-csm": {
      "command": "python",
      "args": ["main.py", "--transport", "stdio"],
      "env": {
        "AKEYLESS_ACCESS_ID": "your_access_id_here",
        "AKEYLESS_ACCESS_KEY": "your_access_key_here",
        "AKEYLESS_API_URL": "https://your-ciphertrust-manager/akeyless-api/v2",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### **Configuration Parameters**
- **`env`**: Environment variables for Akeyless authentication and logging
- **`command`**: Python executable to run the server
- **`args`**: Command line arguments for the server (must include `--transport stdio` for MCP clients)

### **⚠️ Important Notes**
- **Full Path Required**: `args` must include the full absolute path to `main.py`
- **Windows Paths**: Use double backslashes `\\` in Windows paths (e.g., `C:\\thales-cdsp-csm-mcp-server\\main.py`)
- **Unix Paths**: Use forward slashes `/` in Unix/Linux paths (e.g., `/home/user/akeyless-secrets-vault/main.py`)

### **Configuration Templates**
- **[config/mcp-config-uv.json](config/mcp-config-uv.json)** - UV package manager setup
- **[config/mcp-config.json](config/mcp-config.json)** - Basic configuration template

## ⚙️ **Requirements**

- Python 3.10+
- Thales CipherTrust Manager access
- Valid Akeyless credentials

## 🤝 **Support**

- **Issues**: [GitHub Issues](https://github.com/sanyambassi/thales-cdsp-csm-mcp-server/issues)
- **Documentation**: Check the docs folder above

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

