# Cursor Integration Guide

This guide explains how to integrate the repo-to-txt-mcp server with Cursor to provide repository context to language models.

## Overview

Cursor can utilize the repo-to-txt MCP server to analyze GitHub repositories or local folders, convert them to structured text files, and provide this context to language models during conversations.

## Requirements

- Cursor (latest version)
- MCP plugin system enabled in Cursor
- repo-to-txt-mcp server running (either locally or remotely)

## Integration Steps

### Step 1: Install and Run the repo-to-txt-mcp Server

Follow the instructions in the [Installation Guide](./INSTALLATION.md) to set up and run the server.

### Step 2: Add the MCP to Cursor

1. Open Cursor
2. Go to Settings (⚙️)
3. Navigate to the "MCPs" section
4. Click "Add MCP"
5. Enter the following information:
   - **URL**: `http://localhost:8000` (or the URL of your deployed server)
   - **Name**: `repo-to-txt`
   - **Description**: `Convert repositories to text for LLM context`

### Step 3: Configure Access in Cursor

1. In Cursor, navigate to the "Security" section in Settings
2. Under "MCP Access", ensure that `repo-to-txt` is granted access
3. Save your settings

## Using the Integration

### Simple Method: Via Command Palette

1. Open the Command Palette in Cursor (Cmd/Ctrl + Shift + P)
2. Type "Analyze Repository"
3. Select "repo-to-txt: Analyze Repository"
4. Enter the repository URL or local folder path when prompted
5. The repository context will be loaded and made available to the language model

### Advanced Method: Via Chat

You can also use chat commands to interact with the MCP:

```
/repo-to-txt analyze https://github.com/username/repository
```

Additional options:
```
/repo-to-txt analyze https://github.com/username/repository --include-only .py,.js --exclude .pyc,.git
```

## Configuration Options

When analyzing a repository, you can specify several options:

| Option | Description |
|--------|-------------|
| `--include-only` | Comma-separated list of file extensions to include |
| `--exclude` | Comma-separated list of file extensions to exclude |
| `--max-tokens` | Maximum number of tokens for the output |

## Examples

### Analyze a GitHub Repository

```
/repo-to-txt analyze https://github.com/chromewillow/repo-to-txt-mcp
```

### Analyze a Local Repository with Filtering

```
/repo-to-txt analyze /path/to/local/repo --include-only .ts,.tsx,.js,.jsx
```

### Limit Token Count

```
/repo-to-txt analyze https://github.com/username/large-repo --max-tokens 10000
```

## Troubleshooting

### Common Issues

#### Connection Error

If Cursor cannot connect to the MCP server, check that:
- The server is running
- The URL in Cursor settings is correct
- No firewall is blocking the connection

#### Authentication Issues

This MCP does not require authentication by default. If you've configured custom authentication, ensure it's properly set up on both the server and in Cursor.

#### Repository Access

When analyzing GitHub repositories:
- Public repositories should work without issues
- Private repositories may require authentication which you'll need to handle separately

### Getting Support

If you encounter issues with the integration, you can:
1. Check the server logs for errors
2. Consult the [GitHub repository](https://github.com/chromewillow/repo-to-txt-mcp) for known issues
3. Open a new issue in the repository with details of your problem

## Additional Resources

- [Server API Documentation](./API.md)
- [GitHub Repository](https://github.com/chromewillow/repo-to-txt-mcp)