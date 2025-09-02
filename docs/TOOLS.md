# Tools Reference

Available tools in the Thales CSM MCP Server.

## 🛠️ **Available Tools**

| Tool | Description | Main Actions |
|------|-------------|--------------|
| `manage_secrets` | Universal secret management (static, dynamic, rotated) | `create`, `get`, `update`, `delete`, `delete_items`, `list`, `smart_delete_directory` |
| `manage_dfc_keys` | Encryption key management (AES, RSA) | `create`, `update`, `delete`, `list`, `set_state`, `rotate` |
| `manage_auth_methods` | Authentication method management | `create_api_key`, `create_email`, `update`, `delete`, `delete_auth_methods`, `list`, `get` |
| `manage_rotation_settings` | Secret and key rotation management | `set_rotation`, `update_settings`, `list_rotation`, `get_rotation_status` |
| `manage_customer_fragments` | Customer fragment management | `export`, `download`, `list` |
| `security_guidelines` | Security best practices | `compliance` |
| `manage_roles` | Role management and access control | `list`, `get` |
| `manage_targets` | Target management and configuration | `list`, `get`, `create` |
| `manage_analytics` | Analytics and monitoring data | `get` |
| `manage_account` | Account settings and licensing | `get` |
| `get_api_reference` | API reference for native integrations | `get` |

## 🔐 **Secret Management**

### **Primary Tool: `manage_secrets`**
This is the **main tool** for all secret operations.

#### **Basic Operations**
```bash
# Create static secret
manage_secrets action=create_static_secret name=/my/secret value="password123" description="Database password"

# Create dynamic secret (use specific actions instead)
# manage_secrets action=create_dynamic_secret_mysql name=/my/dynamic_secret mysql_host=db.example.com mysql_port=3306 mysql_dbname=app_db mysql_username=admin mysql_password=adminpass password_length=16 user_ttl=1h

# Create rotated secret (not yet implemented - use create_static_secret for now)
# manage_secrets action=create_static_secret name=/my/rotated_secret secret_type=rotated auto_rotate=true rotation_interval=86400

# Get static secret value
manage_secrets action=get_static_secret_value name=/my/secret

# Get dynamic secret
manage_secrets action=get_dynamic_secret name=/my/dynamic_secret

# Get dynamic secret value with target
manage_secrets action=get_dynamic_secret_value name=/my/dynamic_secret

# List secrets in directory
manage_secrets action=list path=/my/secrets

# List only dynamic secrets within a specific directory
manage_secrets action=list path=/my/secrets secret_types=["dynamic-secret"]

# List only static and rotated secrets within a specific directory
manage_secrets action=list path=/my/secrets secret_types=["static-secret", "dynamic-secret"]

# List secrets with name filtering and type filtering within a directory
manage_secrets action=list path=/my/secrets filter_by="database*" secret_types=["dynamic-secret"]

# List ALL dynamic secrets globally (recursive search across entire vault)
manage_secrets action=list_dynamic_secrets

# Update secret
manage_secrets action=update name=/my/secret value="new_password" description="Updated password"

# Delete single secret
manage_secrets action=delete name=/my/secret

# Bulk delete items
manage_secrets action=delete_items items=["/secret1", "/secret2", "/secret3"]

# Smart directory deletion
manage_secrets action=delete_items path=/my/directory
```

#### **Secret Types**
- **Static**: Fixed value secrets (passwords, API keys)
- **Dynamic**: Just In Time (JIT) Secrets (database credentials, temporary tokens)
- **Rotated**: Automatically changing secrets with configurable intervals

#### **Advanced Features**
- **Delete Protection**: `delete_protection=true`
- **Tags**: `tags=["prod", "critical"]`
- **Format Support**: `text`, `json`, `key-value`
- **Customer Fragments**: `protection_key="fragment_id"`

## 🔑 **DFC Key Management**

### **Primary Tool: `manage_dfc_keys`**

#### **Key Operations**
```bash
# Create AES DFC key
manage_dfc_keys action=create name=/my/aes_key key_type=AES256GCM description="Database encryption key"

# Create RSA DFC key with sekf-signed certificate
manage_dfc_keys action=create name=/my/rsa_key key_type=RSA2048 generate_self_signed_certificate=true certificate_ttl=90

# Create key with auto-rotation
manage_dfc_keys action=create name=/my/rotating_key key_type=AES256GCM auto_rotate=true rotation_interval=30

# List DFC keys
manage_dfc_keys action=list path=/my/keys

# Enable/disable DFC key
manage_dfc_keys action=set_state name=/my/key desired_state=Disabled

# Delete a DFC key
manage_dfc_keys action=delete name=/my/key
```

#### **Supported Key Types**
- **AES**: AES128GCM, AES256GCM, AES128SIV, AES256SIV, AES128CBC, AES256CBC
- **RSA**: RSA1024, RSA2048, RSA3072, RSA4096
- **Auto-rotation**: Available for AES keys (7-365 day intervals)

## 🔒 **Authentication Management**

### **Primary Tool: `manage_auth_methods`**
Manage authentication methods for secure access.

#### **Authentication Operations**
```bash
# Create API key method
manage_auth_methods action=create_api_key name=/my/api_key

# List methods
manage_auth_methods action=list

# Delete method
manage_auth_methods action=delete name=/my/api_key
```

## 🔄 **Secret and Key Rotation**

### **Primary Tool: `manage_rotation_settings`**
Manage automatic rotation settings for secrets and DFC keys to maintain security compliance.

#### **Rotation Operations**
```bash
# Set rotation settings for a secret
manage_rotation action=set_rotation item_name=/my/secret auto_rotate=true rotation_interval=30

# Set rotation settings for an encryption key
manage_rotation action=set_rotation item_name=/my/encryption_key auto_rotate=true rotation_interval=90

# Update existing rotation settings
manage_rotation action=update_settings item_name=/my/secret rotation_interval=60

# List items with rotation settings
manage_rotation action=list_rotation path=/my/secrets

# Get rotation status for specific item
manage_rotation action=get_rotation_status item_name=/my/secret
```

#### **Rotation Features**
- **Auto-rotation**: Enable automatic secret/DFC key rotation
- **Configurable Intervals**: Set rotation frequency (7-365 days)
- **Event Notifications**: Configure rotation event alerts

## 🛡️ **Security Guidelines**

### **Primary Tool: `security_guidelines`**
Get security best practices and compliance information.

#### **Guideline Operations**
```bash
# Get SOC2 compliance guidelines
security_guidelines compliance=SOC2

# Get general security guidelines
security_guidelines compliance=general

# Get specific compliance guidelines
security_guidelines compliance=ISO27001
```

## 👥 **Role Management**

### **Primary Tool: `manage_roles`**
Manage roles and access control in the Thales CSM Akeyless Vault.

#### **Role Operations**
```bash
# List all roles
manage_roles action=list

# List roles with filter
manage_roles action=list filter="admin"

# List roles with JSON output
manage_roles action=list json=true

# Get specific role details
manage_roles action=get name="admin-role"

# Get role details with JSON output
manage_roles action=get name="admin-role" json=true
```

#### **Role Features**
- **Filtering**: Search roles by name pattern
- **Pagination**: Support for large role lists
- **JSON Output**: Structured data format for programmatic use
- **Universal Identity**: Support for universal identity authentication

## 🎯 **Target Management**

### **Primary Tool: `manage_targets`**
Manage targets and their configurations in the Thales CSM Akeyless Vault.

#### **Target Operations**
```bash
# List all targets
manage_targets action=list

# List targets with filter
manage_targets action=list filter="database"

# List targets by type
manage_targets action=list target_types=["mysql", "postgres"]

# List targets with JSON output
manage_targets action=list json=true

# Get specific target details
manage_targets action=get name="mysql-database"

# Get target details with versions
manage_targets action=get name="mysql-database" show_versions=true

# Get specific target version
manage_targets action=get name="mysql-database" target_version=2

# Get target details with JSON output
manage_targets action=get name="mysql-database" json=true

# Create new database target
manage_targets action=create target_type="database" name="/database/prod-mysql" db_type="mysql" host="db.example.com" db_name="production" user_name="app_user" pwd="secure_password" description="Production MySQL database"

# Create PostgreSQL target with SSL
manage_targets action=create target_type="database" name="/database/prod-postgres" db_type="postgres" host="postgres.example.com" port="5432" db_name="app_db" user_name="app_user" pwd="secure_password" ssl=true description="Production PostgreSQL with SSL"

# Create Snowflake target with key-based auth
manage_targets action=create target_type="database" name="/database/snowflake-analytics" db_type="snowflake" host="company.snowflakecomputing.com" db_name="ANALYTICS" user_name="data_user" pwd="temp_password" snowflake_account="company.us-east-1" snowflake_api_private_key="base64_encoded_key" description="Analytics Snowflake instance"
```

#### **Supported Target Types**
- **Databases**: `mysql`, `mssql`, `hanadb`, `postgres`, `mongodb`, `snowflake`, `oracle`, `cassandra`, `redshift`, `redis`
- **Cloud Platforms**: `aws`, `azure`, `gcp`, `gke`, `eks`, `k8s`
- **Services**: `ssh`, `rabbitmq`, `artifactory`, `dockerhub`, `github`, `chef`, `web`, `salesforce`
- **Security**: `venafi`, `ldap`

#### **Target Features**
- **Type Filtering**: Filter targets by specific types
- **Version Support**: Include all target versions in responses
- **Version Control**: Get specific target versions by version number
- **Pagination**: Support for large target lists
- **JSON Output**: Structured data format for programmatic use
- **Universal Identity**: Support for universal identity authentication

## 📊 **Analytics & Monitoring**

### **Primary Tool: `manage_analytics`**
Get comprehensive analytics and monitoring data with client-side filtering capabilities.

#### **Analytics Operations**
```bash
# Get all analytics data
manage_analytics action=get

# Get analytics with JSON output
manage_analytics action=get json=true

# Filter by item type
manage_analytics action=get filter_by_type="Targets"

# Filter by certificate risk
manage_analytics action=get filter_by_risk="Expired"

# Filter by product
manage_analytics action=get filter_by_product="sm"

# Combine filters
manage_analytics action=get filter_by_type="Static Secrets" filter_by_product="sm"
```

#### **Analytics Features**
- **Item Counts**: Comprehensive resource type statistics
- **Geographic Data**: Usage patterns by location
- **Request Metrics**: Volume and performance data
- **Certificate Health**: Expiry and risk assessment
- **Client Usage**: Authentication method analytics
- **Product Statistics**: SM, ADP, SRA usage reports
- **Client-Side Filtering**: Filter results without API calls

## ⚙️ **Account Administration**

### **Primary Tool: `manage_account`**
Get account settings, licensing information, and administrative configuration.

#### **Account Operations**
```bash
# Get account settings
manage_account action=get

# Get account settings with JSON output
manage_account action=get json=true
```

#### **Account Information**
- **Company Details**: Name, address, contact information
- **Licensing**: Tier levels and SLA information
- **Product Settings**: Configuration for SM, ADP, SRA
- **Version Control**: Object versioning policies and limits
- **System Access**: JWT TTL and authentication settings
- **Security Policies**: Sharing and data protection configuration

#### **Administrative Features**
- **License Verification**: Check current tier and SLA levels
- **Capacity Planning**: Review version limits and policies
- **Compliance**: Verify security and sharing policies
- **System Configuration**: Monitor account settings and limits

## ⚠️ **Important Notes**

- **Full Paths**: Use absolute paths starting with `/` for all resources
- **Action Required**: Every operation requires an `action` parameter
- **Error Handling**: All tools return structured responses with success/error indicators
- **Enterprise Security**: Built on Thales CipherTrust CSM with Akeyless Vault technology

## 🔗 **API Reference & Native Integrations**

### **Primary Tool: `get_api_reference`**
Get complete API reference information to build applications that directly integrate with Thales CipherTrust/Akeyless APIs.

#### **API Reference Operations**
```bash
# Get S3 workflow reference
get_api_reference api_endpoint=workflow language=python include_error_handling=true

# Get authentication API reference
get_api_reference api_endpoint=auth language=python

# Get secret retrieval API reference
get_api_reference api_endpoint=retrieve-secret language=python

# Get general API reference
get_api_reference language=python
```

#### **Supported Endpoints**
- **`workflow`** or **`generic_workflow`** - Core Akeyless integration patterns
- **`s3_workflow`** - Complete S3 integration workflow
- **`auth`** - Authentication endpoint reference
- **`retrieve-secret`** - Secret retrieval endpoint reference
- **`list-secrets`** - List secrets endpoint reference
- **`list-roles`** - List roles endpoint reference
- **`list-targets`** - List targets endpoint reference

#### **API Reference Features**
- **Complete Workflows**: Full implementation examples for common use cases
- **Multiple Languages**: Code examples in Python (more languages planned)
- **Error Handling**: Comprehensive error handling and retry logic examples
- **Best Practices**: Security and production deployment guidance
- **Native Integration**: Build apps that directly call Akeyless APIs

#### **Use Cases**
- **AI Assistant Development**: Enable AI assistants to build native Akeyless integrations
- **Application Development**: Get working code examples for production applications
- **Learning & Training**: Understand Akeyless APIs without external documentation
- **Workflow Implementation**: Implement complete patterns like S3 + secret management

#### **Example Workflows**

**Core Akeyless Integration Workflow:**
The tool provides a **generic workflow** that demonstrates the fundamental patterns:
1. **Authentication** with Akeyless to get access token
2. **Secret Management** - Create and retrieve secrets
3. **Application Configuration** - Use secrets for runtime configuration
4. **Error Handling** - Proper exception management and retry logic
5. **Best Practices** - Security and production deployment guidance

**S3 Bucket Listing with Akeyless Integration:**
The tool provides a complete workflow demonstrating:
1. **Authentication** with Akeyless to get access token
2. **Secret Retrieval** using the token to fetch AWS credentials
3. **AWS SDK Integration** using retrieved credentials to list S3 objects
4. **Error Handling** with retry logic and proper exception management
5. **Best Practices** for production deployments

#### **Benefits**
- **For Development Teams**: Faster development, reduced errors, security best practices
- **For AI Assistants**: Complete context, code generation, workflow understanding
- **For Production**: Native integrations that don't depend on MCP servers