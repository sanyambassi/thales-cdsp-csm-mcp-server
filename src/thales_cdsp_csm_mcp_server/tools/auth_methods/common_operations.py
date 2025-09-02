"""
Thales CDSP CSM MCP Server - Common Authentication Method Operations

This module provides common operations that work across all authentication method types.
"""

from typing import List, Dict, Any, Optional

from ...core.client import ThalesCDSPCSMClient
from ..base import BaseThalesCDSPCSMTool


class CommonAuthOperations(BaseThalesCDSPCSMTool):
    """Common operations for all authentication method types."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client

    async def delete(self, ctx, name: str, json: bool = False) -> Dict[str, Any]:
        """Delete a specific authentication method."""
        await self.dual_log(ctx, "info", f"Deleting authentication method '{name}'")
        try:
            data = {
                "name": name,
                "json": json
            }
            
            result = await self.client.delete_auth_method(data)
            
            await self.dual_log(ctx, "info", f"Authentication method '{name}' deleted successfully")
            return {
                "success": True,
                "message": f"Authentication method '{name}' deleted successfully",
                "data": result
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to delete authentication method '{name}'", {"error": str(e), "name": name})
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete authentication method '{name}'"
            }
    
    async def delete_auth_methods(self, ctx, path: str, json: bool = False) -> Dict[str, Any]:
        """Delete all authentication methods within a specific path."""
        await self.dual_log(ctx, "info", f"Deleting authentication methods within path '{path}'")
        try:
            data = {
                "path": path,
                "json": json
            }
            
            result = await self.client.delete_auth_methods(data)
            
            await self.dual_log(ctx, "info", f"Authentication methods within path '{path}' deleted successfully")
            return {
                "success": True,
                "message": f"All authentication methods within path '{path}' deleted successfully",
                "data": result
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to delete authentication methods within path '{path}'", {"error": str(e), "path": path})
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete authentication methods within path '{path}'"
            }
    
    async def list(self, ctx, filter: Optional[str] = None, json: bool = False,
                   pagination_token: Optional[str] = None, type: List[str] = None) -> Dict[str, Any]:
        """List all authentication methods."""
        await self.dual_log(ctx, "info", f"Listing authentication methods (filter: {filter})")
        
        try:
            data = {"json": json}
            
            # Add optional parameters if provided
            if filter:
                data["filter"] = filter
            if pagination_token:
                data["pagination-token"] = pagination_token
            if type:
                data["type"] = type
            
            result = await self.client.list_auth_methods(data)
            
            await self.dual_log(ctx, "info", f"Authentication methods listed successfully")
            return {
                "success": True,
                "message": f"Authentication methods listed successfully",
                "data": result
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to list authentication methods", {"error": str(e)})
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to list authentication methods"
            }
    
    async def get(self, ctx, name: str, json: bool = False) -> Dict[str, Any]:
        """Get authentication method details."""
        await self.dual_log(ctx, "info", f"Getting authentication method details: {name}")
        
        try:
            data = {
                "name": name,
                "json": json
            }
            
            result = await self.client.get_auth_method(data)
            
            await self.dual_log(ctx, "info", f"Authentication method '{name}' retrieved successfully")
            return {
                "success": True,
                "message": f"Authentication method '{name}' retrieved successfully",
                "data": result
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to get authentication method '{name}'", {"error": str(e), "name": name})
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get authentication method '{name}'"
            } 