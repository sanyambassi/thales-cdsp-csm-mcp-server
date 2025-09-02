"""
Deletion Operations Module for Secret Management

This module handles all deletion-related operations including smart delete, bulk deletion, and DFC key handling.
"""

import logging
from typing import Dict, Any, Optional, List
from fastmcp import Context
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class DeletionOperations(BaseThalesCDSPCSMTool):
    """Handles all deletion operations for secrets."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    async def _smart_delete(self, ctx: Context, name: Optional[str], items: List[str], delete_immediately: bool, delete_in_days: int, version: int) -> Dict[str, Any]:
        """
        Smart delete logic that handles all deletion scenarios:
        1. Individual item deletion
        2. Multiple items deletion
        3. Directory deletion (with DFC key and delete protection handling)
        """
        try:
            # Validate parameters
            if not name and not items:
                return {
                    "success": False,
                    "error": "Either 'name' or 'items' must be provided",
                    "message": "Please provide either a single item name or a list of items to delete"
                }
            
            if name and items:
                return {
                    "success": False,
                    "error": "Cannot specify both 'name' and 'items'",
                    "message": "Please use either 'name' for single item/directory or 'items' for multiple items"
                }

            # Case 1: Multiple items deletion
            if items:
                await self.dual_log(ctx, "info", f"🚀 Smart delete: Multiple items deletion - {len(items)} items")
                return await self._delete_multiple_items(ctx, items, delete_immediately, delete_in_days, version)
            
            # Case 2: Single name provided - determine if it's an individual item or directory
            if name:
                await self.dual_log(ctx, "info", f"🚀 Smart delete: Analyzing '{name}' to determine deletion strategy...")
                return await self._delete_single_or_directory(ctx, name, delete_immediately, delete_in_days, version)

        except Exception as e:
            await self.dual_log(ctx, "error", f"Smart delete failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Smart delete operation failed"
            }

    async def _delete_multiple_items(self, ctx: Context, items: List[str], delete_immediately: bool, delete_in_days: int, version: int) -> Dict[str, Any]:
        """Delete multiple items using bulk delete_items API."""
        await self.dual_log(ctx, "info", f"Starting bulk deletion of {len(items)} items")
        
        try:
            if not items:
                return {
                    "success": False,
                    "error": "No items provided for deletion",
                    "message": "Please provide a list of items to delete"
                }
            
            result = await self.client.delete_items(items=items)
            await self.dual_log(ctx, "info", f"Successfully deleted {len(items)} items using bulk API")
            return {
                "success": True,
                "message": f"Successfully deleted {len(items)} items",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Bulk deletion failed: {e}")
            await self.dual_log(ctx, "info", "🔄 Falling back to individual deletion strategy...")
            return await self._delete_items_individually(ctx, items, delete_immediately, delete_in_days, version)

    async def _delete_single_or_directory(self, ctx: Context, name: str, delete_immediately: bool, delete_in_days: int, version: int) -> Dict[str, Any]:
        """Determine if name is an individual item or directory and delete accordingly."""
        try:
            # Normalize path for consistent handling (remove trailing slash for directory detection)
            normalized_name = name.rstrip('/')
            
            # Check for ALL items (secrets, DFC keys, etc.) to properly detect directory content
            all_items_result = await self._list_all_items_internal(ctx, normalized_name)
            has_content = self._check_directory_content(all_items_result)
            
            if has_content:
                return await self._delete_directory_smart(ctx, normalized_name, delete_immediately)
            else:
                return await self._delete_individual_item(ctx, name, delete_immediately, delete_in_days, version)
                
        except Exception as e:
            return await self._delete_individual_item(ctx, name, delete_immediately, delete_in_days, version)

    async def _delete_directory_smart(self, ctx: Context, path: str, delete_immediately: bool) -> Dict[str, Any]:
        """
        Smart directory deletion with DFC key and delete protection handling.
        Based on the old implementation's enhanced proactive strategy.
        """
        try:
            await self.dual_log(ctx, "info", f"📁 Starting enhanced directory deletion for: {path}")
            normalized_path = path.rstrip('/')
            errors = []
            warnings = []
            dfc_keys_deleted = 0
            protected_items = []
            
            # Step 1: Find and handle DFC keys (they can only be deleted with delete_item)
            await self.dual_log(ctx, "info", f"🔍 Step 1: Scanning for DFC keys in '{normalized_path}'...")
            dfc_keys = await self._discover_dfc_keys_in_directory(ctx, normalized_path)
            
            if dfc_keys:
                await self.dual_log(ctx, "info", f"🔐 Found {len(dfc_keys)} DFC keys: {dfc_keys}")
                for dfc_key in dfc_keys:
                    try:
                        await self.dual_log(ctx, "info", f"🔑 Deleting DFC key: {dfc_key}")
                        
                        # Check if DFC key has delete protection enabled
                        try:
                            # Try to get item details to check delete protection
                            list_result = await self.client.list_items(
                                path=dfc_key.rsplit('/', 1)[0] if '/' in dfc_key else '/', 
                                filter_by=dfc_key.rsplit('/', 1)[-1] if '/' in dfc_key else dfc_key
                            )
                            
                            if list_result and 'items' in list_result and list_result['items']:
                                item = list_result['items'][0]
                                if item.get('delete_protection'):
                                    protected_items.append(dfc_key)
                                    warnings.append(f"DFC key '{dfc_key}' has delete protection enabled - skipping")
                                    await self.dual_log(ctx, "warning", f"⚠️ DFC key '{dfc_key}' has delete protection enabled - skipping")
                                    continue
                        except Exception as check_error:
                            await self.dual_log(ctx, "warning", f"Could not check delete protection for '{dfc_key}': {check_error}")
                        
                        # Delete the DFC key
                        await self.client.delete_item(
                            dfc_key,
                            accessibility="regular",
                            delete_immediately=delete_immediately,
                            delete_in_days=1 if not delete_immediately else -1
                        )
                        dfc_keys_deleted += 1
                        await self.dual_log(ctx, "info", f"✅ DFC key '{dfc_key}' deleted successfully")
                    except Exception as e:
                        error_msg = f"Failed to delete DFC key '{dfc_key}': {e}"
                        errors.append(error_msg)
                        await self.dual_log(ctx, "error", f"❌ {error_msg}")
            else:
                await self.dual_log(ctx, "info", "🔐 No DFC keys found in directory")
            
            # Step 1.5: Also check for any other items that might need special handling
            await self.dual_log(ctx, "info", f"🔍 Step 1.5: Scanning for all items in '{normalized_path}'...")
            all_items_result = await self.client.list_items(normalized_path, True)
            await self.dual_log(ctx, "info", f"📊 Total items found in directory: {all_items_result}")
            
            # Step 2: Try bulk directory deletion
            await self.dual_log(ctx, "info", f"🗂️ Step 2: Attempting bulk directory deletion...")
            try:
                result = await self.client.delete_items(path=normalized_path)
                
                # Prepare success message with details
                success_msg = f"Directory '{normalized_path}' deleted successfully"
                if dfc_keys_deleted > 0:
                    success_msg += f" ({dfc_keys_deleted} DFC keys processed)"
                if protected_items:
                    success_msg += f" ({len(protected_items)} protected items skipped)"
                if errors:
                    success_msg += f" (with {len(errors)} errors)"
                
                return {
                    "success": True,
                    "message": success_msg,
                    "data": result,
                    "details": {
                        "dfc_keys_deleted": dfc_keys_deleted,
                        "protected_items_skipped": len(protected_items),
                        "errors": errors if errors else None,
                        "warnings": warnings if warnings else None
                    }
                }
            except Exception as e:
                error_msg = f"Bulk directory deletion failed: {e}"
                errors.append(error_msg)
                await self.dual_log(ctx, "error", f"❌ {error_msg}")
                
                return {
                    "success": False,
                    "error": "Directory deletion failed",
                    "message": f"Failed to delete directory '{normalized_path}'. Errors: {'; '.join(errors)}",
                    "details": {
                        "dfc_keys_deleted": dfc_keys_deleted,
                        "protected_items_skipped": len(protected_items),
                        "errors": errors,
                        "warnings": warnings if warnings else None
                    }
                }
                
        except Exception as e:
            await self.dual_log(ctx, "error", f"Smart directory deletion failed for '{path}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Smart directory deletion failed for '{path}'"
            }

    async def _delete_individual_item(self, ctx: Context, name: str, delete_immediately: bool, delete_in_days: int, version: int) -> Dict[str, Any]:
        """Delete a single individual item."""
        await self.dual_log(ctx, "info", f"📄 Deleting individual item: '{name}'")
        
        try:
            result = await self.client.delete_item(name, "regular", delete_immediately, delete_in_days, version)
            await self.dual_log(ctx, "info", f"Item '{name}' deleted successfully")
            return {
                "success": True,
                "message": f"Item '{name}' deleted successfully",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to delete item '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to delete item '{name}'"
            }

    async def _delete_items_individually(self, ctx: Context, items: List[str], delete_immediately: bool, delete_in_days: int, version: int) -> Dict[str, Any]:
        """Fallback: Delete items one by one when bulk deletion fails."""
        if not items:
            return {
                "success": False,
                "error": "No items provided for individual deletion",
                "message": "Please provide a list of items to delete"
            }
        
        await self.dual_log(ctx, "info", f"🔄 Deleting {len(items)} items individually as fallback...")
        deleted_count = 0
        errors = []
        
        for i, item in enumerate(items):
            try:
                # Report progress for each item
                await self.report_progress(ctx, i + 1, len(items), f"Deleting item {i + 1}/{len(items)}: {item}")
                await self.dual_log(ctx, "info", f"🗑️ Deleting item {i + 1}/{len(items)}: {item}")
                
                await self.client.delete_item(item, "regular", delete_immediately, delete_in_days, version)
                deleted_count += 1
                await self.dual_log(ctx, "info", f"✅ Individual deletion successful: {item}")
            except Exception as e:
                error_msg = f"Failed to delete '{item}': {e}"
                errors.append(error_msg)
                await self.dual_log(ctx, "error", f"❌ {error_msg}")
        
        if deleted_count == len(items):
            return {
                "success": True,
                "message": f"Successfully deleted all {deleted_count} items individually",
                "data": {"deleted_count": deleted_count}
            }
        elif deleted_count > 0:
            return {
                "success": True,
                "message": f"Partially successful: {deleted_count}/{len(items)} items deleted",
                "data": {"deleted_count": deleted_count, "errors": errors}
            }
        else:
            return {
                "success": False,
                "error": "All individual deletions failed",
                "message": f"Failed to delete any of the {len(items)} items. Errors: {'; '.join(errors[:3])}"
            }

    async def _smart_delete_directory_with_protection_handling(self, ctx: Context, directory_path: str, disable_protection: bool = True, force_delete: bool = False) -> Dict[str, Any]:
        """
        🧠 ENHANCED Smart Directory Deletion with Protection Management
        
        This method implements the user's requested smart deletion logic:
        1. List all contents of the directory (secrets and keys) 
        2. For each item with delete protection, disable it first
        3. Delete each DFC key individually (required by API)
        4. Delete the directory (secrets get deleted automatically)
        
        Args:
            directory_path: Directory path to delete
            disable_protection: Whether to automatically disable delete protection  
            force_delete: Whether to force deletion even with errors
            
        Returns:
            Dict with detailed deletion results
        """
        try:
            await self.dual_log(ctx, "info", f"🧠 Enhanced Smart Delete: Starting intelligent directory deletion for '{directory_path}'")
            normalized_path = directory_path.rstrip('/')
            
            # Step 1: Comprehensive directory content discovery
            await self.dual_log(ctx, "info", f"📋 Step 1: Discovering ALL contents in directory '{normalized_path}'...")
            
            # Get all items in directory (secrets, keys, folders)
            all_items_result = await self._list_all_items_internal(ctx, normalized_path)
            
            if not all_items_result or 'items' not in all_items_result:
                return {
                    "success": False,
                    "error": "Directory not found or empty",
                    "message": f"No items found in directory '{normalized_path}'"
                }
            
            items = all_items_result.get('items', [])
            
            # Categorize items by type
            secrets = []
            dfc_keys = []
            other_items = []
            protected_items = []
            
            for item in items:
                item_name = item.get('item_name', '')
                item_type = item.get('item_type', '')
                is_protected = item.get('delete_protection', False)
                
                await self.dual_log(ctx, "info", f"📄 Found item: '{item_name}' (type: {item_type}, protected: {is_protected})")
                
                if is_protected:
                    protected_items.append(item_name)
                
                if item_type == 'DFCKey':
                    dfc_keys.append(item_name)
                elif item_type in ['StaticSecret', 'DynamicSecret', 'RotatedSecret']:
                    secrets.append(item_name)
                else:
                    other_items.append(item_name)
            
            await self.dual_log(ctx, "info", f"📊 Directory Analysis:")
            await self.dual_log(ctx, "info", f"   🔐 {len(secrets)} secrets found: {secrets}")
            await self.dual_log(ctx, "info", f"   🔑 {len(dfc_keys)} DFC keys found: {dfc_keys}")
            await self.dual_log(ctx, "info", f"   📁 {len(other_items)} other items found: {other_items}")
            await self.dual_log(ctx, "info", f"   🛡️ {len(protected_items)} protected items found: {protected_items}")
            
            # Step 2: Handle delete protection automatically
            protection_disabled_count = 0
            protection_errors = []
            
            if protected_items and disable_protection:
                await self.dual_log(ctx, "info", f"🛡️ Step 2: Disabling delete protection for {len(protected_items)} items...")
                
                for protected_item in protected_items:
                    try:
                        await self.dual_log(ctx, "info", f"🔓 Disabling protection for: {protected_item}")
                        
                        # Update item to disable delete protection
                        await self.client.update_item(
                            name=protected_item,
                            delete_protection=False
                        )
                        protection_disabled_count += 1
                        await self.dual_log(ctx, "info", f"✅ Protection disabled for: {protected_item}")
                        
                    except Exception as e:
                        error_msg = f"Failed to disable protection for '{protected_item}': {e}"
                        protection_errors.append(error_msg)
                        await self.dual_log(ctx, "error", f"❌ {error_msg}")
            
            # Step 3: Delete DFC keys individually (API requirement)
            dfc_deletion_results = []
            dfc_errors = []
            
            if dfc_keys:
                await self.dual_log(ctx, "info", f"🔑 Step 3: Deleting {len(dfc_keys)} DFC keys individually...")
                
                for dfc_key in dfc_keys:
                    try:
                        await self.dual_log(ctx, "info", f"🗑️ Deleting DFC key: {dfc_key}")
                        
                        await self.client.delete_item(
                            name=dfc_key,
                            accessibility="regular",
                            delete_immediately=True,
                            delete_in_days=-1
                        )
                        dfc_deletion_results.append(dfc_key)
                        await self.dual_log(ctx, "info", f"✅ DFC key deleted: {dfc_key}")
                        
                    except Exception as e:
                        error_msg = f"Failed to delete DFC key '{dfc_key}': {e}"
                        dfc_errors.append(error_msg)
                        await self.dual_log(ctx, "error", f"❌ {error_msg}")
            
            # Step 4: Delete the directory (secrets are deleted automatically)
            await self.dual_log(ctx, "info", f"📁 Step 4: Deleting directory '{normalized_path}' (auto-removes remaining secrets)...")
            
            try:
                directory_result = await self.client.delete_items(path=normalized_path)
                
                # Prepare comprehensive success response
                total_items = len(items)
                success_message = f"🎉 Smart directory deletion completed for '{normalized_path}'"
                
                details = {
                    "directory_path": normalized_path,
                    "total_items_found": total_items,
                    "secrets_found": len(secrets),
                    "dfc_keys_found": len(dfc_keys),
                    "other_items_found": len(other_items),
                    "protection_disabled_count": protection_disabled_count,
                    "dfc_keys_deleted": len(dfc_deletion_results),
                    "directory_deletion": "successful",
                    "protection_errors": protection_errors if protection_errors else None,
                    "dfc_deletion_errors": dfc_errors if dfc_errors else None
                }
                
                # Add summary to message
                if protection_disabled_count > 0:
                    success_message += f" | 🔓 {protection_disabled_count} protections disabled"
                if len(dfc_deletion_results) > 0:
                    success_message += f" | 🔑 {len(dfc_deletion_results)} DFC keys deleted"
                if len(secrets) > 0:
                    success_message += f" | 🔐 {len(secrets)} secrets auto-deleted with directory"
                
                return {
                    "success": True,
                    "message": success_message,
                    "data": directory_result,
                    "details": details
                }
                
            except Exception as e:
                error_msg = f"Directory deletion failed: {e}"
                await self.dual_log(ctx, "error", f"❌ {error_msg}")
                
                return {
                    "success": False,
                    "error": "Directory deletion failed",
                    "message": f"Failed to delete directory '{normalized_path}' after processing {protection_disabled_count} protections and {len(dfc_deletion_results)} DFC keys. Error: {error_msg}",
                    "details": {
                        "directory_path": normalized_path,
                        "protection_disabled_count": protection_disabled_count,
                        "dfc_keys_deleted": len(dfc_deletion_results),
                        "protection_errors": protection_errors,
                        "dfc_deletion_errors": dfc_errors,
                        "directory_deletion_error": error_msg
                    }
                }
                
        except Exception as e:
            await self.dual_log(ctx, "error", f"Enhanced smart delete failed: {e}")
            return {
                "success": False,
                "error": "Smart delete operation failed",
                "message": f"Enhanced smart directory deletion failed for '{directory_path}': {str(e)}"
            }

    def _check_directory_content(self, list_result: Dict[str, Any]) -> bool:
        """Check if list_result indicates directory content."""
        # Check multiple possible response structures for directory content
        if list_result.get('folders') or list_result.get('items'):
            return True
            
        if isinstance(list_result.get('data'), dict):
            data = list_result.get('data', {})
            if data.get('folders') or data.get('items'):
                return True
                
        # Check for any list that might contain items
        if isinstance(list_result, dict):
            for key, value in list_result.items():
                if isinstance(value, list) and len(value) > 0:
                    if any(isinstance(item, dict) and ('item_name' in item or 'name' in item) for item in value):
                        return True
        
        # Additional check for Akeyless-specific response structures
        if isinstance(list_result, dict):
            # Check for any key that contains a list of items
            for key, value in list_result.items():
                if isinstance(value, list) and len(value) > 0:
                    # Look for any item that has identifying properties
                    for item in value:
                        if isinstance(item, dict):
                            # Check for common item identifier fields
                            if any(field in item for field in ['item_name', 'name', 'path', 'id', 'key']):
                                return True
        return False

    async def _list_all_items_internal(self, ctx: Context, path: str) -> Dict[str, Any]:
        """
        Internal utility method: List ALL items in a directory (no filtering).
        Used internally for directory detection, DFC key discovery, and smart delete operations.
        """
        try:
            # Ensure consistent path handling by normalizing trailing slashes
            normalized_path = path.rstrip('/') if path else '/'
            await self.dual_log(ctx, "info", f"🔍 Listing all items from path: {normalized_path}")
            
            # Use the raw client method without any type filtering
            result = await self.client.list_items(normalized_path, True)
            
            await self.dual_log(ctx, "info", f"🔍 Client returned result for path: {normalized_path}")
            
            return result
        except Exception as e:
            await self.dual_log(ctx, "error", f"List all items failed for '{path}': {e}")
            return {"error": str(e)}

    async def _discover_dfc_keys_in_directory(self, ctx: Context, path: str) -> List[str]:
        """Discover DFC keys in a directory (they need special handling)."""
        try:
            # Get ALL items and filter for DFC keys on our side
            await self.dual_log(ctx, "info", f"🔍 Discovering DFC keys in '{path}' by scanning all items...")
            result = await self._list_all_items_internal(ctx, path)
            dfc_keys = []
            
            # Extract DFC key names from the result
            if result.get('items'):
                for item in result['items']:
                    # Check if this is a DFC key by looking at the item type or other indicators
                    if item.get('item_name'):
                        if self._is_dfc_key(item):
                            dfc_keys.append(item['item_name'])
                            await self.dual_log(ctx, "info", f"🔐 Found DFC key: {item['item_name']} (type: {item.get('type', 'unknown')}, item_type: {item.get('item_type', 'unknown')})")
                        else:
                            await self.dual_log(ctx, "debug", f"📝 Item '{item['item_name']}' is NOT a DFC key (type: {item.get('type', 'unknown')}, item_type: {item.get('item_type', 'unknown')})")
            elif isinstance(result.get('data'), dict) and result['data'].get('items'):
                for item in result['data']['items']:
                    if item.get('item_name'):
                        if self._is_dfc_key(item):
                            dfc_keys.append(item['item_name'])
                            await self.dual_log(ctx, "info", f"🔐 Found DFC key: {item['item_name']} (type: {item.get('type', 'unknown')}, item_type: {item.get('item_type', 'unknown')})")
                        else:
                            await self.dual_log(ctx, "debug", f"📝 Item '{item['item_name']}' is NOT a DFC key (type: {item.get('type', 'unknown')}, item_type: {item.get('item_type', 'unknown')})")
            
            await self.dual_log(ctx, "info", f"🔍 Total DFC keys found: {len(dfc_keys)}")
            return dfc_keys
        except Exception as e:
            await self.dual_log(ctx, "warning", f"Could not discover DFC keys in '{path}': {e}")
            return []

    def _is_dfc_key(self, item: Dict[str, Any]) -> bool:
        """Check if an item is a DFC key based on its item_type property only."""
        known_algorithms = [
            'AES128GCM', 'AES256GCM', 'AES128SIV', 'AES256SIV', 'AES128CBC', 'AES256CBC',
            'RSA1024', 'RSA2048', 'RSA3072', 'RSA4096'
        ]
        item_type = item.get('item_type', '').upper()
        if item_type in known_algorithms:
            return True
        return False 