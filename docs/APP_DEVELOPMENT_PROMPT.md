# App Development & Security Migration Prompt

## Overview

The `develop_or_secure_app` prompt is an intelligent prompt that automatically determines whether you want to create a new app or secure an existing one, then provides the appropriate solution with full CipherTrust integration.

## 🎯 **How It Works**

### **Intelligent Detection**
The AI assistant analyzes your request and automatically determines the scenario:

1. **NEW APP CREATION** - Detected when you mention:
   - "create", "build", "develop", "new app", "start from scratch"
   - No existing codebase context
   - Building something completely new

2. **EXISTING APP SECURITY** - Detected when you mention:
   - "secure", "migrate", "existing", "current app", "hardcoded secrets"
   - Reference to existing code or files
   - Want to move secrets to CipherTrust

## 🚀 **Usage Examples**

### **Example 1: Creating a New App**

**User Request:**
```
"I want to create a new Flask web application that connects to a PostgreSQL database. 
The app should use CipherTrust for managing database credentials and API keys."
```

**AI Assistant Response:**
1. **Detects**: New app creation (keywords: "create", "new", "Flask")
2. **Action**: Uses `get_api_reference` tool with `api_endpoint='workflow'`
3. **Output**: Complete Python Flask implementation with CipherTrust integration
4. **Includes**: Database connection, secret management, error handling, testing instructions

### **Example 2: Securing an Existing App**

**User Request:**
```
"I have an existing Python application with hardcoded database passwords and API keys. 
I want to migrate these secrets to CipherTrust for better security."
```

**AI Assistant Response:**
1. **Detects**: Existing app security (keywords: "existing", "hardcoded", "migrate")
2. **Action**: Scans codebase for secrets, then uses `manage_secrets` MCP tool
3. **Output**: Secret migration plan, CipherTrust secret creation, updated code
4. **Includes**: Migration report, testing instructions, security improvements

## 📋 **Prompt Parameters**

```python
async def develop_or_secure_app(
    app_description: str,           # Description of app to create/secure
    app_language: str = "python",   # Programming language (currently Python)
    app_framework: str = "",        # Framework (e.g., Flask, FastAPI, Django)
    deployment_environment: str = "", # Environment (local, cloud, container)
    ctx: Context = None
) -> str:
```

### **Parameter Details**

- **`app_description`** (required): Detailed description of what you want to build or secure
- **`app_language`** (optional): Programming language (defaults to Python)
- **`app_framework`** (optional): Framework if applicable
- **`deployment_environment`** (optional): Where the app will run

## 🔄 **Execution Workflows**

### **New App Creation Workflow**

1. **Use `get_api_reference` tool** with `api_endpoint='workflow'`
2. **Generate complete Python implementation** with CipherTrust integration
3. **Create application structure** with proper secret management
4. **Provide setup and testing instructions**

### **Existing App Security Workflow**

1. **Scan codebase** for hardcoded secrets using intelligent detection
2. **Categorize secrets** by type (key-value pairs vs standalone)
3. **Use `manage_secrets` MCP tool** to create CipherTrust secrets
4. **Generate migration report** with secret mappings
5. **Update code** to use CipherTrust secrets at runtime
6. **Provide testing and validation instructions**

## 🔍 **Secret Detection Patterns**

The AI automatically scans for:

### **Environment Variables**
- `os.getenv()`, `os.environ.get()`, `process.env`, `getenv()`
- `Environment.GetEnvironmentVariable()`, `System.getenv()`

### **Hardcoded Secrets**
- `password`, `secret`, `key`, `token`, `api_key`, `access_key`
- `client_secret`, `private_key`, `certificate`, `credential`

### **Configuration Files**
- `.env`, `config.json`, `settings.py`, `config.py`, `secrets.py`
- `application.properties`, `web.config`, `app.config`

### **Database Connections**
- `mysql://`, `postgresql://`, `mongodb://`, `sqlite://`
- `jdbc:`, `connection_string`, `connection_url`

### **API Endpoints**
- `https://api.`, `http://`, `endpoint`, `base_url`, `api_url`

## 📊 **Secret Type Classification**

### **Key-Value Pairs (JSON Format)**
- **AWS Credentials**: `access_key_id` + `secret_access_key` + `region`
- **Database Credentials**: `username` + `password` + `host` + `port` + `database`
- **OAuth Credentials**: `client_id` + `client_secret` + `redirect_uri`
- **API Credentials**: `api_key` + `api_secret` + `api_url`
- **JWT Credentials**: `jwt_secret` + `jwt_algorithm` + `jwt_expiry`

### **Standalone Secrets (Text Format)**
- Single passwords
- Individual tokens
- Connection strings
- Certificate data
- Encryption keys
- Webhook secrets

## 🛠️ **Tools Used**

### **For New Apps**
- **`get_api_reference`**: Provides complete API integration patterns
- **`manage_secrets`**: Creates initial secrets for the new app

### **For Existing Apps**
- **Codebase Scanner**: Detects hardcoded secrets
- **`manage_secrets`**: Creates CipherTrust secrets
- **Migration Tools**: Updates code and generates reports

## 📝 **Example Outputs**

### **New App Creation Output**
```json
{
  "workflow": "Flask Web Application with CipherTrust Integration",
  "description": "Complete Flask app with database connection and secret management",
  "complete_implementation": {
    "app.py": "# Complete Flask application code...",
    "requirements.txt": "# Dependencies...",
    "config.py": "# Configuration management...",
    "database.py": "# Database connection with CipherTrust..."
  },
  "setup_instructions": [
    "1. Install dependencies: pip install -r requirements.txt",
    "2. Set CipherTrust credentials in environment variables",
    "3. Run the application: python app.py"
  ],
  "testing_instructions": [
    "1. Test database connection",
    "2. Verify secret retrieval",
    "3. Test error handling scenarios"
  ]
}
```

### **Existing App Security Output**
```json
{
  "migration_report": {
    "secrets_found": 5,
    "secrets_migrated": 5,
    "migration_status": "completed"
  },
  "ciphertrust_secrets": {
    "/apps/myapp/prod/database-credentials": "JSON secret with username, password, host, port",
    "/apps/myapp/prod/api-credentials": "JSON secret with api_key, api_secret",
    "/apps/myapp/prod/jwt-secret": "Text secret with JWT signing key"
  },
  "updated_code": {
    "database.py": "# Updated to use CipherTrust secrets...",
    "config.py": "# Updated configuration..."
  },
  "next_steps": [
    "Test all secret retrieval paths",
    "Remove hardcoded secrets from source code",
    "Update deployment scripts"
  ]
}
```

## 🎯 **Best Practices**

### **For New Apps**
- Start with CipherTrust integration from day one
- Use environment variables for CipherTrust credentials only
- Implement proper error handling and logging
- Test secret retrieval thoroughly

### **For Existing Apps**
- Scan incrementally, starting with high-risk files
- Group related secrets logically
- Test thoroughly after migration
- Remove hardcoded secrets completely
- Document the new secret management process

## 🚨 **Important Notes**

### **AI Assistant Guidelines**
- **Use MCP tools** for secret creation during development
- **Never bake secret creation** into production applications
- **Separate development-time** operations from runtime operations
- **Provide comprehensive testing** instructions

### **Security Considerations**
- Store CipherTrust credentials in environment variables only
- Use HTTPS for all API calls
- Implement proper access controls
- Rotate secrets regularly
- Monitor access patterns

## 🔧 **Troubleshooting**

### **Common Issues**
- **Prompt not detected**: Ensure clear language about creating vs securing
- **Secrets not found**: Check file extensions and excluded directories
- **Migration failures**: Verify CipherTrust credentials and permissions
- **Code not updated**: Ensure proper file paths and permissions

### **Getting Help**
- Check the generated migration reports for detailed information
- Use the `manage_secrets` tool to verify secret creation
- Test secret retrieval before removing hardcoded values
- Review the generated code for proper integration patterns

## 🚀 **Getting Started**

1. **Describe your app** clearly (new or existing)
2. **Provide context** about what you want to build or secure
3. **Let the AI determine** the appropriate workflow
4. **Follow the generated instructions** step by step
5. **Test thoroughly** before deploying to production

This prompt provides a complete solution for both app development and security migration, ensuring your applications are secure by design or properly secured through migration. 