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
            action: str = Field(description="Account administration action to perform. SUPPORTED ACTIONS: 'get' (retrieve complete account configuration, licensing details, organizational settings, and system-wide policies)"),
            json: bool = Field(default=False, description="Return structured JSON format for administrative reporting and configuration management. Use TRUE for automated compliance reporting and system integration"),
            uid_token: Optional[str] = Field(default=None, description="Universal identity authentication token. Only required when using universal_identity authentication instead of standard API key authentication")
        ) -> Dict[str, Any]:
            """
            ACCOUNT ADMINISTRATION TOOL - Manage organizational settings and governance
            
            SUPPORTED ACTIONS:
            • get: Retrieve complete account configuration, licensing details, and system-wide policies
            
            ACCOUNT INFORMATION PROVIDED:
            • Organizational details and company profile
            • Licensing and subscription tier information
            • Service tier, SLA level, and feature availability
            • Usage quotas, capacity limits, and billing details
            • System configuration and security policies
            • Governance, compliance, and audit settings
            • Multi-tenant configuration and access controls
            
            USE CASES:
            • Account setup and initial configuration
            • Compliance and audit preparation
            • License management and planning
            • Security policy review and updates
            • Service tier evaluation and upgrades
            • Multi-tenant administration
            
            Example: Review account licensing and compliance configuration
            """
            try:
                if action == "get":
                    return await self._get_account_settings(
                        ctx,
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
                await self.dual_log(ctx, "error", f"Failed to manage account: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while managing account"
                }

    async def _get_account_settings(
        self,
        ctx,
        json: bool = False,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get account settings and licensing information."""
        # Dual logging: Server-side + MCP protocol
        await self.dual_log(ctx, "info", f"Starting operation: get account settings")
        
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