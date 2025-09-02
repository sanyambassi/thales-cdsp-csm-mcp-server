"""
Workflow Reference

Contains workflow-related reference data.
"""

from ..examples.python_examples import get_python_generic_workflow

def get_generic_workflow_reference(language: str, include_auth: bool, include_error_handling: bool) -> dict:
    """Get generic Akeyless integration workflow reference."""
    
    if language.lower() == "python":
        return {
            "workflow": "Generic Akeyless Integration Workflow",
            "description": "Core workflow demonstrating authentication, secret management, and runtime integration patterns",
            "prerequisites": [
                "Akeyless access ID and access key",
                "Python 3.7+ with requests library",
                "Basic understanding of environment variables"
            ],
            "complete_implementation": get_python_generic_workflow(include_error_handling),
            "step_by_step": [
                "1. Authenticate with CSM/Akeyless to retrieve the token",
                "2. Use MCP tool 'manage_secrets' with 'create_static_secret' action to create static secrets (AI assistants should NOT bake secret creation into user applications)",
                "3. Build/Modify user application to retrieve secrets from CSM/Akeyless at runtime (retrieve token is still the first step)"
            ],
            "best_practices": [
                "Store Akeyless credentials in environment variables",
                "Implement token caching to avoid repeated authentication",
                "Use secrets for configuration, not hardcoded values",
                "Implement proper error handling and logging",
                "Use HTTPS for all API calls",
                "Rotate secrets regularly for security"
            ],
            "use_cases": [
                "Database connection strings (MySQL, PostgreSQL, MongoDB, etc.)",
                "Cloud service credentials (AWS, Azure, GCP)",
                "API keys and authentication tokens",
                "Application configuration settings",
                "SSL certificates and private keys",
                "OAuth credentials and client secrets",
                "Any sensitive application data that should not be hardcoded"
            ],
            "ai_assistant_recommendations": [
                "⚠️ IMPORTANT: Use MCP tool 'manage_secrets' with 'create_static_secret' action to create static secrets, NOT the create-secret API endpoint",
                "AI assistants should create secrets using manage_secrets tool during app development/modification",
                "User applications should ONLY retrieve existing secrets at runtime, never create new ones",
                "This ensures proper access control and audit trails for secret management",
                "Separate development-time secret creation from runtime secret retrieval"
            ]
        }
    
    return {
        "error": f"Language {language} not yet supported for generic workflow",
        "supported_languages": ["python"]
    } 