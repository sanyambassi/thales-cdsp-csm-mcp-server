"""
Thales CDSP CSM MCP Server

A Model Context Protocol (MCP) server for managing secrets in Thales CSM Akeyless Vault
"""

from .server import ThalesCDSPCSMMCPServer
from .client import ThalesCDSPCSMConfig, ThalesCDSPCSMClient

__version__ = "0.1.0"
__author__ = "Thales CDSP Team"
__all__ = ["ThalesCDSPCSMMCPServer", "ThalesCDSPCSMConfig", "ThalesCDSPCSMClient"] 