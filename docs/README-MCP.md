# Repo-to-TXT MCP Implementation

This document provides an overview of the MCP (Multimodal Capability Provider) implementation for the repo-to-txt tool.

## Overview

The repo-to-txt-mcp server provides an MCP API that allows AI assistants to analyze Git repositories and convert them to text files for context. The server exposes two main tools:

1. `repo_to_txt` - Analyzes a Git repository or local folder and generates a text file with the folder structure and file contents
2. `get_output_content` - Retrieves the content of a previously generated output file

## API Implementation

The MCP server is implemented using:

- **FastAPI** - For the web server
- **FastMCP** - For the MCP protocol implementation
- **Dulwich** - For Git operations
- **Tiktoken** - For token counting

The server is built with Python and provides a RESTful API that follows the MCP protocol for compatibility with AI assistants.

## Tools

### repo_to_txt

This tool allows analyzing a Git repository or local folder and generating a text file with the folder structure and file contents.

**Parameters:**

- `source` (required): Repository URL or local folder path
- `is_local` (optional, default: false): Whether the source is a local folder
- `personal_token` (optional): Personal access token for private repositories
- `output_dir` (optional): Output directory path
- `directories_only` (optional, default: false): Only include directories in structure
- `exclude` (optional): List of file extensions to exclude (e.g. .log .tmp)
- `include` (optional): List of file extensions to include (e.g. .py .js)
- `concatenate` (optional, default: true): Concatenate file contents
- `include_git` (optional, default: false): Include git-related files
- `include_license` (optional, default: false): Include license files
- `exclude_readme` (optional, default: false): Exclude readme files

**Response:**

```json
{
  "output_file": "/path/to/output.txt",
  "session_folder": "/path/to/session",
  "character_count": 123456,
  "token_count": 12345
}
```

### get_output_content

This tool retrieves the content of a previously generated output file.

**Parameters:**

- `file_path` (required): Path to the output file

**Response:**

```json
{
  "content": "File content as string...",
  "character_count": 123456,
  "token_count": 12345
}
```

## Smithery Integration

The repo-to-txt-mcp server includes a Smithery integration for easy deployment and management. The integration consists of:

- `smithery.yaml` - Smithery configuration file
- `smithery-wrapper.js` - Node.js wrapper script that starts the Python server

## Deployment

The server can be deployed in several ways:

1. **Direct Python**: Run the Python server directly with `python server.py`
2. **Node.js Wrapper**: Use the Node.js wrapper with `node smithery-wrapper.js`
3. **Smithery**: Deploy through Smithery with `npx @smithery/cli@latest run repo-to-txt-mcp`
4. **Docker**: Deploy using the included Dockerfile