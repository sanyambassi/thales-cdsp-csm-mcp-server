"""
Best Practices Data

Contains critical best practices and AI assistant guidance.
"""

def get_best_practices():
    """Get best practices data for API integration."""
    
    return {
        "ai_assistant_guidance": [
            "🔐 Use MCP tool 'manage_secrets' for secret creation during development",
            "📱 User applications should ONLY retrieve secrets at runtime",
            "🚫 Never bake secret creation into production applications",
            "✅ Separate development-time operations from runtime operations",
            "⚠️ IMPORTANT: get-secret-value API returns {secret_name: value} format, not {value: ...}",
            "🔍 Always check actual API response format and handle both possible formats"
        ],
        "critical_best_practices": {
            "get_secret_value_endpoint": [
                "NEVER check for 'success' field - it doesn't exist in the actual response",
                "ALWAYS use your secret name as the key: result[secret_name]",
                "The response format is: {secret_name: 'json_string'}",
                "Parse the JSON string value to get your actual secret data"
            ],
            "code_pattern": {
                "correct": "secret_value = result[secret_name]",
                "incorrect": "secret_value = result.get('value')  # This will fail!",
                "robust": "if secret_name in result: secret_value = result[secret_name]"
            }
        },
        "troubleshooting": {
            "common_issues": [
                {
                    "issue": "Secret retrieval returns unexpected format",
                    "symptoms": "Code expects result['value'] but gets result['/secret/name']",
                    "cause": "API returns {secret_name: value} format, not {value: ...}",
                    "solution": "Use the robust response handler or check for secret name as key"
                },
                {
                    "issue": "JSON parsing fails",
                    "symptoms": "json.loads() throws error on secret value",
                    "cause": "Secret value might be pre-parsed or in unexpected format",
                    "solution": "Check if value is already a dict or needs parsing"
                },
                {
                    "issue": "Secret not found in response",
                    "symptoms": "KeyError when accessing secret data",
                    "cause": "Response structure varies by API version/options",
                    "solution": "Use robust handler that checks multiple formats"
                }
            ],
            "debugging_tips": [
                "Always print the raw API response first: print(f'Raw response: {result}')",
                "Check response keys: print(f'Response keys: {list(result.keys())}')",
                "Verify secret name exists: print(f'Secret name in response: {secret_name in result}')",
                "Use the robust response handler for production code"
            ]
        }
    } 