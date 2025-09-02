"""
Common Operations Module for Secret Management

This module provides shared functionality used across different secret types.
"""

import logging
from typing import Dict, Any, Optional, List
from fastmcp import Context
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class CommonSecretOperations(BaseThalesCDSPCSMTool):
    """Common operations shared across all secret types."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    def _looks_like_key_value(self, value: str) -> bool:
        """
        Detect if a string looks like key-value format.
        
        Args:
            value: String to check
            
        Returns:
            True if it appears to be key-value format
        """
        if not value or not isinstance(value, str):
            return False
            
        # Check for key=value pattern
        if '=' not in value:
            return False
            
        # Count key=value pairs
        pairs = value.replace(';', ',').replace('\n', ',').split(',')
        key_value_count = 0
        total_pairs = 0
        
        for pair in pairs:
            pair = pair.strip()
            if not pair:
                continue
                
            total_pairs += 1
            if '=' in pair:
                key, val = pair.split('=', 1)
                if key.strip() and val.strip():
                    key_value_count += 1
        
        # If more than 50% of pairs are key=value format, consider it key-value
        if total_pairs > 0 and (key_value_count / total_pairs) >= 0.5:
            return True
            
        return False

    def _convert_key_value_to_json(self, key_value_str: str) -> str:
        """
        Convert key-value string format to JSON format.
        
        Args:
            key_value_str: String in key=value format
            
        Returns:
            JSON string representation
        """
        try:
            # Try different separators
            if ';' in key_value_str:
                pairs = key_value_str.split(';')
            elif ',' in key_value_str:
                pairs = key_value_str.split(',')
            elif '\n' in key_value_str:
                pairs = key_value_str.split('\n')
            else:
                # Single key-value pair
                pairs = [key_value_str]
            
            result = {}
            for pair in pairs:
                pair = pair.strip()
                if not pair:
                    continue
                    
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle quoted values
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    
                    if key:  # Only add if key is not empty
                        result[key] = value
            
            import json
            return json.dumps(result)
            
        except Exception as e:
            logger.warning(f"Failed to convert key-value string to JSON: {e}")
            # Return original string if conversion fails
            return key_value_str

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

    async def _list_secrets(self, ctx: Context, path: str, filter_by: Optional[str], secret_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """List secrets in a directory. Handles empty directories gracefully."""
        await self.dual_log(ctx, "info", f"Listing secrets from path: {path}")
        
        # Use user-specified secret types or default to all types
        if secret_types:
            # Validate user-specified types
            valid_types = ["static-secret", "dynamic-secret", "rotated-secret"]
            invalid_types = [t for t in secret_types if t not in valid_types]
            if invalid_types:
                return {
                    "success": False,
                    "error": f"Invalid secret types: {invalid_types}",
                    "message": f"Valid secret types are: {valid_types}"
                }
            types_to_use = secret_types
        else:
            # Use default (all types)
            types_to_use = ["static-secret", "dynamic-secret", "rotated-secret"]
        
        try:
            # Use auto-pagination with proper API parameter
            result = await self.client.list_items(
                path, True, None, filter_by, None, None, None, types_to_use
            )
            
            # Check if directory is empty and provide user-friendly message
            items_count = 0
            if result.get('items'):
                items_count = len(result['items'])
            elif isinstance(result.get('data'), dict) and result['data'].get('items'):
                items_count = len(result['data']['items'])
            
            if items_count == 0:
                message = f"No secrets found in path: {path} (directory is empty)"
            else:
                message = f"Found {items_count} secret(s) in path: {path}"
            
            await self.dual_log(ctx, "info", message)
            
            # Add type filtering information to the response
            response_data = {
                "success": True,
                "message": message,
                "data": result,
                "filtering": {
                    "secret_types_used": types_to_use,
                    "user_specified_types": secret_types is not None,
                    "total_types_included": len(types_to_use)
                }
            }
            
            return response_data
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to list secrets from path '{path}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to list secrets from path '{path}'"
            }

    async def _list_shared_items(self, ctx: Context, accessibility: str, json: bool) -> Dict[str, Any]:
        """List shared items in the secrets manager."""
        await self.dual_log(ctx, "info", f"Listing shared items with accessibility: {accessibility}")
        
        try:
            # Prepare request data
            request_data = {
                "accessibility": accessibility,
                "json": json
            }
            
            # Call the list-shared-items endpoint
            result = await self.client.list_shared_items(request_data)
            
            await self.dual_log(ctx, "info", f"Shared items listed successfully with accessibility: {accessibility}")
            return {
                "success": True,
                "message": f"Shared items listed successfully with accessibility: {accessibility}",
                "data": {
                    "accessibility": accessibility,
                    "result": result
                }
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to list shared items with accessibility: {accessibility}: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to list shared items with accessibility: {accessibility}"
            } 