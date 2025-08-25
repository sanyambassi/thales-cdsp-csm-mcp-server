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