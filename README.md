# repo-to-txt-mcp

An MCP server for analyzing and converting Git repositories to text files for LLM context.

## Overview

repo-to-txt-mcp is a Machine Code Protocol (MCP) server that allows you to analyze GitHub repositories or local folders and convert them into structured text files. This is particularly useful for providing context about repositories to large language models (LLMs) like GPT-4.

This project extends the functionality of the [repo-to-txt](https://github.com/chromewillow/repo-to-txt-mcp) CLI tool to provide a web API that can be integrated into other applications, particularly Cursor's MCP system.

## Features

- **Repository Analysis**: Analyze both local and remote Git repositories
- **Structured Output**: Generate formatted text with folder structure and concatenated file contents
- **File Filtering**: Include or exclude files based on extensions
- **Token Management**: Limit output size by token count
- **Easy Integration**: Designed to work seamlessly with Cursor's MCP system
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- Git

### Installation Options

See the [Installation Guide](docs/INSTALLATION.md) for detailed instructions on:

- Direct installation
- Docker installation
- GitHub Container Registry usage

## Quick Start

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. Start the server:
   ```bash
   node smithery-wrapper.js
   ```

3. The server will be available at `http://localhost:8000`

## API Usage

### Convert a GitHub Repository

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "source": "https://github.com/username/repository",
    "return_file": true
  }'
```

### Filter by File Extensions

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "source": "https://github.com/username/repository",
    "include_only": [".py", ".js", ".md"],
    "exclude": [".pyc", ".git"]
  }'
```

See the [API Documentation](docs/API.md) for complete details.

## Cursor Integration

This server is designed to integrate with Cursor to provide repository context to language models during conversations. 

See the [Cursor Integration Guide](docs/CURSOR-INTEGRATION.md) for instructions on how to set up and use this feature.

## Docker Support

A Dockerfile is included to facilitate containerized deployment:

```bash
docker build -t repo-to-txt-mcp .
docker run -p 8000:8000 repo-to-txt-mcp
```

## Smithery Integration

This project includes configuration for Smithery, a tool for managing MCPs:

```bash
smithery install chromewillow/repo-to-txt-mcp
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project builds on the functionality of the [repo-to-txt](https://github.com/chromewillow/repo-to-txt-mcp) CLI tool
- Thanks to the FastMCP library for simplifying the creation of MCP servers