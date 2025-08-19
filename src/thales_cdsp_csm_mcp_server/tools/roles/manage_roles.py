"""
Thales CDSP CSM MCP Server - Roles Management Tools

This module provides tools for managing roles in the Thales CSM Akeyless Vault.
"""

import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class ManageRolesTools(BaseThalesCDSPCSMTool):
    """Tools for managing roles in the Thales CSM Akeyless Vault."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_manage_roles(server)

    def _register_manage_roles(self, server: FastMCP):
        @server.tool("manage_roles")
        async def manage_roles(
            ctx: Context,
            action: str = Field(description="🔐 ROLES MANAGEMENT: Action to perform: 'list', 'get'"),
            name: Optional[str] = Field(default=None, description="Role name (required for get action)"),
            filter: Optional[str] = Field(default=None, description="Filter by role name or part of it (for list action)"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            pagination_token: Optional[str] = Field(default=None, description="Next page reference (for list action)"),
            uid_token: Optional[str] = Field(default=None, description="The universal identity token, Required only for universal_identity authentication")
        ) -> Dict[str, Any]:
            """
            🔐 ROLES MANAGEMENT TOOL
            
            🏆 ENTERPRISE-GRADE ROLE MANAGEMENT: 
            - Thales CipherTrust Secrets Management (CSM) with Akeyless Vault
            - Enterprise-grade role management with access control and audit trails
            
            📋 AVAILABLE OPERATIONS:
            - list: List all roles with optional filtering
            - get: Get details of a specific role
            
            Example: List all roles or get specific role details
            """
            try:
                if action == "list":
                    return await self._list_roles(
                        filter=filter,
                        json=json,
                        pagination_token=pagination_token,
                        uid_token=uid_token
                    )
                elif action == "get":
                    if not name:
                        return {
                            "success": False,
                            "error": "Role name is required for get action",
                            "message": "Please provide a name for the role"
                        }
                    return await self._get_role(
                        name=name,
                        json=json,
                        uid_token=uid_token
                    )
                else:
                    return {
                        "success": False,
                        "error": f"Invalid action: {action}",
                        "message": "Supported actions: 'list', 'get'"
                    }
            except Exception as e:
                await self.hybrid_log(ctx, "error", f"Failed to manage roles: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while managing roles"
                }

    async def _list_roles(
        self,
        filter: Optional[str] = None,
        json: bool = False,
        pagination_token: Optional[str] = None,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List roles in the Thales CSM Akeyless Vault."""
        try:
            # Prepare request data
            request_data = {
                "json": json
            }
            
            if filter:
                request_data["filter"] = filter
            if pagination_token:
                request_data["pagination-token"] = pagination_token
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call
            response = await self.client._make_request("list-roles", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": "Roles retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to list roles: {e}")
            raise e

    async def _get_role(
        self,
        name: str,
        json: bool = False,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get details of a specific role."""
        try:
            # Prepare request data
            request_data = {
                "name": name,
                "json": json
            }
            
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call
            response = await self.client._make_request("get-role", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": f"Role '{name}' retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to get role '{name}': {e}")
            raise e 