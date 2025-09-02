"""
Secrets Reference

Contains secret management endpoint reference data.
"""

from ..data.response_formats import get_response_formats
from ..data.best_practices import get_best_practices
from ..examples.common_patterns import get_robust_response_handler

def get_create_secret_reference(language: str, include_error_handling: bool) -> dict:
    """Get create secret endpoint reference."""
    
    response_formats = get_response_formats()
    
    return {
        "endpoint": "/create-secret",
        "method": "POST", 
        "description": "Create a new secret in Akeyless",
        "warning": "⚠️ This endpoint should ONLY be used when building applications that need to interact with Akeyless programmatically (for example, a developer wants to expose create secrets funtionality in their application programitically for their end users). For AI assistants building/modifying user applications, use the MCP tool 'manage_secrets' with 'create_static_secret' action instead.",
        "parameters": {
            "name": "Secret name/path",
            "value": "Secret value",
            "token": "Authentication token",
            "description": "Optional description",
            "accessibility": "Access level (default: regular)",
            "multiline-value": "Whether value is multiline (default: true)"
        },
        "response_schema": response_formats["create_secret"]["response_schema"],
        "sample_responses": {
            "🎯 ACTUAL API RESPONSE (REAL OUTPUT)": {
                "status_code": 200,
                "body": {
                    "name": "/app-secrets/api-key"
                },
                "description": "✅ REAL API RESPONSE - Actual secret creation from your CipherTrust vault"
            },
            "success": {
                "status_code": 200,
                "body": {
                    "name": "/app-secrets/database-config"
                },
                "description": "Example response format for reference"
            },
            "error_already_exists": {
                "status_code": 409,
                "body": {
                    "error": "Secret already exists",
                    "message": "A secret with the name '/app-secrets/database-config' already exists"
                },
                "description": "Secret with the same name already exists"
            },
            "error_invalid_token": {
                "status_code": 401,
                "body": {
                    "error": "Invalid or expired token",
                    "message": "Authentication token is invalid or has expired"
                },
                "description": "Authentication token validation failed"
            },
            "error_missing_required": {
                "status_code": 400,
                "body": {
                    "error": "Missing required fields",
                    "message": "name, value, and token are required fields"
                },
                "description": "Required fields missing from request"
            }
        },
        "example_usage": {
            "python": '''import requests

url = "https://your-akeyless-endpoint/create-secret"
data = {
    "name": "/my-secret",
    "value": "secret-value",
    "token": "your-jwt-token",
    "description": "My secret description",
    "accessibility": "regular",
    "multiline-value": True
}

response = requests.post(url, json=data)
result = response.json()

if result.get("success"):
    print(f"✅ Secret '{result['name']}' created successfully (version {result['version']})")
else:
    print(f"❌ Failed to create secret: {result.get('message', 'Unknown error')}")'''
        }
    }

def get_get_secret_reference(language: str, include_error_handling: bool) -> dict:
    """Get secret retrieval endpoint reference."""
    
    response_formats = get_response_formats()
    best_practices = get_best_practices()
    
    return {
        "endpoint": "/get-secret-value",
        "method": "POST",
        "description": "Retrieve secret values from Akeyless",
        "🚨 CRITICAL WARNING": response_formats["get_secret_value"]["🚨 CRITICAL WARNING"],
        "parameters": {
            "names": "Array of secret names to retrieve",
            "token": "Authentication token", 
            "ignore-cache": "Ignore cached values (default: false)",
            "json": "Return JSON format (default: false)"
        },
        "response_schema": response_formats["get_secret_value"]["response_schema"],
        "sample_responses": {
            "🎯 ACTUAL API RESPONSE (REAL OUTPUT)": {
                "status_code": 200,
                "body": {
                    "/app-secrets/database-config": "{\"username\": \"dbuser\", \"password\": \"dbpass123\", \"host\": \"db.example.com\", \"port\": 5432}"
                },
                "description": "✅ REAL API RESPONSE - Actual secret retrieval from your CipherTrust vault"
            },
            "success_text_format": {
                "status_code": 200,
                "body": {
                    "/app-secrets/database-config": "{\"username\": \"testuser\", \"password\": \"testpass123\", \"host\": \"test.example.com\", \"port\": 5432}"
                },
                "description": "Alternative format - returns raw JSON string with secret name as key"
            },
            "success_json_format": {
                "status_code": 200,
                "body": {
                    "/app-secrets/database-config": {
                        "host": "test.example.com",
                        "password": "testpass123",
                        "port": 5432,
                        "username": "testuser"
                    }
                },
                "description": "Secret retrieved in JSON format - returns parsed object when json=true"
            },
            "success_keyvalue_format": {
                "status_code": 200,
                "body": {
                    "/app-secrets/api-credentials": {
                        "api_key": "test123",
                        "region": "us-east-1",
                        "secret_key": "secret456"
                    }
                },
                "description": "Key-value secret retrieved in JSON format - returns parsed object"
            },
            "error_secret_not_found": {
                "status_code": 404,
                "body": {
                    "error": "Secret not found",
                    "message": "The secret '/non-existent-secret' was not found"
                },
                "description": "Requested secret doesn't exist"
            },
            "error_invalid_token": {
                "status_code": 401,
                "body": {
                    "error": "Invalid or expired token",
                    "message": "Authentication token is invalid or has expired"
                },
                "description": "Authentication token validation failed"
            },
            "error_access_denied": {
                "status_code": 403,
                "body": {
                    "error": "Access denied",
                    "message": "You don't have permission to access this secret"
                },
                "description": "Insufficient permissions to access the secret"
            }
        },
        "example_usage": {
            "python": '''import requests
import json

url = "https://your-akeyless-endpoint/get-secret-value"
data = {
    "names": ["/my-secret"],
    "token": "your-jwt-token",
    "ignore-cache": "false",
    "json": False
}

response = requests.post(url, json=data)
result = response.json()

# IMPORTANT: The actual response format uses the secret name as the key
# Response format: {"/secret/name": "secret_value"}
# NO 'success' field is present in the actual API response!

# Get the secret name (first key in the response)
secret_name = list(result.keys())[0] if result else None
if secret_name:
    secret_value = result[secret_name]
    print(f"✅ Secret '{secret_name}' retrieved successfully")
    print(f"Value: {secret_value}")
    
    # If the value is a JSON string, parse it
    try:
        parsed_value = json.loads(secret_value)
        print(f"Parsed JSON: {parsed_value}")
    except json.JSONDecodeError:
        print("Value is not JSON format")
else:
    print(f"❌ No secret found in response: {result}")'''
        },
        "robust_response_handler": {
            "description": "Robust handler that works with both response formats",
            "code": get_robust_response_handler()
        },
        "🚨 CRITICAL BEST PRACTICES": best_practices["critical_best_practices"],
        "troubleshooting": best_practices["troubleshooting"]
    } 