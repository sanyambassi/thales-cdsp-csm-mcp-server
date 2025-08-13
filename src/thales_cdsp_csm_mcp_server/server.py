#!/usr/bin/env python3
"""
Thales CDSP CSM MCP Server

This MCP server provides tools for managing secrets in Thales CSM Akeyless Vault
using FastMCP and the MCP protocol.
"""

import os
import logging
import asyncio
from dotenv import load_dotenv

from fastmcp import FastMCP
from .client import ThalesCDSPCSMConfig, ThalesCDSPCSMClient
from .tools import ThalesCDSPCSMTools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ThalesCDSPCSMMCPServer:
    """MCP Server for Thales CDSP CSM Secrets Management."""
    
    def __init__(self):
        self.config = ThalesCDSPCSMConfig()
        self.client = ThalesCDSPCSMClient(self.config)
        self.server = FastMCP(
            name=os.getenv("MCP_SERVER_NAME", "Thales CDSP CSM Secrets Vault"),
            version=os.getenv("MCP_SERVER_VERSION", "1.0.0")
        )
        self.tools = ThalesCDSPCSMTools(self.client)
        self._setup_tools()
    
    def _setup_tools(self):
        """Setup MCP tools."""
        self.tools.register_tools(self.server)
    
    def add_tool_class(self, tool_class):
        """Add a new tool class to the server."""
        self.tools.add_tool_class(tool_class)
    
    def run(self, transport: str = "stdio", host: str = "localhost", port: int = 8000):
        """
        Run the MCP server.
        
        Args:
            transport: Transport mode - "stdio" or "streamable-http"
            host: Host for HTTP transport (default: localhost)
            port: Port for HTTP transport (default: 8000)
        """
        try:
            logger.info("Starting Thales CDSP CSM MCP Server...")
            logger.info(f"Transport mode: {transport}")
            logger.info(f"API URL: {self.config.api_url}")
            logger.info(f"Access ID: {self.config.access_id[:8]}..." if self.config.access_id else "Access ID: Not set")
            
            # Validate configuration
            if not self.config.access_id or not self.config.access_key:
                logger.error("AKEYLESS_ACCESS_ID and AKEYLESS_ACCESS_KEY must be set")
                return
            
            # Configure transport-specific settings
            if transport == "streamable-http":
                logger.info(f"HTTP server will be available at http://{host}:{port}")
                # Set HTTP-specific configuration
                self.server.host = host
                self.server.port = port
                self.server.streamable_http_path = "/mcp"
                self.server.message_path = "/mcp/message"
                self.server.json_response = True
                self.server.stateless_http = False
            
            # Run the server with specified transport
            if transport == "stdio":
                logger.info("Starting server with stdio transport...")
                self.server.run(transport="stdio")
            elif transport == "streamable-http":
                logger.info(f"Starting server with HTTP transport on {host}:{port}...")
                self.server.run(transport="streamable-http")
            else:
                logger.error(f"Unsupported transport mode: {transport}")
                logger.info("Supported modes: 'stdio', 'streamable-http'")
                return
            
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            # Close the client synchronously since run() is not async
            asyncio.run(self.client.close())


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Thales CDSP CSM MCP Server")
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio",
                       help="Transport mode (default: stdio)")
    parser.add_argument("--host", default="localhost", help="Host for HTTP transport (default: localhost)")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport (default: 8000)")
    
    args = parser.parse_args()
    
    # Create and run server
    server = ThalesCDSPCSMMCPServer()
    server.run(transport=args.transport, host=args.host, port=args.port)


if __name__ == "__main__":
    main() 