# Testing Guide - Thales CSM Akeyless Vault MCP Server

This guide covers both manual and automated testing for the MCP server.

## 🧪 **Testing Overview**

The server supports two transport modes, each requiring different testing approaches:
- **stdio Transport**: Test with MCP clients (Claude Desktop, Cursor)
- **HTTP Transport**: Test with HTTP requests (curl, Postman, web apps)

## 🚀 **Manual Testing**

### **Prerequisites**
- Python 3.10+ installed
- Dependencies installed (`uv sync` or `pip install -r requirements.txt`)
- Valid Thales CSM Akeyless Vault credentials
- Network access to Thales API

### **Environment Setup**
Create a `.env` file with your credentials:
```bash
AKEYLESS_API_URL=https://api.akeyless.io
AKEYLESS_ACCESS_ID=your_access_id_here
AKEYLESS_ACCESS_KEY=your_access_key_here
```

### **Testing stdio Transport**

#### 1. Start Server
```bash
# Using uv (recommended)
uv run python main.py --transport stdio

# Using pip
python main.py --transport stdio
```

**Expected Behavior**: Server starts silently, waiting for MCP client connection.

#### 2. Test with MCP Client
Configure your MCP client (Claude Desktop, Cursor) with:
```json
{
  "mcpServers": {
    "thales-akeyless": {
      "command": "python",
      "args": ["/path/to/akeyless-secrets-vault/main.py", "--transport", "stdio"],
      "env": {
        "AKEYLESS_ACCESS_ID": "your_access_id",
        "AKEYLESS_ACCESS_KEY": "your_access_key"
      }
    }
  }
}
```

### **Testing HTTP Transport**

#### 1. Start HTTP Server
```bash
# Using uv
uv run python main.py --transport streamable-http --host 0.0.0.0 --port 8000

# Using pip
python main.py --transport streamable-http --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
🚀 Starting Thales CSM Akeyless Vault MCP Server...
✅ Server started successfully on http://localhost:8000
```

#### 2. Test HTTP Endpoints

**List Available Tools**:
```bash
curl -X POST http://localhost:8000/tools/list
```

**Create a Test Secret**:
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "create_static_secret",
    "arguments": {
      "name": "test/secret",
      "value": "test-value",
      "description": "Test secret"
    }
  }'
```

**List Items**:
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_items",
    "arguments": {
      "path": "test/"
    }
  }'
```

**Get Secret Value**:
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_secret",
    "arguments": {
      "names": ["test/secret"]
    }
  }'
```

**Delete Test Secret**:
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "delete_item",
    "arguments": {
      "name": "test/secret"
    }
  }'
```

## 🤖 **Automated Testing**

### **Running Test Suite**
```bash
# Using uv
uv run python -m pytest tests/

# Using pip
python -m pytest tests/
```

### **Test Coverage**
```bash
# Install pytest-cov
uv add pytest-cov

# Run with coverage
uv run python -m pytest tests/ --cov=src/ --cov-report=html
```

### **Test Structure**
```
tests/
├── test_server.py      # Server functionality tests
├── test_client.py      # Thales API client tests
├── test_tools.py       # Tool functionality tests
└── conftest.py         # Test configuration
```

## 🔍 **Test Scenarios**

### **1. Basic Functionality**
- [ ] Server starts without errors
- [ ] Tools are properly registered
- [ ] HTTP endpoints respond correctly
- [ ] stdio mode works with MCP clients

### **2. Secret Management**
- [ ] Create secrets with various formats
- [ ] List items from different directories
- [ ] Get secret values successfully
- [ ] Delete items individually and in bulk
- [ ] Path normalization works correctly

### **3. Error Handling**
- [ ] Invalid credentials handled gracefully
- [ ] Non-existent secrets return appropriate errors
- [ ] Missing parameters are validated
- [ ] Network errors handled properly

### **4. Performance**
- [ ] Auto-pagination works for large collections
- [ ] Concurrent requests handled properly
- [ ] Response times are reasonable

## 🧹 **Cleanup After Testing**

### **Remove Test Data**
```bash
# Delete test directory
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "delete_items",
    "arguments": {
      "path": "test/"
    }
  }'
```

### **Verify Cleanup**
```bash
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "name": "list_items",
    "arguments": {
      "path": "test/"
    }
  }'
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **Server Won't Start**
- Check Python version (3.10+ required)
- Verify dependencies are installed
- Check `.env` file configuration

#### **Authentication Failures**
- Verify credentials in `.env` file
- Check network connectivity to Thales API
- Ensure account has API access

#### **Tools Not Found**
- Restart server after configuration changes
- Check tool registration in server logs
- Verify MCP client configuration

#### **Path Resolution Issues**
- All paths are automatically normalized
- Use forward slashes (`/`) for path separators
- Check actual path being used in API calls

### **Debug Information**
When reporting issues, include:
```bash
# System information
python --version
uv --version  # or pip --version
uname -a      # Linux/Mac
systeminfo    # Windows

# Configuration (mask sensitive data)
echo "API URL: $AKEYLESS_API_URL"
echo "Access ID: ${AKEYLESS_ACCESS_ID:0:8}..."
echo "Access Key: ${AKEYLESS_ACCESS_KEY:0:8}..."

# Test results
python -m pytest tests/ -v 2>&1
```

## 📋 **Testing Checklist**

### **Pre-Testing**
- [ ] Environment variables configured
- [ ] Dependencies installed
- [ ] Network connectivity verified
- [ ] Test environment prepared

### **During Testing**
- [ ] All transport modes tested
- [ ] All tools validated
- [ ] Error conditions tested
- [ ] Performance verified

### **Post-Testing**
- [ ] Test data cleaned up
- [ ] Results documented
- [ ] Issues reported
- [ ] Environment restored

## 📚 **Related Documentation**

- [Root README](../README.md) - Project overview and setup
- [Transport Modes](TRANSPORT_MODES.md) - Transport configuration
- [Documentation Overview](README.md) - Available documentation 