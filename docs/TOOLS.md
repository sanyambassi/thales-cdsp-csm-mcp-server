# Tools Reference

This document provides comprehensive documentation of all available tools in the **Thales CipherTrust Secrets Management MCP Server, powered by Akeyless**.

## 🔐 Secret Management Tools

### `manage_secrets`

The universal tool for managing all types of secrets in CipherTrust CSM. This tool handles static, dynamic, and rotated secrets with intelligent operations.

#### **Actions**

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `create` | Create new secrets | `name`, `value` |
| `get` | Retrieve secret values | `name` |
| `update` | Update secret properties and values | `name` |
| `delete` | Smart deletion (auto-detects individual vs directory) | `name` |
| `delete_items` | Bulk deletion | `name` or `items` |
| `list` | List secrets in a directory | `path` (optional) |

#### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | ✅ | Action to perform |
| `name` | string | ✅ | Secret name/path |
| `value` | string | ⚠️ | Secret value (required for create, optional for update) |
| `format` | string | ❌ | Secret format: `text`, `json`, `key-value` |
| `secret_type` | string | ❌ | Type: `static`, `dynamic`, `rotated` |
| `delete_protection` | boolean | ❌ | Enable/disable deletion protection |
| `tags` | List[string] | ❌ | List of tags for organization |
| `description` | string | ❌ | Human-readable description |
| `accessibility` | string | ❌ | Access level (default: "regular") |
| `protection_key` | string | ❌ | Customer fragment ID for encryption |
| `max_versions` | integer | ❌ | Maximum number of versions to keep |
| `metadata` | string | ❌ | Additional metadata in JSON format |
| `new_name` | string | ❌ | New name for the secret (update only) |

#### **Examples**

```bash
# Create a text secret
manage_secrets action=create name=/my/secret value="my_secret_value"

# Create a JSON secret
manage_secrets action=create name=/my/config format=json value='{"key": "value"}'

# Create a key-value secret (auto-converts to JSON)
manage_secrets action=create name=/my/creds format=key-value value="username=admin;password=123"

# Create with delete protection and tags
manage_secrets action=create name=/my/secure-secret value="sensitive_data" delete_protection=true tags=["prod","critical"]

# Update delete protection
manage_secrets action=update name=/my/secret delete_protection=true

# Update secret value only
manage_secrets action=update name=/my/secret value="new_value"

# Update properties only
manage_secrets action=update name=/my/secret description="Updated description" tags=["updated","tag"]

# Smart delete (auto-detects if directory or individual item)
manage_secrets action=delete name=/my/directory

# Bulk delete specific items
manage_secrets action=delete_items items=["/secret1","/secret2","/secret3"]

# List secrets in a directory
manage_secrets action=list path=/my/secrets
```

#### **Smart Features**

- **Auto-Format Detection**: Automatically detects and converts key-value format to JSON
- **Smart Deletion**: Intelligently determines if you're deleting a single item or directory
- **Bulk Operations**: Efficient bulk deletion and management
- **Path Normalization**: Automatic `/` prefix handling and path validation

---

## 🔑 DFC Key Management Tools

### `manage_dfc_keys`

Comprehensive tool for managing Data Fragmentation Keys in CipherTrust CSM. Supports both AES and RSA encryption keys with enterprise-grade features.

#### **Actions**

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `create` | Create new DFC keys | `name`, `key_type` |
| `update` | Update key properties | `name` |
| `delete` | Delete DFC keys | `name` |
| `list` | List keys in a directory | `path` (optional) |
| `set_state` | Enable/disable keys | `name`, `desired_state` |

#### **Key Types**

| Category | Supported Types | Auto-Rotation | Certificate Support |
|----------|----------------|---------------|-------------------|
| **AES Keys** | AES128GCM, AES256GCM, AES128SIV, AES256SIV, AES128CBC, AES256CBC | ✅ Yes | ✅ Yes |
| **RSA Keys** | RSA1024, RSA2048, RSA3072, RSA4096 | ❌ No | ✅ Yes (SHA-256 only) |

#### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | ✅ | Action to perform |
| `name` | string | ✅ | DFC key name/path |
| `key_type` | string | ⚠️ | Encryption algorithm (default: AES256GCM) |
| `protection_key` | string | ❌ | Customer fragment ID |
| `description` | string | ❌ | Human-readable description |
| `accessibility` | string | ❌ | Access level (default: "regular") |
| `delete_protection` | boolean | ❌ | Enable deletion protection |
| `tags` | List[string] | ❌ | List of tags |
| `auto_rotate` | string | ❌ | Enable auto-rotation ("true"/"false") |
| `rotation_interval` | string | ❌ | Days between rotations (7-365) |
| `split_level` | integer | ❌ | Number of fragments (3 or 4, default: 3) |
| `generate_self_signed_certificate` | boolean | ❌ | Generate X.509 certificate |
| `certificate_ttl` | integer | ❌ | Certificate TTL in days (1-365) |
| `certificate_common_name` | string | ❌ | Certificate common name |
| `certificate_organization` | string | ❌ | Certificate organization |
| `certificate_country` | string | ❌ | Certificate country code |
| `certificate_province` | string | ❌ | Certificate province/state |
| `certificate_locality` | string | ❌ | Certificate locality/city |
| `certificate_digest_algo` | string | ❌ | Certificate digest algorithm |
| `certificate_format` | string | ❌ | Certificate format (PEM, DER, etc.) |
| `conf_file_data` | string | ❌ | Configuration file data |
| `expiration_event_in` | List[string] | ❌ | Days before expiration to notify |
| `rotation_event_in` | List[string] | ❌ | Days before rotation to notify |
| `metadata` | string | ❌ | Additional metadata in JSON format |
| `new_name` | string | ❌ | New name for the key (update only) |
| `add_tags` | List[string] | ❌ | Tags to add (update only) |
| `rm_tags` | List[string] | ❌ | Tags to remove (update only) |
| `max_versions` | string | ❌ | Maximum number of versions (update only) |
| `desired_state` | string | ❌ | Desired state: "Enabled" or "Disabled" |
| `delete_immediately` | boolean | ❌ | Delete immediately (bypass soft delete) |
| `delete_in_days` | integer | ❌ | Soft delete retention period in days |
| `version` | integer | ❌ | Version to delete (-1 for all versions) |

#### **Examples**

```bash
# Create AES key with auto-rotation
manage_dfc_keys action=create name=/my/aes-key key_type=AES256GCM auto_rotate=true rotation_interval=30

# Create RSA key (no auto-rotation)
manage_dfc_keys action=create name=/my/rsa-key key_type=RSA2048 auto_rotate=false

# Create RSA key with certificate
manage_dfc_keys action=create name=/my/rsa-cert key_type=RSA2048 generate_self_signed_certificate=true certificate_ttl=90

# Create with delete protection and tags
manage_dfc_keys action=create name=/my/secure-key key_type=AES256GCM delete_protection=true tags=["prod","encryption"]

# Update key properties
manage_dfc_keys action=update name=/my/key description="Updated description" add_tags=["updated"]

# Enable/disable key
manage_dfc_keys action=set_state name=/my/key desired_state=Disabled

# List keys in a directory
manage_dfc_keys action=list path=/my/keys

# Delete key immediately
manage_dfc_keys action=delete name=/my/key delete_immediately=true
```

#### **Validation & Error Handling**

- **RSA Auto-Rotation**: Clear error when attempting to enable auto-rotation for RSA keys
- **Split Level**: Must be 3 or 4 for proper key fragmentation
- **Rotation Interval**: Must be 7-365 days when auto-rotation is enabled
- **Certificate TTL**: Must be 1-365 days when generating certificates
- **RSA Digest Algorithm**: Only SHA-256 is supported for RSA keys

---

## 🔐 Authentication Management Tools

### `manage_auth`

Manage authentication methods and API keys in CipherTrust CSM.

#### **Actions**

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `create` | Create new authentication methods | `name` |
| `list` | List available authentication methods | None |
| `delete` | Remove authentication methods | `name` |

#### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | ✅ | Action to perform |
| `name` | string | ⚠️ | Authentication method name (required for create/delete) |
| `auth_type` | string | ❌ | Type of authentication method |
| `description` | string | ❌ | Human-readable description |

#### **Examples**

```bash
# List all authentication methods
manage_auth action=list

# Create new authentication method
manage_auth action=create name=/my/auth-method auth_type=api_key description="API key for automation"

# Delete authentication method
manage_auth action=delete name=/my/auth-method
```

---

## 🔄 Rotation Management Tools

### `manage_rotation`

Configure secret and key rotation settings in CipherTrust CSM.

#### **Actions**

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `set_rotation` | Configure rotation settings | `name` |
| `update_settings` | Update existing rotation configuration | `name` |
| `list_rotation` | List rotation settings | `path` (optional) |
| `get_rotation_status` | Check rotation status | `name` |

#### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | ✅ | Action to perform |
| `name` | string | ✅ | Secret/key name |
| `auto_rotate` | string | ❌ | Enable auto-rotation ("true"/"false") |
| `rotation_interval` | string | ❌ | Days between rotations (7-365) |
| `rotation_type` | string | ❌ | Type of rotation |
| `description` | string | ❌ | Human-readable description |

#### **Examples**

```bash
# Set rotation settings
manage_rotation action=set_rotation name=/my/secret auto_rotate=true rotation_interval=30

# Update rotation settings
manage_rotation action=update_settings name=/my/secret rotation_interval=60

# List rotation settings
manage_rotation action=list_rotation path=/my/secrets

# Check rotation status
manage_rotation action=get_rotation_status name=/my/secret
```

---

## 📁 Customer Fragment Management Tools

### `manage_customer_fragments`

Manage customer fragment access and configuration in CipherTrust CSM.

#### **Actions**

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `list` | List available customer fragments | None |
| `get` | Get specific fragment details | `name` |
| `create` | Create new fragments | `name` |
| `update` | Update fragment properties | `name` |
| `delete` | Remove fragments | `name` |

#### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | ✅ | Action to perform |
| `name` | string | ⚠️ | Fragment name (required for get/create/update/delete) |
| `description` | string | ❌ | Human-readable description |
| `fragment_type` | string | ❌ | Type of customer fragment |

#### **Examples**

```bash
# List all customer fragments
manage_customer_fragments action=list

# Get specific fragment details
manage_customer_fragments action=get name=/my/fragment

# Create new fragment
manage_customer_fragments action=create name=/my/fragment description="New customer fragment"

# Update fragment properties
manage_customer_fragments action=update name=/my/fragment description="Updated description"

# Delete fragment
manage_customer_fragments action=delete name=/my/fragment
```

---

## 🛡️ Security Guidelines Tools

### `security_guidelines`

Get security guidelines and best practices for different secret types and DFC protection.

#### **Actions**

| Action | Description | Required Parameters |
|--------|-------------|-------------------|
| `get_guidelines` | Get security guidelines | `secret_type` (optional) |
| `get_best_practices` | Get best practices | `operation_type` (optional) |

#### **Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | ✅ | Action to perform |
| `secret_type` | string | ❌ | Type of secret (static, dynamic, rotated) |
| `operation_type` | string | ❌ | Type of operation (create, update, delete, rotate) |

#### **Examples**

```bash
# Get general security guidelines
security_guidelines action=get_guidelines

# Get guidelines for specific secret type
security_guidelines action=get_guidelines secret_type=static

# Get best practices for operations
security_guidelines action=get_best_practices operation_type=create
```

---

## 🔧 Tool Integration Features

### **Common Parameters Across Tools**

All tools support these common parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `json` | boolean | Set output format to JSON |
| `filter_by` | string | Filter results by pattern |
| `path` | string | Path for list operations |

### **Error Handling**

All tools provide:
- **Clear Error Messages**: User-friendly error descriptions
- **Actionable Solutions**: Specific guidance on how to fix issues
- **Validation Feedback**: Immediate feedback on parameter issues
- **Context-Aware Help**: Relevant information based on the operation

### **Response Format**

All tools return consistent response format:

```json
{
  "success": true/false,
  "message": "Human-readable message",
  "data": "Tool-specific data or error details",
  "error": "Error message (if success is false)"
}
```

### **Path Handling**

- **Automatic Normalization**: All paths are automatically prefixed with `/`
- **Trailing Slash Handling**: Consistent path formatting
- **Directory Detection**: Smart detection of directories vs individual items

---

## 🚀 Getting Started with Tools

### **1. Start the MCP Server**
```bash
python main.py
```

### **2. Basic Secret Operations**
```bash
# Create your first secret
manage_secrets action=create name=/my/first-secret value="Hello CipherTrust!"

# List secrets
manage_secrets action=list

# Get secret value
manage_secrets action=get name=/my/first-secret
```

### **3. Advanced Operations**
```bash
# Create DFC key
manage_dfc_keys action=create name=/my/encryption-key key_type=AES256GCM

# Set up rotation
manage_rotation action=set_rotation name=/my/secret auto_rotate=true rotation_interval=30
```

### **4. Security Best Practices**
```bash
# Enable delete protection
manage_secrets action=update name=/my/secret delete_protection=true

# Get security guidelines
security_guidelines action=get_guidelines secret_type=static
```

---

## 📚 Additional Resources

- **Main Documentation**: [README.md](README.md)
- **API Reference**: [docs/README.md](docs/README.md)
- **Transport Modes**: [docs/TRANSPORT_MODES.md](docs/TRANSPORT_MODES.md)
- **Configuration**: [env.example](env.example)

## 🆘 Need Help?

- Check the error messages for specific guidance
- Review the examples above for common use cases
- Ensure your CipherTrust Manager is properly configured
- Verify your Akeyless credentials are correct 