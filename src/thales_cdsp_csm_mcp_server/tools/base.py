"""
Thales CDSP CSM MCP Server - Base Tools

This module provides the base classes and tool registry for all MCP tools.
"""

import logging
from typing import Dict, List, Type

from ..core.client import ThalesCDSPCSMClient

logger = logging.getLogger(__name__)


class BaseThalesCDSPCSMTool:
    """Base class for all Thales CDSP CSM MCP tools."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)


class ThalesCDSPCSMTools:
    """Registry and manager for all Thales CDSP CSM MCP tools."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        self.client = client
        self.tools: Dict[str, BaseThalesCDSPCSMTool] = {}
        self._register_default_tools()
    
    def add_tool_class(self, tool_instance: BaseThalesCDSPCSMTool):
        """Add a tool class instance to the registry."""
        # Convert camelCase to snake_case and remove 'tools' suffix
        class_name = tool_instance.__class__.__name__
        
        # Remove 'Tools' suffix first
        if class_name.endswith('Tools'):
            class_name = class_name[:-5]  # Remove 'Tools'
        
        # Convert camelCase to snake_case
        import re
        tool_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', class_name).lower()
        
        self.tools[tool_name] = tool_instance
        if logger.isEnabledFor(logging.INFO):
            logger.info(f"Registered tool: {tool_name}")
    
    def get_tool(self, tool_name: str) -> BaseThalesCDSPCSMTool:
        """Get a tool by name."""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self.tools.keys())
    
    def _register_default_tools(self):
        """Register the default set of tools."""
        # Import and register consolidated tools from their new locations
        from .secrets.manage_secrets import ManageSecretsTools
        from .dfc_keys.manage_dfc_keys import ManageDFCKeysTools
        from .auth.manage_auth import ManageAuthTools
        from .customer_fragments.manage_customer_fragments import ManageCustomerFragmentsTools
        from .guidelines.security_guidelines import SecurityGuidelinesTools
        from .rotation.manage_rotation import ManageRotationTools
        # Register consolidated tool classes only
        self.add_tool_class(ManageSecretsTools(self.client))
        self.add_tool_class(ManageDFCKeysTools(self.client))
        self.add_tool_class(ManageAuthTools(self.client))
        self.add_tool_class(ManageCustomerFragmentsTools(self.client))
        self.add_tool_class(SecurityGuidelinesTools(self.client))
        self.add_tool_class(ManageRotationTools(self.client))
        
        if logger.isEnabledFor(logging.INFO):
            logger.info(f"Registered {len(self.tools)} consolidated tools") 