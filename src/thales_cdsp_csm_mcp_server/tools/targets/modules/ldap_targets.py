"""
LDAP Targets Management Module

This module handles all LDAP target operations including creation and management.
"""

import logging
from typing import Dict, Any, Optional, List
from ....core.client import ThalesCDSPCSMClient
from ...base import BaseThalesCDSPCSMTool

logger = logging.getLogger(__name__)


class LDAPTargetsManager(BaseThalesCDSPCSMTool):
    """Manages LDAP targets operations."""
    
    def __init__(self, client: ThalesCDSPCSMClient, parent_logger=None):
        super().__init__(client, parent_logger)
        self.client = client
    
    async def create_ldap_target(self, name: str, ldap_url: str, bind_dn: str, bind_dn_password: str,
                                description: Optional[str] = None, ldap_ca_cert: Optional[str] = None,
                                token_expiration: Optional[str] = None, external_username: bool = False,
                                fixed_user_claim_keyname: Optional[str] = "ext_username", group_dn: Optional[str] = None,
                                host_provider: Optional[str] = "explicit", user_attribute: Optional[str] = None,
                                user_dn: Optional[str] = None, password_length: Optional[str] = None,
                                producer_encryption_key_name: Optional[str] = None, user_ttl: str = "60m",
                                custom_username_template: Optional[str] = None, delete_protection: Optional[str] = None,
                                tags: Optional[List[str]] = None, secure_access_enable: Optional[str] = None,
                                secure_access_host: Optional[List[str]] = None, secure_access_delay: Optional[int] = None,
                                secure_access_certificate_issuer: Optional[str] = None, target_name: Optional[str] = None,
                                json: bool = False, uid_token: Optional[str] = None) -> Dict[str, Any]:
        """Create an LDAP target."""
        try:
            # Validate required parameters
            if not ldap_url:
                return {
                    "success": False,
                    "error": "LDAP URL is required for LDAP targets",
                    "message": "Please specify the LDAP server URL"
                }
            
            if not bind_dn:
                return {
                    "success": False,
                    "error": "Bind DN is required for LDAP targets",
                    "message": "Please specify the bind DN for LDAP authentication"
                }
            
            if not bind_dn_password:
                return {
                    "success": False,
                    "error": "Bind DN password is required for LDAP targets",
                    "message": "Please specify the bind DN password for LDAP authentication"
                }
            
            # Build request data
            request_data = {
                "name": name,
                "ldap_url": ldap_url,
                "bind_dn": bind_dn,
                "bind_dn_password": bind_dn_password,
                "json": json
            }
            
            # Add optional fields if provided
            if description:
                request_data["description"] = description
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
            
            result = await self.client.create_ldap_target(request_data)
            return {
                "success": True,
                "data": result,
                "message": f"LDAP target '{name}' created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to create LDAP target '{name}': {e}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to create LDAP target '{name}'"
            }
    
    def get_supported_ldap_types(self) -> List[str]:
        """Get list of supported LDAP types."""
        return ['OpenLDAP', 'ActiveDirectory']
    
    def validate_ldap_type(self, ldap_type: str) -> bool:
        """Validate if the LDAP type is supported."""
        return ldap_type in self.get_supported_ldap_types() 