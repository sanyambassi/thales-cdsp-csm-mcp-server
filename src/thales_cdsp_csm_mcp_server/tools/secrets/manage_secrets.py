"""
Thales CDSP CSM MCP Server - Consolidated Secret Management Tools

This module provides a unified tool for managing all types of secrets
(static, dynamic, rotated) with action-based operations.
"""

import logging
from typing import List, Dict, Any, Optional, Union
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient
from ..secrets.validation import SecretValidator
from .modules import (
    StaticSecretsManager, 
    DynamicSecretsManager, 
    RotatedSecretsManager,
    CommonSecretOperations,
    DeletionOperations
)

logger = logging.getLogger(__name__)


class ManageSecretsTools(BaseThalesCDSPCSMTool):
    """Consolidated tools for managing all types of secrets."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)
        self.validator = SecretValidator()
        # Initialize module managers with shared logger
        self.static_manager = StaticSecretsManager(client, self.logger)
        self.dynamic_manager = DynamicSecretsManager(client, self.logger)
        self.rotated_manager = RotatedSecretsManager(client, self.logger)
        self.common_ops = CommonSecretOperations(client, self.logger)
        self.deletion_ops = DeletionOperations(client, self.logger)

    def register(self, server: FastMCP):
        self._register_manage_secrets(server)

    def _register_manage_secrets(self, server: FastMCP):
        @server.tool("manage_secrets")
        async def manage_secrets(
            ctx: Context,
            action: str = Field(description="Secret management action to perform. SUPPORTED ACTIONS: 'create_static_secret' (create text/JSON secrets), 'get_static_secret_value' (retrieve secret values), 'update' (modify secret properties), 'delete' (smart delete individual items), 'delete_items' (bulk delete multiple items or directories), 'list' (list secrets in directory with type filtering), 'list_dynamic_secrets' (list all dynamic secrets globally), 'create_dynamic_secret_ldap' (create LDAP dynamic secrets), 'create_dynamic_secret_mysql' (create MySQL dynamic secrets), 'create_dynamic_secret_mongodb' (create MongoDB dynamic secrets), 'list_shared_items' (list shared secrets/items)"),
            name: Optional[str] = Field(default=None, description="Secret/directory name/path (required for create_static_secret, get_static_secret_value, update, delete)"),
            new_name: Optional[str] = Field(default=None, description="New name for the secret (for update action)"),
            items: List[str] = Field(default_factory=list, description="List of item names to delete (for bulk delete). Must be an array of strings, e.g., ['/item1', '/item2']"),
            secret_type: Optional[str] = Field(default="static", description="Secret type: 'static' (for create_static_secret action only). For dynamic secrets, use specific actions: create_dynamic_secret_ldap/mysql/mongodb"),
            value: Optional[str] = Field(default=None, description="Secret value (required for create_static_secret, optional for update)"),
            description: Optional[str] = Field(default=None, description="Secret description"),
            format: str = Field(default="text", description="Secret format: 'text', 'json', 'key-value'"),
            accessibility: str = Field(default="regular", description="Accessibility level"),
            protection_key: Optional[str] = Field(default=None, description="Protection key name"),
            custom_field: Optional[Dict[str, str]] = Field(default=None, description="Custom key-value pairs"),
            password: Optional[str] = Field(default=None, description="Password for the secret"),
            username: Optional[str] = Field(default=None, description="Username for the secret"),
            max_versions: Optional[int] = Field(default=None, description="Maximum number of versions to keep"),
            metadata: Optional[str] = Field(default=None, description="Additional metadata in JSON format"),

            multiline_value: bool = Field(default=True, description="Whether the provided value is multiline"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            inject_url: List[str] = Field(default_factory=list, description="Website context URLs"),
            change_event: bool = Field(default=False, description="Trigger an event when a secret value changed"),
            # Dynamic secret specific parameters
            dynamic_type: Optional[str] = Field(default=None, description="Dynamic secret type (for dynamic secrets)"),
            ttl: Optional[int] = Field(default=None, description="Time to live in seconds (for dynamic secrets)"),
            # Dynamic Secret Creation - Common Parameters
            password_length: Optional[str] = Field(default=None, description="Length of password to be generated for dynamic secrets"),
            producer_encryption_key_name: Optional[str] = Field(default=None, description="Dynamic producer encryption key name"),
            user_ttl: Optional[str] = Field(default="60m", description="User TTL for dynamic secrets (default: 60m)"),
            custom_username_template: Optional[str] = Field(default=None, description="Custom username template using go template syntax"),
            delete_protection: Optional[str] = Field(default=None, description="Protection from accidental deletion [true/false]"),
            tags: List[str] = Field(default_factory=list, description="Tags to attach to the dynamic secret"),
            # Secure Access Parameters (Common)
            secure_access_enable: Optional[str] = Field(default=None, description="Enable/Disable secure remote access [true/false]"),
            secure_access_host: List[str] = Field(default_factory=list, description="Target servers for connections"),
            secure_access_delay: Optional[int] = Field(default=None, description="Delay duration in seconds (0-120) after generating credentials"),
            secure_access_certificate_issuer: Optional[str] = Field(default=None, description="Path to SSH Certificate Issuer for Secure Access"),
            secure_access_web: bool = Field(default=False, description="Enable Web Secure Remote Access (for database dynamic secrets)"),
            # LDAP Dynamic Secret Parameters
            provider_type: Optional[str] = Field(default=None, description="Provider type for LDAP dynamic secrets"),
            ldap_url: Optional[str] = Field(default=None, description="LDAP Server URL for dynamic secrets"),
            bind_dn: Optional[str] = Field(default=None, description="Bind DN for LDAP dynamic secrets"),
            bind_dn_password: Optional[str] = Field(default=None, description="Bind DN Password for LDAP dynamic secrets"),
            ldap_ca_cert: Optional[str] = Field(default=None, description="CA Certificate File Content for LDAP"),
            token_expiration: Optional[str] = Field(default=None, description="Token expiration for LDAP dynamic secrets"),
            external_username: bool = Field(default=False, description="Use externally provided username [true/false]"),
            fixed_user_claim_keyname: Optional[str] = Field(default="ext_username", description="Key-name of IdP claim for external username"),
            group_dn: Optional[str] = Field(default=None, description="Group DN for temporary user addition"),
            host_provider: Optional[str] = Field(default="explicit", description="Host provider type [explicit/target]"),
            user_attribute: Optional[str] = Field(default=None, description="User attribute for LDAP dynamic secrets"),
            user_dn: Optional[str] = Field(default=None, description="User DN for LDAP dynamic secrets"),
            # MySQL Dynamic Secret Parameters
            mysql_host: Optional[str] = Field(default="127.0.0.1", description="MySQL host for dynamic secrets"),
            mysql_port: Optional[str] = Field(default="3306", description="MySQL port for dynamic secrets"),
            mysql_dbname: Optional[str] = Field(default=None, description="MySQL database name for dynamic secrets"),
            mysql_username: Optional[str] = Field(default=None, description="MySQL username for dynamic secrets"),
            mysql_password: Optional[str] = Field(default=None, description="MySQL password for dynamic secrets"),
            mysql_creation_statements: Optional[str] = Field(default=None, description="MySQL creation statements"),
            mysql_revocation_statements: Optional[str] = Field(default=None, description="MySQL revocation statements"),
            db_server_certificates: Optional[str] = Field(default=None, description="DB server certificates for verification"),
            db_server_name: Optional[str] = Field(default=None, description="Server name for certificate verification"),
            ssl: bool = Field(default=False, description="Enable/Disable SSL for MySQL dynamic secrets"),
            ssl_certificate: Optional[str] = Field(default=None, description="SSL connection certificate for MySQL"),
            # MongoDB Dynamic Secret Parameters
            mongodb_host_port: Optional[str] = Field(default=None, description="MongoDB server host and port"),
            mongodb_name: Optional[str] = Field(default=None, description="MongoDB name for dynamic secrets"),
            mongodb_username: Optional[str] = Field(default=None, description="MongoDB server username"),
            mongodb_password: Optional[str] = Field(default=None, description="MongoDB server password"),
            mongodb_server_uri: Optional[str] = Field(default=None, description="MongoDB server URI"),
            mongodb_default_auth_db: Optional[str] = Field(default=None, description="MongoDB default authentication database"),
            mongodb_uri_options: Optional[str] = Field(default=None, description="MongoDB server URI options"),
            mongodb_roles: Optional[str] = Field(default="[]", description="MongoDB roles (default: [])"),
            mongodb_custom_data: Optional[str] = Field(default=None, description="MongoDB custom data"),
            mongodb_atlas_api_public_key: Optional[str] = Field(default=None, description="MongoDB Atlas API public key"),
            mongodb_atlas_api_private_key: Optional[str] = Field(default=None, description="MongoDB Atlas API private key"),
            mongodb_atlas_project_id: Optional[str] = Field(default=None, description="MongoDB Atlas project ID"),
            # Target Association
            target_name: Optional[str] = Field(default=None, description="Target name to associate with dynamic secret"),
            # Rotation specific parameters
            rotation_interval: Optional[int] = Field(default=None, description="Rotation interval in seconds (for rotated secrets)"),
            auto_rotate: bool = Field(default=False, description="Enable auto-rotation (for rotated secrets)"),
            # List specific parameters
            path: Optional[str] = Field(default=None, description="Path to list secrets from (for list action only - not used for list_dynamic_secrets)"),
            filter_by: Optional[str] = Field(default=None, description="Filter secrets by pattern (for list action only - not used for list_dynamic_secrets)"),
            secret_types: Optional[List[str]] = Field(default=None, description="Filter by secret types within the specified directory. Options: ['static-secret', 'dynamic-secret', 'rotated-secret']. Leave empty to include all types. Note: This filters within the specified path, unlike 'list_dynamic_secrets' which searches globally."),
            # Delete specific parameters
            delete_immediately: bool = Field(default=False, description="Delete immediately (bypass soft delete)"),
            delete_in_days: int = Field(default=7, description="Soft delete retention period in days"),
            version: int = Field(default=-1, description="Version to delete (-1 for all versions)")
        ) -> Dict[str, Any]:
            """
            SECRETS MANAGEMENT TOOL - Create, retrieve, update, and delete secrets
            
            SUPPORTED ACTIONS:
            • create_static_secret: Create text/JSON secrets with metadata
            • get_static_secret_value: Retrieve secret values securely  
            • update: Modify secret properties and values
            • delete: Delete individual secrets (smart detection)
            • delete_items: Bulk delete multiple secrets or directories
            • list: List secrets in directory with type filtering
            • list_dynamic_secrets: List all dynamic secrets globally
            • create_dynamic_secret_ldap: Create LDAP dynamic secrets
            • create_dynamic_secret_mysql: Create MySQL dynamic secrets
            • create_dynamic_secret_mongodb: Create MongoDB dynamic secrets
            • list_shared_items: List shared secrets and items
            
            DELETE OPERATIONS:
            • Individual: delete(name="/secret1") 
            • Multiple: delete_items(items=["/secret1", "/secret2"])
            • Directory: delete_items(path="/directory/")
            
            Example: Create a database password secret
            """
            try:
                # Static Secret Operations
                if action == "create_static_secret":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting create_static_secret operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for create_static_secret action",
                            "message": "Please provide a name for the secret"
                        }
                    # Note: 'create_static_secret' action is for static secrets only
                    # For dynamic secrets, use: create_dynamic_secret_ldap, create_dynamic_secret_mysql, create_dynamic_secret_mongodb
                    if secret_type and secret_type.lower() != "static":
                        await self.report_progress(ctx, 15, 100, f"Starting create_static_secret operation")
                        return {
                            "success": False,
                            "error": f"Action 'create_static_secret' only supports static secrets",
                            "message": f"For {secret_type} secrets, use: create_dynamic_secret_{secret_type.lower()} or create_dynamic_secret_ldap/mysql/mongodb"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting create_static_secret operation")
                    return await self.static_manager.create_static_secret(
                        ctx,
                        name=name,
                        value=value,
                        description=description,
                        tags=tags,
                        delete_protection=delete_protection,
                        format=format,
                        accessibility=accessibility,
                        protection_key=protection_key,
                        custom_field=custom_field,
                        password=password,
                        username=username,
                        max_versions=max_versions,
                        metadata=metadata,
                        multiline_value=multiline_value,
                        inject_url=inject_url,
                        change_event=change_event
                    )
                
                elif action == "get_static_secret_value":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting get_static_secret_value operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for get_static_secret_value action",
                            "message": "Please provide a name for the static secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting get_static_secret_value operation")
                    return await self.static_manager.get_static_secret_value(ctx, name)
                
                elif action == "update":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting update operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for update action",
                            "message": "Please provide a name for the secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting update operation")
                    return await self.static_manager.update_static_secret(
                        ctx,
                        name=name,
                        new_name=new_name,
                        value=value,
                        description=description,
                        tags=tags,
                        format=format,
                        accessibility=accessibility,
                        protection_key=protection_key,
                        custom_field=custom_field,
                        password=password,
                        username=username,
                        max_versions=max_versions,
                        metadata=metadata,
                        multiline_value=multiline_value,
                        inject_url=inject_url,
                        change_event=change_event,
                        delete_protection=delete_protection
                    )
                
                # Deletion Operations
                elif action == "delete":
                    if name:
                        await self.dual_log(ctx, "info", f"🗑️ Deleting static secret: {name}")
                        return await self.static_manager.delete_static_secret(ctx, name, delete_protection)
                    else:
                        await self.dual_log(ctx, "info", f"🗑️ Starting smart delete operation")
                        return await self.deletion_ops._smart_delete(
                            ctx=ctx,
                            name=name,
                            items=items,
                            delete_immediately=delete_immediately,
                            delete_in_days=delete_in_days,
                            version=version
                        )
                
                elif action == "delete_items":
                    # Handle bulk deletion: either by directory path or specific item list
                    if path and items:
                        return {
                            "success": False,
                            "error": "Cannot specify both 'path' and 'items' - use one or the other",
                            "message": "Please use either 'path' for directory deletion or 'items' for specific item deletion"
                        }
                    if not path and not items:
                        return {
                            "success": False,
                            "error": "Either 'path' or 'items' must be provided",
                            "message": "Please provide either a directory path or a list of items to delete"
                        }
                    
                    if path:
                        # Directory deletion with DFC key handling
                        return await self.deletion_ops._delete_directory_smart(ctx, path, delete_immediately)
                    else:
                        # Multiple specific items deletion
                        return await self.deletion_ops._delete_multiple_items(ctx, items, delete_immediately, delete_in_days, version)
                
                elif action == "smart_delete_directory":
                    return await self.deletion_ops._smart_delete_directory_with_protection_handling(
                        ctx,
                        directory_path=name,
                        disable_protection=True,
                        force_delete=False
                    )
                
                # List Operations
                elif action == "list":
                    await self.report_progress(ctx, 15, 100, "Starting list operation")
                    return await self.common_ops._list_secrets(ctx, path or "/", filter_by, secret_types)
                
                elif action in ["list_shared_items", "list_shared_secrets"]:
                    return await self.common_ops._list_shared_items(ctx, accessibility, json)
                
                # Dynamic Secret Operations
                elif action == "get_dynamic_secret":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting get_dynamic_secret operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for get_dynamic_secret action",
                            "message": "Please provide a name for the dynamic secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting get_dynamic_secret operation")
                    return await self.dynamic_manager.get_dynamic_secret(ctx, name)
                
                elif action == "get_dynamic_secret_value":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting get_dynamic_secret_value operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for get_dynamic_secret_value action",
                            "message": "Please provide a name for the dynamic secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting get_dynamic_secret_value operation")
                    return await self.dynamic_manager.get_dynamic_secret_value(ctx, name)
                
                elif action == "list_dynamic_secrets":
                    return await self.dynamic_manager.list_dynamic_secrets(ctx)
                
                elif action == "create_dynamic_secret_ldap":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting create_dynamic_secret_ldap operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for create_dynamic_secret_ldap action",
                            "message": "Please provide a name for the LDAP dynamic secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting create_dynamic_secret_ldap operation")
                    return await self.dynamic_manager.create_dynamic_secret_ldap(ctx, 
                        name=name, provider_type=provider_type, ldap_url=ldap_url,
                        bind_dn=bind_dn, bind_dn_password=bind_dn_password,
                        ldap_ca_cert=ldap_ca_cert, token_expiration=token_expiration,
                        external_username=external_username, fixed_user_claim_keyname=fixed_user_claim_keyname,
                        group_dn=group_dn, host_provider=host_provider, user_attribute=user_attribute,
                        user_dn=user_dn, password_length=password_length, producer_encryption_key_name=producer_encryption_key_name,
                        user_ttl=user_ttl, custom_username_template=custom_username_template,
                        delete_protection=delete_protection, tags=tags, secure_access_enable=secure_access_enable,
                        secure_access_host=secure_access_host, secure_access_delay=secure_access_delay,
                        secure_access_certificate_issuer=secure_access_certificate_issuer,
                        target_name=target_name, json=json
                    )
                
                elif action == "create_dynamic_secret_mysql":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting create_dynamic_secret_mysql operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for create_dynamic_secret_mysql action",
                            "message": "Please provide a name for the MySQL dynamic secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting create_dynamic_secret_mysql operation")
                    return await self.dynamic_manager.create_dynamic_secret_mysql(ctx, 
                        name=name, mysql_host=mysql_host, mysql_port=mysql_port,
                        mysql_dbname=mysql_dbname, mysql_username=mysql_username,
                        mysql_password=mysql_password, mysql_creation_statements=mysql_creation_statements,
                        mysql_revocation_statements=mysql_revocation_statements, db_server_certificates=db_server_certificates,
                        db_server_name=db_server_name, ssl=ssl, ssl_certificate=ssl_certificate,
                        password_length=password_length, producer_encryption_key_name=producer_encryption_key_name,
                        user_ttl=user_ttl, custom_username_template=custom_username_template,
                        delete_protection=delete_protection, tags=tags, secure_access_enable=secure_access_enable,
                        secure_access_host=secure_access_host, secure_access_delay=secure_access_delay,
                        secure_access_certificate_issuer=secure_access_certificate_issuer, secure_access_web=secure_access_web,
                        target_name=target_name, json=json
                    )
                
                elif action == "create_dynamic_secret_mongodb":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting create_dynamic_secret_mongodb operation")
                        return {
                            "success": False,
                            "error": "Secret name is required for create_dynamic_secret_mongodb action",
                            "message": "Please provide a name for the MongoDB dynamic secret"
                        }
                    await self.report_progress(ctx, 15, 100, f"Starting create_dynamic_secret_mongodb operation")
                    return await self.dynamic_manager.create_dynamic_secret_mongodb(ctx, 
                        name=name, mongodb_host_port=mongodb_host_port, mongodb_name=mongodb_name,
                        mongodb_username=mongodb_username, mongodb_password=mongodb_password,
                        mongodb_server_uri=mongodb_server_uri, mongodb_default_auth_db=mongodb_default_auth_db,
                        mongodb_uri_options=mongodb_uri_options, mongodb_roles=mongodb_roles,
                        mongodb_custom_data=mongodb_custom_data, mongodb_atlas_api_public_key=mongodb_atlas_api_public_key,
                        mongodb_atlas_api_private_key=mongodb_atlas_api_private_key, mongodb_atlas_project_id=mongodb_atlas_project_id,
                        password_length=password_length, producer_encryption_key_name=producer_encryption_key_name,
                        user_ttl=user_ttl, custom_username_template=custom_username_template,
                        delete_protection=delete_protection, tags=tags, secure_access_enable=secure_access_enable,
                        secure_access_host=secure_access_host, secure_access_delay=secure_access_delay,
                        secure_access_certificate_issuer=secure_access_certificate_issuer, secure_access_web=secure_access_web,
                        target_name=target_name, json=json
                    )
                
                else:
                    return {
                        "success": False,
                        "error": f"Unsupported action: {action}",
                        "message": f"Supported actions: create_static_secret, get_static_secret_value, update, delete, delete_items, list, smart_delete_directory, list_shared_items, list_shared_secrets, get_dynamic_secret, get_dynamic_secret_value, list_dynamic_secrets, create_dynamic_secret_ldap, create_dynamic_secret_mysql, create_dynamic_secret_mongodb"
                    }
            except Exception as e:
                await self.dual_log(ctx, "error", f"Failed to {action} secret '{name}': {e}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": f"Failed to {action} secret '{name}'"
                }