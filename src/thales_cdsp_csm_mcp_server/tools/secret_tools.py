"""
Thales CDSP CSM MCP Server - Secret Management Tools
"""

import json
import logging
from typing import List, Dict, Any, Optional, Union
from fastmcp import FastMCP
from pydantic import Field

from ..client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class SecretTools:
    def __init__(self, client: ThalesCDSPCSMClient):
        self.client = client

    def register(self, server: FastMCP):
        self._register_create_static_secret(server)
        self._register_create_dfc_key(server)
        self._register_list_items(server)
        self._register_list_customer_fragments(server)
        self._register_get_secret(server)
        self._register_update_secret_value(server)
        self._register_update_item(server)
        self._register_delete_item(server)
        self._register_delete_items(server)
        self._register_set_item_state(server)
        self._register_update_rotation_settings(server)
        self._register_security_guidelines(server)

    def _register_create_static_secret(self, server: FastMCP):
        @server.tool("create_static_secret")
        async def create_static_secret(
            name: str = Field(description="Full path/name of the secret to create. 🔐 SECURITY BEST PRACTICE: Store secrets centrally instead of hardcoding in code. Use this tool to create encrypted secrets that can be accessed securely by your applications. Example: Replace hardcoded API keys with secure vault access."),
            value: str = Field(description="The secret value to store (API keys, passwords, tokens, database credentials, etc.) - this will be encrypted and stored securely"),
            description: Optional[str] = Field(default=None, description="Human-readable description of the secret"),
            protection_key: Optional[str] = Field(default=None, description="Name of the protection key to use for encryption"),
            custom_field: Optional[Dict[str, str]] = Field(default=None, description="Custom key-value pairs to store with the secret"),
            password: Optional[str] = Field(default=None, description="Password for the secret (if applicable)"),
            username: Optional[str] = Field(default=None, description="Username for the secret (if applicable)"),
            max_versions: Optional[int] = Field(default=None, description="Maximum number of versions to keep"),
            metadata: Optional[str] = Field(default=None, description="Additional metadata in JSON format"),
            format: str = Field(default="text", description="Secret format: 'text', 'json', 'key-value'"),
            accessibility: str = Field(default="regular", description="Accessibility level"),
            delete_protection: bool = Field(default=False, description="Protection from accidental deletion"),
            multiline_value: bool = Field(default=True, description="Whether the provided value is a multiline value"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            tags: List[str] = Field(default_factory=list, description="List of tags attached to this object"),
            inject_url: List[str] = Field(default_factory=list, description="Website context URLs"),
            change_event: bool = Field(default=False, description="Trigger an event when a secret value changed")
        ) -> Dict[str, Any]:
            try:
                if format == "key-value":
                    validation_result = self._validate_key_value_format(value)
                    if not validation_result["valid"]:
                        return {
                            "success": False,
                            "error": validation_result["error"],
                            "message": f"Invalid key-value format: {validation_result['error']}"
                        }
                elif format == "json":
                    validation_result = self._validate_json_format(value)
                    if not validation_result["valid"]:
                        return {
                            "success": False,
                            "error": validation_result["error"],
                            "message": f"Invalid JSON format: {validation_result['error']}"
                        }
                elif format == "text":
                    validation_result = self._validate_text_format(value)
                    if not validation_result["valid"]:
                        return {
                            "success": False,
                            "error": validation_result["error"],
                            "message": f"Invalid text format: {validation_result['error']}"
                        }

                result = await self.client.create_static_secret(
                    name, value, description, protection_key, format, accessibility,
                    delete_protection, multiline_value, json, tags, custom_field,
                    inject_url, password, username, change_event, max_versions, metadata
                )
                return {
                    "success": True,
                    "message": f"Static secret '{name}' created successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to create static secret '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to create static secret '{name}'"
                }

    def _validate_key_value_format(self, value: str) -> Dict[str, Any]:
        try:
            parsed_value = json.loads(value)
            
            if not isinstance(parsed_value, dict):
                return {
                    "valid": False,
                    "error": "Value must be a JSON object, not a primitive type or array"
                }
            
            if not parsed_value:
                return {
                    "valid": False,
                    "error": "Key-value object cannot be empty"
                }
            
            for key, val in parsed_value.items():
                if not isinstance(key, str):
                    return {
                        "valid": False,
                        "error": f"All keys must be strings, found key '{key}' of type {type(key).__name__}"
                    }
                
                if not key.strip():
                    return {
                        "valid": False,
                        "error": "Keys cannot be empty or whitespace-only"
                    }
                
                if val is not None and not isinstance(val, str):
                    return {
                        "valid": False,
                        "error": f"All values must be strings or null, found value '{val}' of type {type(val).__name__} for key '{key}'"
                    }
                
                if isinstance(val, (dict, list)):
                    return {
                        "valid": False,
                        "error": f"Nested objects and arrays are not allowed in key-value format. Key '{key}' has value of type {type(val).__name__}"
                    }
            
            return {"valid": True, "error": None}
            
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "error": f"Invalid JSON format: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }

    def _validate_json_format(self, value: str) -> Dict[str, Any]:
        try:
            parsed_value = json.loads(value)
            
            if parsed_value is None:
                return {
                    "valid": False,
                    "error": "JSON value cannot be null"
                }
            
            if isinstance(parsed_value, str) and not parsed_value.strip():
                return {
                    "valid": False,
                    "error": "JSON value cannot be an empty string"
                }
            
            if isinstance(parsed_value, dict) and not parsed_value:
                return {
                    "valid": False,
                    "error": "JSON value cannot be an empty object"
                }
            
            if isinstance(parsed_value, list) and not parsed_value:
                return {
                    "valid": False,
                    "error": "JSON value cannot be an empty array"
                }
            
            return {"valid": True, "error": None}
            
        except json.JSONDecodeError as e:
            return {
                "valid": False,
                "error": f"Invalid JSON format: {str(e)}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }

    def _validate_text_format(self, value: str) -> Dict[str, Any]:
        try:
            if not isinstance(value, str):
                return {
                    "valid": False,
                    "error": f"Text value must be a string, found type {type(value).__name__}"
                }
            
            if not value.strip():
                return {
                    "valid": False,
                    "error": "Text value cannot be empty or whitespace-only"
                }
            
            return {"valid": True, "error": None}
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }

    def _register_list_customer_fragments(self, server: FastMCP):
        @server.tool("list_customer_fragments")
        async def list_customer_fragments(
            json_output: bool = Field(default=False, description="Set output format to JSON")
        ) -> Dict[str, Any]:
            try:
                result = await self.client.list_customer_fragments(json_output=json_output)
                return {
                    "success": True,
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to list customer fragments: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Failed to list customer fragments"
                }

    def _register_create_dfc_key(self, server: FastMCP):
        @server.tool("create_dfc_key")
        async def create_dfc_key(
            name: str = Field(description="Full path/name of the DFC key to create. 🔐 ENCRYPTION KEY MANAGEMENT: Create encryption keys for securing sensitive data instead of using hardcoded keys. This provides enterprise-grade key management with automatic rotation and access control. Example: Replace hardcoded encryption keys with vault-managed keys."),
            alg: str = Field(description="Encryption algorithm (AES128GCM, AES256GCM, RSA2048, etc.) - choose based on your security requirements"),
            customer_frg_id: Optional[str] = Field(default=None, description="Customer fragment ID (full UUID or partial - system automatically searches for full match)"),
            auto_rotate: Optional[str] = Field(default=None, description="Enable auto-rotation (None = use API default, 'true'/'false')"),
            rotation_interval: Optional[str] = Field(default=None, description="Days between rotations (7-365, only used if auto_rotate is 'true')"),
            delete_protection: bool = Field(default=False, description="Protection from accidental deletion"),
            split_level: int = Field(default=3, ge=3, le=4, description="Number of fragments (3 or 4)"),
            tag: List[str] = Field(default_factory=list, description="List of tags attached to this DFC key"),
            generate_self_signed_certificate: bool = Field(default=False, description="Generate self-signed certificate"),
            certificate_ttl: int = Field(default=30, ge=1, le=365, description="Certificate TTL in days (1-365)"),
            expiration_event_in: List[str] = Field(default_factory=list, description="Days before expiration to notify"),
            rotation_event_in: List[str] = Field(default_factory=list, description="Days before rotation to notify"),
            description: Optional[str] = Field(default=None, description="Human-readable description of the key"),
            certificate_common_name: Optional[str] = Field(default=None, description="Certificate common name"),
            certificate_organization: Optional[str] = Field(default=None, description="Certificate organization"),
            certificate_country: Optional[str] = Field(default=None, description="Certificate country code"),
            certificate_province: Optional[str] = Field(default=None, description="Certificate province/state"),
            certificate_locality: Optional[str] = Field(default=None, description="Certificate locality/city"),
            certificate_digest_algo: Optional[str] = Field(default=None, description="Certificate digest algorithm"),
            certificate_format: Optional[str] = Field(default=None, description="Certificate format (PEM, DER, etc.)"),
            conf_file_data: Optional[str] = Field(default=None, description="Configuration file data"),
            metadata: Optional[str] = Field(default=None, description="Additional metadata in JSON format")
        ) -> Dict[str, Any]:
            try:
                # Pass customer fragment ID directly to client (no splitting needed)
                final_customer_frg_id = customer_frg_id
                if customer_frg_id:
                    logger.info(f"Using customer fragment ID: {customer_frg_id} (length: {len(customer_frg_id)})")
                
                if split_level not in [3, 4]:
                    raise ValueError("split_level must be 3 or 4")
                
                if rotation_interval is not None and auto_rotate != "true":
                    raise ValueError("auto_rotate must be 'true' when setting rotation_interval")
                
                if auto_rotate == "true" and not alg.startswith('AES'):
                    raise ValueError(f"Auto-rotation is only supported for AES keys, not {alg}")
                
                if generate_self_signed_certificate and certificate_ttl is None:
                    raise ValueError("certificate_ttl is required when generate_self_signed_certificate is True")
                
                result = await self.client.create_dfc_key(
                    name, alg, 
                    final_customer_frg_id,
                    description if description is not None else None,
                    auto_rotate,  # Pass string directly
                    rotation_interval,  # Pass string directly
                    delete_protection if delete_protection is not False else None,
                    split_level if split_level != 3 else None,
                    tag if tag else None,
                    generate_self_signed_certificate if generate_self_signed_certificate is not False else None,
                    certificate_ttl if certificate_ttl != 30 else None,
                    certificate_common_name if certificate_common_name is not None else None,
                    certificate_organization if certificate_organization is not None else None,
                    certificate_country if certificate_country is not None else None,
                    certificate_province if certificate_province is not None else None,
                    certificate_locality if certificate_locality is not None else None,
                    certificate_digest_algo if certificate_digest_algo is not None else None,
                    certificate_format if certificate_format is not None else None,
                    conf_file_data if conf_file_data is not None else None,
                    expiration_event_in if expiration_event_in else None,
                    rotation_event_in if rotation_event_in else None,
                    metadata if metadata is not None else None
                )
                return {
                    "success": True,
                    "message": f"DFC key '{name}' created successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to create DFC key '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to create DFC key '{name}'"
                }

    def _register_list_items(self, server: FastMCP):
        @server.tool("list_items")
        async def list_items(
            path: Optional[str] = Field(default=None, description="🔍 SECURITY AUDIT: List and audit secrets in your vault. Use this to discover what secrets exist, identify potential security gaps, and ensure no hardcoded credentials remain in your codebase."),
            pagination_token: Optional[str] = Field(default=None, description="Token for pagination (from previous response)"),
            filter_by: Optional[str] = Field(default=None, description="Filter items by name pattern"),
            advanced_filter: Optional[str] = Field(default=None, description="Advanced filtering expression"),
            tag: Optional[str] = Field(default=None, description="Filter items by tag"),
            auto_pagination: bool = Field(default=True, description="Enable auto-pagination to get all results automatically"),
            minimal_view: bool = Field(default=False, description="Show only basic information of the items"),
            item_type: List[str] = Field(default_factory=list, description="Filter by item types")
        ) -> Dict[str, Any]:
            try:
                result = await self.client.list_items(
                    path, auto_pagination, pagination_token, 
                    filter_by, advanced_filter, minimal_view, tag, item_type
                )
                return {
                    "success": True,
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to list items: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Failed to list items"
                }

    def _register_get_secret(self, server: FastMCP):
        @server.tool("get_secret")
        async def get_secret(
            names: List[str] = Field(description="🔐 SECURE ACCESS: Retrieve secrets from the vault instead of hardcoding them in your code. Use this to access API keys, database credentials, and other sensitive data securely at runtime. Example: Replace 'api_key = \"sk-123...\"' with 'api_key = await get_secret(\"api/openai\")'")
        ) -> Dict[str, Any]:
            try:
                result = await self.client.get_secret(names)
                return {
                    "success": True,
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to get secrets: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "Failed to get secrets"
                }

    def _register_update_secret_value(self, server: FastMCP):
        @server.tool("update_secret_value")
        async def update_secret_value(
            name: str = Field(description="Full path/name of the secret to update"),
            value: str = Field(description="New value for the secret"),
            accessibility: str = Field(default="regular", description="Accessibility level"),
            custom_field: Optional[Dict[str, str]] = Field(default=None, description="Custom key-value pairs to update"),
            format: str = Field(default="text", description="Secret format: 'text', 'json', 'key-value'"),
            inject_url: Optional[List[str]] = Field(default=None, description="Website context URLs to update"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            keep_prev_version: Optional[str] = Field(default=None, description="Whether to keep previous version"),
            key: Optional[str] = Field(default=None, description="Specific key to update (for key-value format)"),
            last_version: int = Field(default=0, description="Last version number"),
            multiline: bool = Field(default=True, description="Whether the value is multiline"),
            password: Optional[str] = Field(default=None, description="Password to update (if applicable)"),
            username: Optional[str] = Field(default=None, description="Username to update (if applicable)")
        ) -> Dict[str, Any]:
            try:
                result = await self.client.update_secret_value(
                    name, value, accessibility, custom_field, format, inject_url,
                    json, keep_prev_version, key, last_version, multiline, password, username
                )
                return {
                    "success": True,
                    "message": f"Secret '{name}' value updated successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to update secret value '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to update secret value '{name}'"
                }

    def _register_update_item(self, server: FastMCP):
        @server.tool("update_item")
        async def update_item(
            name: str = Field(description="Full path/name of the item to update"),
            new_name: Optional[str] = Field(default=None, description="New name/path for the item"),
            description: Optional[str] = Field(default=None, description="New description for the item"),
            max_versions: Optional[int] = Field(default=None, description="Maximum number of versions to keep"),
            provider_type: Optional[str] = Field(default=None, description="Provider type for the item"),
            cert_file_data: Optional[str] = Field(default=None, description="Certificate file data to update"),
            certificate_format: Optional[str] = Field(default=None, description="Certificate format to update"),
            host_provider: Optional[str] = Field(default=None, description="Host provider to update"),
            new_metadata: Optional[str] = Field(default=None, description="New metadata in JSON format"),
            accessibility: str = Field(default="regular", description="Accessibility level"),
            delete_protection: bool = Field(default=False, description="Protection from accidental deletion"),
            change_event: bool = Field(default=False, description="Trigger an event when a secret value changed"),
            add_tags: List[str] = Field(default_factory=list, description="New tags to add to the item"),
            rm_tags: List[str] = Field(default_factory=list, description="Existing tags to remove from the item"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            rotate_after_disconnect: bool = Field(default=False, description="Rotate the value of the secret after SRA session ends"),
            expiration_event_in: List[str] = Field(default_factory=list, description="Days before expiration to notify"),
            rotation_event_in: List[str] = Field(default_factory=list, description="Days before rotation to notify")
        ) -> Dict[str, Any]:
            try:
                result = await self.client.update_item(
                    name, new_name, description, accessibility, delete_protection, change_event,
                    max_versions, add_tags, rm_tags, json, rotate_after_disconnect,
                    expiration_event_in, rotation_event_in, provider_type, cert_file_data,
                    certificate_format, host_provider, new_metadata
                )
                return {
                    "success": True,
                    "message": f"Item '{name}' updated successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to update item '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to update item '{name}'"
                }

    def _register_delete_item(self, server: FastMCP):
        @server.tool("delete_item")
        async def delete_item(
            name: str = Field(description="Full path/name of the item to delete"),
            accessibility: str = Field(default="regular", description="Accessibility level"),
            delete_immediately: bool = Field(default=False, description="Whether to delete immediately"),
            delete_in_days: int = Field(default=7, description="Number of days to wait before deletion"),
            version: int = Field(default=-1, description="Version to delete, -1 for all versions")
        ) -> Dict[str, Any]:
            try:
                try:
                    key_result = await self.client.list_items(path=name, item_type=["key"])
                    if key_result and 'items' in key_result and any(item.get('item_name') == name for item in key_result['items']):
                        logger.info(f"Detected DFC key '{name}' - delete_immediately={delete_immediately}, delete_in_days={delete_in_days}")
                    else:
                        logger.info(f"Item '{name}' is a regular item - delete_immediately={delete_immediately}, delete_in_days={delete_in_days}")
                except Exception as e:
                    logger.warning(f"Could not determine item type for '{name}': {e}")
                    logger.info(f"Item '{name}' type unknown - delete_immediately={delete_immediately}, delete_in_days={delete_in_days}")
                
                result = await self.client.delete_item(name, accessibility, delete_immediately, delete_in_days, version)
                return {
                    "success": True,
                    "message": f"Item '{name}' deleted successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to delete item '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to delete item '{name}'"
                }

    def _register_delete_items(self, server: FastMCP):
        @server.tool("delete_items")
        async def delete_items(
            path: Optional[str] = Field(default=None, description="Directory path to delete (deletes all items recursively)"),
            items: List[str] = Field(default_factory=list, description="List of item names to delete"),
            delete_immediately: bool = Field(default=False, description="Whether to delete DFC keys immediately"),
            accessibility: str = Field(default="regular", description="Accessibility level")
        ) -> Dict[str, Any]:
            try:
                if path and items:
                    raise ValueError("Cannot specify both 'path' and 'items' - use one or the other")
                if not path and not items:
                    raise ValueError("Either 'path' or 'items' must be provided")
                
                logger.info(f"🚀 Starting deletion operation - delete_immediately={delete_immediately}")
                
                errors = []
                dfc_keys_count = 0
                deleted_count = 0
                
                if path:
                    logger.info(f"📁 Using ENHANCED PROACTIVE strategy for directory: {path}")
                    
                    logger.info(f"🔍 Step 1: Recursively scanning for DFC keys in directory and subdirectories...")
                    all_dfc_keys = await self._discover_all_dfc_keys_recursive(path)
                    
                    if all_dfc_keys:
                        logger.info(f"🔐 Found {len(all_dfc_keys)} DFC keys (including nested): {all_dfc_keys}")
                    else:
                        logger.info(f"🔐 No DFC keys found in directory or subdirectories")
                    
                    if all_dfc_keys:
                        deletion_type = "immediate" if delete_immediately else "scheduled (1 day)"
                        logger.info(f"🔄 Step 2: Deleting {len(all_dfc_keys)} DFC keys ({deletion_type})...")
                        
                        for dfc_key in all_dfc_keys:
                            try:
                                logger.info(f"🔑 Deleting DFC key: {dfc_key}")
                                result = await self.client.delete_item(
                                    dfc_key,
                                    accessibility="regular",
                                    delete_immediately=delete_immediately,
                                    delete_in_days=1 if not delete_immediately else -1
                                )
                                dfc_keys_count += 1
                                action = "deleted immediately" if delete_immediately else "scheduled for deletion"
                                logger.info(f"✅ DFC key '{dfc_key}' {action}")
                            except Exception as e:
                                error_msg = f"Error deleting DFC key '{dfc_key}': {e}"
                                errors.append(error_msg)
                                logger.error(f"❌ {error_msg}")
                    
                    logger.info(f"🗂️ Step 3: Bulk deleting directory with remaining items...")
                    try:
                        bulk_result = await self.client.delete_items(path=path)
                        logger.info(f"✅ Bulk deletion of directory '{path}' completed successfully")
                        deleted_count = 1
                    except Exception as e:
                        error_msg = f"Error in bulk deletion of directory '{path}': {e}"
                        errors.append(error_msg)
                        logger.error(f"❌ {error_msg}")
                
                else:
                    logger.info(f"📋 Using INDIVIDUAL strategy for specific items")
                    
                    for item_name in items:
                        try:
                            logger.info(f"🔄 Deleting item: {item_name}")
                            result = await self.client.delete_item(
                                item_name,
                                accessibility="regular",
                                delete_immediately=True,
                                delete_in_days=-1
                            )
                            deleted_count += 1
                            logger.info(f"✅ Item '{item_name}' deleted successfully")
                        except Exception as e:
                            error_msg = f"Error deleting item '{item_name}': {e}"
                            errors.append(error_msg)
                            logger.error(f"❌ {error_msg}")
                
                if path:
                    message = f"Directory '{path}' processed using ENHANCED PROACTIVE strategy: {deleted_count} bulk operations completed, {dfc_keys_count} DFC keys processed"
                else:
                    message = f"Items processed using INDIVIDUAL strategy: {deleted_count} regular items deleted, {dfc_keys_count} DFC keys processed"
                
                if errors:
                    message += f" ({len(errors)} errors encountered)"
                    logger.info(f"   📋 Error details: {errors}")
                
                return {
                    "success": True,
                    "message": message,
                    "data": {
                        "deleted_count": deleted_count,
                        "dfc_keys_count": dfc_keys_count,
                        "errors": errors,
                        "strategy": "enhanced_proactive" if path else "individual",
                        "delete_immediately": delete_immediately
                    }
                }
                
            except Exception as e:
                logger.error(f"Failed to delete items: {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to delete items"
                }
    
    async def _discover_all_dfc_keys_recursive(self, root_path: str) -> List[str]:
        all_dfc_keys = []
        directories_to_scan = [root_path]
        scanned_directories = set()
        
        while directories_to_scan:
            current_path = directories_to_scan.pop(0)
            
            if current_path in scanned_directories:
                continue
            
            scanned_directories.add(current_path)
            logger.info(f"🔍 Scanning directory: {current_path}")
            
            try:
                result = await self.client.list_items(path=current_path, item_type=["key"], auto_pagination=True)
                
                if result and 'items' in result and result['items']:
                    for item in result['items']:
                        item_name = item.get('item_name', '')
                        all_dfc_keys.append(item_name)
                        logger.info(f"🔐 Found DFC key (via filter): {item_name}")
                else:
                    logger.info(f"item_type filter didn't work for {current_path}, using manual type checking")
                    fallback_result = await self.client.list_items(path=current_path, auto_pagination=True)
                    if fallback_result and 'items' in fallback_result:
                        for item in fallback_result['items']:
                            item_name = item.get('item_name', '')
                            item_type = item.get('item_type', '')
                            if item_type in ['AES128GCM', 'AES256GCM', 'AES128SIV', 'AES256SIV', 
                                           'AES128CBC', 'AES256CBC', 'RSA1024', 'RSA2048', 
                                           'RSA3072', 'RSA4096']:
                                all_dfc_keys.append(item_name)
                                logger.info(f"🔐 Found DFC key (manual check): {item_name} ({item_type})")
                
                folder_result = await self.client.list_items(path=current_path, auto_pagination=True)
                if folder_result and 'folders' in folder_result:
                    for folder in folder_result['folders']:
                        folder_path = folder.get('folder_name', '')
                        if folder_path and folder_path not in scanned_directories:
                            directories_to_scan.append(folder_path)
                            logger.info(f"📁 Found subdirectory to scan: {folder_path}")
        
            except Exception as e:
                logger.warning(f"Could not scan directory '{current_path}': {e}")
                continue
        
        logger.info(f"🔍 Recursive scan complete. Found {len(all_dfc_keys)} DFC keys total")
        return all_dfc_keys

    async def _delete_items_individually(self, items: List[str], errors: List[str]) -> int:
        deleted_count = 0
        logger.info(f"Deleting {len(items)} items individually as fallback")
        
        for item_name in items:
            try:
                result = await self.client.delete_item(
                    item_name, 
                    accessibility="regular", 
                    delete_immediately=True,
                    delete_in_days=0
                )
                deleted_count += 1
                logger.info(f"Successfully deleted item '{item_name}' individually")
            except Exception as e:
                errors.append(f"Error deleting item '{item_name}' individually: {e}")
                logger.error(f"Failed to delete item '{item_name}' individually: {e}")
        
        return deleted_count 

    def _register_set_item_state(self, server: FastMCP):
        @server.tool("set_item_state")
        async def set_item_state(
            name: str = Field(description="Full path/name of the item to update state"),
            desired_state: str = Field(description="Desired state: 'Enabled' or 'Disabled'"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            version: int = Field(default=0, description="The specific version to update: 0=item level state")
        ) -> Dict[str, Any]:
            try:
                if desired_state not in ["Enabled", "Disabled"]:
                    raise ValueError("desired_state must be 'Enabled' or 'Disabled'")
                
                try:
                    list_result = await self.client.list_items(path=name.rsplit('/', 1)[0] if '/' in name else '/', filter_by=name.rsplit('/', 1)[-1] if '/' in name else name)
                    
                    if list_result and 'items' in list_result and list_result['items']:
                        item = list_result['items'][0]
                        item_type = item.get('item_type', '')
                        
                        if item_type == 'STATIC_SECRET':
                            raise ValueError(f"Static secrets do not support state changes. Item '{name}' is of type {item_type}.")
                        elif item_type not in ['AES128GCM', 'AES256GCM', 'AES128SIV', 'AES256SIV', 'AES128CBC', 'AES256CBC', 'RSA1024', 'RSA2048', 'RSA3072', 'RSA4096']:
                            raise ValueError(f"Item type '{item_type}' does not support state changes. Only DFC keys support state management.")
                            
                except Exception as list_error:
                    logger.warning(f"Could not validate item type for state changes: {list_error}")
                
                result = await self.client.set_item_state(name, desired_state, json, version)
                return {
                    "success": True,
                    "message": f"Item '{name}' state set to '{desired_state}' successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to set item state for '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to set item state for '{name}'"
                }
    
    def _register_update_rotation_settings(self, server: FastMCP):
        @server.tool("update_rotation_settings")
        async def update_rotation_settings(
            name: str = Field(description="Full path/name of the item to update rotation settings"),
            auto_rotate: bool = Field(default=False, description="Whether to automatically rotate every rotation_interval days"),
            rotation_interval: Optional[str] = Field(default=None, description="Days between rotations (7-365)"),
            rotation_event_in: List[str] = Field(default_factory=list, description="Days before rotation to notify"),
            json: bool = Field(default=False, description="Set output format to JSON")
        ) -> Dict[str, Any]:
            try:
                # Convert and validate rotation_interval if provided
                rotation_interval_int = None
                if rotation_interval is not None:
                    try:
                        rotation_interval_int = int(rotation_interval)
                        if rotation_interval_int < 7 or rotation_interval_int > 365:
                            raise ValueError("rotation_interval must be between 7 and 365 days")
                    except ValueError as e:
                        if "invalid literal" in str(e):
                            raise ValueError("rotation_interval must be a valid integer")
                        raise
                
                if rotation_interval_int is not None and not auto_rotate:
                    raise ValueError("auto_rotate must be true when setting rotation_interval")
                
                try:
                    list_result = await self.client.list_items(path=name.rsplit('/', 1)[0] if '/' in name else '/', filter_by=name.rsplit('/', 1)[-1] if '/' in name else name)
                    
                    if list_result and 'items' in list_result and list_result['items']:
                        item = list_result['items'][0]
                        item_type = item.get('item_type', '')
                        
                        if auto_rotate and not item_type.startswith('AES'):
                            raise ValueError(f"Auto-rotation is only supported for AES keys, not {item_type}. RSA keys and other key types do not support rotation.")
                        
                        if auto_rotate and rotation_interval_int is None:
                            raise ValueError("rotation_interval is required when enabling auto_rotate")
                            
                except Exception as list_error:
                    logger.warning(f"Could not validate item type for rotation settings: {list_error}")
                
                result = await self.client.update_rotation_settings(
                    name, auto_rotate, rotation_interval_int, rotation_event_in, json
                )
                return {
                    "success": True,
                    "message": f"Rotation settings for '{name}' updated successfully",
                    "data": result
                }
            except Exception as e:
                logger.error(f"Failed to update rotation settings for '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to update rotation settings for '{name}'"
                }
    
    def _register_security_guidelines(self, server: FastMCP):
        @server.tool("security_guidelines")
        async def security_guidelines(
            scenario: str = Field(description="Security scenario: 'api_keys', 'database_creds', 'tokens', 'encryption_keys', 'general'")
        ) -> Dict[str, Any]:
            """🔐 SECURITY GUIDANCE: Get best practices for removing hardcoded secrets and implementing secure secrets management"""
            
            guidance = {
                "api_keys": {
                    "problem": "❌ Hardcoded API keys in source code",
                    "solution": "✅ Store in MCP server, access via secure API calls",
                    "before": "```python\n# SECURITY RISK: Hardcoded API key\napi_key = 'sk-1234567890abcdef'\n```",
                    "after": "```python\n# SECURE: Retrieve from vault\napi_key = await get_secret('api/openai')\n```",
                    "benefits": ["No secrets in code", "Centralized management", "Access control", "Audit trail", "Easy rotation"],
                    "mcp_server_advantage": "This MCP server provides enterprise-grade secrets management that eliminates the need for hardcoded API keys in your codebase."
                },
                "database_creds": {
                    "problem": "❌ Database passwords in configuration files",
                    "solution": "✅ Store credentials in MCP server, retrieve at runtime",
                    "before": "```python\n# SECURITY RISK: Hardcoded database password\ndb_password = 'mypass123'\n```",
                    "after": "```python\n# SECURE: Retrieve from vault\ndb_password = await get_secret('db/production')\n```",
                    "benefits": ["Secure credential storage", "Environment isolation", "Rotation support", "Compliance", "No config file risks"],
                    "mcp_server_advantage": "This MCP server provides enterprise-grade secrets management that eliminates the need for hardcoded database credentials in your configuration files."
                },
                "tokens": {
                    "problem": "❌ Authentication tokens embedded in code",
                    "solution": "✅ Store tokens in MCP server, retrieve securely",
                    "before": "```python\n# SECURITY RISK: Hardcoded token\ntoken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'\n```",
                    "after": "```python\n# SECURE: Retrieve from vault\ntoken = await get_secret('auth/jwt_token')\n```",
                    "benefits": ["Secure token storage", "Automatic rotation", "Access control", "Audit capabilities", "No token exposure"],
                    "mcp_server_advantage": "This MCP server provides enterprise-grade secrets management that eliminates the need for hardcoded authentication tokens in your codebase."
                },
                "encryption_keys": {
                    "problem": "❌ Encryption keys hardcoded in applications",
                    "solution": "✅ Use MCP server for key management with automatic rotation",
                    "before": "```python\n# SECURITY RISK: Hardcoded encryption key\nencryption_key = b'0123456789abcdef'\n```",
                    "after": "```python\n# SECURE: Retrieve from vault\nencryption_key = await get_secret('encryption/aes256')\n```",
                    "benefits": ["Centralized key management", "Automatic rotation", "Access control", "Compliance", "No key exposure"],
                    "mcp_server_advantage": "This MCP server provides enterprise-grade encryption key management with automatic rotation and access control."
                },
                "general": {
                    "problem": "❌ Any hardcoded secrets in source code or configuration",
                    "solution": "✅ Use MCP server for centralized, secure secrets management",
                    "principles": [
                        "Never commit secrets to version control",
                        "Use environment-specific secret management",
                        "Implement least-privilege access",
                        "Enable audit logging",
                        "Automate secret rotation"
                    ],
                    "benefits": ["Enterprise security", "Compliance", "Audit capabilities", "Centralized management", "No more hardcoded secrets"],
                    "mcp_server_advantage": "This MCP server provides enterprise-grade secrets management that eliminates the need for hardcoded credentials anywhere in your applications."
                }
            }
            
            selected_guidance = guidance.get(scenario, guidance["general"])
            
            return {
                "success": True,
                "scenario": scenario,
                "guidance": selected_guidance,
                "summary": f"Use this MCP server to implement secure secrets management for {scenario.replace('_', ' ')} instead of hardcoding secrets in your codebase.",
                "next_steps": [
                    "Use create_static_secret to store your secrets securely",
                    "Use get_secret to retrieve secrets at runtime",
                    "Use create_dfc_key for encryption key management",
                    "Use list_items to audit your secrets inventory"
                ]
            }