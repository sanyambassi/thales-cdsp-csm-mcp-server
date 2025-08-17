#!/usr/bin/env python3
"""
Thales CipherTrust Secrets Management MCP Server
Powered by Akeyless Vault Technology

A Model Context Protocol (MCP) server for managing secrets in Thales CipherTrust 
Secrets Management (CSM) through AI assistants and applications.
"""

import asyncio
import argparse
from src.thales_cdsp_csm_mcp_server.server.mcp_server import ThalesCDSPCSMMCPServer

def main():
    parser = argparse.ArgumentParser(
        description="Thales CipherTrust Secrets Management MCP Server - Powered by Akeyless",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Start with stdio transport
  python main.py --transport streamable-http --port 8000  # Start HTTP server
        """
    )
    
    parser.add_argument(
        "--transport", 
        choices=["stdio", "streamable-http"], 
        default="stdio",
        help="Transport mode (default: stdio)"
    )
    parser.add_argument(
        "--host", 
        default="0.0.0.0",
        help="Host address for HTTP transport (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for HTTP transport (default: 8000)"
    )
    
    args = parser.parse_args()
    
    # Create server instance (logging will be configured in server initialization)
    server = ThalesCDSPCSMMCPServer()
    
    # Use the server's run method which handles all transport modes
    server.run(transport=args.transport, host=args.host, port=args.port)

if __name__ == "__main__":
    main() 