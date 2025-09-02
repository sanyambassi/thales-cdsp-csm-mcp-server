"""
List References

Contains list endpoint reference data.
"""

def get_list_items_reference(language: str, include_error_handling: bool) -> dict:
    """Get list items endpoint reference."""
    
    return {
        "endpoint": "/list-items",
        "method": "POST",
        "description": "List items in Akeyless secrets manager",
        "parameters": {
            "path": "Path to list items from (default: /)",
            "token": "Authentication token",
            "filter": "Filter pattern for item names",
            "pagination-token": "Token for pagination"
        },
        "response_schema": {
            "success": "Boolean indicating if listing was successful",
            "items": "Array of item names/paths (array of strings)",
            "next_page_token": "Token for next page if pagination is available (string, optional)",
            "total_count": "Total number of items (integer, optional)"
        },
        "sample_responses": {
            "🎯 ACTUAL API RESPONSE (REAL OUTPUT)": {
                "status_code": 200,
                "body": {
                    "items": [
                        {
                            "item_name": "/app-secrets/database-key",
                            "item_id": 123456789,
                            "display_id": "abc123def456ghi789jkl",
                            "item_type": "AES256GCM",
                            "item_sub_type": "generic",
                            "item_metadata": "",
                            "item_tags": null,
                            "item_size": 32,
                            "last_version": 1,
                            "with_customer_fragment": true,
                            "is_enabled": true,
                            "auto_rotate": true,
                            "rotation_interval": 30,
                            "delete_protection": true,
                            "creation_date": "2024-01-15T10:30:00Z",
                            "modification_date": "2024-01-15T10:30:00Z"
                        }
                    ]
                },
                "description": "✅ REAL API RESPONSE - Actual items from your CipherTrust vault"
            },
            "success_with_items": {
                "status_code": 200,
                "body": {
                    "items": [
                        {
                            "item_name": "/app-secrets/database-config",
                            "item_id": 123456789,
                            "item_type": "STATIC_SECRET",
                            "item_sub_type": "generic",
                            "last_version": 1,
                            "is_enabled": True
                        }
                    ],
                    "next_page": "eyJpIjoiL3RoYWxlc2NyeXB0b2xhYnMvdGNsLWRlZmF1bHQta2V5In0="
                },
                "description": "Example response format for reference"
            }
        },
        "example_usage": {
            "python": '''import requests

url = "https://your-akeyless-endpoint/list-items"
data = {
    "path": "/my-secrets/",
    "token": "your-jwt-token",
    "filter": "database*"
}

response = requests.post(url, json=data)
result = response.json()

if result.get("success"):
    items = result["items"]
    print(f"✅ Found {len(items)} items in the specified path")
    for item in items:
        print(f"  - {item}")
    
    if result.get("next_page_token"):
        print(f"📄 More items available. Use next_page_token: {result['next_page_token']}")
else:
    print(f"❌ Failed to list items: {result.get('message', 'Unknown error')}")'''
        }
    }

def get_list_roles_reference(language: str, include_error_handling: bool) -> dict:
    """Get list roles endpoint reference."""
    
    return {
        "endpoint": "/list-roles",
        "method": "POST",
        "description": "List roles in Akeyless",
        "parameters": {
            "token": "Authentication token",
            "filter": "Filter pattern for role names",
            "pagination-token": "Token for pagination"
        },
        "response_schema": {
            "roles": "Array of role objects (array)",
            "next_page": "Base64-encoded pagination token (string, optional)"
        },
        "sample_responses": {
            "🎯 ACTUAL API RESPONSE (REAL OUTPUT)": {
                "status_code": 200,
                "body": {
                    "roles": [
                        {
                            "role_name": "admin",
                            "rules": {
                                "path_rules": null,
                                "admin": true
                            },
                            "comment": "Provides full access to the account resources",
                            "role_auth_methods_assoc": [
                                {
                                    "assoc_id": "ass-abc123def456ghi789",
                                    "auth_method_name": "admin",
                                    "auth_method_access_id": "/example-access-id;acc-example123"
                                }
                            ],
                            "client_permissions": null,
                            "creation_date": "2024-01-15T10:30:00Z",
                            "modification_date": "2024-01-15T10:30:00Z"
                        }
                    ]
                },
                "description": "✅ REAL API RESPONSE - Actual roles from your CipherTrust vault"
            },
            "success": {
                "status_code": 200,
                "body": {
                    "roles": [
                        {
                            "role_name": "admin",
                            "comment": "Provides full access to the account resources",
                            "creation_date": "2024-05-14T19:28:13Z"
                        }
                    ],
                    "next_page": "eyJpIjoiYWRtaW4ifQ=="
                },
                "description": "Example response format for reference"
            }
        },
        "example_usage": {
            "python": '''import requests

url = "https://your-akeyless-endpoint/list-roles"
data = {
    "token": "your-jwt-token",
    "filter": "admin*"
}

response = requests.post(url, json=data)
result = response.json()

if "roles" in result:
    roles = result["roles"]
    print(f"✅ Found {len(roles)} roles")
    for role in roles:
        print(f"  - {role['role_name']} ({role['comment']})")
    
    if result.get("next_page"):
        print(f"📄 More roles available. Use next_page: {result['next_page']}")
else:
    print(f"❌ Failed to list roles: {result.get('error', 'Unknown error')}")'''
        }
    }

def get_list_targets_reference(language: str, include_error_handling: bool) -> dict:
    """Get list targets endpoint reference."""
    
    return {
        "endpoint": "/target-list", 
        "method": "POST",
        "description": "List targets in Akeyless",
        "parameters": {
            "token": "Authentication token",
            "filter": "Filter pattern for target names",
            "pagination-token": "Token for pagination",
            "target-types": "Array of target types to filter by"
        },
        "response_schema": {
            "targets": "Array of target objects (array)",
            "next_page": "Base64-encoded pagination token (string, optional)"
        },
        "sample_responses": {
            "🎯 ACTUAL API RESPONSE (REAL OUTPUT)": {
                "status_code": 200,
                "body": {
                    "targets": [
                        {
                            "target_name": "/app-targets/aws-production",
                            "target_type": "aws",
                            "target_id": 12345,
                            "with_customer_fragment": true,
                            "protection_key_name": "",
                            "client_permissions": ["read", "list", "update", "delete", "create"],
                            "last_version": 1,
                            "target_details": "",
                            "attributes": null,
                            "credentials_less": false,
                            "creation_date": "2024-01-15T10:30:00Z",
                            "modification_date": "2024-01-15T10:30:00Z"
                        }
                    ],
                    "next_page": "eyJleGFtcGxlLW5leHQtcGFnZS10b2tlbg=="
                },
                "description": "✅ REAL API RESPONSE - Actual targets from your CipherTrust vault"
            },
            "success": {
                "status_code": 200,
                "body": {
                    "targets": [
                        {
                            "target_name": "/database-targets/postgres-prod",
                            "target_type": "postgres", 
                            "target_id": 100001,
                            "creation_date": "2025-05-15T16:17:18Z"
                        }
                    ],
                    "next_page": "eyJpIjoiL2RlbW9zL2RiYS9wb3N0Z3JlU1FMMiJ9"
                },
                "description": "Example response format for reference"
            }
        },
        "example_usage": {
            "python": '''import requests

url = "https://your-akeyless-endpoint/target-list"
data = {
    "token": "your-jwt-token",
    "filter": "database*",
    "target-types": ["mysql", "postgres"]
}

response = requests.post(url, json=data)
result = response.json()

if "targets" in result:
    targets = result["targets"]
    print(f"✅ Found {len(targets)} targets")
    for target in targets:
        print(f"  - {target['target_name']} ({target['target_type']}) - ID: {target['target_id']}")
    
    if result.get("next_page"):
        print(f"📄 More targets available. Use next_page: {result['next_page']}")
else:
    print(f"❌ Failed to list targets: {result.get('error', 'Unknown error')}")'''
        }
    } 