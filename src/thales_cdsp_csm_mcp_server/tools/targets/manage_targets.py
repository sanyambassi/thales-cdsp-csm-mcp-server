"""
Thales CDSP CSM MCP Server - Targets Management Tools

This module provides tools for managing targets in the Thales CSM Akeyless Vault.
"""

import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient
from .modules import DatabaseTargetsManager, LDAPTargetsManager, CloudTargetsManager, ServiceTargetsManager, TargetDeletionOperations

logger = logging.getLogger(__name__)


class ManageTargetsTools(BaseThalesCDSPCSMTool):
    """Tools for managing targets in the Thales CSM Akeyless Vault."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)
        # Initialize module managers with shared logger
        self.database_manager = DatabaseTargetsManager(client, self.logger)
        self.ldap_manager = LDAPTargetsManager(client, self.logger)
        self.cloud_manager = CloudTargetsManager(client, self.logger)
        self.service_manager = ServiceTargetsManager(client, self.logger)
        self.deletion_ops = TargetDeletionOperations(client, self.logger)

    def register(self, server: FastMCP):
        self._register_manage_targets(server)

    def _register_manage_targets(self, server: FastMCP):
        @server.tool("manage_targets")
        async def manage_targets(
            ctx: Context,
            action: str = Field(description="Target management action to perform. SUPPORTED ACTIONS: 'list' (discover all targets with filtering), 'get' (retrieve detailed target configuration), 'create' (create new database/LDAP targets), 'delete' (delete individual target), 'delete_targets' (bulk delete targets by path)"),
            name: Optional[str] = Field(default=None, description="Exact target name or identifier (REQUIRED for 'get' and 'create' actions). Examples: 'prod-mysql-db', 'aws-production', 'k8s-cluster-west'"),
            filter: Optional[str] = Field(default=None, description="Pattern to filter target names (for 'list' action). Supports wildcards. Examples: 'prod-*', '*database*', 'aws-*'"),
            json: bool = Field(default=False, description="Return structured JSON output for programmatic processing. Use TRUE when integrating with automation scripts or other tools"),
            pagination_token: Optional[str] = Field(default=None, description="Continuation token for large result sets. Automatically provided in previous response metadata when more results are available"),
            target_types: Optional[List[str]] = Field(default=None, description="Filter by specific target types. SUPPORTED: ['mysql', 'postgres', 'mongodb', 'aws', 'azure', 'gcp', 'k8s', 'ssh', 'ldap', 'github', 'dockerhub', 'artifactory', 'salesforce', 'snowflake', 'redshift', 'mssql', 'cassandra', 'hanadb', 'rabbitmq', 'venafi', 'chef', 'web', 'gke', 'eks', 'oracle']. Use multiple types as array."),
            show_versions: bool = Field(default=False, description="Include complete version history and configuration changes for the target (for 'get' action). Essential for audit trails and rollback scenarios"),
            target_version: Optional[int] = Field(default=None, description="Target version (for 'get' action: retrieve specific version, for 'delete' action: delete specific version). Use 0 for latest, positive integers for specific versions, or omit for current active version"),
            uid_token: Optional[str] = Field(default=None, description="Universal identity authentication token. Only required when using universal_identity authentication instead of standard API key authentication"),
            # Create action parameters - Target type selection
            target_type: Optional[str] = Field(default=None, description="Type of target to create (REQUIRED for 'create' action). Examples: 'database', 'ldap', 'aws', 'azure', 'gcp', 'k8s', 'ssh'"),
            # Database target parameters
            db_type: Optional[str] = Field(default=None, description="Database type for database targets. Supported values: 'mysql', 'mssql', 'hanadb', 'postgres', 'mongodb', 'snowflake', 'oracle', 'cassandra', 'redshift', 'redis'"),
            host: Optional[str] = Field(default=None, description="Host address or endpoint (REQUIRED for database targets)"),
            port: Optional[str] = Field(default=None, description="Port number (optional, uses default if not specified)"),
            db_name: Optional[str] = Field(default=None, description="Database name (REQUIRED for database targets)"),
            user_name: Optional[str] = Field(default=None, description="Username (REQUIRED for database targets)"),
            pwd: Optional[str] = Field(default=None, description="Password (REQUIRED for database targets)"),
            connection_type: Optional[str] = Field(default="credentials", description="Type of connection to database. Options: 'credentials', 'cloud-identity', 'wallet', 'parent-target'"),
            ssl: bool = Field(default=False, description="Enable/Disable SSL connection to database"),
            ssl_certificate: Optional[str] = Field(default=None, description="SSL connection certificate data"),
            # LDAP target parameters
            ldap_url: Optional[str] = Field(default=None, description="LDAP Server URL (REQUIRED for LDAP targets)"),
            bind_dn: Optional[str] = Field(default=None, description="Bind DN (REQUIRED for LDAP targets)"),
            bind_dn_password: Optional[str] = Field(default=None, description="Bind DN Password (REQUIRED for LDAP targets)"),
            server_type: Optional[str] = Field(default="OpenLDAP", description="LDAP server type. Options: 'OpenLDAP', 'ActiveDirectory'"),
            ldap_ca_cert: Optional[str] = Field(default=None, description="CA Certificate File Content for LDAP"),
            token_expiration: Optional[str] = Field(default=None, description="Token expiration for LDAP"),
            # Common target parameters
            description: Optional[str] = Field(default=None, description="Description of the target for documentation and management purposes"),
            protection_key: Optional[str] = Field(default=None, description="Protection key name for encrypting target secrets (uses account default if not specified)"),
            max_versions: Optional[str] = Field(default=None, description="Maximum number of versions to keep for the target"),
            cluster_mode: bool = Field(default=False, description="Enable cluster mode for high availability (database targets)"),
            # Cloud-specific parameters
            cloud_service_provider: Optional[str] = Field(default=None, description="Cloud service provider (currently supports Azure)"),
            azure_client_id: Optional[str] = Field(default=None, description="Azure client ID for cloud identity authentication"),
            azure_client_secret: Optional[str] = Field(default=None, description="Azure client secret for cloud identity authentication"),
            azure_tenant_id: Optional[str] = Field(default=None, description="Azure tenant ID for cloud identity authentication"),
            # MongoDB Atlas specific
            mongodb_atlas: bool = Field(default=False, description="Enable MongoDB Atlas specific configuration"),
            mongodb_atlas_api_public_key: Optional[str] = Field(default=None, description="MongoDB Atlas API public key"),
            mongodb_atlas_api_private_key: Optional[str] = Field(default=None, description="MongoDB Atlas API private key"),
            mongodb_atlas_project_id: Optional[str] = Field(default=None, description="MongoDB Atlas project ID"),
            mongodb_default_auth_db: Optional[str] = Field(default=None, description="MongoDB server default authentication database"),
            mongodb_uri_options: Optional[str] = Field(default=None, description="MongoDB server URI options"),
            # Oracle specific
            oracle_service_name: Optional[str] = Field(default=None, description="Oracle database service name"),
            oracle_wallet_login_type: Optional[str] = Field(default=None, description="Oracle Wallet login type (password/mtls)"),
            oracle_wallet_p12_file_data: Optional[str] = Field(default=None, description="Oracle wallet p12 file data in base64"),
            oracle_wallet_sso_file_data: Optional[str] = Field(default=None, description="Oracle wallet sso file data in base64"),
            # Snowflake specific
            snowflake_account: Optional[str] = Field(default=None, description="Snowflake account identifier"),
            snowflake_api_private_key: Optional[str] = Field(default=None, description="Snowflake RSA private key (base64 encoded)"),
            snowflake_api_private_key_password: Optional[str] = Field(default=None, description="Snowflake private key passphrase"),
            # Parent target
            parent_target_name: Optional[str] = Field(default=None, description="Name of the parent target (required when connection-type is 'parent-target')"),
            # Additional parameters
            db_server_certificates: Optional[str] = Field(default=None, description="Database server certificates for verification"),
            db_server_name: Optional[str] = Field(default=None, description="Server name for certificate verification"),
            # Delete action parameters
            force_deletion: bool = Field(default=False, description="Enforce deletion (bypass protection)"),
            path: Optional[str] = Field(default=None, description="Path to delete targets from (for delete_targets action)")
        ) -> Dict[str, Any]:
            """
            TARGET MANAGEMENT TOOL - Manage external system connections and integrations
            
            SUPPORTED ACTIONS:
            • list: Discover all configured targets with filtering
            • get: Retrieve detailed target configuration and credentials
            • create: Create new database or LDAP targets
            • delete: Delete individual target with version control
            • delete_targets: Bulk delete targets within a specific path
            
            SUPPORTED TARGET TYPES:
            • Database: MySQL, PostgreSQL, MSSQL, Oracle, Snowflake, MongoDB, Cassandra, HanaDB, Redshift, Redis
            • LDAP: OpenLDAP, Active Directory
            • Cloud: AWS, Azure, GCP
            
            Example: Create a MySQL database target for application connections
            """
            try:
                if action == "list":
                    return await self._list_targets(
                        ctx,
                        filter=filter,
                        json=json,
                        pagination_token=pagination_token,
                        target_types=target_types,
                        uid_token=uid_token
                    )
                elif action == "get":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting get operation")
                        return {
                            "success": False,
                            "error": "Target name is required for get action",
                            "message": "Please provide a name for the target"
                        }
                    return await self._get_target(
                        ctx,
                        name=name,
                        json=json,
                        show_versions=show_versions,
                        target_version=target_version,
                        uid_token=uid_token
                    )
                elif action == "create":
                    if not name:
                        await self.report_progress(ctx, 15, 100, f"Starting create operation")
                        return {
                            "success": False,
                            "error": "Target name is required for create action",
                            "message": "Please provide a name for the target"
                        }
                    if not target_type:
                        return {
                            "success": False,
                            "error": "Target type is required for create action",
                            "message": "Please specify the target type (e.g., 'database', 'ldap', 'aws', 'azure', 'gcp')"
                        }
                    
                    # Route to appropriate creation method based on target type
                    if target_type.lower() == "database":
                        return await self.database_manager.create_database_target(
                            name=name,
                            db_type=db_type,
                            host=host,
                            port=port,
                            db_name=db_name,
                            username=user_name,
                            password=pwd,
                            connection_type=connection_type,
                            description=description,
                            ssl=ssl,
                            ssl_certificate=ssl_certificate,
                            key=protection_key,
                            max_versions=max_versions,
                            cluster_mode=cluster_mode,
                            cloud_service_provider=cloud_service_provider,
                            azure_client_id=azure_client_id,
                            azure_client_secret=azure_client_secret,
                            azure_tenant_id=azure_tenant_id,
                            mongodb_atlas=mongodb_atlas,
                            mongodb_atlas_api_public_key=mongodb_atlas_api_public_key,
                            mongodb_atlas_api_private_key=mongodb_atlas_api_private_key,
                            mongodb_atlas_project_id=mongodb_atlas_project_id,
                            mongodb_default_auth_db=mongodb_default_auth_db,
                            mongodb_uri_options=mongodb_uri_options,
                            oracle_service_name=oracle_service_name,
                            oracle_wallet_login_type=oracle_wallet_login_type,
                            oracle_wallet_p12_file_data=oracle_wallet_p12_file_data,
                            oracle_wallet_sso_file_data=oracle_wallet_sso_file_data,
                            snowflake_account=snowflake_account,
                            snowflake_api_private_key=snowflake_api_private_key,
                            snowflake_api_private_key_password=snowflake_api_private_key_password,
                            parent_target_name=parent_target_name,
                            db_server_certificates=db_server_certificates,
                            db_server_name=db_server_name,
                            json=json,
                            uid_token=uid_token
                        )
                    elif target_type.lower() == "ldap":
                        return await self.ldap_manager.create_ldap_target(
                            name=name,
                            ldap_url=ldap_url,
                            bind_dn=bind_dn,
                            bind_dn_password=bind_dn_password,
                            description=description,
                            ldap_ca_cert=ldap_ca_cert,
                            token_expiration=token_expiration,
                            json=json,
                            uid_token=uid_token
                        )
                    else:
                        return {
                            "success": False,
                            "error": f"Unsupported target type: {target_type}",
                            "message": f"Target type '{target_type}' is not yet supported. Supported types: 'database', 'ldap'"
                        }
                elif action == "delete":
                    if not name:
                        return {
                            "success": False,
                            "error": "Target name is required for delete action",
                            "message": "Please provide a name for the target to delete"
                        }
                    return await self.deletion_ops.delete_target(
                        ctx, name, force_deletion, target_version, json, uid_token
                    )
                elif action == "delete_targets":
                    if not path:
                        return {
                            "success": False,
                            "error": "Path is required for delete_targets action",
                            "message": "Please provide a path to delete targets from"
                        }
                    return await self.deletion_ops.delete_targets_by_path(
                        ctx, path, force_deletion, json, uid_token
                    )
                else:
                    return {
                        "success": False,
                        "error": f"Invalid action: {action}",
                        "message": "Supported actions: 'list', 'get', 'create', 'delete', 'delete_targets'"
                    }
            except Exception as e:
                await self.dual_log(ctx, "error", f"Failed to manage targets: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while managing targets"
                }

    async def _list_targets(
        self,
        ctx,
        filter: Optional[str] = None,
        json: bool = False,
        pagination_token: Optional[str] = None,
        target_types: Optional[List[str]] = None,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List targets in the Thales CSM Akeyless Vault."""
        # Dual logging: Server-side + MCP protocol
        await self.dual_log(ctx, "info", "Starting operation: list targets")
        try:
            # Prepare request data
            request_data = {
                "json": json
            }
            
            if filter:
                request_data["filter"] = filter
            if pagination_token:
                request_data["pagination-token"] = pagination_token
            if target_types:
                request_data["type"] = target_types
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call
            response = await self.client._make_request("target-list", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": "Targets retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to list targets: {e}")
            raise e

    async def _get_target(
        self,
        ctx,
        name: str,
        json: bool = False,
        show_versions: bool = False,
        target_version: Optional[int] = None,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get details of a specific target."""
        # Dual logging: Server-side + MCP protocol
        await self.dual_log(ctx, "info", f"Starting operation: get target '{name}'")
        try:
            # Prepare request data
            request_data = {
                "name": name,
                "json": json,
                "show-versions": show_versions
            }
            
            if target_version is not None:
                request_data["target-version"] = target_version
            
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call - use target-get-details for more comprehensive information
            response = await self.client._make_request("target-get-details", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": f"Target '{name}' retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to get target '{name}': {e}")
            raise e

    async def _create_database_target(
        self,
        name: str,
        db_type: str,
        host: str,
        db_name: str,
        user_name: str,
        pwd: str,
        port: Optional[str] = None,
        connection_type: str = "credentials",
        description: Optional[str] = None,
        ssl: bool = False,
        ssl_certificate: Optional[str] = None,
        protection_key: Optional[str] = None,
        max_versions: Optional[str] = None,
        cluster_mode: bool = False,
        cloud_service_provider: Optional[str] = None,
        azure_client_id: Optional[str] = None,
        azure_client_secret: Optional[str] = None,
        azure_tenant_id: Optional[str] = None,
        mongodb_atlas: bool = False,
        mongodb_atlas_api_public_key: Optional[str] = None,
        mongodb_atlas_api_private_key: Optional[str] = None,
        mongodb_atlas_project_id: Optional[str] = None,
        mongodb_default_auth_db: Optional[str] = None,
        mongodb_uri_options: Optional[str] = None,
        oracle_service_name: Optional[str] = None,
        oracle_wallet_login_type: Optional[str] = None,
        oracle_wallet_p12_file_data: Optional[str] = None,
        oracle_wallet_sso_file_data: Optional[str] = None,
        snowflake_account: Optional[str] = None,
        snowflake_api_private_key: Optional[str] = None,
        snowflake_api_private_key_password: Optional[str] = None,
        parent_target_name: Optional[str] = None,
        db_server_certificates: Optional[str] = None,
        db_server_name: Optional[str] = None,
        json: bool = False,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new database target in the Thales CSM Akeyless Vault."""
        # Dual logging: Server-side + MCP protocol
        await self.dual_log(ctx, "info", f"Starting operation: create database target '{name}'")
        try:
            # Validate required database parameters
            if not db_type:
                        return {
                    "success": False,
                    "error": "Database type is required for database targets",
                    "message": "Please specify the database type. Supported values: 'mysql', 'mssql', 'hanadb', 'postgres', 'mongodb', 'snowflake', 'oracle', 'cassandra', 'redshift', 'redis'"
                }
            if not host:
                        return {
                    "success": False,
                    "error": "Host is required for database targets",
                    "message": "Please provide the database host address"
                }
            if not db_name:
                        return {
                    "success": False,
                    "error": "Database name is required for database targets",
                    "message": "Please provide the database name"
                }
            if not user_name:
                        return {
                    "success": False,
                    "error": "Username is required for database targets",
                    "message": "Please provide the database username"
                }
            if not pwd:
                        return {
                    "success": False,
                    "error": "Password is required for database targets",
                    "message": "Please provide the database password"
                }
            
            # Prepare request data with required fields
            request_data = {
                "name": name,
                "db-type": db_type,
                "host": host,
                "db-name": db_name,
                "user-name": user_name,
                "pwd": pwd,
                "connection-type": connection_type,
                "json": json
            }
            
            # Add optional fields if provided
            if port:
                request_data["port"] = port
            if description:
                request_data["description"] = description
            if ssl:
                request_data["ssl"] = ssl
            if ssl_certificate:
                request_data["ssl-certificate"] = ssl_certificate
            if protection_key:
                request_data["key"] = protection_key
            if max_versions:
                request_data["max-versions"] = max_versions
            if cluster_mode:
                request_data["cluster-mode"] = cluster_mode
            if cloud_service_provider:
                request_data["cloud-service-provider"] = cloud_service_provider
            if azure_client_id:
                request_data["azure-client-id"] = azure_client_id
            if azure_client_secret:
                request_data["azure-client-secret"] = azure_client_secret
            if azure_tenant_id:
                request_data["azure-tenant-id"] = azure_tenant_id
            if mongodb_atlas:
                request_data["mongodb-atlas"] = mongodb_atlas
            if mongodb_atlas_api_public_key:
                request_data["mongodb-atlas-api-public-key"] = mongodb_atlas_api_public_key
            if mongodb_atlas_api_private_key:
                request_data["mongodb-atlas-api-private-key"] = mongodb_atlas_api_private_key
            if mongodb_atlas_project_id:
                request_data["mongodb-atlas-project-id"] = mongodb_atlas_project_id
            if mongodb_default_auth_db:
                request_data["mongodb-default-auth-db"] = mongodb_default_auth_db
            if mongodb_uri_options:
                request_data["mongodb-uri-options"] = mongodb_uri_options
            if oracle_service_name:
                request_data["oracle-service-name"] = oracle_service_name
            if oracle_wallet_login_type:
                request_data["oracle-wallet-login-type"] = oracle_wallet_login_type
            if oracle_wallet_p12_file_data:
                request_data["oracle-wallet-p12-file-data"] = oracle_wallet_p12_file_data
            if oracle_wallet_sso_file_data:
                request_data["oracle-wallet-sso-file-data"] = oracle_wallet_sso_file_data
            if snowflake_account:
                request_data["snowflake-account"] = snowflake_account
            if snowflake_api_private_key:
                request_data["snowflake-api-private-key"] = snowflake_api_private_key
            if snowflake_api_private_key_password:
                request_data["snowflake-api-private-key-password"] = snowflake_api_private_key_password
            if parent_target_name:
                request_data["parent-target-name"] = parent_target_name
            if db_server_certificates:
                request_data["db-server-certificates"] = db_server_certificates
            if db_server_name:
                request_data["db-server-name"] = db_server_name
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call to create the database target
            response = await self.client._make_request("target-create-db", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": f"Database target '{name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to create database target '{name}': {e}")
            raise e

    async def _create_ldap_target(
        self,
        name: str,
        ldap_url: str,
        bind_dn: str,
        bind_dn_password: str,
        server_type: str = "OpenLDAP",
        ldap_ca_cert: Optional[str] = None,
        token_expiration: Optional[str] = None,
        description: Optional[str] = None,
        protection_key: Optional[str] = None,
        max_versions: Optional[str] = None,
        json: bool = False,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new LDAP target in the Thales CSM Akeyless Vault."""
        # Dual logging: Server-side + MCP protocol
        await self.dual_log(ctx, "info", f"Starting operation: create ldap target '{name}'")
        try:
            # Validate required LDAP parameters
            if not ldap_url:
                        return {
                    "success": False,
                    "error": "LDAP URL is required for LDAP targets",
                    "message": "Please provide the LDAP server URL"
                }
            if not bind_dn:
                        return {
                    "success": False,
                    "error": "Bind DN is required for LDAP targets",
                    "message": "Please provide the Bind DN"
                }
            if not bind_dn_password:
                        return {
                    "success": False,
                    "error": "Bind DN Password is required for LDAP targets",
                    "message": "Please provide the Bind DN Password"
                }
            
            # Prepare request data with required fields
            request_data = {
                "name": name,
                "ldap-url": ldap_url,
                "bind-dn": bind_dn,
                "bind-dn-password": bind_dn_password,
                "server-type": server_type,
                "json": json
            }
            
            # Add optional fields if provided
            if description:
                request_data["description"] = description
            if protection_key:
                request_data["key"] = protection_key
            if max_versions:
                request_data["max-versions"] = max_versions
            if ldap_ca_cert:
                request_data["ldap-ca-cert"] = ldap_ca_cert
            if token_expiration:
                request_data["token-expiration"] = token_expiration
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call to create the LDAP target
            response = await self.client._make_request("target-create-ldap", request_data)
            
            return {
                "success": True,
                "data": response,
                "message": f"LDAP target '{name}' created successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to create LDAP target '{name}': {e}")
            raise e 