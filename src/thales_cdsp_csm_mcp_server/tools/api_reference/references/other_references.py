"""
Other References

Contains other endpoint reference data.
"""

def get_delete_item_reference(language: str, include_error_handling: bool) -> dict:
    """Get delete item endpoint reference."""
    
    return {
        "endpoint": "/delete-item",
        "method": "POST",
        "description": "Delete a single item from Akeyless",
        "parameters": {
            "name": "Item name/path to delete",
            "token": "Authentication token",
            "accessibility": "Access level (default: regular)",
            "delete-immediately": "Delete immediately (default: false)",
            "delete-in-days": "Days before deletion (default: 7)"
        },
        "response_schema": {
            "item_name": "Name/path of the deleted item (string)",
            "item_id": "Unique identifier of the deleted item (integer)"
        },
        "sample_responses": {
            "success": {
                "status_code": 200,
                "body": {
                    "item_name": "/app-secrets/database-config",
                    "item_id": 555666777
                },
                "description": "Item deleted successfully - returns item name and ID"
            }
        },
        "example_usage": {
            "python": '''import requests

url = "https://your-akeyless-endpoint/delete-item"
data = {
    "name": "/my-secret",
    "token": "your-jwt-token",
    "accessibility": "regular",
    "delete-immediately": False,
    "delete-in-days": 7
}

response = requests.post(url, json=data)
result = response.json()

if "item_name" in result:
    print(f"✅ Successfully deleted item: {result['item_name']} (ID: {result['item_id']})")
else:
    print(f"❌ Failed to delete item: {result.get('error', 'Unknown error')}")'''
        }
    }

def get_codebase_scan_reference(language: str, include_error_handling: bool) -> dict:
    """Get codebase scanning reference for secret detection and migration."""
    
    return {
        "title": "Codebase Secret Scanning & Migration Guide",
        "description": "Comprehensive guide for scanning existing codebases and migrating hardcoded secrets to CipherTrust",
        "scanning_patterns": {
            "environment_variables": [
                "os.getenv()", "os.environ.get()", "process.env", "getenv()"
            ],
            "hardcoded_secrets": [
                "password", "secret", "key", "token", "api_key", "access_key"
            ],
            "configuration_files": [
                ".env", "config.json", "settings.py", "config.py", "secrets.py"
            ]
        },
        "secret_classification": {
            "key_value_pairs": {
                "aws_credentials": ["access_key_id", "secret_access_key", "region"],
                "database_credentials": ["username", "password", "host", "port", "database"]
            },
            "standalone_secrets": [
                "single_passwords", "individual_tokens", "connection_strings"
            ]
        },
        "migration_workflow": [
            "1. Scan codebase for hardcoded secrets using pattern detection",
            "2. Categorize secrets by type (key-value pairs vs standalone)",
                            "3. Use manage_secrets MCP tool with 'create_static_secret' action to create CipherTrust secrets",
            "4. Generate migration report with secret mappings",
            "5. Update code to use CipherTrust secrets at runtime",
            "6. Provide testing and validation instructions"
        ],
        "best_practices": [
            "Scan incrementally - start with high-risk files first",
            "Use pattern-based detection for comprehensive coverage",
            "Classify secrets by type for proper CipherTrust organization",
            "Generate detailed migration reports for tracking",
            "Test thoroughly after migrating secrets",
            "Remove hardcoded secrets from source code",
            "Use environment variables for CipherTrust credentials only"
        ]
    }

def get_secret_migration_reference(language: str, include_error_handling: bool) -> dict:
    """Get secret migration reference for moving secrets to CipherTrust."""
    
    return {
        "title": "Secret Migration to CipherTrust Guide",
        "description": "Complete workflow for migrating hardcoded secrets to CipherTrust using MCP tools",
        "migration_phases": {
            "phase_1_discovery": {
                "title": "Secret Discovery & Classification",
                "steps": [
                    "Scan codebase for hardcoded secrets",
                    "Identify secret types and relationships",
                    "Categorize as key-value pairs or standalone",
                    "Document current secret usage patterns"
                ]
            },
            "phase_2_planning": {
                "title": "Migration Planning",
                "steps": [
                    "Design CipherTrust secret structure",
                    "Plan secret naming conventions",
                    "Determine access control requirements",
                    "Create migration timeline"
                ]
            },
            "phase_3_execution": {
                "title": "Secret Migration",
                "steps": [
                    "Use manage_secrets MCP tool with 'create_static_secret' action to create secrets",
                    "Group related secrets as JSON when appropriate",
                    "Set proper access controls and descriptions",
                    "Test secret retrieval and validation"
                ]
            }
        },
        "secret_organization_strategies": {
            "hierarchical_structure": {
                "description": "Organize secrets by application and environment",
                "example": "/apps/my-app/prod/database-credentials",
                "benefits": "Clear organization, easy access control, environment separation"
            }
        },
        "migration_tools": {
            "manage_secrets": {
                "description": "Primary MCP tool for secret creation and management",
                "actions": ["create", "update", "delete", "list"],
                "use_cases": "Creating new secrets, updating existing ones, bulk operations"
            }
        },
        "migration_checklist": [
            "✅ Scan codebase for all hardcoded secrets",
            "✅ Categorize secrets by type and relationship",
            "✅ Design CipherTrust secret organization structure",
                            "✅ Use manage_secrets MCP tool with 'create_static_secret' action to create secrets",
            "✅ Test secret retrieval and validation",
            "✅ Update application code to use CipherTrust",
            "✅ Remove hardcoded secrets from source code"
        ]
    } 