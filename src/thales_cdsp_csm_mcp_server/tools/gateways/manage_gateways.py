"""
Thales CDSP CSM MCP Server - Gateway Management Tools

This module provides tools for managing Akeyless gateways.
"""

import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class ManageGatewaysTools(BaseThalesCDSPCSMTool):
    """Tools for managing Akeyless gateways."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_manage_gateways(server)

    def _register_manage_gateways(self, server: FastMCP):
        @server.tool("manage_gateways")
        async def manage_gateways(
            ctx: Context,
            action: str = Field(description="Gateway management action to perform. SUPPORTED ACTIONS: 'list' (list available gateways with detailed information and filtering)"),
            # List specific parameters
            path: Optional[str] = Field(default=None, description="Path to list gateways from (for list action)"),
            filter_by: Optional[str] = Field(default=None, description="Filter gateways by pattern (for list action)"),
            # General parameters
            json: bool = Field(default=False, description="Set output format to JSON")
        ) -> Dict[str, Any]:
            """
            GATEWAY MANAGEMENT TOOL - Monitor and manage gateway infrastructure
            
            SUPPORTED ACTIONS:
            • list: List available gateways with detailed information and filtering
            
            GATEWAY INFORMATION PROVIDED:
            • Gateway configuration and status
            • Connection details and endpoints
            • Performance metrics and health status
            • Access control and security settings
            • Integration and routing information
            
            USE CASES:
            • Gateway infrastructure monitoring
            • Connection troubleshooting and diagnostics
            • Performance analysis and optimization
            • Security configuration review
            • Gateway inventory and management
            
            Example: List all gateways to monitor infrastructure health
            """
            try:
                if action == "list":
                    return await self._list_gateways(path or "/", filter_by, json)
                else:
                    return {
                        "success": False,
                        "error": f"Unsupported action: {action}",
                        "message": f"Supported actions: list"
                    }
            except Exception as e:
                await self.dual_log(ctx, "error", f"Failed to {action} gateways - Error: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to {action} gateways"
                }

    async def _list_gateways(self, path: str, filter_by: Optional[str], json: bool) -> Dict[str, Any]:
        """List available gateways."""
        # Dual logging: Server-side + MCP protocol
        await self.dual_log(ctx, "info", f"Starting operation: {action}")
        
        try:
            # Prepare request data
            request_data = {
                "json": json
            }
            
            # Call the list-gateways endpoint
            result = await self.client.list_gateways(request_data)
            
            return {
                "success": True,
                "message": f"Gateways listed successfully from path: {path}",
                "data": {
                    "path": path,
                    "filter": filter_by,
                    "result": result
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to list gateways from path: {path}"
            } 