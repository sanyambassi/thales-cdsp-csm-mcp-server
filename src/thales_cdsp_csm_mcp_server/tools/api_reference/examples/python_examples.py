"""
Python Code Examples

Contains reusable Python code examples for Akeyless integration.
"""

def get_python_generic_workflow(include_error_handling: bool = False) -> dict:
    """Get Python implementation for generic Akeyless workflow."""
    
    basic_impl = '''import os
import json
import requests
from typing import Dict, Any, Optional

class AkeylessClient:
    """Generic Akeyless client for authentication and secret management."""
    
    def __init__(self, access_id: str, access_key: str, base_url: str):
        self.access_id = access_id
        self.access_key = access_key
        self.base_url = base_url.rstrip('/')
        self.token = None
    
    def authenticate(self) -> str:
        """Authenticate with Akeyless and get access token."""
        url = f"{self.base_url}/auth"
        data = {
            "access-id": self.access_id,
            "access-key": self.access_key
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        self.token = result.get("token")
        return self.token
    
    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve a secret using the authentication token."""
        if not self.token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        url = f"{self.base_url}/get-secret-value"
        data = {
            "names": [secret_name],
            "token": self.token,
            "ignore-cache": "false",
            "json": False
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        
        # Handle the actual API response format: {secret_name: value}
        if secret_name in result:
            return result[secret_name]
        elif "value" in result:
            # Fallback for other response formats
            return result["value"]
        else:
            raise ValueError(f"Unexpected response format: {result}")

class ApplicationConfig:
    """Application configuration using Akeyless secrets."""
    
    def __init__(self, akeyless_client: AkeylessClient):
        self.akeyless_client = akeyless_client
    
    def get_database_config(self, secret_name: str) -> Dict[str, str]:
        """Get database configuration from Akeyless secret."""
        secret_data = self.akeyless_client.get_secret(secret_name)
        # Handle different response formats
        if isinstance(secret_data, str):
            # If it's a JSON string, parse it
            config = json.loads(secret_data)
        elif isinstance(secret_data, dict):
            # If it's already a dict, use it directly
            config = secret_data
        else:
            # Fallback to empty dict
            config = {}
        return config
    
    def get_api_key(self, secret_name: str) -> str:
        """Get API key from Akeyless secret."""
        secret_data = self.akeyless_client.get_secret(secret_name)
        # Handle different response formats
        if isinstance(secret_data, str):
            # If it's a JSON string, try to parse it
            try:
                parsed = json.loads(secret_data)
                return parsed.get("api_key", "")
            except json.JSONDecodeError:
                # If not JSON, return as-is
                return secret_data
        elif isinstance(secret_data, dict):
            # If it's already a dict, extract api_key
            return secret_data.get("api_key", "")
        else:
            return str(secret_data) if secret_data else ""

def main():
    """Example usage of generic Akeyless integration."""
    # Configuration from environment variables
    akeyless_access_id = os.getenv("AKEYLESS_ACCESS_ID")
    akeyless_access_key = os.getenv("AKEYLESS_ACCESS_KEY")
    akeyless_url = os.getenv("AKEYLESS_URL", "https://your-akeyless-endpoint")
    
    if not akeyless_access_id or not akeyless_access_key:
        print("Error: AKEYLESS_ACCESS_ID and AKEYLESS_ACCESS_KEY must be set")
        return
    
    try:
        # Initialize and authenticate
        client = AkeylessClient(akeyless_access_id, akeyless_access_key, akeyless_url)
        client.authenticate()
        print("✅ Successfully authenticated with Akeyless")
        
        # Initialize application config
        app_config = ApplicationConfig(client)
        
        # Example: Get database configuration
        db_config = app_config.get_database_config("database-credentials")
        print(f"📊 Database config loaded: {list(db_config.keys())}")
        
        # Example: Get API key
        api_key = app_config.get_api_key("external-api-key")
        print(f"🔑 API key loaded: {api_key[:8]}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()'''
    
    result = {"basic_implementation": basic_impl}
    
    if include_error_handling:
        error_handling = '''
# Enhanced error handling and retry logic
import time
from requests.exceptions import RequestException

class AkeylessClient:
    def __init__(self, access_id: str, access_key: str, base_url: str, max_retries: int = 3):
        self.access_id = access_id
        self.access_key = access_key
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.max_retries = max_retries
    
    def authenticate(self) -> str:
        """Authenticate with Akeyless and get token with retry logic."""
        for attempt in range(self.max_retries):
            try:
                url = f"{self.base_url}/auth"
                data = {
                    "access-id": self.access_id,
                    "access-key": self.access_key
                }
                
                response = requests.post(url, json=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                self.token = result.get("token")
                
                if not self.token:
                    raise ValueError("No token received from authentication")
                
                return self.token
                
            except RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Authentication failed after {self.max_retries} attempts: {e}")
                print(f"Authentication attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                raise Exception(f"Authentication error: {e}")
    
    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve a secret using the authentication token with retry logic."""
        if not self.token:
            raise ValueError("Not authenticated. Call authenticate() first.")
        
        for attempt in range(self.max_retries):
            try:
                url = f"{self.base_url}/get-secret-value"
                data = {
                    "names": [secret_name],
                    "token": self.token,
                    "ignore-cache": "false",
                    "json": False
                }
                
                response = requests.post(url, json=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # Handle the actual API response format: {secret_name: value}
                if secret_name in result:
                    return result[secret_name]
                elif "value" in result:
                    # Fallback for other response formats
                    return result["value"]
                else:
                    raise ValueError(f"Unexpected response format: {result}")
                
            except RequestException as e:
                if attempt == self.max_retries - 1:
                    raise Exception(f"Secret retrieval failed after {self.max_retries} attempts: {e}")
                print(f"Secret retrieval attempt {attempt + 1} failed, retrying...")
                time.sleep(2 ** attempt)
            except Exception as e:
                raise Exception(f"Secret retrieval error: {e}")'''
        
        result["error_handling"] = error_handling
    
    return result 