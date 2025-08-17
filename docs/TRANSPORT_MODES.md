# Transport Modes

The MCP server supports multiple transport modes for different use cases with **Thales CipherTrust Secrets Management (CSM)**, powered by Akeyless Vault technology.

## 🚀 Available Transports

### stdio (Default)
**Use Case**: MCP client integration (Claude Desktop, Cursor, etc.)
**Features**: Direct communication, no network exposure, automatic tool discovery

```bash
# Start with stdio transport
python main.py

# Or explicitly specify
python main.py --transport stdio
```

### HTTP (streamable-http)
**Use Case**: Web applications, API testing, remote access, monitoring
**Features**: RESTful HTTP endpoints, network accessible, health monitoring, tool for testing

```bash
# Start HTTP server
python main.py --transport streamable-http --port 8000

# Custom host and port
python main.py --transport streamable-http --host 127.0.0.1 --port 9000
```



## ⚙️ Configuration Options

### Command Line Arguments
- `--transport`: Transport mode (stdio, streamable-http)
- `--host`: Host address (default: 0.0.0.0)
- `--port`: Port number (default: 8000 for HTTP)
- `--help`: Show help and available options

### Environment Variables
```env
MCP_TRANSPORT=http
MCP_HOST=0.0.0.0
MCP_PORT=8000
```

## 🔒 Security Considerations

### stdio Transport
- ✅ **Most Secure**: No network exposure
- ✅ **Local Only**: Direct process communication
- ✅ **Automatic**: No configuration needed

### HTTP Transport
- ⚠️ **Network Accessible**: Configure firewall rules
- ⚠️ **Authentication**: Consider adding auth middleware
- ✅ **Flexible**: Multiple client support



## 🏥 Health Monitoring

### Health Check Endpoint
When running in HTTP mode, the server provides a health check endpoint for monitoring and load balancer integration:

```bash
# Check server health
curl http://localhost:8000/health

# Response includes:
# - Server status and version
# - MCP protocol versions supported
# - Available tools count and names
# - Configuration status
# - Connectivity information
```

**Example Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-15 14:30:00",
  "server": {
    "name": "Thales CipherTrust Secrets Management MCP Server",
    "version": "1.0.0",
    "transport_mode": "streamable-http"
  },
  "mcp_protocol": {
    "latest": "2025-06-18",
    "backward": "2025-03-26",
    "supported_versions": ["2025-06-18", "2025-03-26"]
  },
  "tools": {
    "count": 6,
    "available": ["manage_secrets", "manage_dfc_keys", "manage_auth", "manage_rotation", "manage_customer_fragments", "security_guidelines"]
  },
  "configuration": {
    "status": "configured",
    "api_url_configured": true,
    "access_id_configured": true,
    "access_key_configured": true
  },
  "connectivity": {
    "client_status": "connected",
    "api_url": "https://your-cm-hostname/akeyless-api/v2/"
  }
}
```

## 📱 Client Integration

### MCP Clients (stdio)
```json
{
  "mcpServers": {
    "ciphertrust-csm": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/akeyless-secrets-vault"
    }
  }
}
```

### HTTP Clients
```bash
# Test with curl
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "manage_secrets", "arguments": {"action": "list"}}'
```



## 🚨 Troubleshooting

### Common Issues
- **Port Already in Use**: Change port number or stop conflicting service
- **Permission Denied**: Run with appropriate permissions or change port
- **Connection Refused**: Check firewall settings and host configuration



## 🏢 Enterprise Integration

This MCP server is designed for enterprise environments using **Thales CipherTrust Secrets Management**:

- **CipherTrust Manager**: Integrates with your existing CipherTrust infrastructure
- **Enterprise Security**: Built on proven enterprise security platform
- **Akeyless Technology**: Leverages Akeyless Vault technology for modern secrets management
- **Professional Support**: Enterprise support through Thales

## 📚 Next Steps

- **Getting Started**: See main [README.md](../README.md)
- **API Reference**: See [docs/README.md](README.md)
- **Examples**: Check the main README for usage examples 