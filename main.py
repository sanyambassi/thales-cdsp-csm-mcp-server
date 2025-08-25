#!/usr/bin/env python3
"""
Thales CSM MCP Server

Simple MCP server for Thales CipherTrust Secrets Management.
"""

import asyncio
import argparse
import signal
import sys
import logging
from src.thales_cdsp_csm_mcp_server.server.mcp_server import ThalesCDSPCSMMCPServer

# Global variable to hold the server instance for graceful shutdown
server_instance = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\nGraceful shutdown initiated...")
    
    global server_instance
    if server_instance:
        print("Cleaning up server resources...")
        try:
            # Close client connections if available
            if hasattr(server_instance, 'client') and server_instance.client:
                print("Closing client connections...")
                # Note: Akeyless client cleanup is handled automatically
            
            print("Server cleanup completed")
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    print("Thales CSM MCP Server shutdown complete. Goodbye!")
    sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Thales CSM MCP Server - Simple secrets management",
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
    
    # Setup graceful shutdown handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    global server_instance
    try:
        # Create server instance (logging will be configured in server initialization)
        server_instance = ThalesCDSPCSMMCPServer()
        
        print("Starting Thales CSM MCP Server...")
        print("Press Ctrl+C for graceful shutdown")
        
        # Use the server's run method which handles all transport modes
        server_instance.run(transport=args.transport, host=args.host, port=args.port)
        
    except KeyboardInterrupt:
        # This shouldn't be reached due to signal handler, but just in case
        print("\nKeyboard interrupt received")
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"Server startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 