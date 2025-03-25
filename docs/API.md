# repo-to-txt-mcp API Documentation

This document describes the API endpoints provided by the repo-to-txt MCP server.

## Base URL

When running locally: `http://localhost:8000`

## Endpoints

### GET /

Returns information about the API.

**Response:**

```json
{
  "name": "repo-to-txt-mcp",
  "description": "MCP server for analyzing and converting Git repositories to text files",
  "version": "1.0.0",
  "endpoints": [
    {"path": "/", "method": "GET", "description": "API information"},
    {"path": "/analyze", "method": "POST", "description": "Analyze a git repository or local folder"},
    {"path": "/health", "method": "GET", "description": "Health check"}
  ]
}
```

### GET /health

Health check endpoint.

**Response:**

```json
{
  "status": "healthy"
}
```

### POST /analyze

Analyze a git repository or local folder and return structured information.

**Request Parameters:**

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| source | string | URL of git repository or path to local folder | Yes |
| output_dir | string | Output directory for the txt file | No |
| include_only | array | List of file extensions to include | No |
| exclude | array | List of file extensions to exclude | No |
| max_token_length | integer | Maximum number of tokens for the output | No |
| return_file | boolean | Whether to return the file content directly in the response | No |

**Example Request:**

```json
{
  "source": "https://github.com/username/repo",
  "include_only": [".py", ".js", ".md"],
  "exclude": [".pyc", ".git"],
  "max_token_length": 10000,
  "return_file": true
}
```

**Response:**

```json
{
  "success": true,
  "result": {
    "repo_name": "repo",
    "token_count": 8500,
    "file_count": 25,
    "file_types": {".py": 10, ".js": 8, ".md": 7}
  },
  "file_path": "/path/to/output/repo.txt",
  "file_content": "# Repository: repo\n\n## Structure\n..."
}
```

If `return_file` is set to `false`, the `file_content` field will be omitted.

**Error Response:**

```json
{
  "error": "Error message"
}
```

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Missing or invalid parameters |
| 500 | Internal Server Error - Something went wrong on the server |

## Rate Limiting

The API does not currently implement rate limiting, but excessive usage may be subject to limitations in the future.

## Usage Examples

### cURL

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"source": "https://github.com/username/repo", "return_file": true}'
```

### Python

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "source": "https://github.com/username/repo",
        "include_only": [".py", ".js", ".md"],
        "return_file": True
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"Repository analysis successful. Token count: {data['result']['token_count']}")
    print(data['file_content'])
else:
    print(f"Error: {response.json().get('error')}")
```

### JavaScript

```javascript
fetch('http://localhost:8000/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    source: 'https://github.com/username/repo',
    return_file: true
  })
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log(`Repository analysis successful. Token count: ${data.result.token_count}`);
    console.log(data.file_content);
  } else {
    console.error(`Error: ${data.error}`);
  }
})
.catch(error => console.error('Error:', error));
```