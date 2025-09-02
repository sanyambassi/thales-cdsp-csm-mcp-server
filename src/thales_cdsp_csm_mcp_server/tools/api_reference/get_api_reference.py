"""
Thales CDSP CSM MCP Server - API Reference Tools (OPTIMIZED VERSION)

This module provides tools for getting API references to build native Akeyless integrations.
Now optimized with a clean, modular structure.
"""

import logging
from typing import Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient

# Import from modular structure
from .references import (
    get_auth_reference,
    get_create_secret_reference,
    get_get_secret_reference,
    get_generic_workflow_reference,
    get_list_items_reference,
    get_list_roles_reference,
    get_list_targets_reference,
    get_delete_item_reference,
    get_codebase_scan_reference,
    get_secret_migration_reference
)
from .data.response_formats import get_response_formats
from .data.best_practices import get_best_practices

logger = logging.getLogger(__name__)


class GetAPIReferenceTools(BaseThalesCDSPCSMTool):
    """Tools for getting API references to build native Akeyless integrations."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_get_api_reference(server)

    def _register_get_api_reference(self, server: FastMCP):
        @server.tool("get_api_reference")
        async def get_api_reference(
            ctx: Context,
            api_endpoint: str = Field(description="API endpoint or integration pattern to get reference for. SUPPORTED: 'workflow' (complete integration patterns), 'auth' (authentication flows), 'create-secret' (secret creation), 'get-secret-value' (secret retrieval), 'list-items' (item listing), 'delete-item' (item deletion), 'list-roles' (role management), 'list-targets' (target management)"),
            language: str = Field(default="python", description="Target programming language for code examples and implementation details"),
            include_auth: bool = Field(default=True, description="Include complete authentication workflow and token management examples"),
            include_error_handling: bool = Field(default=True, description="Include production-ready error handling, retry logic, and exception management")
        ) -> Dict[str, Any]:
            """
            API REFERENCE TOOL - Generate production-ready code examples and integration patterns
            
            SUPPORTED ENDPOINTS:
            • workflow: Complete integration patterns and best practices
            • auth: Authentication flows and token management
            • create-secret: Secret creation and management APIs
            • get-secret-value: Secret retrieval and access patterns
            • list-items: Item listing and discovery APIs
            • delete-item: Item deletion and cleanup operations
            • list-roles: Role management and access control
            • list-targets: Target management and configuration
            
            INTEGRATION FEATURES:
            • Production-ready code examples with authentication
            • Complete error handling and retry logic
            • Best practices for secure integration patterns
            • Multi-language support (Python, JavaScript, etc.)
            • Token management and session handling
            
            USE CASES:
            • Building custom applications and integrations
            • CI/CD pipeline integration and automation
            • Microservice authentication and configuration
            • Native client development and SDK creation
            • Production system integration and deployment
            
            Example: Generate complete Python client code for secret management
            """
            
            # Dual logging: Server-side + MCP protocol
            await self.dual_log(ctx, "info", f"Getting API reference for endpoint: {api_endpoint} (language: {language})")
            
            try:
                # Handle workflow requests
                if api_endpoint.lower() in ["workflow", "generic_workflow", "core_workflow"]:
                    result = get_generic_workflow_reference(language, include_auth, include_error_handling)
                    await self.dual_log(ctx, "info", f"Generated workflow reference for {language}")
                    return result
                
                # Handle specific API endpoints
                endpoint_refs = {
                    "auth": get_auth_reference(language, include_error_handling),
                    "create-secret": get_create_secret_reference(language, include_error_handling),
                    "get-secret-value": get_get_secret_reference(language, include_error_handling),
                    "list-items": get_list_items_reference(language, include_error_handling),
                    "delete-item": get_delete_item_reference(language, include_error_handling),
                    "list-roles": get_list_roles_reference(language, include_error_handling),
                    "list-targets": get_list_targets_reference(language, include_error_handling),
                    "codebase-scan": get_codebase_scan_reference(language, include_error_handling),
                    "secret-migration": get_secret_migration_reference(language, include_error_handling)
                }
                
                if api_endpoint.lower() in endpoint_refs:
                    result = endpoint_refs[api_endpoint.lower()]
                    await self.dual_log(ctx, "info", f"Generated API reference for {api_endpoint} in {language}")
                    return result
                
                # Return general reference if endpoint not found
                result = self._get_general_reference(language, include_auth, include_error_handling)
                await self.dual_log(ctx, "info", f"Generated general API reference for {language}")
                return result
                
            except Exception as e:
                await self.dual_log(ctx, "error", f"Failed to generate API reference for {api_endpoint}: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to generate API reference for endpoint: {api_endpoint}"
                }
    
    def _get_general_reference(self, language: str, include_auth: bool, include_error_handling: bool) -> Dict[str, Any]:
        """Get general API reference information."""
        
        response_formats = get_response_formats()
        best_practices = get_best_practices()
        
        return {
            "title": "Akeyless Secrets Manager API Reference",
            "description": "Complete reference for native Akeyless integrations",
            "🚨 CRITICAL API BEHAVIOR": response_formats["get_secret_value"]["🚨 CRITICAL WARNING"],
            "base_url": "https://your-akeyless-endpoint",
            "authentication": {
                "method": "API Key Authentication",
                "endpoint": "/auth",
                "required_fields": ["access-id", "access-key"],
                "response": "Returns JWT token for subsequent requests",
                "token_usage": "Include token in request body, not Authorization header"
            },
            "common_endpoints": [
                "/auth - Authentication endpoint",
                "/create-secret - Create secrets",
                "/get-secret-value - Retrieve secrets", 
                "/list-items - List secrets manager items",
                "/delete-item - Delete individual items",
                "/delete-items - Bulk delete items",
                "/list-roles - List roles and permissions",
                "/target-list - List connection targets"
            ],
            "mcp_tool_actions": [
                "create_static_secret - Create static secrets via MCP tool",
                "get_static_secret_value - Get static secret values via MCP tool",
                "create_dynamic_secret_ldap - Create LDAP dynamic secrets via MCP tool",
                "create_dynamic_secret_mysql - Create MySQL dynamic secrets via MCP tool",
                "create_dynamic_secret_mongodb - Create MongoDB dynamic secrets via MCP tool",
                "get_dynamic_secret - Get dynamic secret metadata via MCP tool",
                "get_dynamic_secret_value - Get dynamic secret values via MCP tool"
            ],
            "workflows": [
                "workflow or generic_workflow - Core Akeyless integration patterns"
            ],
            "supported_languages": ["python"],
            "best_practices": [
                "Store credentials in environment variables",
                "Implement proper error handling and retry logic",
                "Use token caching to avoid repeated authentication",
                "Always use HTTPS for API calls",
                "Implement proper logging for audit trails"
            ],
            "when_to_use_mcp_vs_api": [
                "Use MCP tools (manage_secrets) for: AI assistant development, app modification, secret creation during development",
                "Use direct API calls for: Runtime secret retrieval, custom applications, CI/CD pipelines, production integrations",
                "MCP tools provide: Simplified interface, built-in validation, consistent error handling",
                "Direct APIs provide: Full control, custom logic, performance optimization"
            ],
            "ai_assistant_guidance": best_practices["ai_assistant_guidance"],
            "🚨 CRITICAL BEST PRACTICES": best_practices["critical_best_practices"]
        } 