"""
Dynamic Secrets Management Module

This module handles all dynamic secret operations including creation, retrieval, and management.
"""

import logging
from typing import Dict, Any, Optional, List
from fastmcp import Context
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class DynamicSecretsManager(BaseThalesCDSPCSMTool):
    """Manages dynamic secrets operations."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    async def get_dynamic_secret(self, ctx: Context, name: str) -> Dict[str, Any]:
        """Get dynamic secret metadata."""
        await self.dual_log(ctx, "info", f"Getting dynamic secret metadata: {name}")
        
        try:
            result = await self.client.get_dynamic_secret(name)
            await self.dual_log(ctx, "info", f"Dynamic secret '{name}' metadata retrieved successfully")
            return {
                "success": True,
                "message": f"Dynamic secret '{name}' metadata retrieved successfully",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to get dynamic secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get dynamic secret '{name}'"
            }
    
    async def get_dynamic_secret_value(self, ctx: Context, name: str) -> Dict[str, Any]:
        """Get dynamic secret value."""
        await self.dual_log(ctx, "info", f"Getting dynamic secret value: {name}")
        
        try:
            result = await self.client.get_dynamic_secret_value(name)
            await self.dual_log(ctx, "info", f"Dynamic secret '{name}' value retrieved successfully")
            return {
                "success": True,
                "message": f"Dynamic secret '{name}' value retrieved successfully",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to get dynamic secret value '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to get dynamic secret value '{name}'"
            }
    
    async def list_dynamic_secrets(self, ctx: Context) -> Dict[str, Any]:
        """List all dynamic secrets globally."""
        await self.dual_log(ctx, "info", "Listing all dynamic secrets globally")
        
        try:
            result = await self.client.list_dynamic_secrets()
            await self.dual_log(ctx, "info", "Dynamic secrets listed successfully")
            return {
                "success": True,
                "message": "Dynamic secrets listed successfully from entire vault (global search)",
                "data": result
            }
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to list dynamic secrets: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to list dynamic secrets globally"
            }
    
    async def create_dynamic_secret_ldap(self, ctx: Context, name: str, provider_type: Optional[str] = None,
                                        ldap_url: Optional[str] = None, bind_dn: Optional[str] = None,
                                        bind_dn_password: Optional[str] = None, ldap_ca_cert: Optional[str] = None,
                                        token_expiration: Optional[str] = None, external_username: bool = False,
                                        fixed_user_claim_keyname: Optional[str] = "ext_username", group_dn: Optional[str] = None,
                                        host_provider: Optional[str] = "explicit", user_attribute: Optional[str] = None,
                                        user_dn: Optional[str] = None, password_length: Optional[str] = None,
                                        producer_encryption_key_name: Optional[str] = None, user_ttl: str = "60m",
                                        custom_username_template: Optional[str] = None, delete_protection: Optional[str] = None,
                                        tags: List[str] = None, secure_access_enable: Optional[str] = None,
                                        secure_access_host: List[str] = None, secure_access_delay: Optional[int] = None,
                                        secure_access_certificate_issuer: Optional[str] = None, target_name: Optional[str] = None,
                                        json: bool = False, uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create an LDAP dynamic secret."""
        await self.dual_log(ctx, "info", f"Creating LDAP dynamic secret: {name}")
        
        try:
            request_data = {
                "name": name,
                "json": json
            }
            
            # Add optional fields if provided
            if provider_type:
                request_data["provider_type"] = provider_type
            if ldap_url:
                request_data["ldap_url"] = ldap_url
            if bind_dn:
                request_data["bind_dn"] = bind_dn
            if bind_dn_password:
                request_data["bind_dn_password"] = bind_dn_password
            if ldap_ca_cert:
                request_data["ldap_ca_cert"] = ldap_ca_cert
            if token_expiration:
                request_data["token_expiration"] = token_expiration
            if external_username:
                request_data["external_username"] = external_username
            if fixed_user_claim_keyname:
                request_data["fixed_user_claim_keyname"] = fixed_user_claim_keyname
            if group_dn:
                request_data["group_dn"] = group_dn
            if host_provider:
                request_data["host_provider"] = host_provider
            if user_attribute:
                request_data["user_attribute"] = user_attribute
            if user_dn:
                request_data["user_dn"] = user_dn
            if password_length:
                request_data["password_length"] = password_length
            if producer_encryption_key_name:
                request_data["producer_encryption_key_name"] = producer_encryption_key_name
            if user_ttl:
                request_data["user_ttl"] = user_ttl
            if custom_username_template:
                request_data["custom_username_template"] = custom_username_template
            if delete_protection:
                request_data["delete_protection"] = delete_protection
            if tags:
                request_data["tags"] = tags
            if secure_access_enable:
                request_data["secure_access_enable"] = secure_access_enable
            if secure_access_host:
                request_data["secure_access_host"] = secure_access_host
            if secure_access_delay:
                request_data["secure_access_delay"] = secure_access_delay
            if secure_access_certificate_issuer:
                request_data["secure_access_certificate_issuer"] = secure_access_certificate_issuer
            if target_name:
                request_data["target_name"] = target_name
            if uid_token:
                request_data["uid_token"] = uid_token
            
            # Make API call to create the LDAP dynamic secret
            result = await self.client.create_dynamic_secret_ldap(request_data)
            
            await self.dual_log(ctx, "info", f"LDAP dynamic secret '{name}' created successfully")
            return {
                "success": True,
                "data": result,
                "message": f"LDAP dynamic secret '{name}' created successfully"
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to create LDAP dynamic secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create LDAP dynamic secret '{name}'"
            }

    async def create_dynamic_secret_mysql(self, ctx: Context, name: str, mysql_host: Optional[str] = "127.0.0.1",
                                         mysql_port: Optional[str] = "3306", mysql_dbname: Optional[str] = None,
                                         mysql_username: Optional[str] = None, mysql_password: Optional[str] = None,
                                         mysql_creation_statements: Optional[str] = None, mysql_revocation_statements: Optional[str] = None,
                                         db_server_certificates: Optional[str] = None, db_server_name: Optional[str] = None,
                                         ssl: bool = False, ssl_certificate: Optional[str] = None, password_length: Optional[str] = None,
                                         producer_encryption_key_name: Optional[str] = None, user_ttl: str = "60m",
                                         custom_username_template: Optional[str] = None, delete_protection: Optional[str] = None,
                                         tags: List[str] = None, secure_access_enable: Optional[str] = None,
                                         secure_access_host: List[str] = None, secure_access_delay: Optional[int] = None,
                                         secure_access_certificate_issuer: Optional[str] = None, secure_access_web: bool = False,
                                         target_name: Optional[str] = None, json: bool = False, uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create a MySQL dynamic secret."""
        await self.dual_log(ctx, "info", f"Creating MySQL dynamic secret: {name}")
        
        try:
            request_data = {
                "name": name,
                "json": json
            }
            
            # Add optional fields if provided
            if mysql_host:
                request_data["mysql_host"] = mysql_host
            if mysql_port:
                request_data["mysql_port"] = mysql_port
            if mysql_dbname:
                request_data["mysql_dbname"] = mysql_dbname
            if mysql_username:
                request_data["mysql_username"] = mysql_username
            if mysql_password:
                request_data["mysql_password"] = mysql_password
            if mysql_creation_statements:
                request_data["mysql_creation_statements"] = mysql_creation_statements
            if mysql_revocation_statements:
                request_data["mysql_revocation_statements"] = mysql_revocation_statements
            if db_server_certificates:
                request_data["db_server_certificates"] = db_server_certificates
            if db_server_name:
                request_data["db_server_name"] = db_server_name
            if ssl:
                request_data["ssl"] = ssl
            if ssl_certificate:
                request_data["ssl_certificate"] = ssl_certificate
            if password_length:
                request_data["password_length"] = password_length
            if producer_encryption_key_name:
                request_data["producer_encryption_key_name"] = producer_encryption_key_name
            if user_ttl:
                request_data["user_ttl"] = user_ttl
            if custom_username_template:
                request_data["custom_username_template"] = custom_username_template
            if delete_protection:
                request_data["delete_protection"] = delete_protection
            if tags:
                request_data["tags"] = tags
            if secure_access_enable:
                request_data["secure_access_enable"] = secure_access_enable
            if secure_access_host:
                request_data["secure_access_host"] = secure_access_host
            if secure_access_delay:
                request_data["secure_access_delay"] = secure_access_delay
            if secure_access_certificate_issuer:
                request_data["secure_access_certificate_issuer"] = secure_access_certificate_issuer
            if secure_access_web:
                request_data["secure_access_web"] = secure_access_web
            if target_name:
                request_data["target_name"] = target_name
            if uid_token:
                request_data["uid_token"] = uid_token
            
            # Make API call to create the MySQL dynamic secret
            result = await self.client.create_dynamic_secret_mysql(request_data)
            
            await self.dual_log(ctx, "info", f"MySQL dynamic secret '{name}' created successfully")
            return {
                "success": True,
                "data": result,
                "message": f"MySQL dynamic secret '{name}' created successfully"
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to create MySQL dynamic secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create MySQL dynamic secret '{name}'"
            }

    async def create_dynamic_secret_mongodb(self, ctx: Context, name: str, mongodb_host_port: Optional[str] = None,
                                           mongodb_name: Optional[str] = None, mongodb_username: Optional[str] = None,
                                           mongodb_password: Optional[str] = None, mongodb_server_uri: Optional[str] = None,
                                           mongodb_default_auth_db: Optional[str] = None, mongodb_uri_options: Optional[str] = None,
                                           mongodb_roles: Optional[str] = "[]", mongodb_custom_data: Optional[str] = None,
                                           mongodb_atlas_api_public_key: Optional[str] = None, mongodb_atlas_api_private_key: Optional[str] = None,
                                           mongodb_atlas_project_id: Optional[str] = None, password_length: Optional[str] = None,
                                           producer_encryption_key_name: Optional[str] = None, user_ttl: str = "60m",
                                           custom_username_template: Optional[str] = None, delete_protection: Optional[str] = None,
                                           tags: List[str] = None, secure_access_enable: Optional[str] = None,
                                           secure_access_host: List[str] = None, secure_access_delay: Optional[int] = None,
                                           secure_access_certificate_issuer: Optional[str] = None, secure_access_web: bool = False,
                                           target_name: Optional[str] = None, json: bool = False, uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create a MongoDB dynamic secret."""
        await self.dual_log(ctx, "info", f"Creating MongoDB dynamic secret: {name}")
        
        try:
            request_data = {
                "name": name,
                "json": json
            }
            
            # Add optional fields if provided
            if mongodb_host_port:
                request_data["mongodb_host_port"] = mongodb_host_port
            if mongodb_name:
                request_data["mongodb_name"] = mongodb_name
            if mongodb_username:
                request_data["mongodb_username"] = mongodb_username
            if mongodb_password:
                request_data["mongodb_password"] = mongodb_password
            if mongodb_server_uri:
                request_data["mongodb_server_uri"] = mongodb_server_uri
            if mongodb_default_auth_db:
                request_data["mongodb_default_auth_db"] = mongodb_default_auth_db
            if mongodb_uri_options:
                request_data["mongodb_uri_options"] = mongodb_uri_options
            if mongodb_roles:
                request_data["mongodb_roles"] = mongodb_roles
            if mongodb_custom_data:
                request_data["mongodb_custom_data"] = mongodb_custom_data
            if mongodb_atlas_api_public_key:
                request_data["mongodb_atlas_api_public_key"] = mongodb_atlas_api_public_key
            if mongodb_atlas_api_private_key:
                request_data["mongodb_atlas_api_private_key"] = mongodb_atlas_api_private_key
            if mongodb_atlas_project_id:
                request_data["mongodb_atlas_project_id"] = mongodb_atlas_project_id
            if password_length:
                request_data["password_length"] = password_length
            if producer_encryption_key_name:
                request_data["producer_encryption_key_name"] = producer_encryption_key_name
            if user_ttl:
                request_data["user_ttl"] = user_ttl
            if custom_username_template:
                request_data["custom_username_template"] = custom_username_template
            if delete_protection:
                request_data["delete_protection"] = delete_protection
            if tags:
                request_data["tags"] = tags
            if secure_access_enable:
                request_data["secure_access_enable"] = secure_access_enable
            if secure_access_host:
                request_data["secure_access_host"] = secure_access_host
            if secure_access_delay:
                request_data["secure_access_delay"] = secure_access_delay
            if secure_access_certificate_issuer:
                request_data["secure_access_certificate_issuer"] = secure_access_certificate_issuer
            if secure_access_web:
                request_data["secure_access_web"] = secure_access_web
            if target_name:
                request_data["target_name"] = target_name
            if uid_token:
                request_data["uid_token"] = uid_token
            
            # Make API call to create the MongoDB dynamic secret
            result = await self.client.create_dynamic_secret_mongodb(request_data)
            
            await self.dual_log(ctx, "info", f"MongoDB dynamic secret '{name}' created successfully")
            return {
                "success": True,
                "data": result,
                "message": f"MongoDB dynamic secret '{name}' created successfully"
            }
            
        except Exception as e:
            await self.dual_log(ctx, "error", f"Failed to create MongoDB dynamic secret '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create MongoDB dynamic secret '{name}'"
            } 