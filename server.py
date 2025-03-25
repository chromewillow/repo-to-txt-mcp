import os
import json
import logging
from fastapi import FastAPI, HTTPException, Query, Body
from fastmcp import FastMCP
from typing import List, Optional, Dict, Any
from repo_to_txt import analyze_repo

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Repo to TXT MCP API")
mcp = FastMCP(app)

@mcp.tool("repo_to_txt", 
         description="Convert a Git repository or local folder to a text file for LLM context")
async def repo_to_txt_tool(
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
         description="Get the content of a generated output file")
async def get_output_content_tool(
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

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# Add explicit FastAPI POST endpoint for repo_to_txt
@app.post("/repo_to_txt")
async def repo_to_txt_endpoint(
    source: str = Body(..., description="Repository URL or local folder path"),
    is_local: bool = Body(False, description="Whether the source is a local folder"),
    personal_token: Optional[str] = Body(None, description="Personal access token for private repositories"),
    output_dir: Optional[str] = Body(None, description="Output directory path"),
    directories_only: bool = Body(False, description="Only include directories in structure"),
    exclude: Optional[List[str]] = Body(None, description="File extensions to exclude (e.g. .log .tmp)"),
    include_only: Optional[List[str]] = Body(None, description="File extensions to include (e.g. .py .js)"),
    concatenate: bool = Body(True, description="Concatenate file contents"),
    include_git: bool = Body(False, description="Include git-related files"),
    include_license: bool = Body(False, description="Include license files"),
    exclude_readme: bool = Body(False, description="Exclude readme files"),
    return_file: bool = Body(False, description="Whether to return the file content in the response"),
):
    """
    Convert a Git repository or local folder to a text file that provides context for LLMs.
    The output includes the folder structure and optionally concatenated file contents.
    """
    try:
        logger.info(f"Analyzing repository: {source}")
        
        # Log the parameters
        logger.info(f"Parameters: is_local={is_local}, directories_only={directories_only}, " +
                   f"include_git={include_git}, include_license={include_license}, " +
                   f"exclude_readme={exclude_readme}, return_file={return_file}")
        
        if include_only:
            logger.info(f"Include only: {include_only}")
        if exclude:
            logger.info(f"Exclude: {exclude}")
            
        result = analyze_repo(
            source,
            output_dir,
            is_local,
            personal_token,
            directories_only,
            exclude,
            include_only,
            include_git,
            include_license,
            exclude_readme
        )
        
        logger.info(f"Analysis result: {result}")
        
        if not isinstance(result, dict):
            logger.error(f"Result is not a dictionary: {result}")
            raise HTTPException(status_code=500, detail="Failed to analyze repository")
        
        response = {
            "success": True,
            "result": result
        }
        
        if return_file and "output_file" in result:
            # Read file content if needed
            logger.info(f"Reading file content from {result['output_file']}")
            with open(result["output_file"], "r", encoding="utf-8") as f:
                response["file_content"] = f.read()
        
        return response
        
    except Exception as e:
        logger.error(f"Error analyzing repository: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Add explicit FastAPI GET endpoint for output content
@app.post("/get_output_content")
async def get_output_content_endpoint(
    file_path: str = Body(..., description="Path to the output file"),
):
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
    
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting repo-to-txt MCP server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)