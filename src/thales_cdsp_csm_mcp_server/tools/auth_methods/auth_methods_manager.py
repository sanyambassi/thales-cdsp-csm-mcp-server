"""
Thales CDSP CSM MCP Server - Authentication Methods Manager

This module provides the main manager that orchestrates all authentication method types
and provides a unified tool interface.
"""

from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient
from .api_key_auth_method import ApiKeyAuthMethod
from .email_auth_method import EmailAuthMethod
from .common_operations import CommonAuthOperations


class AuthMethodsManager(BaseThalesCDSPCSMTool):
    """Main manager for all authentication method types."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)
        self.api_key = ApiKeyAuthMethod(client, self.logger)
        self.email = EmailAuthMethod(client, self.logger)
        self.common = CommonAuthOperations(client, self.logger)
    
    def register(self, server: FastMCP):
        self._register_manage_auth_methods(server)
    
    def _register_manage_auth_methods(self, server: FastMCP):
        @server.tool("manage_auth_methods")
        async def manage_auth_methods(
            ctx: Context,
            action: str = Field(description="Authentication method management action to perform. SUPPORTED ACTIONS: 'create_api_key' (create API key authentication), 'create_email' (create email authentication), 'list' (list all authentication methods), 'get' (retrieve specific auth method details), 'update' (modify auth method properties), 'delete' (delete individual auth method), 'delete_auth_methods' (bulk delete auth methods by path)"),
            name: Optional[str] = Field(default=None, description="Authentication method name (required for create_api_key, update, delete, get)"),
            new_name: Optional[str] = Field(default=None, description="New name for the authentication method (for update action)"),
            path: Optional[str] = Field(default=None, description="Path for bulk operations (required for delete_auth_methods)"),
            # API Key specific parameters
            access_expires: Optional[int] = Field(default=0, description="Access expiration date in Unix timestamp (0 for no expiry)"),
            audit_logs_claims: List[str] = Field(default_factory=list, description="Subclaims to include in audit logs"),
            bound_ips: List[str] = Field(default_factory=list, description="CIDR whitelist for IP restrictions"),
            delete_protection: Optional[str] = Field(default=None, description="Protection from accidental deletion [true/false]"),
            description: Optional[str] = Field(default=None, description="Auth Method description"),
            expiration_event_in: List[str] = Field(default_factory=list, description="Days before expiration to be notified"),
            force_sub_claims: bool = Field(default=True, description="Enforce role-association must include sub claims"),
            gw_bound_ips: List[str] = Field(default_factory=list, description="CIDR whitelist for Gateway IP restrictions"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            jwt_ttl: Optional[int] = Field(default=0, description="JWT TTL"),
            product_type: List[str] = Field(default_factory=list, description="Product type for auth method [sm, sra, pm, dp, ca]"),
            # Email specific parameters
            email: Optional[str] = Field(default=None, description="Email address for email authentication method"),
            enable_mfa: Optional[str] = Field(default=None, description="Enable MFA for this authentication method [True/False]"),
            mfa_type: str = Field(default="email", description="Enable two-factor-authentication via [email/auth app]"),
            # List specific parameters
            filter: Optional[str] = Field(default=None, description="Filter by auth method name or part of it"),
            pagination_token: Optional[str] = Field(default=None, description="Next page reference"),
            type: List[str] = Field(default_factory=list, description="Auth method types to filter by [api_key, azure_ad, oauth2/jwt, saml2, ldap, aws_iam, oidc, universal_identity, gcp, k8s, cert]"),
            # General parameters
            accessibility: str = Field(default="regular", description="Accessibility level"),
            tags: List[str] = Field(default_factory=list, description="List of tags attached to this object")
        ) -> Dict[str, Any]:
            """
            AUTHENTICATION METHODS MANAGEMENT TOOL - Create, manage, and secure authentication methods
            
            SUPPORTED ACTIONS:
            • create_api_key: Create API key authentication methods with IP restrictions and expiration
            • create_email: Create email-based authentication methods with MFA support
            • list: List all authentication methods with filtering and pagination
            • get: Retrieve detailed authentication method configuration and status
            • update: Modify authentication method properties, credentials, and settings
            • delete: Delete individual authentication methods with proper cleanup
            • delete_auth_methods: Bulk delete authentication methods within a specific path
            
            SECURITY FEATURES:
            • IP address restrictions and CIDR whitelisting
            • Access expiration and JWT TTL management
            • Multi-factor authentication (MFA) support
            • Audit logging and compliance tracking
            • Delete protection and access control
            
            Example: Create a secure API key for application authentication
            """
            # Dual logging: Server-side + MCP protocol
            await self.dual_log(ctx, "info", f"Starting authentication method operation: {action}")
            
            try:
                if action == "create_api_key":
                    if not name:
                        return {
                            "success": False,
                            "error": "Authentication method name is required for create_api_key action",
                            "message": "Please provide a name for the authentication method"
                        }
                    return await self.api_key.create(name, 
                        access_expires=access_expires, audit_logs_claims=audit_logs_claims,
                        bound_ips=bound_ips, delete_protection=delete_protection,
                        description=description, expiration_event_in=expiration_event_in,
                        force_sub_claims=force_sub_claims, gw_bound_ips=gw_bound_ips,
                        json=json, jwt_ttl=jwt_ttl, product_type=product_type,
                        accessibility=accessibility, tags=tags
                    )
                elif action == "create_email":
                    if not name:
                        return {
                            "success": False,
                            "error": "Authentication method name is required for create_email action",
                            "message": "Please provide a name for the authentication method"
                        }
                    if not email:
                        return {
                            "success": False,
                            "error": "Email address is required for create_email action",
                            "message": "Please provide an email address for the authentication method"
                        }
                    return await self.email.create(name, email, 
                        access_expires=access_expires, audit_logs_claims=audit_logs_claims,
                        bound_ips=bound_ips, delete_protection=delete_protection,
                        description=description, enable_mfa=enable_mfa, expiration_event_in=expiration_event_in,
                        force_sub_claims=force_sub_claims, gw_bound_ips=gw_bound_ips,
                        json=json, jwt_ttl=jwt_ttl, mfa_type=mfa_type, product_type=product_type,
                        accessibility=accessibility, tags=tags
                    )
                elif action == "update":
                    if not name:
                        return {
                            "success": False,
                            "error": "Authentication method name is required for update action",
                            "message": "Please provide a name for the authentication method"
                        }
                    return await self.api_key.update(
                        name=name, new_name=new_name, access_expires=access_expires,
                        audit_logs_claims=audit_logs_claims, bound_ips=bound_ips,
                        delete_protection=delete_protection, description=description,
                        expiration_event_in=expiration_event_in, force_sub_claims=force_sub_claims,
                        gw_bound_ips=gw_bound_ips, json=json, jwt_ttl=jwt_ttl,
                        product_type=product_type, accessibility=accessibility, tags=tags
                    )
                elif action == "delete":
                    if not name:
                        return {
                            "success": False,
                            "error": "Authentication method name is required for delete action",
                            "message": "Please provide a name for the authentication method"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting deletion of authentication method: {name}")
                    return await self._smart_delete_auth_method(ctx, name, json)
                elif action == "delete_auth_methods":
                    if not path:
                        return {
                            "success": False,
                            "error": "Path is required for delete_auth_methods action",
                            "message": "Please provide a path to delete all authentication methods from"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting bulk deletion of authentication methods from path: {path}")
                    return await self._smart_delete_auth_methods(ctx, path, json)
                elif action == "list":
                    return await self.common.list(ctx, filter, json, pagination_token, type)
                elif action == "get":
                    if not name:
                        return {
                            "success": False,
                            "error": "Authentication method name is required for get action",
                            "message": "Please provide a name for the authentication method"
                        }
                    return await self.common.get(ctx, name, json)
                else:
                    return {
                        "success": False,
                        "error": f"Unsupported action: {action}",
                        "message": f"Supported actions: create_api_key, create_email, update, delete, delete_auth_methods, list, get"
                    }
            except Exception as e:
                await self.dual_log(ctx, "error", f"Failed to {action} auth method '{name}' - Error: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to {action} auth method '{name}'"
                }
    
    async def _smart_delete_auth_method(self, ctx: Context, name: str, json: bool = False) -> Dict[str, Any]:
        """
        Smart delete logic for authentication methods that handles:
        1. Individual auth method deletion
        2. Directory deletion (if name ends with /)
        """
        try:
            await self.report_progress(ctx, 25, 100, f"Analyzing authentication method: {name}")
            
            # Check if this looks like a directory (ends with /)
            if name.endswith('/'):
                await self.dual_log(ctx, "info", f"Smart delete: Detected directory path '{name}'")
                await self.report_progress(ctx, 50, 100, f"Processing directory deletion for: {name}")
                return await self._delete_auth_methods_directory(ctx, name, json)
            else:
                await self.dual_log(ctx, "info", f"Smart delete: Detected individual auth method '{name}'")
                await self.report_progress(ctx, 50, 100, f"Processing individual deletion for: {name}")
                return await self.common.delete(ctx, name, json)
                
        except Exception as e:
            await self.dual_log(ctx, "error", f"Smart delete auth method failed for '{name}' - Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Smart delete auth method operation failed for '{name}'"
            }
    
    async def _smart_delete_auth_methods(self, ctx: Context, path: str, json: bool = False) -> Dict[str, Any]:
        """
        Smart delete logic for bulk auth method deletion that handles:
        1. Directory deletion with proper cleanup
        2. Error handling and reporting
        """
        try:
            await self.dual_log(ctx, "info", f"Smart delete auth methods: Starting bulk deletion for path '{path}'")
            await self.report_progress(ctx, 25, 100, f"Starting bulk deletion for path: {path}")
            return await self._delete_auth_methods_directory(ctx, path, json)
                
        except Exception as e:
            await self.dual_log(ctx, "error", f"Smart delete auth methods failed for path '{path}' - Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Smart delete auth methods operation failed for path '{path}'"
            }
    
    async def _delete_auth_methods_directory(self, ctx: Context, path: str, json: bool = False) -> Dict[str, Any]:
        """
        Enhanced directory deletion for authentication methods with proper error handling.
        """
        try:
            # Normalize path
            normalized_path = path.rstrip('/')
            await self.dual_log(ctx, "info", f"Deleting auth methods directory: {normalized_path}")
            await self.report_progress(ctx, 50, 100, f"Processing directory: {normalized_path}")
            
            # First, try to list what's in the directory to provide better feedback
            try:
                await self.report_progress(ctx, 60, 100, f"Scanning directory contents: {normalized_path}")
                list_result = await self.common.list(ctx, filter=normalized_path, json=json)
                if list_result.get("success") and list_result.get("data"):
                    await self.dual_log(ctx, "info", f"Found auth methods in directory: {normalized_path} - Count: {len(list_result.get('data', []))}")
            except Exception as list_error:
                await self.dual_log(ctx, "warning", f"Could not list auth methods in directory: {normalized_path} - Error: {str(list_error)}")
            
            # Perform the bulk deletion
            await self.report_progress(ctx, 80, 100, f"Executing bulk deletion for: {normalized_path}")
            result = await self.common.delete_auth_methods(ctx, normalized_path, json)
            
            if result.get("success"):
                await self.report_progress(ctx, 100, 100, f"Successfully deleted directory: {normalized_path}")
                await self.dual_log(ctx, "info", f"Successfully deleted auth methods directory: {normalized_path}")
            else:
                await self.dual_log(ctx, "error", f"Failed to delete auth methods directory: {normalized_path} - Error: {result.get('error')}")
            
            return result
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Directory deletion failed for auth methods: {normalized_path} - Error: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete auth methods directory '{normalized_path}'"
            } 