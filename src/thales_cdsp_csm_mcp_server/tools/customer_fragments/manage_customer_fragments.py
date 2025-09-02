"""
Thales CDSP CSM MCP Server - Consolidated Customer Fragments Management Tools

This module provides a unified tool for managing customer fragments
with action-based operations.
"""

import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class ManageCustomerFragmentsTools(BaseThalesCDSPCSMTool):
    """Consolidated tools for managing customer fragments."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_manage_customer_fragments(server)

    def _register_manage_customer_fragments(self, server: FastMCP):
        @server.tool("manage_customer_fragments")
        async def manage_customer_fragments(
            ctx: Context,
            action: str = Field(description="Customer fragment management action to perform. SUPPORTED ACTIONS: 'list' (list customer fragments with filtering), 'export' (export customer fragments), 'download' (download customer fragments - alias for export)"),
            # List specific parameters
            path: Optional[str] = Field(default=None, description="Path to list fragments from (for list action)"),
            filter_by: Optional[str] = Field(default=None, description="Filter fragments by pattern (for list action)"),
            # Export specific parameters
            json: bool = Field(default=False, description="Set output format to JSON (for export action)")
        ) -> Dict[str, Any]:
            """
            CUSTOMER FRAGMENT MANAGEMENT TOOL - Manage customer fragment encryption and security
            
            SUPPORTED ACTIONS:
            • list: List customer fragments with path filtering and pattern matching
            • export: Export customer fragments with optional JSON format
            • download: Download customer fragments (alias for export action)
            
            SECURITY FEATURES:
            • Customer fragment encryption for enhanced security
            • Access control and audit trails
            • Enterprise-grade fragment management
            • Compliance and security reporting
            
            USE CASES:
            • Customer fragment inventory and management
            • Security compliance and audit preparation
            • Fragment backup and export operations
            • Enhanced encryption key management
            
            Example: List and export customer fragments for security audit
            """
            try:
                if action == "list":
                    return await self._list_customer_fragments(path or "/", filter_by)
                elif action == "export":
                    return await self._export_customer_fragments(json)
                elif action == "download":
                    return await self._export_customer_fragments(json)
                else:
                    return {
                        "success": False,
                        "error": f"Unsupported action: {action}",
                        "message": f"Supported actions: list, export, download"
                    }
            except Exception as e:
                await self.dual_log(ctx, "error", f"Failed to {action} customer fragments - Error: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to {action} customer fragments"
                }

    async def _list_customer_fragments(self, path: str, filter_by: Optional[str]) -> Dict[str, Any]:
        """List customer fragments in a directory."""
        self.dual_log(ctx, "info", f"Listing customer fragments from path: {path}")
        result = await self.client.list_customer_fragments(json_output=False)
        self.dual_log(ctx, "info", f"Successfully listed customer fragments")
        return {
            "success": True,
            "message": f"Listed all customer fragments",
            "data": result
        }

    async def _export_customer_fragments(self, json: bool) -> Dict[str, Any]:
        """Export customer fragments."""
        self.dual_log(ctx, "info", f"Exporting customer fragments (JSON format: {json})")
        result = await self.client.export_customer_fragments(json)
        self.dual_log(ctx, "info", f"Successfully exported customer fragments")
        return {
            "success": True,
            "message": f"Exported customer fragments successfully",
            "data": result
        } 