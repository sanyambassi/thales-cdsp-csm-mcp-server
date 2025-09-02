# Testing Guide

Complete guide for testing the Thales CSM MCP Server.

## 🧪 **Quick Start**

### **1. Run Automated Tests**
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_mcp_protocol.py

# Run with verbose output
python -m pytest -v tests/

# Use the test runner script
python tests/run_tests.py
```

### **2. Manual Testing**

#### **stdio Transport**
```bash
# Start server
python main.py --transport stdio

# Test with MCP client (Claude Desktop, Cursor)
# Configure your MCP client to use this server
```

#### **HTTP Transport**
```bash
# Start server
python main.py --transport streamable-http --host localhost --port 8000

# Test health endpoint
curl http://localhost:8000/health
```

## 📋 **Essential Test Commands**

### **1. Protocol Initialization**
```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "id": 1,
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": {},
    "clientInfo": {"name": "Test Client", "version": "1.0.0"}
  }
}
```

### **2. Send Initialized Notification**
```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized",
  "params": {}
}
```

### **3. List Tools**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 3
}
```

### **4. List Prompts**
```json
{
  "jsonrpc": "2.0",
  "method": "prompts/list",
  "id": 4
}
```

### **5. Test Secret Operations**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 5,
  "params": {
    "name": "manage_secrets",
    "arguments": {
      "action": "list",
      "path": "/"
    }
  }
}
```

### **6. Test DFC Key Operations**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 6,
  "params": {
    "name": "manage_dfc_keys",
    "arguments": {
      "action": "list"
    }
  }
}
```

## 🔍 **Expected Results**

- **Health endpoint**: Shows server status, tools, and prompts
- **Tools list**: Returns available tools (count varies based on configuration)
- **Prompts list**: Returns all available prompts
- **Tool calls**: Return success/error responses

## ⚠️ **Important Notes**

- Always initialize before calling tools
- Use unique `id` for each request
- Check error responses for debugging
- Ensure Akeyless credentials are configured

## 🧪 **Test Workflow**

1. Start server
2. Send initialization
3. List tools and prompts
4. Test specific tool operations
5. Check responses

## 📋 **Test Files**

- **`tests/test_mcp_protocol.py`** - MCP protocol compliance tests
- **`tests/run_tests.py`** - Simple test runner script

## ✅ **What Gets Tested**

- MCP protocol compliance
- Tool functionality
- HTTP transport
- Health endpoints
- Error handling

## 🚀 **Prerequisites**

- Python 3.10+
- Dependencies installed (`pip install -r requirements.txt`)
- Valid Akeyless credentials in `.env` file

## 🔧 **Troubleshooting**

### **Common Issues**
- **Server won't start**: Check Python version and dependencies
- **Authentication failed**: Verify credentials in `.env` file
- **Tools not found**: Restart server after configuration changes
- **HTTP errors**: Check port availability and firewall settings