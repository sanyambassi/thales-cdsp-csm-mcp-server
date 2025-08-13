"""
Base tools class for Thales CDSP CSM MCP server.

This module provides the base class and common functionality
for all Thales CDSP CSM MCP tools.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP
from pydantic import Field

from ..client import ThalesCDSPCSMClient


class BaseThalesCDSPCSMTool(ABC):
    """Base class for Thales CDSP CSM MCP tools."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        self.client = client
    
    @abstractmethod
    def register(self, server: FastMCP):
        """Register this tool with the MCP server."""
        pass


class ThalesCDSPCSMTools:
    """Collection of Thales CDSP CSM MCP tools."""
    
    def __init__(self, client: ThalesCDSPCSMClient):
        self.client = client
        self._tool_classes: List[BaseThalesCDSPCSMTool] = []
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register the default set of tools."""
        from .secret_tools import SecretTools
        
        
        self._tool_classes.append(SecretTools(self.client))

    
    def add_tool_class(self, tool_class: BaseThalesCDSPCSMTool):
        """Add a new tool class to the collection."""
        self._tool_classes.append(tool_class)
    
    def register_tools(self, server: FastMCP):
        """Register all tools with the MCP server."""
        for tool_class in self._tool_classes:
            tool_class.register(server)
    
    def get_tool_count(self) -> int:
        """Get the total number of tools registered."""
        total = 0
        for tool_class in self._tool_classes:
            # This is a simple count - in a real implementation you might
            # want to track the actual number of tools per class
            total += 1
        return total 