# Tools Reference

Available tools in the Thales CSM MCP Server.

## 🛠️ **Available Tools**

| Tool | Description | Main Actions |
|------|-------------|--------------|
| `manage_secrets` | Universal secret management (static, dynamic, rotated) | `create`, `get`, `update`, `delete`, `delete_items`, `list`, `smart_delete_directory` |
| `manage_dfc_keys` | Encryption key management (AES, RSA) | `create`, `update`, `delete`, `list`, `set_state` |
| `manage_auth` | Authentication method management | `create`, `update`, `delete`, `list`, `get` |
| `manage_rotation` | Secret and key rotation management | `set_rotation`, `update_settings`, `list_rotation`, `get_rotation_status` |
| `manage_customer_fragments` | Customer fragment management | `create`, `delete`, `list` |
| `security_guidelines` | Security best practices | `compliance` |

## 🔐 **Secret Management**

### **Primary Tool: `manage_secrets`**
This is the **main tool** for all secret operations.

#### **Basic Operations**
```bash
# Create static secret
manage_secrets action=create name=/my/secret value="password123" description="Database password"

# Create dynamic secret
manage_secrets action=create name=/my/dynamic_secret secret_type=dynamic dynamic_type=mysql ttl=3600

# Create rotated secret
manage_secrets action=create name=/my/rotated_secret secret_type=rotated auto_rotate=true rotation_interval=86400

# Get secret value
manage_secrets action=get name=/my/secret

# List secrets in directory
manage_secrets action=list path=/my/secrets

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

### **Primary Tool: `manage_auth`**
Manage authentication methods for secure access.

#### **Authentication Operations**
```bash
# Create API key method
manage_auth action=create name=/my/api_key method_type=api_key access_id="your_id" access_key="your_key"

# Create AWS IAM method
manage_auth action=create name=/my/aws_auth method_type=aws_iam aws_access_key_id="AKIA..." aws_secret_access_key="..." aws_region="us-east-1"

# Create Azure AD method
manage_auth action=create name=/my/azure_auth method_type=azure_ad tenant_id="..." client_id="..." client_secret="..."

# List methods
manage_auth action=list

# Update method
manage_auth action=update name=/my/api_key method_type=api_key access_key="new_key"

# Delete method
manage_auth action=delete name=/my/api_key
```

#### **Supported Methods**
- **API Key**: Standard API key authentication
- **AWS IAM**: AWS Identity and Access Management
- **Azure AD**: Azure Active Directory

## 🔄 **Secret and Key Rotation**

### **Primary Tool: `manage_rotation`**
Manage automatic rotation settings for secrets and encryption keys to maintain security compliance.

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

## ⚠️ **Important Notes**

- **Full Paths**: Use absolute paths starting with `/` for all resources
- **Action Required**: Every operation requires an `action` parameter
- **Error Handling**: All tools return structured responses with success/error indicators
- **Enterprise Security**: Built on Thales CipherTrust CSM with Akeyless Vault technology