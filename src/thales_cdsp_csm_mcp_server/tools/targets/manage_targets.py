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

logger = logging.getLogger(__name__)


class ManageTargetsTools(BaseThalesCDSPCSMTool):
    """Tools for managing targets in the Thales CSM Akeyless Vault."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_manage_targets(server)

    def _register_manage_targets(self, server: FastMCP):
        @server.tool("manage_targets")
        async def manage_targets(
            ctx: Context,
            action: str = Field(description="🔐 TARGETS MANAGEMENT: Action to perform: 'list', 'get' (get includes version support)"),
            name: Optional[str] = Field(default=None, description="Target name (required for get action)"),
            filter: Optional[str] = Field(default=None, description="Filter by target name or part of it (for list action)"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            pagination_token: Optional[str] = Field(default=None, description="Next page reference (for list action)"),
            target_types: Optional[List[str]] = Field(default=None, description="List of target types to filter by (for list action). Options: hanadb, cassandra, aws, ssh, gke, eks, mysql, mongodb, snowflake, mssql, redshift, artifactory, azure, rabbitmq, k8s, venafi, gcp, oracle, dockerhub, ldap, github, chef, web, salesforce, postgres"),
            show_versions: bool = Field(default=False, description="Include all target versions in reply (for get action)"),
            target_version: Optional[int] = Field(default=None, description="Specific target version to retrieve (0 for latest)"),
            uid_token: Optional[str] = Field(default=None, description="The universal identity token, Required only for universal_identity authentication")
        ) -> Dict[str, Any]:
            """
            🔐 TARGETS MANAGEMENT TOOL
            
            🏆 ENTERPRISE-GRADE TARGET MANAGEMENT: 
            - Thales CipherTrust Secrets Management (CSM) with Akeyless Vault
            - Enterprise-grade target management with access control and audit trails
            
            📋 AVAILABLE OPERATIONS:
            - list: List all targets with optional filtering by type
            - get: Get detailed information about a specific target (includes version support)
            
            🎯 SUPPORTED TARGET TYPES:
            hanadb, cassandra, aws, ssh, gke, eks, mysql, mongodb, snowflake, 
            mssql, redshift, artifactory, azure, rabbitmq, k8s, venafi, gcp, 
            oracle, dockerhub, ldap, github, chef, web, salesforce, postgres
            
            Example: List all targets or get detailed target information with version control
            """
            try:
                if action == "list":
                    return await self._list_targets(
                        filter=filter,
                        json=json,
                        pagination_token=pagination_token,
                        target_types=target_types,
                        uid_token=uid_token
                    )
                elif action == "get":
                    if not name:
                        return {
                            "success": False,
                            "error": "Target name is required for get action",
                            "message": "Please provide a name for the target"
                        }
                    return await self._get_target(
                        name=name,
                        json=json,
                        show_versions=show_versions,
                        target_version=target_version,
                        uid_token=uid_token
                    )
                else:
                    return {
                        "success": False,
                        "error": f"Invalid action: {action}",
                        "message": "Supported actions: 'list', 'get'"
                    }
            except Exception as e:
                await self.hybrid_log(ctx, "error", f"Failed to manage targets: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while managing targets"
                }

    async def _list_targets(
        self,
        filter: Optional[str] = None,
        json: bool = False,
        pagination_token: Optional[str] = None,
        target_types: Optional[List[str]] = None,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """List targets in the Thales CSM Akeyless Vault."""
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
        name: str,
        json: bool = False,
        show_versions: bool = False,
        target_version: Optional[int] = None,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get details of a specific target."""
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