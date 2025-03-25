# LLM Chat Repo Context - CLI Version

This is a command-line interface (CLI) version of the [LLM Chat Repo Context](https://github.com/lukaszliniewicz/LLM_Chat_Repo_Context) tool, which helps provide context about code repositories to Large Language Models (LLMs) without the need to copy and paste multiple files manually.

## Features

- Analyze local and remote Git repositories
- Generate folder structure
- Concatenate file contents
- Count tokens in the output (using tiktoken)
- Save analysis as a text file
- Filter files by extension

## Requirements

- Python 3.6+
- dulwich
- tiktoken

Install requirements:

```bash
pip install dulwich tiktoken
```

## Usage

```bash
python repo_to_txt.py SOURCE [OPTIONS]
```

### Arguments

- `SOURCE`: Repository URL or local folder path

### Options

- `--local`: Source is a local folder
- `--token`, `-t`: Personal access token for private repositories
- `--output-dir`, `-o`: Output directory
- `--directories-only`, `-d`: Only include directories in structure
- `--exclude`, `-e`: File extensions to exclude (e.g. .log .tmp)
- `--include`, `-i`: File extensions to include (e.g. .py .js)
- `--no-concatenate`: Do not concatenate file contents
- `--include-git`: Include git files
- `--include-license`: Include license files
- `--exclude-readme`: Exclude readme files

## Examples

### Analyze a GitHub repository

```bash
python repo_to_txt.py https://github.com/username/repository
```

### Analyze a local directory

```bash
python repo_to_txt.py /path/to/local/repo --local
```

### Include only Python and JavaScript files

```bash
python repo_to_txt.py https://github.com/username/repository --include .py .js
```

### Exclude binary and log files

```bash
python repo_to_txt.py https://github.com/username/repository --exclude .exe .bin .log
```

### Only show directory structure, don't concatenate files

```bash
python repo_to_txt.py https://github.com/username/repository --no-concatenate
```

## Output

The tool creates a session folder with a timestamped name in the format:
`[repo_name]_[timestamp]` or `[folder_name]_[timestamp]`

Inside the session folder, it generates a text file with:
1. The complete folder structure
2. Concatenated contents of all (or selected) files

The file can be copied and pasted into LLM chat interfaces to provide context about the repository.

## Original Project

This CLI tool is based on [LLM Chat Repo Context](https://github.com/lukaszliniewicz/LLM_Chat_Repo_Context) by lukaszliniewicz, which provides a GUI interface with additional features.