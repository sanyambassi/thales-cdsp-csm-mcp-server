"""
Database Targets Management Module

This module handles all database target operations including creation and management.
"""

import logging
from typing import Dict, Any, Optional, List
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class DatabaseTargetsManager(BaseThalesCDSPCSMTool):
    """Manages database targets operations."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    async def create_database_target(self, name: str, db_type: str, host: str, port: str,
                                   db_name: str, username: str, password: str,
                                   connection_type: str = "credentials", description: Optional[str] = None,
                                   ssl: bool = False, ssl_certificate: Optional[str] = None,
                                   db_server_certificates: Optional[str] = None, db_server_name: Optional[str] = None,
                                   oracle_service_name: Optional[str] = None, oracle_wallet_login_type: Optional[str] = None,
                                   oracle_wallet_p12_file_data: Optional[str] = None, oracle_wallet_sso_file_data: Optional[str] = None,
                                   snowflake_account: Optional[str] = None, snowflake_api_private_key: Optional[str] = None,
                                   snowflake_api_private_key_password: Optional[str] = None, mongodb_atlas: bool = False,
                                   mongodb_atlas_api_private_key: Optional[str] = None, mongodb_atlas_api_public_key: Optional[str] = None,
                                   mongodb_atlas_project_id: Optional[str] = None, mongodb_default_auth_db: Optional[str] = None,
                                   mongodb_uri_options: Optional[str] = None, cluster_mode: bool = False,
                                   cloud_service_provider: Optional[str] = None, azure_client_id: Optional[str] = None,
                                   azure_client_secret: Optional[str] = None, azure_tenant_id: Optional[str] = None,
                                   key: Optional[str] = None, max_versions: Optional[str] = None,
                                   parent_target_name: Optional[str] = None,
                                   tags: Optional[List[str]] = None, json: bool = False,
                                   uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create a database target."""
        try:
            # Validate required parameters
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
                    "message": "Please specify the database host"
                }
            

            
            if not db_name:
                return {
                    "success": False,
                    "error": "Database name is required for database targets",
                    "message": "Please specify the database name"
                }
            
            if not username:
                return {
                    "success": False,
                    "error": "Username is required for database targets",
                    "message": "Please specify the database username"
                }
            
            if not password:
                return {
                    "success": False,
                    "error": "Password is required for database targets",
                    "message": "Please specify the database password"
                }
            
            # Build request data
            request_data = {
                "name": name,
                "db-type": db_type,
                "host": host,
                "db-name": db_name,
                "user-name": username,
                "pwd": password,
                "connection-type": connection_type,
                "json": json
            }
            
            # Add optional fields if provided
            if port:
                request_data["port"] = port
            
            # Add optional fields if provided
            if description:
                request_data["description"] = description
            if ssl:
                request_data["ssl"] = ssl
            if ssl_certificate:
                request_data["ssl-certificate"] = ssl_certificate
            if db_server_certificates:
                request_data["db-server-certificates"] = db_server_certificates
            if db_server_name:
                request_data["db-server-name"] = db_server_name
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
            if mongodb_atlas:
                request_data["mongodb-atlas"] = mongodb_atlas
            if mongodb_atlas_api_private_key:
                request_data["mongodb-atlas-api-private-key"] = mongodb_atlas_api_private_key
            if mongodb_atlas_api_public_key:
                request_data["mongodb-atlas-api-public-key"] = mongodb_atlas_api_public_key
            if mongodb_atlas_project_id:
                request_data["mongodb-atlas-project-id"] = mongodb_atlas_project_id
            if mongodb_default_auth_db:
                request_data["mongodb-default-auth-db"] = mongodb_default_auth_db
            if mongodb_uri_options:
                request_data["mongodb-uri-options"] = mongodb_uri_options
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
            if key:
                request_data["key"] = key
            if max_versions:
                request_data["max-versions"] = max_versions
            if parent_target_name:
                request_data["parent-target-name"] = parent_target_name
            if tags:
                request_data["tags"] = tags
            if uid_token:
                request_data["uid-token"] = uid_token
            
            result = await self.client._make_request("target-create-db", request_data)
            return {
                "success": True,
                "data": result,
                "message": f"Database target '{name}' created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to create database target '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create database target '{name}'"
            }
    
    def get_supported_database_types(self) -> List[str]:
        """Get list of supported database types."""
        return [
            'mysql', 'mssql', 'hanadb', 'postgres', 'mongodb', 
            'snowflake', 'oracle', 'cassandra', 'redshift', 'redis'
        ]
    
    def validate_database_type(self, db_type: str) -> bool:
        """Validate if the database type is supported."""
        return db_type.lower() in self.get_supported_database_types() 