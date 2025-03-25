#!/usr/bin/env python3

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import List, Dict, Optional, Union, Any
import importlib.util

# Import FastMCP for serving
try:
    from fastmcp import FastMCP, Request, Response
except ImportError:
    print("FastMCP not installed. Run: pip install fastmcp")
    sys.exit(1)

# Import the repo_to_txt module
# Try to import from local file first, then from package
repo_to_txt_spec = importlib.util.find_spec("repo_to_txt")
if repo_to_txt_spec:
    import repo_to_txt
else:
    # If module not found, attempt to import from the local file
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("repo_to_txt", "repo_to_txt.py")
        repo_to_txt = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(repo_to_txt)
    except Exception as e:
        print(f"Error importing repo_to_txt: {e}")
        sys.exit(1)

# Create MCP server
app = FastMCP()

@app.route("/")
async def root() -> Response:
    """Root endpoint that provides information about the API."""
    return Response(
        status_code=200,
        content={
            "name": "repo-to-txt-mcp",
            "description": "MCP server for analyzing and converting Git repositories to text files",
            "version": "1.0.0",
            "endpoints": [
                {"path": "/", "method": "GET", "description": "API information"},
                {"path": "/analyze", "method": "POST", "description": "Analyze a git repository or local folder"},
                {"path": "/health", "method": "GET", "description": "Health check"},
            ]
        }
    )

@app.route("/health")
async def health_check() -> Response:
    """Health check endpoint."""
    return Response(status_code=200, content={"status": "healthy"})

@app.route("/analyze", methods=["POST"])
async def analyze(request: Request) -> Response:
    """
    Analyze a git repository or local folder and return structured information.
    
    Post parameters:
    - source: URL of git repository or path to local folder
    - output_dir: (Optional) Output directory for the txt file
    - include_only: (Optional) List of file extensions to include
    - exclude: (Optional) List of file extensions to exclude
    - max_token_length: (Optional) Maximum number of tokens for the output
    - return_file: (Optional) Whether to return the file content directly in the response
    """
    try:
        # Parse request data
        data = request.json if request.json else {}
        
        # Get parameters
        source = data.get("source")
        if not source:
            return Response(status_code=400, content={"error": "Source parameter is required"})
        
        output_dir = data.get("output_dir")
        include_only = data.get("include_only", [])
        exclude = data.get("exclude", [])
        max_token_length = data.get("max_token_length", 0)
        return_file = data.get("return_file", False)
        
        # Create temporary directory if output_dir not specified
        temp_dir = None
        if not output_dir:
            temp_dir = tempfile.mkdtemp()
            output_dir = temp_dir
        
        # Run repo analysis
        try:
            result = repo_to_txt.analyze_repo(
                source=source,
                output_dir=output_dir,
                include_only=include_only,
                exclude=exclude,
                max_token_length=max_token_length
            )
            
            # Get the path to the output txt file
            txt_file_path = None
            for file in os.listdir(output_dir):
                if file.endswith(".txt"):
                    txt_file_path = os.path.join(output_dir, file)
                    break
            
            # Read file content if needed
            file_content = None
            if return_file and txt_file_path and os.path.exists(txt_file_path):
                with open(txt_file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()
            
            # Prepare response
            response_data = {
                "success": True,
                "result": result,
                "file_path": txt_file_path
            }
            
            if file_content is not None:
                response_data["file_content"] = file_content
            
            return Response(status_code=200, content=response_data)
        
        finally:
            # Clean up temporary directory if created
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    except Exception as e:
        return Response(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Start the server
    print(f"Starting repo-to-txt MCP server on port {port}")
    app.start(port=port)