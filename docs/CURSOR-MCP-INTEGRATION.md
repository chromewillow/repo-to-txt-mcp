# Integrating repo-to-txt-mcp with Cursor

This document explains how to integrate the repo-to-txt-mcp server with Cursor's MCP functionality.

## Option 1: Direct URL Integration

If you're running the Python server directly, you can add it to Cursor's MCP configuration:

1. Start the Python server:
   ```bash
   python server.py
   ```

2. Add the following to your `~/.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "repo-to-txt-mcp": {
         "url": "http://localhost:8000"
       },
       // ... other servers
     }
   }
   ```

3. Restart Cursor or refresh the MCP servers in settings.

## Option 2: Using Smithery Integration (Recommended)

For a more seamless integration with Cursor using Smithery:

1. Add to your `~/.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "repo-to-txt-mcp": {
         "command": "npx",
         "args": [
           "-y",
           "@smithery/cli@latest",
           "run",
           "repo-to-txt-mcp",
           "--config",
           "\"{\\\"port\\\":8000}\""
         ]
       }
     }
   }
   ```

2. Restart Cursor or refresh the MCP servers in settings.

## Option 3: Local Development with Smithery

If you're developing or running the code locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/chromewillow/repo-to-txt-mcp.git
   cd repo-to-txt-mcp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

3. Make the wrapper script executable:
   ```bash
   chmod +x smithery-wrapper.js
   ```

4. Add to your `~/.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "repo-to-txt-mcp": {
         "command": "node",
         "args": [
           "/path/to/repo-to-txt-mcp/smithery-wrapper.js",
           "--config",
           "\"{\\\"port\\\":8000}\""
         ]
       }
     }
   }
   ```

5. Restart Cursor or refresh the MCP servers in settings.

## Using the MCP Tools in Cursor

Once integrated, you can use the MCP tools in Cursor's AI assistant:

1. For repository analysis:
   ```
   Could you analyze the GitHub repository https://github.com/username/repository using the repo_to_txt tool?
   ```

2. To fetch content from a previously generated file:
   ```
   Get the content from the output file /path/to/output.txt using the get_output_content tool.
   ```

## Requirements

Make sure you have the following dependencies installed:

```bash
pip install fastapi fastmcp dulwich tiktoken uvicorn
```

## Troubleshooting

- **Server not starting**: Ensure Python and required packages are installed
- **Connection errors**: Check the port is correct in your configuration
- **Server not visible in Cursor**: Restart Cursor or refresh MCP servers in settings
- **Permission errors**: Ensure the smithery-wrapper.js has execute permissions

## Using with Custom Port

If you need to use a custom port:

```json
{
  "mcpServers": {
    "repo-to-txt-mcp": {
      "command": "npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "repo-to-txt-mcp",
        "--config",
        "\"{\\\"port\\\":8001}\""
      ]
    }
  }
}
```

The server automatically detects the port from the config and environment variables.