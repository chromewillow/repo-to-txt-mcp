# MCP Architecture

Since we can't directly upload binary image files through the GitHub API, this markdown file serves as a placeholder for the MCP architecture diagram.

The architecture of the repo-to-txt-mcp server follows this pattern:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│               │     │               │     │               │
│  Cursor IDE   │────►│  smithery.js  │────►│   server.py   │
│ (MCP Client)  │     │  (JS Wrapper) │     │ (Python MCP)  │
│               │     │               │     │               │
└───────────────┘     └───────────────┘     └───────────────┘
                                                    │
                                                    ▼
                                         ┌───────────────────┐
                                         │                   │
                                         │   repo_to_txt.py  │
                                         │   (Core Logic)    │
                                         │                   │
                                         └───────────────────┘
```

1. **Cursor IDE** acts as the MCP client, sending requests to the MCP server
2. **smithery-wrapper.js** serves as a Node.js wrapper that starts the Python server
3. **server.py** implements the MCP API endpoints using FastAPI and FastMCP
4. **repo_to_txt.py** contains the core logic for repository analysis and text conversion