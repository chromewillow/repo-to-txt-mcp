import os
import json
from fastapi import FastAPI, HTTPException, Query
from fastmcp import MCP
from typing import List, Optional, Dict, Any
from repo_to_txt import analyze_repo

app = FastAPI(title="Repo to TXT MCP API")
mcp = MCP(app)

@mcp.tool("repo_to_txt", 
         description="Convert a Git repository or local folder to a text file for LLM context",
         output_schema={
             "type": "object",
             "properties": {
                 "output_file": {"type": "string", "description": "Path to the generated output file"},
                 "session_folder": {"type": "string", "description": "Path to the session folder"},
                 "character_count": {"type": "integer", "description": "Character count in the output file"},
                 "token_count": {"type": "integer", "description": "Estimated token count in the output file"}
             },
             "required": ["output_file", "session_folder"]
         })
async def repo_to_txt(
    source: str = Query(..., description="Repository URL or local folder path"),
    is_local: bool = Query(False, description="Whether the source is a local folder"),
    personal_token: Optional[str] = Query(None, description="Personal access token for private repositories"),
    output_dir: Optional[str] = Query(None, description="Output directory path"),
    directories_only: bool = Query(False, description="Only include directories in structure"),
    exclude: Optional[List[str]] = Query(None, description="File extensions to exclude (e.g. .log .tmp)"),
    include: Optional[List[str]] = Query(None, description="File extensions to include (e.g. .py .js)"),
    concatenate: bool = Query(True, description="Concatenate file contents"),
    include_git: bool = Query(False, description="Include git-related files"),
    include_license: bool = Query(False, description="Include license files"),
    exclude_readme: bool = Query(False, description="Exclude readme files"),
) -> Dict[str, Any]:
    """
    Convert a Git repository or local folder to a text file that provides context for LLMs.
    The output includes the folder structure and optionally concatenated file contents.
    """
    try:
        result = analyze_repo(
            source,
            output_dir,
            is_local,
            personal_token,
            directories_only,
            exclude,
            include,
            concatenate,
            include_git,
            include_license,
            exclude_readme
        )
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to analyze repository")
        
        output_file, session_folder = result
        
        # Get file stats
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            char_count = len(content)
        
        from repo_to_txt import count_tokens
        token_count = count_tokens(content)
        
        return {
            "output_file": output_file,
            "session_folder": session_folder,
            "character_count": char_count,
            "token_count": token_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@mcp.tool("get_output_content",
         description="Get the content of a generated output file",
         output_schema={
             "type": "object",
             "properties": {
                 "content": {"type": "string", "description": "Content of the output file"},
                 "character_count": {"type": "integer", "description": "Character count in the output file"},
                 "token_count": {"type": "integer", "description": "Estimated token count in the output file"}
             },
             "required": ["content", "character_count", "token_count"]
         })
async def get_output_content(
    file_path: str = Query(..., description="Path to the output file"),
) -> Dict[str, Any]:
    """
    Retrieve the content of a previously generated output file.
    """
    try:
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Output file not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            char_count = len(content)
        
        from repo_to_txt import count_tokens
        token_count = count_tokens(content)
        
        return {
            "content": content,
            "character_count": char_count,
            "token_count": token_count
        }
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)