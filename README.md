# Repo-to-TXT MCP Server

An MCP (Multimodal Capability Provider) server implementation for the [LLM Chat Repo Context](https://github.com/lukaszliniewicz/LLM_Chat_Repo_Context) tool, which analyzes Git repositories and converts them to text files suitable for providing context to LLMs.

## Features

- Analyze Git repositories or local folders and convert them to text files
- Generate folder structure
- Concatenate file contents
- Filter files by extension
- Count tokens in the output (using tiktoken)
- REST API for integration with LLM platforms

## Requirements

- Python 3.6+
- FastAPI
- FastMCP
- Dulwich
- Tiktoken

## Installation

```bash
pip install fastapi fastmcp dulwich tiktoken uvicorn
```

## Usage

### Starting the server

```bash
python server.py
```

The server will start on `http://0.0.0.0:8000`.

### API Endpoints

The MCP server provides the following tools:

#### 1. repo_to_txt

Converts a Git repository or local folder to a text file for LLM context.

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

#### 2. get_output_content

Retrieves the content of a previously generated output file.

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

## Integration with LLM Platforms

This MCP server can be integrated with LLM platforms that support the MCP protocol, enabling LLMs to analyze repositories and provide context-aware responses about code.

## Original Project

This MCP server is based on [LLM Chat Repo Context](https://github.com/lukaszliniewicz/LLM_Chat_Repo_Context) by lukaszliniewicz, which provides both GUI and CLI interfaces for analyzing repositories and generating text files for LLM context.

## License

MIT License