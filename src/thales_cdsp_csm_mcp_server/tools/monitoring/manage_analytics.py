"""
Thales CDSP CSM MCP Server - Analytics Management Tools

This module provides tools for managing analytics and monitoring data in the Thales CSM Akeyless Vault.
"""

import logging
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP, Context
from pydantic import Field

from ..base import BaseThalesCDSPCSMTool
from ...core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class ManageAnalyticsTools(BaseThalesCDSPCSMTool):
    """Tools for managing analytics and monitoring data in the Thales CSM Akeyless Vault."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        super().__init__(client)

    def register(self, server: FastMCP):
        self._register_manage_analytics(server)

    def _register_manage_analytics(self, server: FastMCP):
        @server.tool("manage_analytics")
        async def manage_analytics(
            ctx: Context,
            action: str = Field(description="📊 ANALYTICS MANAGEMENT: Action to perform: 'get'"),
            json: bool = Field(default=False, description="Set output format to JSON"),
            filter_by_type: Optional[str] = Field(default=None, description="Filter analytics by item type (e.g., 'Targets', 'Static Secrets', 'DFC Key')"),
            filter_by_risk: Optional[str] = Field(default=None, description="Filter certificates by risk level ('Expired', 'Healthy')"),
            filter_by_product: Optional[str] = Field(default=None, description="Filter by product ('sm', 'adp', 'sra')"),
            uid_token: Optional[str] = Field(default=None, description="The universal identity token, Required only for universal_identity authentication")
        ) -> Dict[str, Any]:
            """
            📊 ANALYTICS MANAGEMENT TOOL
            
            🏆 ENTERPRISE-GRADE MONITORING & REPORTING: 
            - Thales CipherTrust Secrets Management (CSM) with Akeyless Vault
            - Comprehensive analytics and usage reporting
            - Client-side filtering for focused insights
            
            📋 AVAILABLE OPERATIONS:
            - get: Get comprehensive analytics data with optional filtering
            
            📈 ANALYTICS DATA INCLUDES:
            - Item counts by type (Targets, Secrets, Keys, etc.)
            - Geographic usage data
            - Request volumes and response times
            - Certificate expiry information
            - Client usage reports
            - Product-specific statistics
            
            Example: Get analytics data or filter by specific criteria
            """
            try:
                if action == "get":
                    return await self._get_analytics(
                        json=json,
                        filter_by_type=filter_by_type,
                        filter_by_risk=filter_by_risk,
                        filter_by_product=filter_by_product,
                        uid_token=uid_token
                    )
                else:
                    return {
                        "success": False,
                        "error": f"Invalid action: {action}",
                        "message": "Supported actions: 'get'"
                    }
            except Exception as e:
                await self.hybrid_log(ctx, "error", f"Failed to manage analytics: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "message": "An error occurred while managing analytics"
                }

    async def _get_analytics(
        self,
        json: bool = False,
        filter_by_type: Optional[str] = None,
        filter_by_risk: Optional[str] = None,
        filter_by_product: Optional[str] = None,
        uid_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get analytics data with optional client-side filtering."""
        try:
            # Prepare request data
            request_data = {
                "json": json
            }
            
            if uid_token:
                request_data["uid-token"] = uid_token
            
            # Make API call
            response = await self.client._make_request("get-analytics-data", request_data)
            
            # Apply client-side filtering if requested
            if any([filter_by_type, filter_by_risk, filter_by_product]):
                filtered_response = self._apply_analytics_filters(
                    response, 
                    filter_by_type, 
                    filter_by_risk, 
                    filter_by_product
                )
                response = filtered_response
            
            return {
                "success": True,
                "data": response,
                "message": "Analytics data retrieved successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to get analytics data: {e}")
            raise e

    def _apply_analytics_filters(
        self,
        data: Dict[str, Any],
        filter_by_type: Optional[str] = None,
        filter_by_risk: Optional[str] = None,
        filter_by_product: Optional[str] = None
    ) -> Dict[str, Any]:
        """Apply client-side filtering to analytics data."""
        filtered_data = data.copy()
        
        # Filter by item type
        if filter_by_type and "analytics_data" in data and "all_items" in data["analytics_data"]:
            all_items = data["analytics_data"]["all_items"]
            if len(all_items) > 1:  # Skip header row
                filtered_items = [all_items[0]]  # Keep header
                for item in all_items[1:]:
                    if len(item) > 1 and filter_by_type.lower() in item[0].lower():
                        filtered_items.append(item)
                filtered_data["analytics_data"]["all_items"] = filtered_items
        
        # Filter by certificate risk
        if filter_by_risk and "certificates_expiry_data" in data:
            cert_data = data["certificates_expiry_data"]
            if "risk_counts" in cert_data:
                risk_counts = cert_data["risk_counts"]
                if filter_by_risk in risk_counts:
                    filtered_data["certificates_expiry_data"]["risk_counts"] = {
                        filter_by_risk: risk_counts[filter_by_risk]
                    }
        
        # Filter by product
        if filter_by_product and "usage_reports" in data:
            usage_reports = data["usage_reports"]
            if filter_by_product in usage_reports:
                filtered_data["usage_reports"] = {
                    filter_by_product: usage_reports[filter_by_product]
                }
        
        return filtered_data 