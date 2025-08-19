"""
Thales CDSP CSM MCP Server - Account Management Tools

This module provides tools for managing account settings and licensing in the Thales CSM Akeyless Vault.
"""

import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class ManageAccountTools(BaseThalesCDSPCSMTool):
    """Tools for managing account settings and licensing in the Thales CSM Akeyless Vault."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_manage_account(server)

    def _register_manage_account(self, server: FastMCP):
        @server.tool("manage_account")
        async def manage_account(
            ctx: Context,
            action: str = Field(description="⚙️ ACCOUNT MANAGEMENT: Action to perform: 'get'"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            uid_token: Optional[str] = Field(default=None, description="The universal identity token, Required only for universal_identity authentication")
        ) -> Dict[str, Any]:
            """
            ⚙️ ACCOUNT MANAGEMENT TOOL
            
            🏆 ENTERPRISE-GRADE ACCOUNT ADMINISTRATION: 
            - Thales CipherTrust Secrets Management (CSM) with Akeyless Vault
            - Account settings and licensing information
            - SLA and tier level details
            
            📋 AVAILABLE OPERATIONS:
            - get: Get account settings and licensing information
            
            📊 ACCOUNT INFORMATION INCLUDES:
            - Company details and contact information
            - Licensing tier and SLA levels
            - Product-specific settings and limits
            - Version control policies
            - System access configuration
            - Security and sharing policies
            
            Example: Get account settings and licensing details
            """
            try:
                if action == "get":
                    return await self._get_account_settings(
                        json=json,
                        uid_token=uid_token
                    )
                else:
                    return {
                        "success": False,
                        "error": f"Invalid action: {action}",
                        "message": "Supported actions: 'get'"
                    }
            except Exception as e:
                await self.hybrid_log(ctx, "error", f"Failed to manage account: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while managing account"
                }

    async def _get_account_settings(
        self,
        json: bool = False,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get account settings and licensing information."""
        try:
            # Prepare request data
            request_data = {
                "json": json
            }
            
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call
            response = await self.client._make_request("get-account-settings", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": "Account settings retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to get account settings: {e}")
            raise e 