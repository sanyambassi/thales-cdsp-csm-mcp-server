"""
Authentication Reference

Contains authentication endpoint reference data.
"""

from ..data.response_formats import get_response_formats

def get_auth_reference(language: str, include_error_handling: bool) -> dict:
    """Get authentication endpoint reference."""
    
    response_formats = get_response_formats()
    
    return {
        "endpoint": "/auth",
        "method": "POST",
        "description": "Authenticate with Akeyless and get access token",
        "parameters": {
            "access-id": "Your Akeyless access ID",
            "access-key": "Your Akeyless access key"
        },
        "response_schema": response_formats["auth"]["response_schema"],
        "sample_responses": {
            "🎯 ACTUAL API RESPONSE (REAL OUTPUT)": {
                "status_code": 200,
                "body": {
                    "token": "t-d1c4d8d09a7dd7dd3f1001db0b9ef660m"
                },
                "description": "✅ REAL API RESPONSE - JWT token with 't-' prefix from actual API call"
            },
            "success": {
                "status_code": 200,
                "body": {
                    "token": "t-abc123def456example789token"
                },
                "description": "Example authentication response - returns JWT token with 't-' prefix"
            },
            "error_invalid_credentials": {
                "status_code": 401,
                "body": {
                    "error": "Invalid access credentials",
                    "message": "The provided access ID or access key is incorrect"
                },
                "description": "Authentication failed due to invalid credentials"
            },
            "error_missing_fields": {
                "status_code": 400,
                "body": {
                    "error": "Missing required fields",
                    "message": "access-id and access-key are required"
                },
                "description": "Request missing required authentication fields"
            }
        },
        "example_usage": {
            "python": '''import requests

url = "https://your-akeyless-endpoint/auth"
data = {
    "access-id": "your-access-id",
    "access-key": "your-access-key"
}

response = requests.post(url, json=data)
result = response.json()

if result.get("success"):
    token = result["token"]
    print(f"✅ Authentication successful. Token expires in {result.get('expires_in', 'unknown')} seconds")
else:
    print(f"❌ Authentication failed: {result.get('message', 'Unknown error')}")'''
        }
    } 