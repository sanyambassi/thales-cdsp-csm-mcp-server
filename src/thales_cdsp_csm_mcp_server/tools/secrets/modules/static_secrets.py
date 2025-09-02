"""
Static Secrets Management Module

This module handles all static secret operations including creation, retrieval, updates, and deletion.
"""

import logging
from typing import Dict, Any, Optional, List
from fastmcp import Context
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class StaticSecretsManager(BaseThalesCDSPCSMTool):
    """Manages static secrets operations."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    async def create_static_secret(self, ctx: Context, name: str, value: str, description: Optional[str] = None,
                                  tags: Optional[List[str]] = None, delete_protection: Optional[str] = None,
                                  format: str = "text", accessibility: str = "regular", protection_key: Optional[str] = None,
                                  custom_field: Optional[Dict[str, str]] = None, password: Optional[str] = None,
                                  username: Optional[str] = None, max_versions: Optional[int] = None,
                                  metadata: Optional[str] = None, multiline_value: bool = True,
                                  inject_url: Optional[List[str]] = None, change_event: bool = False) -> Dict[str, Any]:
        """Create a static secret."""
        await self.dual_log(ctx, "info", f"Creating static secret: {name}")
        
        try:
            request_data = {
                "name": name,
                "value": value,
                "json": True,
                "format": format,
                "accessibility": accessibility,
                "multiline_value": multiline_value,
                "change_event": change_event
            }
            
            if description:
                request_data["description"] = description
            if tags:
                request_data["tags"] = tags
            if delete_protection:
                request_data["delete-protection"] = delete_protection
            if protection_key:
                request_data["protection_key"] = protection_key
            if custom_field:
                request_data["custom_field"] = custom_field
            if password:
                request_data["password"] = password
            if username:
                request_data["username"] = username
            if max_versions:
                request_data["max_versions"] = max_versions
            if metadata:
                request_data["metadata"] = metadata
            if inject_url:
                request_data["inject_url"] = inject_url
            
            result = await self.client.create_static_secret(**request_data)
            await self.dual_log(ctx, "info", f"Static secret '{name}' created successfully")
            return {
                "success": True,
                "data": result,
                "message": f"Static secret '{name}' created successfully"
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to create static secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create static secret '{name}'"
            }
    
    async def get_static_secret_value(self, ctx: Context, name: str) -> Dict[str, Any]:
        """Get a static secret value."""
        await self.dual_log(ctx, "info", f"Retrieving static secret: {name}")
        
        try:
            result = await self.client.get_secret([name])
            await self.dual_log(ctx, "info", f"Static secret '{name}' retrieved successfully")
            return {
                "success": True,
                "message": f"Static secret '{name}' retrieved successfully",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to get static secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get static secret '{name}'"
            }
    
    async def update_static_secret(self, ctx: Context, name: str, new_name: Optional[str] = None,
                                  value: Optional[str] = None, description: Optional[str] = None,
                                  tags: Optional[List[str]] = None, format: str = "text",
                                  accessibility: str = "regular", protection_key: Optional[str] = None,
                                  custom_field: Optional[Dict[str, str]] = None, password: Optional[str] = None,
                                  username: Optional[str] = None, max_versions: Optional[int] = None,
                                  metadata: Optional[str] = None, multiline_value: bool = True,
                                  inject_url: Optional[List[str]] = None, change_event: bool = False,
                                  delete_protection: Optional[str] = None) -> Dict[str, Any]:
        """Update a static secret."""
        await self.dual_log(ctx, "info", f"Updating static secret: {name}")
        
        try:
            # Check if we need to update properties (not just the value)
            needs_property_update = any([
                delete_protection is not None,
                description is not None,
                tags is not None,
                accessibility is not None,
                protection_key is not None,
                max_versions is not None,
                metadata is not None,
                new_name is not None
            ])

            # If no value provided and no properties to update, return error
            if not value and not needs_property_update:
                return {
                    "success": False,
                    "error": "Either 'value' or property update parameters are required for update",
                    "message": "Please provide either a new value or properties to update (like delete_protection, description, etc.)"
                }

            if needs_property_update:
                # Use update_item for property updates (including delete_protection)
                result = await self.client.update_item(
                    name=name,
                    new_name=new_name,
                    description=description,
                    accessibility=accessibility,
                    delete_protection=delete_protection,
                    change_event=change_event,
                    max_versions=max_versions,
                    add_tags=tags if tags else None,
                    rm_tags=None,  # Not supported in current interface
                    json=False
                )
                
                # If value also changed, update it separately
                if value:
                    await self.client.update_secret_value(
                        name, value, accessibility,
                        custom_field, format,
                        inject_url or [], False,
                        None, None, 0, multiline_value,
                        password, username
                    )
                
                await self.dual_log(ctx, "info", f"Static secret '{name}' properties updated successfully")
                return {
                    "success": True,
                    "message": f"Secret '{name}' properties updated successfully",
                    "data": result
                }
            else:
                # Use update_secret_value for value-only updates (more efficient)
                result = await self.client.update_secret_value(
                    name, value, accessibility,
                    custom_field, format,
                    inject_url or [], False,
                    None, None, 0, multiline_value,
                    password, username
                )
                await self.dual_log(ctx, "info", f"Static secret '{name}' value updated successfully")
                return {
                    "success": True,
                    "message": f"Secret '{name}' value updated successfully",
                    "data": result
                }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to update static secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to update static secret '{name}'"
            }
    
    async def delete_static_secret(self, ctx: Context, name: str, delete_protection: Optional[str] = None) -> Dict[str, Any]:
        """Delete a static secret."""
        await self.dual_log(ctx, "info", f"Deleting static secret: {name}")
        
        try:
            # Check if delete protection is enabled
            if delete_protection:
                # First disable delete protection
                await self.client.update_item(
                    name=name,
                    delete_protection=False
                )
                await self.dual_log(ctx, "info", f"Delete protection disabled for: {name}")
            
            # Delete the secret
            result = await self.client.delete_item(name, "regular", True, -1, -1)
            await self.dual_log(ctx, "info", f"Static secret '{name}' deleted successfully")
            return {
                "success": True,
                "message": f"Static secret '{name}' deleted successfully",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to delete static secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete static secret '{name}'"
            } 