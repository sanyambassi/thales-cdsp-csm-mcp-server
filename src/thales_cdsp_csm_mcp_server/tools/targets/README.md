# Targets Management Tools

This module provides tools for managing targets in the Thales CSM Akeyless Vault.

## Available Operations

### List Targets
- **Action**: `list`
- **Description**: List all targets with optional filtering by type
- **Parameters**:
  - `filter`: Filter by target name or part of it
  - `json`: Set output format to JSON (default: false)
  - `pagination_token`: Next page reference for pagination
  - `target_types`: List of target types to filter by
  - `uid_token`: Universal identity token (for universal_identity authentication)

### Get Target
- **Action**: `get`
- **Description**: Get detailed information about a specific target (includes version support)
- **Parameters**:
  - `name`: Target name (required)
  - `json`: Set output format to JSON (default: false)
  - `show_versions`: Include all target versions in reply (default: false)
  - `target_version`: Specific target version to retrieve (0 for latest, optional)
  - `uid_token`: Universal identity token (for universal_identity authentication)

### Create Target
- **Action**: `create`
- **Description**: Create new targets with comprehensive configuration options for multiple target types
- **Required Parameters**:
  - `name`: Target name (required)
  - `target_type`: Type of target to create (required) - Examples: 'database', 'ldap', 'aws', 'azure', 'gcp'

#### **Database Targets**
- **Required Parameters**:
  - `db_type`: Database type - Supported values: 'mysql', 'mssql', 'hanadb', 'postgres', 'mongodb', 'snowflake', 'oracle', 'cassandra', 'redshift', 'redis'
  - `host`: Database host address
  - `db_name`: Database name
  - `user_name`: Database username
  - `pwd`: Database password
- **Optional Parameters**:
  - `port`: Database port number
  - `connection_type`: Connection type - Options: 'credentials', 'cloud-identity', 'wallet', 'parent-target'
  - `ssl`: Enable SSL connection (default: false)
  - `ssl_certificate`: SSL certificate data
  - `cluster_mode`: Enable cluster mode for high availability
  - `cloud_service_provider`: Cloud service provider (Azure support)
  - `azure_client_id`, `azure_client_secret`, `azure_tenant_id`: Azure authentication
  - `mongodb_atlas`: MongoDB Atlas specific configuration
  - `oracle_service_name`: Oracle database service name
  - `snowflake_account`: Snowflake account identifier
  - `parent_target_name`: Parent target for inheritance

#### **LDAP Targets**
- **Required Parameters**:
  - `ldap_url`: LDAP Server URL
  - `bind_dn`: Bind DN
  - `bind_dn_password`: Bind DN Password
- **Optional Parameters**:
  - `server_type`: LDAP server type - Options: 'OpenLDAP', 'ActiveDirectory' (default: 'OpenLDAP')
  - `ldap_ca_cert`: CA Certificate File Content
  - `token_expiration`: Token expiration

#### **Common Parameters (All Target Types)**
- `description`: Target description
- `protection_key`: Protection key for encryption
- `max_versions`: Maximum number of versions to keep

## Supported Target Types

The following target types are supported for filtering:
- **Databases**: `mysql`, `mssql`, `hanadb`, `postgres`, `mongodb`, `snowflake`, `oracle`, `cassandra`, `redshift`, `redis`
- **Cloud Platforms**: `aws`, `azure`, `gcp`, `gke`, `eks`, `k8s`
- **Services**: `ssh`, `rabbitmq`, `artifactory`, `dockerhub`, `github`, `chef`, `web`, `salesforce`
- **Security**: `venafi`, `ldap`

## Usage Examples

### List all targets
```python
# List all targets
await manage_targets(action="list")

# List targets with filter
await manage_targets(action="list", filter="database")

# List targets by type
await manage_targets(action="list", target_types=["mysql", "postgres"])

# List targets with JSON output
await manage_targets(action="list", json=True)
```

### Get specific target
```python
# Get target details
await manage_targets(action="get", name="mysql-database")

# Get target details with versions
await manage_targets(action="get", name="mysql-database", show_versions=True)

# Get specific target version
await manage_targets(action="get", name="mysql-database", target_version=2)

# Get target details with JSON output
await manage_targets(action="get", name="mysql-database", json=True)
```

### Create new targets
```python
# Create MySQL target
await manage_targets(
    action="create",
    target_type="database",
    name="/database/prod-mysql",
    db_type="mysql",
    host="db.example.com",
    db_name="production",
    user_name="app_user",
    pwd="secure_password",
    description="Production MySQL database"
)

# Create PostgreSQL target with SSL
await manage_targets(
    action="create",
    target_type="database",
    name="/database/prod-postgres",
    db_type="postgres",
    host="postgres.example.com",
    port="5432",
    db_name="app_db",
    user_name="app_user",
    pwd="secure_password",
    ssl=True,
    description="Production PostgreSQL with SSL"
)

# Create Snowflake target with key-based auth
await manage_targets(
    action="create",
    target_type="database",
    name="/database/snowflake-analytics",
    db_type="snowflake",
    host="company.snowflakecomputing.com",
    db_name="ANALYTICS",
    user_name="data_user",
    pwd="temp_password",
    snowflake_account="company.us-east-1",
    snowflake_api_private_key="base64_encoded_key",
    description="Analytics Snowflake instance"
)

# Create LDAP target for Active Directory
await manage_targets(
    action="create",
    target_type="ldap",
    name="/ldap/ad-corp",
    ldap_url="ldaps://ad.example.com:636",
    bind_dn="CN=ServiceAccount,OU=ServiceAccounts,DC=example,DC=com",
    bind_dn_password="secure_password",
    server_type="ActiveDirectory",
    description="Corporate Active Directory"
)

# Create OpenLDAP target with CA certificate
await manage_targets(
    action="create",
    target_type="ldap",
    name="/ldap/openldap-dev",
    ldap_url="ldap://ldap.example.com:389",
    bind_dn="cn=admin,dc=example,dc=com",
    bind_dn_password="admin_password",
    server_type="OpenLDAP",
    ldap_ca_cert="-----BEGIN CERTIFICATE-----...",
    description="Development OpenLDAP server"
)
```