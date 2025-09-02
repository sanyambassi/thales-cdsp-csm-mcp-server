#!/usr/bin/env python3
"""
Akeyless MCP Server Prompts

Actionable prompt templates for AI assistants to execute Akeyless operations.
"""

from fastmcp import Context
from pydantic import Field


async def get_account_summary(ctx: Context = None) -> str:
    """Get comprehensive account summary from Akeyless vault."""
    
    return """Use the manage_account tool to get account overview.

Execute this workflow:
1. Call manage_account with action='get'
2. The tool will retrieve comprehensive account information
3. Return account details including:
   - Company profile and contact information
   - Licensing and SLA details
   - Product settings and configuration
   - Security policies and access controls
   - System-wide configuration settings

This provides a complete view of your Akeyless account status and configuration."""


async def get_account_analytics(ctx: Context = None) -> str:
    """Get comprehensive analytics and monitoring data from Akeyless vault."""
    
    return """Use the manage_analytics tool to get usage analytics.

Execute this workflow:
1. Call manage_analytics with action='get'
2. The tool will retrieve comprehensive monitoring data
3. Return analytics including:
   - Item counts by type (Secrets, Targets, Keys, etc.)
   - Geographic distribution and access patterns
   - Request volumes and performance metrics
   - Certificate status and risk assessment
   - Multi-product usage statistics

This provides insights into your Akeyless infrastructure usage and health."""


async def create_auth_api_key(
    auth_method_name: str = Field(description="Name for the authentication method in Linux path format (e.g., /folder1/folder2/auth_method)"),
    ctx: Context = None
) -> str:
    """Create a new API key authentication method in Akeyless vault."""
    
    return f"""Use the manage_auth_methods tool to create a new API key authentication method.

Execute this workflow:
1. Call manage_auth_methods with action='create_api_key'
2. Set parameters:
   - name: '{auth_method_name}'
3. The tool will create the authentication method
4. Return the new auth method details and credentials

This establishes a new API key authentication method named '{auth_method_name}' in your Akeyless vault."""


async def create_auth_email(
    auth_method_name: str = Field(description="Name for the authentication method in Linux path format (e.g., /folder1/folder2/auth_method)"),
    email_address: str = Field(description="Email address for the authentication method"),
    ctx: Context = None
) -> str:
    """Create a new email-based authentication method in Akeyless vault."""
    
    return f"""Use the manage_auth_methods tool to create a new email-based authentication method.

Execute this workflow:
1. Call manage_auth_methods with action='create_email'
2. Set parameters:
   - name: '{auth_method_name}'
   - email: '{email_address}'
3. The tool will create the authentication method
4. Return the new auth method details and credentials

This establishes a new email-based authentication method named '{auth_method_name}' with email '{email_address}' in your Akeyless vault."""


async def develop_or_secure_app(
        app_context: str = Field(description="Context about the app - either 'new app' description or 'existing app' details to secure. For new apps, describe the app type, purpose, and requirements. For existing apps, provide details about the codebase to secure."),
        ctx: Context = None
    ) -> str:
    """Intelligently develop a new app or secure an existing app with CipherTrust integration."""
    
    return f"""🔐 INTELLIGENT APP DEVELOPMENT & SECURITY MIGRATION PROMPT

This prompt will automatically determine whether you're creating a NEW app or securing an EXISTING app, then provide the appropriate solution.

📋 APP CONTEXT PROVIDED:
{app_context}

🎯 INTELLIGENT DETECTION LOGIC:

The AI assistant will analyze your request and determine the scenario:

1. **NEW APP CREATION** - If you mention:
   - "create", "build", "develop", "new app", "start from scratch"
   - No existing codebase context
   - Building something completely new

2. **EXISTING APP SECURITY** - If you mention:
   - "secure", "migrate", "existing", "current app", "hardcoded secrets"
   - Reference to existing code or files
   - Want to move secrets to CipherTrust

🔄 EXECUTION WORKFLOW:

**For NEW APP CREATION:**
1. Use get_api_reference tool with api_endpoint='workflow'
2. Generate complete Python implementation (default language)
3. Create application structure with CipherTrust integration
4. Provide setup and testing instructions

**For EXISTING APP SECURITY:**
1. Scan codebase for hardcoded secrets using intelligent detection
2. Infer programming language from codebase structure
3. Categorize secrets by type (key-value pairs vs standalone)
4. Use manage_secrets tool to create CipherTrust secrets
5. Generate migration report and updated code
6. Provide testing and validation instructions

🔍 SECRET DETECTION PATTERNS:

The AI will scan for:
- Environment variables (os.getenv, process.env)
- Hardcoded strings with keywords (key, secret, password, token, api_key)
- Configuration files (.env, config.json, settings.py)
- Database connection strings
- API credentials and endpoints

📊 SECRET TYPE CLASSIFICATION:

**Key-Value Pairs (JSON format):**
- AWS: access_key_id + secret_access_key
- Database: username + password + host + port
- OAuth: client_id + client_secret
- API: api_key + api_secret

**Standalone Secrets (Text format):**
- Single passwords
- Individual tokens
- Connection strings
- Certificate data

🚀 NEXT STEPS:

The AI assistant will now:
1. Analyze your request to determine the scenario
2. Execute the appropriate workflow
3. Provide comprehensive implementation or migration solution
4. Include testing and validation instructions

This ensures you get exactly what you need - whether building a new secure app or migrating existing secrets to enterprise-grade security with CipherTrust.""" 