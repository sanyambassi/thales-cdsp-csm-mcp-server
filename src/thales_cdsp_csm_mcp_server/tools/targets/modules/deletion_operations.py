"""
Target Deletion Operations Module

This module handles all target deletion operations including individual
target deletion and bulk deletion by path.
"""

import logging
from typing import Dict, Any, Optional
from ...base import BaseThalesCDSPCSMTool
from ....core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class TargetDeletionOperations(BaseThalesCDSPCSMTool):
    """Handles target deletion operations."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client

    async def delete_target(self, ctx, name: str, force_deletion: bool = False, 
                          target_version: Optional[int] = None, json: bool = False,
                          uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Delete a single target using /target-delete endpoint."""
        await self.dual_log(ctx, "info", f"Starting operation: delete target '{name}'")
        
        try:
            # Prepare request data
            request_data = {
                "name": name,
                "force-deletion": force_deletion,
                "json": json
            }
            
            # Add optional fields if provided
            if target_version is not None:
                request_data["target-version"] = target_version
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call to delete target
            result = await self.client._make_request("target-delete", request_data)
            
            return {
                "success": True,
                "data": result,
                "message": f"Target '{name}' deleted successfully"
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to delete target '{name}'", {"error": str(e), "name": name})
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete target '{name}'"
            }

    async def delete_targets_by_path(self, ctx, path: str, force_deletion: bool = False,
                                   json: bool = False, uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Delete multiple targets in a path using /delete-targets endpoint."""
        await self.dual_log(ctx, "info", f"Starting operation: delete targets in path '{path}'")
        
        try:
            # Prepare request data
            request_data = {
                "path": path,
                "force-deletion": force_deletion,
                "json": json
            }
            
            # Add optional fields if provided
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call to delete targets by path
            result = await self.client._make_request("delete-targets", request_data)
            
            return {
                "success": True,
                "data": result,
                "message": f"Targets in path '{path}' deleted successfully"
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to delete targets in path '{path}'", {"error": str(e), "path": path})
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete targets in path '{path}'"
            } 