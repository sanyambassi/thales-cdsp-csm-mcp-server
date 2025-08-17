#!/usr/bin/env python3
"""
STDIO MCP Test Script

This script tests the MCP server over STDIO transport mode.
It performs initialization, tools/list, and list_items commands using stdio transport.
"""

import asyncio
import json
import subprocess
import sys
import pytest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.mark.asyncio
async def test_stdio_mcp():
    """Test MCP server over STDIO transport."""
    print("🔍 Testing MCP server over STDIO transport...")
    print("Starting server process...")
    print("-" * 60)
    
    try:
        # Start the server process with UTF-8 encoding
        process = subprocess.Popen(
            [sys.executable, "main.py", "--transport", "stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            encoding='utf-8',
            errors='replace'
        )
        
        # Step 1: Initialize
        print("📝 Step 1: Initialize")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",  # Latest version (also supports 2025-03-26)
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "STDIO-MCP-Test",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialize request
        request_str = json.dumps(init_request) + "\n"
        process.stdin.write(request_str)
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        assert response_line, "No response from initialize"
        
        data = json.loads(response_line)
        assert 'result' in data, f"Initialize failed: {data}"
        
        server_info = data['result'].get('serverInfo', {})
        print(f"   ✅ Initialized: {server_info.get('name', 'Unknown')} v{server_info.get('version', 'Unknown')}")
        
        # Step 2: Send initialized notification (no response expected)
        print("\n📝 Step 2: Send initialized notification")
        init_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {}
        }
        
        notification_str = json.dumps(init_notification) + "\n"
        process.stdin.write(notification_str)
        process.stdin.flush()
        
        # No response expected for notifications - move to next step
        print("   ✅ Notification sent (no response expected)")
        
        # Step 3: List tools
        print("\n📝 Step 3: List tools")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
            "params": {}
        }
        
        tools_str = json.dumps(tools_request) + "\n"
        process.stdin.write(tools_str)
        process.stdin.flush()
        
        # Read tools response
        tools_response = process.stdout.readline()
        assert tools_response, "No response from tools/list"
        
        tools_data = json.loads(tools_response)
        assert 'result' in tools_data, f"Tools list failed: {tools_data}"
        
        tools = tools_data['result'].get('tools', [])
        print(f"   ✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"      - {tool.get('name', 'Unknown')}")
        
        # Verify we have expected consolidated tools
        tool_names = [tool.get('name') for tool in tools]
        expected_tools = [
            'manage_secrets',
            'manage_dfc_keys', 
            'manage_auth',
            'manage_customer_fragments',
            'security_guidelines',
            'manage_rotation'
        ]
        
        for tool in expected_tools:
            assert tool in tool_names, f"Consolidated tool '{tool}' not found"
        
        print("   ✅ All expected consolidated tools found")
        
        # Step 4: List items from root directory using manage_secrets
        print("\n📝 Step 4: List items from root directory")
        list_items_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "manage_secrets",
                "arguments": {
                    "action": "list",
                    "path": "/"
                }
            }
        }
        
        list_items_str = json.dumps(list_items_request) + "\n"
        process.stdin.write(list_items_str)
        process.stdin.flush()
        
        # Read list items response
        list_items_response = process.stdout.readline()
        assert list_items_response, "No response from list_items"
        
        list_items_data = json.loads(list_items_response)
        # Full response data available for debugging if needed
        
        assert 'result' in list_items_data, f"List items failed: {list_items_data}"
        
        # Parse the consolidated tool response
        result = list_items_data['result']
        message = result.get('message', 'No message')
        
        print(f"   ✅ Response: {message}")
        
        # Handle different response formats - check both direct data and structuredContent
        items = []
        folders = []
        
        # First try direct data field
        if 'data' in result:
            data = result['data']
            if isinstance(data, dict):
                items = data.get('items', [])
                folders = data.get('folders', [])
            elif isinstance(data, list):
                items = data
        
        # If no items found, check structuredContent
        if not items and 'structuredContent' in result:
            structured_data = result['structuredContent']
            if 'data' in structured_data:
                data = structured_data['data']
                if isinstance(data, dict):
                    items = data.get('items', [])
                    folders = data.get('folders', [])
                elif isinstance(data, list):
                    items = data
        
        print(f"   📊 Found {len(items)} items and {len(folders)} folders in root directory:")
        
        # Display items
        for item in items:
            if isinstance(item, dict):
                item_name = item.get('item_name', item.get('name', item.get('path', item.get('id', 'Unknown'))))
                item_type = item.get('item_type', item.get('type', 'Unknown'))
                print(f"      📄 {item_name} ({item_type})")
            else:
                print(f"      📄 {item}")
        
        # Display folders
        for folder in folders:
            print(f"      📁 {folder}")
            
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        # Clean up
        if 'process' in locals():
            process.terminate()
            process.wait()

if __name__ == "__main__":
    asyncio.run(test_stdio_mcp()) 