# Tools Reference

Available tools in the Thales CSM MCP Server.

## 🛠️ **Available Tools**

| Tool | Description | Main Actions |
|------|-------------|--------------|
| `manage_secrets` | Create, read, update, delete secrets | `create`, `get`, `update`, `delete`, `list` |
| `manage_dfc_keys` | Manage encryption keys | `create`, `delete`, `list` |
| `manage_auth` | Authentication and access control | `create`, `update`, `delete`, `list` |
| `manage_rotation` | Secret rotation policies | `create`, `update`, `delete`, `list` |
| `manage_customer_fragments` | Enhanced security features | `create`, `delete`, `list` |
| `security_guidelines` | Security best practices | `compliance` |

## 🔐 **Secret Management**

### **Basic Operations**
```bash
# Create secret
manage_secrets action=create name=/my/secret value="password123"

# Get secret
manage_secrets action=get name=/my/secret

# List secrets
manage_secrets action=list path=/

# Delete secret
manage_secrets action=delete name=/my/secret
```

### **Secret Types**
- **Static**: Fixed value secrets
- **Dynamic**: Auto-generated secrets
- **Rotated**: Rotating secrets

## 🔑 **Key Management**

### **DFC Keys**
```bash
# Create encryption key
manage_dfc_keys action=create name=/my/key key_type=AES256GCM

# List keys
manage_dfc_keys action=list

# Delete key
manage_dfc_keys action=delete name=/my/key
```

### **Key Types**
- **AES**: Symmetric encryption
- **RSA**: Asymmetric encryption
- **Custom**: User-defined types

## 🔒 **Authentication**

### **Access Control**
```bash
# List auth policies
manage_auth action=list

# Create policy
manage_auth action=create name=/policy/readonly permissions=["read"]

# Update policy
manage_auth action=update name=/policy/readonly permissions=["read","write"]
```

## 🔄 **Secret Rotation**

### **Rotation Policies**
```bash
# Create rotation policy
manage_rotation action=create name=/policy/daily schedule="daily"

# List policies
manage_rotation action=list

# Update policy
manage_rotation action=update name=/policy/daily schedule="weekly"
```

## 🛡️ **Security Guidelines**

### **Compliance**
```bash
# Get security guidelines
security_guidelines compliance=SOC2

# Get general guidelines
security_guidelines compliance=general
```

## 📋 **Common Parameters**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `action` | ✅ | Operation to perform |
| `name` | ✅ | Resource name/path |
| `value` | ⚠️ | Secret value (for create/update) |
| `path` | ❌ | Directory path (for list) |
| `description` | ❌ | Human-readable description |

## 🎯 **Quick Examples**

```bash
# Create a database password
manage_secrets action=create name=/db/password value="db123" description="Database password"

# List all secrets in /app folder
manage_secrets action=list path=/app

# Create encryption key for backups
manage_dfc_keys action=create name=/backup/key key_type=AES256GCM description="Backup encryption key"

# Get SOC2 compliance guidelines
security_guidelines compliance=SOC2
```