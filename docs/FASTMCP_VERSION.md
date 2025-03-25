# FastMCP Version Compatibility

This document provides information about the FastMCP version compatibility of the repo-to-txt-mcp server.

## Current Compatibility

The server is currently compatible with:

- **FastMCP version 0.4.1** (confirmed working)

## Version-Specific Changes

### For FastMCP 0.4.1

The following adaptations were made to work with FastMCP 0.4.1:

1. Import `FastMCP` instead of `MCP`:
   ```python
   from fastmcp import FastMCP
   ```

2. Initialize the MCP object with `FastMCP` instead of `MCP`:
   ```python
   mcp = FastMCP(app)
   ```

3. Remove the `output_schema` parameter from tool decorators:
   ```python
   @mcp.tool("repo_to_txt", 
            description="Convert a Git repository or local folder to a text file for LLM context")
   ```

4. Add explicit FastAPI endpoints for each tool function, as FastMCP 0.4.1 doesn't automatically create FastAPI endpoints for tools:
   ```python
   @app.post("/repo_to_txt")
   async def repo_to_txt_endpoint(...):
       # Implementation
   ```

5. Add proper error logging and handling for better debugging.

## Future Compatibility

If upgrading to FastMCP 0.7.0 or newer, the following changes would be needed:

1. Change import back to `from fastmcp import MCP`
2. Change initialization to `mcp = MCP(app)`
3. Re-add `output_schema` parameter to tool decorators for better OpenAPI documentation
4. Remove explicit FastAPI endpoints if tools are automatically registered as endpoints in newer FastMCP versions

## Troubleshooting

If you encounter issues with FastMCP compatibility:

1. Check the installed FastMCP version:
   ```bash
   pip show fastmcp
   ```

2. If using a different version, either:
   - Adapt the code for your FastMCP version
   - Install the compatible FastMCP version:
     ```bash
     pip install fastmcp==0.4.1
     ```

## Related Files

The following files contain FastMCP-specific code:

- `server.py` - Main server file with FastMCP integration
- `requirements.txt` - Specifies FastMCP dependency version