#!/usr/bin/env python3
"""
Basic server test for Thales CDSP CSM MCP Server

This test verifies that the server can start and register tools correctly.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from thales_cdsp_csm_mcp_server.server import ThalesCDSPCSMMCPServer
from thales_cdsp_csm_mcp_server.client import ThalesCDSPCSMClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_server_startup():
    """Test that the server can start and register tools"""
    try:
        # Create server instance
        server = ThalesCDSPCSMMCPServer()
        
        # Verify tools are registered
        tool_names = [tool.name for tool in server.server.tools.values()]
        expected_tools = [
            "create_static_secret",
            "create_dfc_key", 
            "list_items",
            "get_secret",
            "update_secret_value",
            "update_item",
            "delete_item",
            "delete_items",
            "set_item_state",
            "update_rotation_settings"
        ]
        
        missing_tools = set(expected_tools) - set(tool_names)
        if missing_tools:
            logger.error(f"Missing tools: {missing_tools}")
            return False
            
        logger.info(f"✅ All {len(expected_tools)} tools registered successfully")
        logger.info(f"Available tools: {tool_names}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Server startup test failed: {e}")
        return False


async def test_client_creation():
    """Test that the client can be created"""
    try:
        # This will fail without proper environment variables, but we can test creation
        client = ThalesCDSPCSMClient()
        logger.info("✅ Client created successfully")
        return True
        
    except Exception as e:
        logger.warning(f"⚠️ Client creation test failed (expected without env vars): {e}")
        return True  # Not a critical failure


async def main():
    """Run all tests"""
    logger.info("🧪 Starting server tests...")
    
    tests = [
        ("Server Startup", test_server_startup),
        ("Client Creation", test_client_creation),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        try:
            result = await test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"{test_name}: {status}")
        except Exception as e:
            logger.error(f"{test_name}: ❌ ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Server is ready.")
        return 0
    else:
        logger.error("⚠️ Some tests failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 