#!/usr/bin/env python3
"""
Example usage of Thales CDSP CSM Akeyless Vault MCP Server

This file demonstrates how to use the various tools available in the MCP server.
Note: These are examples and require proper Thales API credentials to run.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from thales_cdsp_csm_mcp_server.client import ThalesCDSPCSMClient
from thales_cdsp_csm_mcp_server.tools.secret_tools import SecretTools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_secret_management():
    """Example of creating and managing static secrets"""
    logger.info("🔐 Example: Secret Management")
    
    # Note: This requires proper Thales API credentials
    try:
        client = ThalesCDSPCSMClient()
        tools = SecretTools(client)
        
        # Example 1: Create a simple text secret
        logger.info("Creating text secret...")
        # await tools.create_static_secret(
        #     name="/examples/text-secret",
        #     value="This is a simple text secret",
        #     description="Example text secret",
        #     tags=["example", "text"]
        # )
        
        # Example 2: Create a JSON configuration secret
        logger.info("Creating JSON secret...")
        # await tools.create_static_secret(
        #     name="/examples/api-config",
        #     value='{"api_key": "sk-123456", "endpoint": "https://api.example.com", "timeout": 30}',
        #     format="json",
        #     description="API configuration",
        #     tags=["example", "json", "api"]
        # )
        
        # Example 3: Create a key-value secret
        logger.info("Creating key-value secret...")
        # await tools.create_static_secret(
        #     name="/examples/database-config",
        #     value='{"host": "localhost", "port": "5432", "database": "mydb", "user": "appuser"}',
        #     format="key-value",
        #     description="Database connection details",
        #     tags=["example", "key-value", "database"]
        # )
        
        logger.info("✅ Secret management examples completed")
        
    except Exception as e:
        logger.warning(f"⚠️ Secret management examples skipped (no credentials): {e}")


async def example_dfc_key_management():
    """Example of creating and managing DFC keys"""
    logger.info("🔑 Example: DFC Key Management")
    
    try:
        client = ThalesCDSPCSMClient()
        tools = SecretTools(client)
        
        # Example 1: Create AES encryption key with auto-rotation
        logger.info("Creating AES encryption key...")
        # await tools.create_dfc_key(
        #     name="/examples/encryption-key",
        #     alg="AES256GCM",
        #     auto_rotate=True,
        #     rotation_interval=30,
        #     description="Example encryption key with auto-rotation",
        #     tags=["example", "encryption", "auto-rotate"]
        # )
        
        # Example 2: Create RSA key for signing
        logger.info("Creating RSA signing key...")
        # await tools.create_dfc_key(
        #     name="/examples/signing-key",
        #     alg="RSA2048",
        #     description="Example RSA signing key",
        #     tags=["example", "signing", "rsa"]
        # )
        
        logger.info("✅ DFC key management examples completed")
        
    except Exception as e:
        logger.warning(f"⚠️ DFC key management examples skipped (no credentials): {e}")


async def example_listing_and_filtering():
    """Example of listing and filtering items"""
    logger.info("📋 Example: Listing and Filtering")
    
    try:
        client = ThalesCDSPCSMClient()
        tools = SecretTools(client)
        
        # Example 1: List all items in examples directory
        logger.info("Listing all items...")
        # result = await tools.list_items(path="/examples")
        # logger.info(f"Found {len(result.get('items', []))} items")
        
        # Example 2: List only DFC keys
        logger.info("Listing DFC keys only...")
        # result = await tools.list_items(
        #     path="/examples",
        #     item_type='["key"]',
        #     minimal_view=True
        # )
        # logger.info(f"Found {len(result.get('items', []))} DFC keys")
        
        # Example 3: List secrets with filtering
        logger.info("Listing secrets with name filtering...")
        # result = await tools.list_items(
        #     path="/examples",
        #     filter_by="config",
        #     item_type='["static-secret"]'
        # )
        # logger.info(f"Found {len(result.get('items', []))} config secrets")
        
        logger.info("✅ Listing and filtering examples completed")
        
    except Exception as e:
        logger.warning(f"⚠️ Listing examples skipped (no credentials): {e}")


async def example_bulk_operations():
    """Example of bulk operations"""
    logger.info("🗂️ Example: Bulk Operations")
    
    try:
        client = ThalesCDSPCSMClient()
        tools = SecretTools(client)
        
        # Example 1: Delete entire test directory
        logger.info("Deleting test directory...")
        # result = await tools.delete_items(path="/examples")
        # logger.info(f"Deleted {result.get('data', {}).get('deleted_count', 0)} items")
        
        # Example 2: Delete specific items
        logger.info("Deleting specific items...")
        # result = await tools.delete_items(
        #     items=["/examples/old-secret1", "/examples/old-secret2"]
        # )
        # logger.info(f"Deleted {result.get('data', {}).get('deleted_count', 0)} items")
        
        logger.info("✅ Bulk operations examples completed")
        
    except Exception as e:
        logger.warning(f"⚠️ Bulk operations examples skipped (no credentials): {e}")


async def main():
    """Run all examples"""
    logger.info("🚀 Thales CDSP CSM Akeyless Vault MCP Server Examples")
    logger.info("=" * 60)
    logger.info("Note: These examples require proper Thales API credentials")
    logger.info("=" * 60)
    
    examples = [
        ("Secret Management", example_secret_management),
        ("DFC Key Management", example_dfc_key_management),
        ("Listing and Filtering", example_listing_and_filtering),
        ("Bulk Operations", example_bulk_operations),
    ]
    
    for example_name, example_func in examples:
        logger.info(f"\n--- {example_name} ---")
        try:
            await example_func()
        except Exception as e:
            logger.error(f"❌ {example_name} failed: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎯 Examples completed!")
    logger.info("To run these examples with real data:")
    logger.info("1. Set AKEYLESS_ACCESS_ID and AKEYLESS_ACCESS_KEY environment variables")
    logger.info("2. Uncomment the example code in this file")
    logger.info("3. Run: python tests/example_usage.py")


if __name__ == "__main__":
    asyncio.run(main()) 