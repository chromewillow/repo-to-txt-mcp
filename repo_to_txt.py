import os
import shutil
import argparse
import logging
import sys
from datetime import datetime
from dulwich import porcelain
import tempfile
import time
import tiktoken

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_binary(file_path):
    try:
        with open(file_path, 'tr') as check_file:
            check_file.read()
            return False
    except:
        return True

def is_git_related(path):
    git_patterns = ['.git', '.gitignore', '.gitattributes']
    return any(pattern in path for pattern in git_patterns)

def should_exclude(file, ignore_git, exclude_license, exclude_readme):
    if ignore_git and is_git_related(file):
        return True
    if exclude_license and file.lower() in ['license', 'license.txt', 'license.md']:
        return True
    if exclude_readme and file.lower() in ['readme', 'readme.txt', 'readme.md']:
        return True
    return False

def get_structure(path, only_dirs=False, exclude=None, include=None, ignore_git=True, exclude_license=True, exclude_readme=False):
    structure = []
    for root, dirs, files in os.walk(path):
        if ignore_git and is_git_related(root):
            continue

        level = root.replace(path, '').count(os.sep)
        indent = '│   ' * (level - 1) + '├── '
        subindent = '│   ' * level + '├── '

        if only_dirs:
            structure.append(f'{indent}{os.path.basename(root)}/')
        else:
            structure.append(f'{indent}{os.path.basename(root)}/')
            for f in files:
                if should_exclude(f, ignore_git, exclude_license, exclude_readme):
                    continue
                if exclude and any(f.endswith(ext) for ext in exclude):
                    continue
                if include and not any(f.endswith(ext) for ext in include):
                    continue
                structure.append(f'{subindent}{f}')
    return '\n'.join(structure)

def concatenate_files(path, exclude=None, include=None, ignore_git=True, exclude_license=True, exclude_readme=False):
    content = []
    file_positions = {}
    current_position = 0

    for root, dirs, files in sorted(os.walk(path)):
        if ignore_git and is_git_related(root):
            continue

        rel_path = os.path.relpath(root, path)
        if rel_path != '.':
            header = f"\n---{rel_path}/---\n"
        else:
            header = f"\n---/---\n"
        content.append(header)
        current_position += len(header)

        for file in sorted(files):
            if should_exclude(file, ignore_git, exclude_license, exclude_readme):
                continue
            file_path = os.path.join(root, file)

            # Check if file is binary
            if is_binary(file_path):
                continue
            if exclude and any(file.endswith(ext) for ext in exclude):
                continue
            if include and not any(file.endswith(ext) for ext in include):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
            except Exception as e:
                logging.error(f"Error reading file {file_path}: {str(e)}")
                continue

            file_header = f"\n--{file}--\n"
            content.append(file_header)
            file_positions[os.path.join(rel_path, file)] = current_position
            current_position += len(file_header)
            content.append(file_content)
            current_position += len(file_content)

    return '\n'.join(content), file_positions

def safe_remove(path):
    def onerror(func, path, exc_info):
        logging.warning(f"Failed to remove {path}. Skipping.")

    if os.path.isdir(path):
        shutil.rmtree(path, onerror=onerror)
    elif os.path.exists(path):
        try:
            os.remove(path)
        except Exception as e:
            logging.warning(f"Failed to remove file {path}: {str(e)}")

def count_tokens(text):
    try:
        encoding = tiktoken.encoding_for_model("gpt-4")
        return len(encoding.encode(text))
    except Exception as e:
        logging.error(f"Error counting tokens: {str(e)}")
        return 0

def analyze_repo(source, output_dir=None, is_local=False, pat=None, 
                directories_only=False, exclude=None, include_only=None, 
                include_git=False, include_license=False, exclude_readme=False,
                max_token_length=0):
    """
    Analyze a git repository or local folder and return structured information.
    
    Args:
        source (str): URL of git repository or path to local folder
        output_dir (str, optional): Output directory for the txt file
        is_local (bool): Whether source is a local folder
        pat (str, optional): Personal access token for private repositories
        directories_only (bool): Only include directories in structure
        exclude (list): List of file extensions to exclude
        include_only (list): List of file extensions to include
        include_git (bool): Include git-related files
        include_license (bool): Include license files
        exclude_readme (bool): Exclude readme files
        max_token_length (int): Maximum number of tokens for the output
        
    Returns:
        dict: Information about the analysis, including file paths and statistics
    """
    temp_dir = None
    try:
        if is_local or os.path.exists(source):
            # Using local folder directly
            folder_path = source
            logging.info("Analyzing local folder...")
        else:
            # Clone the repository to a temporary directory
            temp_dir = tempfile.mkdtemp()
            logging.info(f"Cloning repository: {source}")

            # Add authentication if PAT is provided
            if pat:
                # For GitHub, insert PAT into URL
                if 'github.com' in source:
                    repo_url = source.replace('https://', f'https://{pat}@')
                else:
                    repo_url = source
            else:
                repo_url = source

            try:
                porcelain.clone(repo_url, temp_dir)
            except Exception as e:
                logging.error(f"Failed to clone repository: {str(e)}")
                safe_remove(temp_dir)
                raise e

            folder_path = temp_dir

        logging.info("Generating folder structure")
        structure = get_structure(
            folder_path,
            directories_only,
            exclude,
            include_only,
            not include_git,
            not include_license,
            exclude_readme
        )

        content = f"Folder structure:\n{structure}\n"
        file_positions = {}

        # Always concatenate for MCP server
        logging.info("Concatenating file contents")
        concat_content, file_positions = concatenate_files(
            folder_path,
            exclude,
            include_only,
            not include_git,
            not include_license,
            exclude_readme
        )
        content += f"\nConcatenated content:\n{concat_content}"

        # Limit token count if specified
        if max_token_length > 0:
            token_count = count_tokens(content)
            if token_count > max_token_length:
                logging.info(f"Content exceeds token limit ({token_count} > {max_token_length}). Truncating...")
                # Simple truncation - could be improved with more sophisticated methods
                encoding = tiktoken.encoding_for_model("gpt-4")
                tokens = encoding.encode(content)
                content = encoding.decode(tokens[:max_token_length])
                logging.info(f"Content truncated to {max_token_length} tokens")

        # Create session name and folder
        if is_local or os.path.exists(source):
            folder_name = os.path.basename(os.path.abspath(source))
            session_name = f"{folder_name}_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}"
        else:
            if '://' in source:
                repo_name = source.split('/')[-1].replace('.git', '')
            else:
                repo_name = os.path.basename(source).replace('.git', '')
            session_name = f"{repo_name}_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}"

        # Create output directory if not specified
        if output_dir is None:
            output_dir = os.path.join(os.getcwd(), "LLM_Chat_Repo_Context")
        
        os.makedirs(output_dir, exist_ok=True)
        session_folder = os.path.join(output_dir, session_name)
        os.makedirs(session_folder, exist_ok=True)

        # Save content to file
        output_file = os.path.join(session_folder, f"{session_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Count tokens and characters
        token_count = count_tokens(content)
        char_count = len(content)
        
        logging.info(f"Output written to {output_file}")
        logging.info(f"Characters: {char_count}, Tokens: {token_count}")
        
        # Return as a dictionary for easier JSON conversion
        return {
            "repo_name": folder_name if is_local or os.path.exists(source) else repo_name,
            "output_file": output_file,
            "session_folder": session_folder,
            "token_count": token_count,
            "char_count": char_count,
            "file_count": len(file_positions)
        }

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise e
    finally:
        if temp_dir:
            logging.info("Cleaning up temporary directory")
            time.sleep(1)
            safe_remove(temp_dir)

def main():
    parser = argparse.ArgumentParser(description='LLM Chat Repo Context - CLI Version')
    parser.add_argument('source', help='Repository URL or local folder path')
    parser.add_argument('--local', action='store_true', help='Source is a local folder')
    parser.add_argument('--token', '-t', help='Personal access token for private repositories')
    parser.add_argument('--output-dir', '-o', help='Output directory')
    parser.add_argument('--directories-only', '-d', action='store_true', help='Only include directories in structure')
    parser.add_argument('--exclude', '-e', nargs='+', help='File extensions to exclude (e.g. .log .tmp)')
    parser.add_argument('--include', '-i', nargs='+', help='File extensions to include (e.g. .py .js)')
    parser.add_argument('--include-git', action='store_true', help='Include git files')
    parser.add_argument('--include-license', action='store_true', help='Include license files')
    parser.add_argument('--exclude-readme', action='store_true', help='Exclude readme files')
    parser.add_argument('--max-tokens', type=int, default=0, help='Maximum number of tokens for output')
    
    args = parser.parse_args()
    
    try:
        result = analyze_repo(
            args.source,
            args.output_dir,
            args.local,
            args.token,
            args.directories_only,
            args.exclude,
            args.include,
            args.include_git,
            args.include_license,
            args.exclude_readme,
            args.max_tokens
        )
        print(f"Analysis complete. Output saved to {result['output_file']}")
        print(f"Token count: {result['token_count']}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()