"""
Response Formats Data

Contains the actual API response formats and critical warnings.
"""

def get_response_formats():
    """Get response format data for API endpoints."""
    
    return {
        "get_secret_value": {
            "🚨 CRITICAL WARNING": {
                "message": "This endpoint returns {secret_name: secret_value} format, NOT {success, value, name} format!",
                "example": "Response: {'/app-secrets/database-config': '{\"username\": \"dbuser\", \"password\": \"dbpass123\"}'}",
                "action": "Always check for your secret name as the key, never rely on 'success' or 'value' fields"
            },
            "actual_format": {
                "status_code": 200,
                "body": {
                    "/app-secrets/database-config": "{\"username\": \"dbuser\", \"password\": \"dbpass123\", \"host\": \"db.example.com\", \"port\": 5432}"
                },
                "description": "🚨 THIS IS THE ACTUAL RESPONSE FORMAT FROM REAL API CALL! Secret name as key, value as string. NO 'success' or 'value' fields present."
            },
            "response_schema": {
                "⚠️ IMPORTANT - ACTUAL RESPONSE FORMAT": "The API returns {secret_name: secret_value} format, NOT the traditional {success, value, name} format",
                "secret_name": "The secret name/path as the key in the response (e.g., '/test-secret-api-ref')",
                "secret_value": "The secret value as a string (e.g., 'test-value-for-api-reference')",
                "note": "This endpoint does NOT reliably include 'success', 'value', or 'name' fields. Always check for your secret name as the key."
            }
        },
        "auth": {
            "response_schema": {
                "token": "JWT token for subsequent API calls (string, starts with 't-')"
            },
            "actual_format": {
                "status_code": 200,
                "body": {
                    "token": "t-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
                },
                "description": "✅ ACTUAL API RESPONSE - Returns JWT token with 't-' prefix"
            }
        },
        "create_secret": {
            "response_schema": {
                "name": "Name/path of the created secret (string)"
            },
            "actual_format": {
                "status_code": 200,
                "body": {
                    "name": "/app-secrets/api-key"
                },
                "description": "✅ ACTUAL API RESPONSE - Returns only the secret name/path"
            }
        },
        "delete_item": {
            "response_schema": {
                "item_name": "Name/path of the deleted item (string)",
                "item_id": "Unique identifier of the deleted item (integer)"
            },
            "actual_format": {
                "status_code": 200,
                "body": {
                    "item_name": "/app-secrets/temp-secret",
                    "item_id": 123456789
                },
                "description": "✅ ACTUAL API RESPONSE - Returns item name and ID"
            }
        },
        "list_items": {
            "response_schema": {
                "items": "Array of item objects with detailed metadata (array)",
                "next_page": "Base64-encoded pagination token (string, optional)"
            },
            "actual_format": {
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
                "description": "✅ ACTUAL API RESPONSE - Returns array of items with detailed metadata"
            }
        },
        "list_roles": {
            "response_schema": {
                "roles": "Array of role objects with permissions and associations (array)",
                "next_page": "Base64-encoded pagination token (string, optional)"
            },
            "actual_format": {
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
                "description": "✅ ACTUAL API RESPONSE - Returns array of roles with detailed permissions"
            }
        },
        "list_targets": {
            "response_schema": {
                "targets": "Array of target objects with connection details (array)",
                "next_page": "Base64-encoded pagination token (string, optional)"
            },
            "actual_format": {
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
                "description": "✅ ACTUAL API RESPONSE - Returns array of targets with pagination"
            }
        }
    } 