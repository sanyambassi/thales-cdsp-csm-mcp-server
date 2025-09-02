# MCP Server Configuration

This directory contains configuration files for the Thales CDSP CSM MCP Server.

## Configuration Files

- `mcp-config.json` - Standard Python configuration
- `mcp-config-uv.json` - UV package manager configuration

## Transport Types

### STDIO Transport
For STDIO transport, the MCP client will start the server process directly using the `command` and `args` specified in the config.

### HTTP Transport
For HTTP transport, you need to:

1. **Start the server manually first:**
   ```bash
   # Using standard Python
   python main.py --transport streamable-http --host 0.0.0.0 --port 8000
   
   # Using UV
   uv run python main.py --transport streamable-http --host 0.0.0.0 --port 8000
   ```

2. **Configure environment variables:**
   ```bash
   export AKEYLESS_API_URL="https://api.akeyless.io"  # or your on-prem URL
   export AKEYLESS_ACCESS_ID="your_access_id_here"
   export AKEYLESS_ACCESS_KEY="your_access_key_here"
   export AKEYLESS_VERIFY_SSL="true"  # or "false" for self-signed certificates
   export LOG_LEVEL="INFO"
   ```

3. **Use the HTTP configuration:**
   The config file will contain only the URL to connect to the running server:
   ```json
   "thales-cdsp-csm-http-cloud": {
     "url": "http://localhost:8000/mcp"
   }
   ```

## Environment Variables

Set these environment variables before starting the server:

- `AKEYLESS_API_URL` - Akeyless API endpoint (cloud or on-prem)
- `AKEYLESS_ACCESS_ID` - Your Akeyless access ID
- `AKEYLESS_ACCESS_KEY` - Your Akeyless access key
- `AKEYLESS_VERIFY_SSL` - SSL certificate verification (true/false)
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## Usage Examples

### Cloud Configuration
```bash
export AKEYLESS_API_URL="https://api.akeyless.io"
export AKEYLESS_ACCESS_ID="your_cloud_access_id"
export AKEYLESS_ACCESS_KEY="your_cloud_access_key"
export AKEYLESS_VERIFY_SSL="true"
python main.py --transport streamable-http --port 8000
```

### On-Premises Configuration
```bash
export AKEYLESS_API_URL="https://your-cm-hostname/akeyless-api/v2"
export AKEYLESS_ACCESS_ID="your_onprem_access_id"
export AKEYLESS_ACCESS_KEY="your_onprem_access_key"
export AKEYLESS_VERIFY_SSL="false"  # Often needed for self-signed certificates
python main.py --transport streamable-http --port 8000
```