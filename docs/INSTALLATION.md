# Installation Guide

This guide provides instructions for installing and running the repo-to-txt-mcp server.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Git

## Installation Methods

### Method 1: Direct Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chromewillow/repo-to-txt-mcp.git
   cd repo-to-txt-mcp
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Node.js dependencies:
   ```bash
   npm install
   ```

4. Start the server:
   ```bash
   node smithery-wrapper.js
   ```

The server will start on port 8000 by default. You can change the port by setting the `PORT` environment variable:
```bash
PORT=3000 node smithery-wrapper.js
```

### Method 2: Docker Installation

1. Build the Docker image:
   ```bash
   docker build -t repo-to-txt-mcp .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 repo-to-txt-mcp
   ```

You can access the server at `http://localhost:8000`.

### Method 3: Using GitHub Container Registry

Pull and run the pre-built Docker image:
```bash
docker pull ghcr.io/chromewillow/repo-to-txt-mcp:latest
docker run -p 8000:8000 ghcr.io/chromewillow/repo-to-txt-mcp:latest
```

## Requirements

The following Python packages are required:
- `fastmcp`: For serving the MCP server
- `dulwich`: For Git operations
- `tiktoken`: For token counting

The following Node.js packages are required:
- `fs`: For file system operations
- `path`: For path operations

## Verifying Installation

After installation, you can verify that the server is running correctly:

```bash
curl http://localhost:8000/health
```

You should receive a response like:
```json
{
  "status": "healthy"
}
```

## Troubleshooting

### Common Issues

#### Port Already in Use

If you get an error like "Address already in use", it means that port 8000 is already being used by another application. You can use a different port:

```bash
PORT=3000 node smithery-wrapper.js
```

#### Python Not Found

If you get an error about Python not being found, make sure that Python is installed and available in your PATH. The wrapper script attempts to find Python using several common executable names (`python3`, `python`, `py`).

#### Missing Dependencies

If you encounter errors about missing Python or Node.js dependencies, make sure you have installed all required packages:

```bash
pip install -r requirements.txt
npm install
```

### Getting Help

If you continue to experience issues, please:

1. Check the [GitHub Issues](https://github.com/chromewillow/repo-to-txt-mcp/issues) to see if your problem has been reported
2. Open a new issue with details about your environment and the specific error messages

## Next Steps

After installation, check out the [API Documentation](API.md) to learn how to use the server.