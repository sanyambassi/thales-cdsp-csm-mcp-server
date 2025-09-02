"""
Common Patterns

Contains reusable code patterns and robust handlers.
"""

def get_robust_response_handler():
    """Get robust response handler for different API response formats."""
    
    return '''import requests
import json
from typing import Dict, Any, Optional

def get_secret_robust(secret_name: str, token: str, base_url: str) -> Optional[Dict[str, Any]]:
    """
    Robust secret retrieval that handles different response formats.
    
    Args:
        secret_name: Name of the secret to retrieve
        token: Authentication token
        base_url: Base URL for the API
        
    Returns:
        Parsed secret value as dictionary, or None if failed
    """
    url = f"{base_url}/get-secret-value"
    data = {
        "names": [secret_name],
        "token": token,
        "ignore-cache": "false",
        "json": False
    }
    
    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Handle different response formats
        if secret_name in result:
            # Format 1: {"/secret/name": "json_string"}
            secret_value = result[secret_name]
        elif "value" in result:
            # Format 2: {"value": "json_string", "name": "secret_name"}
            secret_value = result["value"]
        else:
            # Format 3: Direct value or unexpected format
            print(f"⚠️ Unexpected response format: {result}")
            return None
        
        # Parse JSON value
        try:
            if isinstance(secret_value, str):
                parsed_value = json.loads(secret_value)
            else:
                parsed_value = secret_value
            
            print(f"✅ Secret '{secret_name}' retrieved successfully")
            return parsed_value
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON from secret value: {e}")
            print(f"Raw value: {secret_value}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

# Usage example
if __name__ == "__main__":
    # Example usage
    secret_data = get_secret_robust(
        secret_name="/demo_app/aws_credentials",
        token="your-jwt-token",
        base_url="https://your-akeyless-endpoint"
    )
    
    if secret_data:
        print(f"AWS Access Key ID: {secret_data.get('access_key_id', 'Not found')}")
        print(f"AWS Region: {secret_data.get('region', 'Not found')}")
    else:
        print("Failed to retrieve secret")''' 